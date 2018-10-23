from urllib.parse import urlparse, urlunparse, urljoin 

import requests
import bs4

from autolog import autolog, call_log_class, call_log_class_soft, blogger


@call_log_class
class RequestHandler():
	default_port = 80
	default_headers = None

	def __init__(self, url = None):
		if(url is not None):
		    self.addr = url

	@property
	def addr(self):
		try:
			return self._addr
		except AttributeError:
			return None

	@addr.setter
	def addr(self, url ='', port = default_port):
		parsed = urlparse(url)
		if(len(parsed.scheme) == 0 and len(parsed.netloc) == 0 and len(parsed.path) > 0):
			try:
				parsed = urlparse('http://' + url)
			except:
				raise ValueError('somethings wrong with url')

		if(parsed.scheme != 'http'):
			raise ValueError('inappropriate url using other protocol')

		if(self.addr is not None and parsed.path[0] == '/'): #/path 의 경우 현재 내가 접속한 곳을 기준으로 바꾼다.
				new_path = parsed.path
				parsed = urlparse(self.addr)
				parsed = parsed._replace(path = new_path)

		try: #url 자체가 port 번호를 가지고 있는지 파악, port번호가 없으면 port 번호를 받아서 넘겨준다.(기본 80)
			port = parsed.netloc.split(':')[1]
		except IndexError:
			parsed = parsed._replace(netloc = parsed.netloc + ":" + str(port))


		self._addr = urlunparse(parsed)


	def do_get(self, URL = addr, params = '', headers = default_headers):
		self.addr = URL #URL을 형식에 맞게 갱신
		r = requests.get(self.addr, params = params, headers = headers)
		r.raise_for_status()

		return r


	def do_post(self, URL = addr, data = '', headers = default_headers):
		self.addr = URL
		r = requests.post(self.addr, data = data, headers = headers)
		r.raise_for_status()

		return r

	def do_put(self, URL = addr, data = '', headers = default_headers):
		self.addr = URL;
		r = requests.put(self.addr, data = data, headers = headers)
		r.raise_for_status()

		return r

	def parseHTML():
		pass

@call_log_class
class Browser(RequestHandler):
	def __init__(self, UA = '', default_port = 80):
		super(Browser, self).__init__()

		self.UA = UA
		self.default_port = default_port

		self.default_headers = {'user-agent': self.UA}

	def load_page(self, url = ''):
		pass
		# self.page = page(url)

if __name__ == '__main__':
	b = Browser()
	b.addr = 'www.naver.com/asdf/asdf.png'