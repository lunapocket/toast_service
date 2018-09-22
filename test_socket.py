import socket
from autolog import *

if __name__ == '__main__':

	HOST = '127.0.0.1'
	PORT = 8192 #kernel will designate the port
	BUFSIZE = 1024
	ADDR = (HOST, PORT)

	while True:
		blogger.info("creating socket")
		clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		blogger.info("connecting to server")
		clientSocket.connect(ADDR)

		message = b"hello, world"
		blogger.debug('sending data: %s', message)
		len_sent = clientSocket.send(message)

		blogger.debug("connection has been established")
		response = clientSocket.recv(len_sent)

		blogger.debug("response from server: %s"%response)

		blogger.debug("cleaning up")
		clientSocket.close()

		input()