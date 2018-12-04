from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
import threading
import os
import tempfile
import csv
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

	STORAGE_DIR = os.getcwd() + '/files/storage/'
	DB_PATH = os.getcwd() + '/files/filelist.csv'
	DB_FILE = open(DB_PATH, 'w', newline='', encoding = 'utf-8')

	_active_record = {} #tempfile key / filename, time_expire, password, framesize, written_frame,size
	record_lock = threading.Lock()
	db_lock = threading.Lock()

	active_db = []

	@classmethod
	def set_active_record(cls, input = None):
		with cls.record_lock:
			if not input:
				return
			cls._active_record.update(input)

	@classmethod
	def get_active_record(cls):
		with cls.record_lock:
			return cls._active_record

	@classmethod
	def inc_written_frame(cls, key = None):
		with cls.record_lock:
			try:
				cls._active_record[key]['written_frame_size'] = cls._active_record[key]['written_frame_size'] + 1
			except KeyError:
				pass

	@classmethod
	def del_active_record(cls, key = None):
		with cls.record_lock:
			if not input:
				return
			try:
				del cls._active_record[key]
			except KeyError:
				pass

	@classmethod
	def _update_db(cls, key, record):
		with cls.db_lock:
			writer = csv.writer(cls.DB_FILE, delimiter = ',')
			data = [key, record['file_name'], record['time_expire'], record['password']]
			writer.writerow(data)
			cls.active_db.append(data)
			cls.DB_FILE.flush()
			# print(cls.active_db)
	
	@classmethod
	def _dump_csv(cls):
		with open(DB_PATH, 'r', encoding = 'utf-8') as f:
			reader = csv.reader(f)
			active_db = list(reader)
			print(active_db)

	def __init__(self, request, client_address, server):
		# https://stackoverflow.com/questions/4685217/parse-raw-http-headers
		BaseHTTPRequestHandler.__init__(self, request, client_address, server)
		# blogger.info(self.headers.__dict__)
		#'self._headers': [('Host', '127.0.0.1:8192'), ('User-Agent', 'Mozilla/5.0')]... '''

		#!! load CSV into ram to search it
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
		form = cgi.FieldStorage(
				fp = self.rfile,
				headers = self.headers,
				environ = {'REQUEST_METHOD': 'POST'}
			)

		parsed = self._parse_multipart(form)

		if self.path == "/uploadFileInit":
			self.init_recv(parsed)
		

		if self.path == "/uploadFile":
			self.process_recv(parsed)
			# print(parsed)

		# print('---- start')
		# print(self.headers['content-length'])
		# print('---- end')
		return

	def init_recv(self, data):
		tempfile_info = tempfile.mkstemp(dir = self.STORAGE_DIR) #requesting a key
		key = os.path.basename(tempfile_info[1])
		data['fp'] = os.fdopen(tempfile_info[0], mode = 'w+b') #very temporary! may need to be reset
		data['frame_size'] = int(data['frame_size'])
		data['written_frame_size'] = 0
		data['lock'] = threading.Lock()

		if data['time_expire'] == '':
			data['time_expire'] = 'NULL'
		if data['password'] == '':
			data['password'] = 'NULL'

		self.set_active_record({key:data})
		self.send_response(200)
		self.send_header('content-length', len(key.encode('utf-8')))
		self.end_headers()
		self.wfile.write(key.encode('utf-8'))

	def process_recv(self, data):
		ret = self._write_file(data['key'], data['start'], data['file'])
		if ret == 0:
			self.finalize_recv(data)
			return
		else:
			self.send_response(200)

	def finalize_recv(self, data):
		self.send_response(200)
		key = data['key']
		record = self.get_active_record()[key]
		self.del_active_record(key)
		self._update_db(key, record)

	def error_recv(self, data):
		self.send_response(404)

	def _write_file(self, key, start, content):
		try: 
			data = self.get_active_record()[key]
		except KeyError:
			self.error_recv() #fail handling in fron side

		# print(data)

		with data['lock']:
			data['fp'].seek(int(start))
			data['fp'].write(content)
			self.inc_written_frame(key)
			if data['frame_size'] ==  data['written_frame_size']:
				return 0 #meaning that process is finished
			else:
				return 1

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
		certfile="c://temp/keys/toast2_cert.pem", keyfile="c://temp/keys/toast2_key.pem")
	server.serve_forever()