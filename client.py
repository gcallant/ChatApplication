import socket
import sys

address = '127.0.0.1'
port = 10000

target = (address, port)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect(target)

while clientSocket:
    clientInput = raw_input("Enter R, P, or C: ")

    if clientInput:
        clientSocket.send(clientInput)
