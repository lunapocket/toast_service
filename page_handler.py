from urllib.parse import urlparse, urlunparse, urljoin
import tempfile

import requests
from bs4 import BeautifulSoup

from autolog import autolog, call_log_class, call_log_class_soft, blogger


@call_log_class
class RequestHandler(object):
	default_port = 80
	default_headers = None

	def __init__(self, url = None, UA = '', default_port = ''):
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

		if(len(parsed.netloc) == 0 and parsed.path[0] == '/'): #/path 의 경우 현재 내가 접속한 곳을 기준으로 바꾼다.
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

@call_log_class
class Browser(RequestHandler):
	default_headers = {}
	def __init__(self, url = '', UA = '', default_port = 80):
		super().__init__()

		self.UA = UA
		self.default_port = default_port
		if UA:
			self.default_headers['user-agent'] = self.UA

	def load_page(self, url = ''):
		self.image_bytes = {};
		self.addr = url

		r = self.do_get(url)
		_type = self._get_type(r)
		if(_type == 'text'):
			soup = BeautifulSoup(r.text,'html.parser')
			for tag in soup.find_all('img'):
				self.image_bytes[tag['src']] = self.do_get(tag['src']).content
		if(_type == 'image'):
			self.image_bytes[urlparse(self.addr).path] = r.content

		return r.content

	def do_request(self, URL = '', params = '', headers = default_headers, type = 'get'):
		if(type == 'get'):
			r = self.do_get(URL, params, headers)
		elif(type == 'post'):
			r = self.do_post(URL, params, headers)
		elif(type == 'put'):
			r = self.do_put(URL, params, headers)

		self._type = self._get_type(r)

		if(self._type == 'text'):
			content = r.text
		else:
			content = r.content

		return content

	def _get_type(self, r): #image or text 반환
		try:
			content_type = r.headers['content-type']
		except KeyError:
			return 'raw' #nothing is specified, so return raw
		if('text' in content_type):
			return 'text'
		elif('image' in content_type):
			return 'image'
		else:
			return 'raw'


if __name__ == '__main__':
	b = Browser(UA = '2013034135/JiHoonLee/Browser/COMNET2018', default_port = 80)
	b.addr = 'www.naver.com/asdf/asdf.png'