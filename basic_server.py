import socketserver
from autolog import autolog, call_log_class
# logger.getlogger

@call_log_class
class EchoRequestHandler(socketserver.BaseRequestHandler):

	
	def __init__(self, request, client_address, server):
		socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
		return

	
	def setup(self):
		return socketserver.BaseRequestHandler.setup(self)
	
	def handle(self):
		data = self.request.recv(1024)
		print('recv() -> %s'%data)
		self.request.send(data)
		return

	
	def finish(self):
		return socketserver.BaseRequestHandler.finish(self)

@call_log_class
class EchoServer(socketserver.TCPServer):

	
	def __init__(self, server_address, handler_class=EchoRequestHandler):
		socketserver.TCPServer.__init__(self, server_address, handler_class)
		return

	
	def server_activate(self):
		socketserver.TCPServer.server_activate(self)

	@autolog(msg = "Handling requests, press ^c to quit")
	def server_forever(self):
		while True:
			self.handle_request()
		return

	
	def handle_request(self):
		return socketserver.TCPServer.handle_request(self)

	
	def verify_request(self, request, client_address):
		return socketserver.TCPServer.verify_request(self, request, client_address)

	
	def process_request(self, request, client_address):
		return socketserver.TCPServer.process_request(self, request, client_address)

	
	def server_close(self):
		return socketserver.TCPServer.server_close(self)

	
	def finish_request(self, request, client_address):
		return socketserver.TCPServer.finish_request(self, request, client_address)

	
	def close_request(self, request_address):
		return socketserver.TCPServer.close_request(self, request_address)


@call_log_class
class A(object):

	def __init__(self, msg='hi'):
		print('inited A')

	def __call__(self, *args):
		print('called')
		return
		
	def foo(self, *args, **kwargs):
		'''I am Foo DoC'''

		print("sum is %d"%sum(args))

		# A.bar(self, *args)
		return None

	def bar(self, *args, **kwargs):
		'''I am Bar DoC'''

		print("sum is %d"%sum(args))
		return None

if __name__ == '__main__':
	a = A()
	# autolog

	a.foo(3,4)
	# A.foo = autolog(msg = 'hi')(A.foo)
	# A.foo(1,2)
	

	a.bar(1,2)
	# A.bar = autolog(A.bar)
	# A.bar(1,2)