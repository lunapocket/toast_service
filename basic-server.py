import socketserver
from autolog import Autolog
# logger.getlogger

autolog = Autolog(None)

class EchoRequestHandler(socketserver.BaseRequestHandler):

	@Autolog
	def __init__(self, request, client_address, server):
		socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
		return

	@Autolog
	def setup(self):
		return SocketServer.BaseRequestHandler.setup(self)

	@Autolog
	def handle(self):
		autolog.logger.debug('recv() -> %s'%data)
		data = self.request.recv(1024)
		return

	@Autolog
	def finish(self):
		return SocketServer.BaseRequestHandler.finish(self)

class EchoServer(socketserver.TCPServer):

	@Autolog
	def __init__(self, server_address, handler_class=EchoRequestHandler):
		socketserver.TCPServer.__init(self, server_address, handler_class)
		return

	@Autolog
	def server_activate(self):
		socketserver.TCPServer.server_activate(self)

	@Autolog
	def serve_forever(self):
		autolog.logger.info("Handling requests, press ^c to quit")
		while True:
			self.handle_request()
		return

	@Autolog
	def handle_request(self):
		return socketserver.TCPServer.handle_request(self)

	@Autolog
	def verify_request(self, request, client_address):
		return socketserver.TCPServer.verify_request(self, request, client_address)

	@Autolog
	def process_request(self, request, client_address):
		return socketserver.TCPServer.process_request(self, request, client_address)

	@Autolog
	def server_close(self):
		return socketserver.TCPServer.server_close(self)

	@Autolog
	def finish_request(self, request, client_address):
		return socketserver.TCPServer.finish_request(self, request, client_address)

	@Autolog
	def close_request(self, request_address):
		return socketserver.TCPServer.close_request(self, request_address)


# class A(object):
# 	@Autolog
# 	def foo(*args, **kwargs):
# 		return None

if __name__ == '__main__':
		
	# on the fly testerc