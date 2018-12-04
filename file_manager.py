from threading import Lock
import tempfile
import os

class Test(object):
	def send(self, key):
		basefile = os.getcwd() + '\\files\\storage\\%s' % key

		for i in self.iter_chunk(basefile, chunk_size = 1024):
			print(self._wrap_chunk(i))
		print(self._wrap_chunk(b''))

	def iter_chunk(self, file_path, chunk_size = 1024768):
		with open(file_path, 'rb') as f:
			while True:
				data = f.read(chunk_size)
				if not data:
					break
				yield data

	def _wrap_chunk(self, blob):
		return b'%x\r\n%s\r\n' % (len(blob), blob)


class Record(object):

	def __init__(self, key = None, IP = None, realname = None, password = None, time_expire = None, frame = None, written_frame_szie = None):
		self.key = key
		self.IP = IP
		self.realname = realname
		self.password = password
		self.time_expire = time_expire
		self.frame = frame
		self.written_frame_size = written_frame_size

class FileManager(object):

	def __init__(self):
		self._active_record = {} # dict of key (tempfile 명): IP , realname, password, time_expire, frame, written_frame_size
		self.record_lock = Lock()
		self.db_lock = Lock()

	def parse_multipart(self):
		pass

	def init_recv(self, info_list = {}):
		temp_file_name = self._request_key()

		return temp_file_name

	def process_recv(self):
		pass


	def finish_recv(self):
		#close fp and update db and 
		pass

	def _request_key(self):
		'''making temp file and return the name so that can be added to the record'''
		return tempfile.mkstemp(dir = os.getcwd() + '/files/storage/')

	@property
	def active_record(self):
		with record_lock:
			return _active_record

	@active_record.setter
	def active_record(self, input = None):
		with record_lock:
			if not input:
				return
			_active_record.update(input)
			

	def _update_db(self):
		with db_lock:
			pass

if __name__ == '__main__':
	ex = Test()
	ex.send('alice.txt')