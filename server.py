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

def usage():
    print 'USAGE: python server.py <ADDRESS> <PORT> <MAXQUEUE> <BUFFERSIZE>'
    exit(0)

address = '127.0.0.1'

if len(sys.argv) > 1:
    if sys.argv[1] in ('-h', '-H', '--help', '--HELP'):
        if(sys.argv[1].isDigit()):
            address = int(sys.argv[1])
        elif(not sys.argv[1].isDigit()):
            address = sys.argv[1]
        usage()

    else:
        address = sys.argv[1]
else:
    usage()

maxQueue = 2
bufferSize = 1024

if len(sys.argv) > 2:
    if sys.argv[2].isdigit():
        port = int(sys.argv[2])
        if port < 1000 or port > 65535:
            usage()
else:
    usage()

if len(sys.argv) > 3:
    if sys.argv[3].isdigit():
        maxQueue = int(sys.argv[3])

        if maxQueue < 1 or maxQueue > 999:
            usage()
else:
    maxQueue = 2

if len(sys.argv) > 4:
    if sys.argv[4].isdigit():
        bufferSize = int(sys.argv[4])
        if bufferSize < 32 or bufferSize > 99999:
            usage()
    else:
        bufferSize = 1024
else:
    bufferSize = 1024

roomCount = 0
cQ = Qu()
clientQueue = {}

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((address, port))
serverSocket.listen(5)

inputs = [serverSocket]
output = []
messageQueue = {}

startGame = False
playerOne = ''
playerTwo = ''
winner = -1
wait = None

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
                messageQueue[clientConnection].put(status + str(roomCount))
                output.append(clientConnection)

                roomCount += 1

                if roomCount == maxQueue:
                    startGame = True

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

                if startGame == True:
                    if '1' in data:
                        playerOne = data[:1]

                        if wait is None:
                            wait = fd
                    else:
                        playerTwo = data[:1]

                        if wait is None:
                            wait = fd

                    if playerOne != '' and playerTwo != '':
                        if playerOne == 'R' and playerTwo == 'R':
                            winner = 0
                        elif playerOne == 'R' and playerTwo == 'P':
                            winner = 2
                        elif playerOne == 'R' and playerTwo == 'S':
                            winner = 1
                        elif playerOne == 'P' and playerTwo == 'R':
                            winner = 1
                        elif playerOne == 'P' and playerTwo == 'P':
                            winner = 0
                        elif playerOne == 'P' and playerTwo == 'S':
                            winner = 2
                        elif playerOne == 'S' and playerTwo == 'R':
                            winner = 2
                        elif playerOne == 'S' and playerTwo == 'P':
                            winner = 1
                        elif playerOne == 'S' and playerTwo == 'S':
                            winner = 0
                    else:
                        messageQueue[fd].put('wait')
                        if fd not in output:
                            output.append(fd)
                else:
                    messageQueue[fd].put('wait')
                    if fd not in output:
                        output.append(fd)

                    if '1' in data:
                        playerOne = data[:1]
                        if wait is None:
                            wait = fd
                    else:
                        playerTwo = data[:2]
                        if wait is None:
                            wait = fd

                if winner != -1:
                    messageQueue[fd].put(winner)
                    if fd not in output:
                        output.append(fd)

                    wait.send(str(winner))

                    wait = None
                    startGame = False
                    playerOne = ''
                    playerTwo = ''
                    winner = -1
                    roomCount = 2

                else:
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
                    print ''


    for fd in outputfd:
        try:
            if roomCount > 0:
                message = messageQueue[fd].get_nowait()
                fd.send(str(message))
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
