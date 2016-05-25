import socket
import sys

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

target = (address, port)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect(target)

while clientSocket:
    clientInput = getinput()

    if clientInput:
        clientSocket.send(clientInput)