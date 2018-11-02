import socket
import ssl
from autolog import *

if __name__ == '__main__':

	HOST = '127.0.0.1'
	PORT = 8192 #kernel will designate the port
	BUFSIZE = 1024
	ADDR = (HOST, PORT)

	import os
	import socket, ssl

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	context = ssl.SSLContext()
	context.load_verify_locations("c:/temp/keys/toast2_cert.pem")
	ssl_sock = context.wrap_socket(s)
	print("ssl_estabilished")
	ssl_sock.connect(('127.0.0.1',8192))
	print("socket sent")
	ssl_sock.send('hello ~MySSL !')
	print(ssl_sock.recv(4096))
	ssl_sock.close()

	# while True:
		# blogger.info("creating socket")
		# clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# blogger.info("connecting to server")
		# clientSocket.connect(ADDR)

		# message = b"hello, world"
		# blogger.debug('sending data: %s', message)
		# len_sent = clientSocket.send(message)

		# blogger.debug("connection has been established")
		# response = clientSocket.recv(len_sent)

		# blogger.debug("response from server: %s"%response)

		# blogger.debug("cleaning up")
		# clientSocket.close()

		# input()