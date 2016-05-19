import socket
import select
import sys

port = 10000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind(('127.0.0.1', port))

serverSocket.listen()

input = [serverSocket, sys.stdin]

while 1:
	inputfd, outputfd, exceptfd = select.select(input, [], [])
	
	for client in inputfd:
		if client == serverSocket:
			client = serverSocket.accept();
			address = serverSocket.accept();
			
			input.append(client)

		else:
			payload = client.recv(1024)
			
			if payload:
				client.send(payload)
			else:
				client.close()

				input.remove(client)

serverSocket.close()
