from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import threading
import os
from urllib.parse import urlparse

import ssl

import cgi
from io import BytesIO as IO

from file_manager import Record
from autolog import autolog, call_log_class, call_log_class_soft, blogger
# logger.getlogger

# @call_log_class
class securedHTTPServer(HTTPServer):
	'''
	https://stackoverflow.com/questions/8582766/adding-ssl-support-to-socketserver
	python official docs about ssl
	'''
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

# @call_log_class
class ThreadedHTTPRequestHandler(BaseHTTPRequestHandler):

	active_record = {} #key and other info
	record_lock = threading.Lock()
	db_lock = threading.Lock()

	def __init__(self, request, client_address, server):
		# https://stackoverflow.com/questions/4685217/parse-raw-http-headers
		BaseHTTPRequestHandler.__init__(self, request, client_address, server)
		# blogger.info(self.headers.__dict__)
		#'self._headers': [('Host', '127.0.0.1:8192'), ('User-Agent', 'Mozilla/5.0')]... '''

		# print(self.request_version)

		return  

	def do_GET(self):
		self.parsed_path = urlparse(self.path)
		filepath = self.parsed_path.path
		filename, file_extension = os.path.splitext(filepath)
		message = self._getFile(filepath)

		if self.request_version == "HTTP/1.1":
			if message != 0:
				self.send_response(200)
				if file_extension == '.jpg':
					self.send_header('Content-Type', 'image/jpeg')
				else:
					self.send_header('Content-Type', 'text/html')
				self.end_headers()
				self.wfile.write(message)
			else:
				self.send_response(404)
				self.end_headers()
		else:
			self.send_response(400)
			self.end_headers()
		# message = bytes(self.requestline,'utf8')

		return

	def do_POST(self):
		# multipart 오브젝트가 가지고 있어야 할 것 
		content_length = int(self.headers.get('content-length', 0))
		body = self.rfile.read(content_length)
		environ={'REQUEST_METHOD': 'POST'}

		print(self.headers.get('content-type'))
		print(self.client_address)

		if('multipart/form-data' in self.headers.get('content-type')):
			parsed = cgi.FieldStorage(IO(body), headers = self.headers, environ = environ)

			# print(parsed)
			

		# print('---- start')
		# print(self.headers['content-length'])
		# print('---- end')
		return

	def _parse_multipart(self, fs):
		'''fieldstorage -> dict'''
		data = {}
		for element in fs.list:
			data[element.name] = element.value

		return data		
	
	def _getFile(self, filename):
		'''get and read file and return the bytestring '''
		path = os.path.abspath("./files/" + filename)
		
		try:
			with open(path, "rb") as f:
				doc = f.read()
		except:
			doc = 0

		return doc
	
# @call_log_class_soft
class ThreadedHTTPServer(socketserver.ThreadingMixIn, securedHTTPServer):
	pass


if __name__ == '__main__':
	address = ('127.0.0.1', 8192) #let the kernal give us a port
	server = ThreadedHTTPServer(address, ThreadedHTTPRequestHandler, 
		certfile="c://temp/keys/toast2_cert.pem", keyfile="c://temp/keys/toast2_key.pem", f)
	server.serve_forever()
