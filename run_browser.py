from ast import literal_eval

from browser_UI import *
from page_handler import *

from autolog import autolog, call_log_class, call_log_class_soft, blogger

@call_log_class
class run(UI, Browser):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.execB.config(command = self.execCallback)
		self.loadB.config(command = self.loadCallback)
		self.getB.config(command = self.getCallback)
		self.postB.config(command = self.postCallback)
		self.putB.config(command = self.putCallback)

	def updateAddr(self): #addr_bar에 있는 경로로 addr을 맞춤.
		self.addr = self.addr_bar.get()
		try:
			self.tempPayload = literal_eval(self.payload_entry.get())
		except:
			self.tempPayload = self.payload_entry.get()

		if(type(self.tempPayload) != type({}) and type(self.tempPayload) != type('str')):
			self.tempPayload = str(self.tempPayload)

		self.addr_bar.delete(0, END)
		self.addr_bar.insert(0, self.addr)

	def loadCallback(self):
		self.page_canvas.clear()
		self.updateAddr()
		content = self.load_page(self.addr)
		
		i = 0
		for key, value in self.image_bytes.items():
			i = i + 1
			self.page_canvas.writeNextObject(type = 'image', content = value, expandscroll = False)
			self.page_canvas.writeNextObject(content = 'pic) %d : %s'%(i, key), expandscroll = False)


		self.page_canvas.writeNextObject(content = str(content), expandscroll = False)

	def getCallback(self):
		self.page_canvas.clear()
		self.updateAddr()
		content = self.do_request(URL = self.addr, params = self.tempPayload, type = 'get')
		if(self._type == 'image'):
			self.page_canvas.writeNextObject(type = 'image', content = content)
		else:
			self.page_canvas.writeNextObject(content = content)

	def postCallback(self):
		self.page_canvas.clear()
		self.updateAddr()
		content = self.do_request(URL = self.addr, params = self.tempPayload, type = 'post')
		if(self._type == 'image'):
			self.page_canvas.writeNextObject(type = 'image', content = content)
		else:
			self.page_canvas.writeNextObject(content = content)
		

	def putCallback(self):
		self.page_canvas.clear()
		self.updateAddr()
		content = self.do_request(URL = self.addr, params = self.tempPayload, type = 'put')
		if(self._type == 'image'):
			self.page_canvas.writeNextObject(type = 'image', content = content)
		else:
			self.page_canvas.writeNextObject(content = content)

	def execCallback(self):
		# console_canvas.create_text(2, 0, anchor=NW, text = 'hi')
		oldstdout = sys.stdout
		sys.stdout = mystdout = StringIO()
		cmd = self.console_entry.get()

		self.console_canvas.writeNextObject(content = '>> ' + cmd)
		try:
			eval(cmd)
			content = mystdout.getvalue()
			if(len(content) == 0):
				eval('print('+ cmd +')')
				content = mystdout.getvalue()
			self.console_canvas.writeNextObject(content = content)
		except:
			pass
		mystdout.close()

		self.console_entry.delete(0, END)

if __name__ == '__main__':
	b = run(UA = '2013034135/JiHoonLee/Browser/COMNET2018')
	# b.addr_bar.insert(0, 'httpbin.org/get')
	# b.loadCallback()
	b.window.mainloop()