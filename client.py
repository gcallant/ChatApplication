import socket

def getinput():
    isCleanInput = False
    options = ('R', 'P', 'C')

    while(isCleanInput is False):
        clientInput = raw_input("Enter R, P, or C: ").upper()

        if clientInput in options:
            isCleanInput = True

    return clientInput


address = '127.0.0.1'
port = 10000
bufferSize = 1024

target = (address, port)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(target)

status = clientSocket.recv(bufferSize)

print(status)

if status == 'queue':
    while status == 'queue':
        print 'The room is full, you have been added to the queue.'

        status = clientSocket.recv(bufferSize)
    print(status)
    print 'You are now connected!'

while clientSocket:
    clientInput = getinput()

    if clientInput:
        clientSocket.send(clientInput)