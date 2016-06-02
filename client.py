import socket

def getinput():
    isCleanInput = False
    options = ('R', 'P', 'S')

    while(isCleanInput is False):
        clientInput = raw_input("Enter R, P, or S: ").upper()

        if clientInput in options:
            isCleanInput = True

    return clientInput


address = '127.0.0.1'
port = 10002
bufferSize = 1024

choices = ('R', 'P', 'S')

target = (address, port)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(target)

status = clientSocket.recv(bufferSize)
player = '-1'

if '0' in status:
    player = '1'
elif '1' in status:
    player = '2'

print(status)

if 'queue' in status:
    while status == 'queue':
        print 'The room is full, you have been added to the queue.'

        status = clientSocket.recv(bufferSize)
    print(status)
    print 'You are now connected!'

while clientSocket:
    clientInput = getinput()

    if clientInput:
        clientSocket.send(clientInput)
        result = clientSocket.recv(bufferSize)

        if 'wait' in result:
            print 'Waiting for your opponent!'

            result = clientSocket.recv(bufferSize)
            if choices in result:
                result = clientSocket.recv(bufferSize)

        if '0' in result:
            print 'The match was a draw!'
        elif '1' in result and player == '1':
            print 'You won!'
        elif '1' in result and player == '2':
            print 'You lost!'
        elif '2' in result and player == '1':
            print 'You lost!'
        elif '2' in result and player == '2':
            print 'You Won!'

        print result
