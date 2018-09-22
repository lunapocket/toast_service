import socket

if __name__ == '__main__':

	HOST = '127.0.0.1'
	PORT = 0 #kernel will designate the port
	BUFSIZE = 1024
	ADDR = (HOST, PORT)

	clientSocket = socket(socket.AF_INET, socket.SOCK_STREAM)

	clientSocket.connect(ADDR)

	print("connection has been established")
`