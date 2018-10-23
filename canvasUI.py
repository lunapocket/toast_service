import tkinter
from tkinter import *

from autolog import blogger

class advCanvas(Canvas):
	objCount = 0; #tag 대신 사용
	objs = [];

	def writeNextObject(self, type = 'text', content = '', xoffset = 0, yoffset = 5, startx = 2):
		self.x = startx
		if self.objCount == 0:
			x = self.x; y = 1;
		else:
				beforeCoord = self.bbox(self.objs[self.objCount - 1]) #바로 이전 친구 참조
				x = self.x; y = beforeCoord[3] + yoffset

			

		if type == 'text':
			objTemp = self.create_text(x, y, anchor=NW, text = content, tags = str(self.objCount), width = self.winfo_width() * 0.9)

		self.objs.append(objTemp);
		self.objCount = self.objCount + 1
