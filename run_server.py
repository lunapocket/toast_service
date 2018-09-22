if __name__ == '__main__':
	from basic_server import *
	from autolog import *

	import threading

	address = ('127.0.0.1', 8192) #let the kernal give us a port

	server = ThreadedEchoServer(address, ThreadedEchoRequestHandler)
	ip, port = server.server_address

	t = threading.Thread(target = server.serve_forever)
	t.setDaemon(True)
	t.start()

	blogger.info('server on %s:%s on %s', ip, port, t.getName())
