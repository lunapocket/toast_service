from basic_server import *
if __name__ == '__main__':

	address = ('localhost', 8192) #let the kernal give us a port

	server = EchoServer(address, EchoRequestHandler)
	ip, port = server.server_address

	server.server_forever()

