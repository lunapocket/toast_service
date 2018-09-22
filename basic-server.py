import socketserver
from autolog import AutoLog
# logger.getlogger




class EchoRequestHandler(socketserver.BaseRequestHandler):

	# self.logger =
	def __init__(self, request, client_address, server):
		pass

class A(object):

	@AutoLog
	def foo():
		return None

if __name__ == '__main__':
	A.foo()
	# on the fly testerc