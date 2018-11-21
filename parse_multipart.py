import cgi
from io import BytesIO as IO

class MultiForm(object):

	def __init__(self, headers, body):
		parsed = cgi.FieldStorage(IO(body.encode('utf-8')), headers = headers3, environ = environ)

	def headers_to_dict(self):
		'''[('Host', '127.0.0.1:8192'), ('User-Agent', 'Mozilla/5.0')] 형태를 dict로 변경'''



	



if __name__ == '__main__':
	body_file = '''-----------------------------146043902153
Content-Disposition: form-data; name="start"

5120
-----------------------------146043902153
Content-Disposition: form-data; name="end"

6144
-----------------------------146043902153
Content-Disposition: form-data; name="file"; filename="blob"
Content-Type: application/octet-stream

 just begun to dream that she
was walking hand in hand with Dinah, and saying to her very
earnestly, `Now, Dinah, tell me the truth:  did you ever eat a
bat?' when suddenly, thump! thump! down she came upon a heap of
sticks and dry leaves, and the fall was over.

  Alice was not a bit hurt, and she jumped up on to her feet in a
moment:  she looked up, but it was all dark overhead; before her
was another long passage, and the White Rabbit was still in
sight, hurrying down it.  There was not a moment to be lost:
away went Alice like the wind, and was just in time to hear it
say, as it turned a corner, `Oh my ears and whiskers, how late
it's getting!'  She was close behind it when she turned the
corner, but the Rabbit was no longer to be seen:  she found
herself in a long, low hall, which was lit up by a row of lamps
hanging from the roof.

  There were doors all round the hall, but they were all locked;
and when Alice had been all the way down one side and up the
other, trying every door, she
-----------------------------146043902153--'''
	body_original = '''-----------------------------265001916915724
Content-Disposition: form-data; name="time-expire"

1234
-----------------------------265001916915724
Content-Disposition: form-data; name="password"


-----------------------------265001916915724--
'''

	body1 = '''-----------------------------spam
Content-Disposition: form-data; name="time-expire"; filename=blob

1234
-----------------------------spam
Content-Disposition: form-data; name="password"; filename= hi
Content-Type: binary/octect-stream

hihi
-----------------------------spam--
'''
	body2 = """
--spam
Content-Disposition: form-data; name="param1"; filename=blob
Content-Type: binary/octet-stream

value1
--spam--
"""
	body = body_file
	headers={'content-type': 'multipart/form-data; boundary=spam;', 'content-length': len(body)}
	headers2 ={'content-type': 'multipart/form-data; boundary=---------------------------265001916915724', 'content-length': len(body)}
	headers3 ={'content-type': 'multipart/form-data; boundary=---------------------------146043902153', 'content-length': len(body)}
	environ={'REQUEST_METHOD': 'POST'}

	input_headers = [('Host', '127.0.0.1:8192'), ('User-Agent', 'Mozilla/5.0')]

	parsed = cgi.FieldStorage(IO(body.encode('utf-8')), headers = headers3, environ = environ)
	# parsed2 = cgi.parse_multipart(IO(body.encode('utf-8')), pdict = headers2)