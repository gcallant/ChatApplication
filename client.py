import socket
import sys

def getinput():
    isCleanInput = False
    options = ('R', 'P', 'S')

    while(isCleanInput is False):
        clientInput = raw_input("Enter R, P, or S: ").upper()

        if clientInput in options:
            isCleanInput = True

    return clientInput

def usage():
    print 'USAGE: python client.py <ADDRESS> <PORT> <BUFFERSIZE>'
    exit(0)

if len(sys.argv) > 1:
    if sys.argv[1] in ('-h', '-H', '--help', '--HELP'):
        usage()
    else:
        if len(sys.argv) > 2:

            address = sys.argv[1]

            if sys.argv[2].isdigit():
                port = int(sys.argv[2])
                if port < 1000 or port > 25000:
                    usage()
        else:
            usage()

        if len(sys.argv) > 3:
            if sys.argv[3].isdigit():
                bufferSize = int(sys.argv[3])
                if bufferSize < 32 or bufferSize > 99999:
                    usage()
        else:
            bufferSize = 1024
else:
    usage()

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

isPlaying = True

while isPlaying:
    clientInput = getinput()

    if clientInput:
        clientSocket.send(clientInput + str(player))
        result = clientSocket.recv(bufferSize)

        if 'wait' in result:
            print 'Waiting for your opponent!'

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

        print 'Disconnecting to make room for other players. Thank you for playing SPEED-RPS!'

        clientSocket.close()
        isPlaying = False
