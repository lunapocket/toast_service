from browser_UI import *
from page_handler import *

class run(UI, Browser):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.execB.config(command = self.execCallback)
		self.loadB.config(command = self.loadCallback)
		self.getB.config(command = self.getCallback)
		self.postB.config(command = self.postCallback)
		self.putB.config(command = self.putCallback)

	def loadCallback():
		pass

	def getCallback():
		pass

	def postCallback():
		pass

	def putCallback():
		pass

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
	# b.window.mainloop()