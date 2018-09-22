import socketserver
import threading
from autolog import autolog, call_log_class
# logger.getlogger

@call_log_class
class ThreadedEchoRequestHandler(socketserver.BaseRequestHandler):

	def handle(self):
		data = self.request.recv(1024)
		cur_thread = threading.currentThread()
		response = '%s: %s' % (cur_thread.getName(), data)
		self.request.send(bytes(response, 'utf8'))
		return

	
@call_log_class
class ThreadedEchoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass


if __name__ == '__main__':
	pass
	# a = A()
	# # autolog

	# a.foo(3,4)
	# # A.foo = autolog(msg = 'hi')(A.foo)
	# # A.foo(1,2)
	

	# a.bar(1,2)
	# # A.bar = autolog(A.bar)
	# # A.bar(1,2)