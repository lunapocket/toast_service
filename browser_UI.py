import tkinter
from tkinter import *

from io import StringIO
import sys

from canvasUI import advCanvas

from autolog import blogger


window=tkinter.Tk()


window.title('Web Browser')
window.geometry("1024x600+100+100")
window.resizable(True, True)

content = tkinter.Frame(window)
page_frame = tkinter.Frame(content)
console_frame = tkinter.Frame(content)
# frame = tkinter.Frame(content, borderwidth = 5, relief="sunken", width=1024, height=600)

addr_bar = tkinter.Entry(content)
addr_label = tkinter.Label(content, text = "address : ")
loadB = tkinter.Button(content, text = "rget",
	overrelief="solid", width=5, command=lambda: loadCallback(), repeatdelay=1000, repeatinterval=100)
getB = tkinter.Button(content, text = "get",
	overrelief="solid", width=5, command=lambda: getCallback(), repeatdelay=1000, repeatinterval=100)
postB = tkinter.Button(content, text = "post",
	overrelief="solid", width=5, command=lambda: postCallback(), repeatdelay=1000, repeatinterval=100)
putB = tkinter.Button(content, text = "put",
	overrelief="solid", width=5, command=lambda: putCallback(), repeatdelay=1000, repeatinterval=100)

page_scrollbar = Scrollbar(page_frame)
page_canvas = Canvas(page_frame, bg ='#FFFFFF')

console_scrollbar = Scrollbar(console_frame)
console_canvas = advCanvas(console_frame, bg ='#FFFFFF', width=150, yscrollcommand = console_scrollbar.set)
console_entry = tkinter.Entry(console_frame)

console_scrollbar['command'] = console_canvas.yview

execB = tkinter.Button(console_frame, text = "exec",
	overrelief="solid", width=5, command=lambda: execCallback(), repeatdelay=1000, repeatinterval=100)

def loadCallback():
	pass

def getCallback():
	pass

def postCallback():
	pass

def putCallback():
	pass

def execCallback():
	# console_canvas.create_text(2, 0, anchor=NW, text = 'hi')
	oldstdout = sys.stdout
	sys.stdout = mystdout = StringIO()
	cmd = console_entry.get()

	console_canvas.writeNextObject(content = '>> ' + cmd)
	try:
		eval(cmd)
		content = mystdout.getvalue()
		if(len(content) == 0):
			eval('print('+ cmd +')')
			content = mystdout.getvalue()
		console_canvas.writeNextObject(content = content)
	except:
		pass
	mystdout.close()

	console_entry.delete(0, END)

content.grid(row = 0, column = 0, sticky = (N, S, E ,W))
addr_label.grid(row = 0, column = 0, sticky = W)
addr_bar.grid(row = 0, column = 1, sticky = (E, W))
loadB.grid(row = 0, column = 2)
getB.grid(row = 0, column = 3)
postB.grid(row = 0, column = 4)
putB.grid(row = 0, column = 5)

page_frame.grid(row = 1, column = 0, columnspan = 2, sticky = (N, S, E, W))
page_canvas.grid(row = 0, column = 0, sticky = (N, S, E, W))
page_scrollbar.grid(row = 0, column = 1, sticky = (N, S, E))

console_frame.grid(row = 1, column = 2, columnspan = 4, sticky = (N, S, E, W))
console_canvas.grid(row = 0, column = 0, sticky = (N, S, E, W))
console_scrollbar.grid(row = 0, column = 1, sticky = (N, S, W))
console_entry.grid(row = 1, column = 0, sticky = (E, W))
execB.grid(row = 1, column = 1, sticky = (E, W))

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=0)
content.columnconfigure(1, weight=99)
content.columnconfigure(2, weight=1)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.columnconfigure(5, weight=1)
# content.rowconfigure(0, weight=1)
content.rowconfigure(1, weight=1)
page_frame.columnconfigure(0, weight=99)
page_frame.rowconfigure(0, weight=99)

console_frame.columnconfigure(0, weight=99)
console_frame.rowconfigure(0, weight=99)

#exec은 간단하므로 여기에 구현

if __name__ == '__main__':
	window.mainloop()
