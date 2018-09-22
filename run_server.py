if __name__ == '__main__':
	from basic_server import *

	address = ('127.0.0.1', 8192) #let the kernal give us a port

	server = EchoServer(address, EchoRequestHandler)
	ip, port = server.server_address

	server.server_forever()

