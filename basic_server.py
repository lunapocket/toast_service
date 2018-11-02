from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import threading
import os
from urllib.parse import urlparse

import ssl

from autolog import autolog, call_log_class, call_log_class_soft
# logger.getlogger

@call_log_class
class securedHTTPServer(HTTPServer):
	'''https://stackoverflow.com/questions/8582766/adding-ssl-support-to-socketserver'''
	'''python official docs about ssl'''
	def __init__(self, server_address, RequestHandlerClass, 
			certfile = None, keyfile = None, 
			ssl_version=ssl.PROTOCOL_TLS, bind_and_activate=True):

		HTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
		self.certfile = certfile
		self.keyfile = keyfile
		self.ssl_version = ssl_version
		if certfile == None:
			self.context = None
		else:
			self.context = ssl.SSLContext(protocol = ssl_version)
			self.context.load_cert_chain(certfile = certfile, keyfile = keyfile)

	def get_request(self):
		if self.context == None:
			return super().get_request() #인증서 정보가 없으면 기본 연결 사용
		newsocket, fromaddr = self.socket.accept()
		# blogger.info("new socket set")
		connstream = self.context.wrap_socket(newsocket, server_side = True)

		return connstream, fromaddr

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
class ThreadedHTTPServer(socketserver.ThreadingMixIn, securedHTTPServer):
	pass


if __name__ == '__main__':
	address = ('127.0.0.1', 8192) #let the kernal give us a port
	server = ThreadedHTTPServer(address, ThreadedHTTPRequestHandler, 
		certfile="c://temp/keys/toast2_cert.pem", keyfile="c://temp/keys/toast2_key.pem")
	server.serve_forever()