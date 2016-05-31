import Queue
import socket
import select
import sys

class Qu:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

address = '127.0.0.1'
port = 10000
bufferSize = 1024
maxQueue = 2
roomCount = 0
cQ = Qu()
clientQueue = {}


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((address, port))
serverSocket.listen(5)

inputs = [serverSocket]
output = []
messageQueue = {}

while inputs:
    # select will return three lists containing subsets of the contents that were passed in
    inputfd, outputfd, exceptfd = select.select(inputs, output, inputs)

    for fd in inputfd:
        if fd is serverSocket:
            # a new connection is ready to be made to the server.
            # we will need to accept it here, check to see if there are 2 players, and possible add to clientQueue
            clientConnection, clientAddress = fd.accept()

            # if there are < 2 people currently connected
            if roomCount < maxQueue:
                status = 'ready'
                inputs.append(clientConnection)

                # also put in the messageQueue for data the server will send; messageQueue acts as a buffer
                messageQueue[clientConnection] = Queue.Queue()
                messageQueue[clientConnection].put(status)
                output.append(clientConnection)

                roomCount += 1
            # else, add to clientQueue and make status = 'false'
            else:
                status = 'queue'

                clientQueue[clientConnection] = Queue.Queue()
                cQ.enqueue(clientConnection)
                messageQueue[clientConnection] = Queue.Queue()
                messageQueue[clientConnection].put(status)
                output.append(clientConnection)

        else:
            # a client has sent data, so the server needs to receive it
            data = fd.recv(bufferSize)

            if data:
                print 'Server received a message. Adding to messageQueue'
                messageQueue[fd].put(data)

                if fd not in output:
                    output.append(fd)
            else:
                # client has disconnected
                print 'A client has disconnected. Cleaning output list and messageQueue'

                if fd in output:
                    output.remove(fd)

                inputs.remove(fd)
                del messageQueue[fd]

                fd.close()

                roomCount -= 1
                try:
                    if cQ.size >= 1:
                        nextClient = cQ.dequeue()

                        if len(clientQueue) >= 1:
                            print 'dequeued successfully'

                        inputs.append(nextClient)
                        status = 'ready'
                        messageQueue[nextClient] = Queue.Queue()
                        messageQueue[nextClient].put(status)
                        output.append(nextClient)

                        roomCount += 1
                except Exception:
                    print 'hi'


    for fd in outputfd:
        try:
            message = messageQueue[fd].get_nowait()
            fd.send(message)
        except Queue.Empty:
            output.remove(fd)

    for fd in exceptfd:
        # if there is an exception, remove that fd from input, clean up the messageQueue, and close the fd
        inputs.remove(fd)
        del messageQueue[fd]

        if fd in output:
            output.remove(fd)

        fd.close()

serverSocket.close()
