#!/usr/bin/env python

#Copyright (c) Kathleen Baker
#>>curl localhost:12345
#>>telnet localhost 12345
# in telnet: GET / HTTP/1.0
import socket, os, sys, select

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#to fix ports being unavailable - don't need to wait
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#any port bigger tha 1024 and < something
#0.0.0.0 is everything on this computer
serverSocket.bind(("0.0.0.0", 12346))

#doesn't matter if 5, but usually always use 5
#number of connections we want the os to queue before handling them
serverSocket.listen(5)

while True:
	print "Waiting for connection..."
	(incomingSocket, address) = serverSocket.accept()
	print "We got a connection from %s" % (str (address))
	
	pid = os.fork()
	if (pid == 0):
		#in child process
		outgoingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		outgoingSocket.connect(("www.google.com",80))

		request = bytearray()
		while True:
			#to stop deadlock -if nothing to receive won't wait here
			incomingSocket.setblocking(0)
			#need to filter out this error (11)
			try:
				part = incomingSocket.recv(1024)
			except IOError, exception:
				if exception.errno == 11:
					part = None
				else:
					raise
			if (part):
				print part
				request.extend(part)
				outgoingSocket.sendall(part)
			outgoingSocket.setblocking(0)
			try:
				part = outgoingSocket.recv(1024)
			except IOError, exception:
				if exception.errno == 11:
					part = None
				else:
					raise
			if (part):
				incomingSocket.sendall(part)
			#to fix using CPU
			#wait on this line until inc/outSock has data, or either has an error, or 1 second goes by
			select.select([incomingSocket, outgoingSocket], [], [incomingSocket, outgoingSocket], 1.0)
		print request
		sys.exit(0)
	else:
		#in parent process- want to loop around for next connection
		pass

