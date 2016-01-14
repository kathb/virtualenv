#!/usr/bin/env python

#Copyright (c) Kathleen Baker

import socket

#AF_INET - socket on internet IP
#SOCK_STREAM - TCP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#double brackets because is a tuple
clientSocket.connect(("www.google.com",80))

#must have two \n
request = "GET / HTTP/1.0\n\n"

clientSocket.sendall(request)

response = bytearray()
while True:
	#usually 1024 or 2048
	part = clientSocket.recv(1024)
	if (part):
		response.extend(part)
	else:
		break

print response

