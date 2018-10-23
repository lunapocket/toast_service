import tkinter
from tkinter import *

class advCanvans(Canvas):
	objCount = 0; #tag 대신 사용

	def writeNextObject(self, type = 'text', content = '', xoffset = 2, yoffset = 0):
		if objCount == 0:
			x = 0; y = 0;
		
		try:
			beforeCoord = self.bbox(objCount - 1)[0] #바로 이전 친구 참조
			x = beforeCoord[0] + xoffset; y = beforeCoord[3] + yoffset
		except:
			x = 0; y = 0;

		if type == 'text':
			self.create_text(x = x, y = y, anchor=NW, text = content, tags = self.objCount, width = self.width * 0.9)

		self.objCount = self.objCount + 1

