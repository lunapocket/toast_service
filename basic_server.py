from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import threading
import os
from urllib.parse import urlparse


from autolog import autolog, call_log_class, call_log_class_soft
# logger.getlogger

@call_log_class
class ThreadedHTTPRequestHandler(BaseHTTPRequestHandler):

	def __init__(self, request, client_address, server):
		# https://stackoverflow.com/questions/4685217/parse-raw-http-headers
		BaseHTTPRequestHandler.__init__(self, request, client_address, server)
		
		

		print(self.request_version)


		return  

	def do_GET(self):
		self.parsed_path = urlparse(self.path)
		filepath = self.parsed_path.path
		filename, file_extension = os.path.splitext(filepath)
		
		message = self._getFile(filepath)

		if self.request_version == "HTTP/1.1":
			if message != 0:
				self.send_response(200)
				self.send_header('Content-Length', '1024')
				if file_extension == '.jpg':
					self.send_header('Content-Type', 'image/jpeg')
				else:
					self.send_header('Content-Type', 'text/html')
				self.end_headers()
				self.wfile.write(message)
			else:
				self.send_response(404)
				self.send_header('Content-Length', '1024')
				self.end_headers()
		else:
			self.send_response(400)
			self.send_header('Content-Length', '1024')
			self.end_headers()
		# message = bytes(self.requestline,'utf8')
		
		

		return

	
	def _getFile(self, filename):
		path = os.path.abspath("./files/" + filename)
		
		try:
			with open(path, "rb") as f:
				doc = f.read()
		except:
			doc = 0

		return doc
	
@call_log_class_soft
class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
	pass


if __name__ == '__main__':
	address = ('127.0.0.1', 8192) #let the kernal give us a port
	server = ThreadedHTTPServer(address, ThreadedHTTPRequestHandler)
	server.serve_forever()