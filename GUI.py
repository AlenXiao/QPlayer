# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import sys
import os
from UserDict import UserDict
from win32com.client import Dispatch
filename = "Qmp3player"

def stripnulls(data):
	"strip whitespace and nulls"
	return data.replace("\00", "").strip()

class FileInfo(UserDict):
	"store file metadata"
	def __init__(self, filename=None):
		UserDict.__init__(self)
		self["name"] = filename

class MP3FileInfo(FileInfo):
	"store ID3v1.0 MP3 tags"
	tagDataMap = {"title"   : (  3,  33, stripnulls),
					"artist"  : ( 33,  63, stripnulls),
					"album"   : ( 63,  93, stripnulls),
					"year"    : ( 93,  97, stripnulls),
					"comment" : ( 97, 126, stripnulls),
					"genre"   : (127, 128, ord)}

	def __parse(self, filename):
		"parse ID3v1.0 tags from MP3 file"
		self.clear()
		try:                               
			fsock = open(filename, "rb", 0)
			try:                           
				fsock.seek(-128, 2)        
				tagdata = fsock.read(128)  
			finally:                       
				fsock.close()              
			if tagdata[:3] == "TAG":
				for tag, (start, end, parseFunc) in self.tagDataMap.items():
					self[tag] = parseFunc(tagdata[start:end])               
		except IOError:                    
			pass                           

	def __setitem__(self, key, item):
		if key == "name" and item:
			self.__parse(item)
		FileInfo.__setitem__(self, key, item)

def listDirectory(directory, fileExtList):                                        
	"get list of file info objects for files of particular extensions"
	fileList = [os.path.normcase(f)
				for f in os.listdir(directory)]           
	fileList = [os.path.join(directory, f) 
				for f in fileList
				if os.path.splitext(f)[1] in fileExtList] 
	def getFileInfoClass(filename, module=sys.modules[FileInfo.__module__]):      
		"get file info class from filename extension"                             
		subclass = "%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]       
		return hasattr(module, subclass) and getattr(module, subclass) or FileInfo
	return [getFileInfoClass(f)(f) for f in fileList]                             

"""if __name__ == "__main__":
    for info in listDirectory("/music/_singles/", [".mp3"]):
        print "\n".join(["%s=%s" % (k, v) for k, v in info.items()])
        print
"""
	
		
for info in listDirectory(r"D:\Python\python\code\Mini+Player",[".mp3"]):
	medialist = "\n".join(["%s=%s" % (k, v) for k, v in info.items()])
		
class Application(Frame):
	def __init__(self,master=None):
		Frame.__init__(self,master)
		self.pack()
		self.createWidgets()
		
	def createWidgets(self):
		self.QUIT = Button(self)
		self.QUIT["text"] = "退出"
		self.QUIT["fg"] = "red"
		self.QUIT["command"] = self.quit
		
		self.QUIT.pack({"side": "right"})
		
		
		self.PLAY = Button(self)
		self.PLAY["text"] = "播放"
		self.PLAY["command"] = OnPlay
		
		self.PLAY.pack({"side": "left"})
		
		self.PLAY = Button(self)
		self.PLAY["text"] = "暂停"
		self.PLAY["command"] = OnPause
		
		self.PLAY.pack({"side": "left"})
		
		self.PLAY = Button(self)
		self.PLAY["text"] = "停止"
		self.PLAY["command"] = OnStop
		
		self.PLAY.pack({"side": "left"})
		
		
		self.Mp3InfoLabel = Label(self)
		self.Mp3InfoLabel["text"] = mp3filename
		
		self.Mp3InfoLabel.pack()
		
		self.Mp3InfoLabel = Label(self)
		self.Mp3InfoLabel["text"] = medialist
		
		self.Mp3InfoLabel.pack()
		
		
		
	def quit(self):
		sys.exit(0)
	
	def say_hi(self):
		tkMessageBox.showinfo('Message','Hello!')
	

	
mp3filename = 'x.mp3'


wmp=Dispatch('WMPlayer.OCX')
media=wmp.newMedia(mp3filename)
wmp.currentPlaylist.appendItem(media)
#medialist = wmp.currentPlaylist
def OnPlay():
	wmp.controls.play()
def OnPause():
	wmp.controls.pause()
def OnNext():
	wmp.controls.next()
def OnStop():
	wmp.controls.stop()
Position = 'wmp.controls.currentPositionString()'
#medialist = wmp.currentMedia.getItemInfo(mp3filename)
app = Application()
app.master.title('Qmp3player')
app.mainloop()
