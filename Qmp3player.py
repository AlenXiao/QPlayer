# -*- coding: utf-8 -*-

#
#
# Created: Wed Nov 26 10:19:46 2014
# Author: MarcoQin
# Email: qyyfy2009@gmail.com
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4 import phonon
from PyQt4.phonon import Phonon
from images import images_rc
from PyQt4.QtGui import *
from PyQt4.phonon import *
import sys
import os
import cPickle as pickle

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Qmp3player(QtGui.QMainWindow):
    # 初始化GUI和播放引擎
    def __init__(self):
        super(Qmp3player, self).__init__()
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
        self.mediaObject = Phonon.MediaObject(self)
        self.mediaInformation = Phonon.MediaObject(self)
        self.mediaObject.setTickInterval(1000)
        self.mediaObject.tick.connect(self.updateTick)
        self.mediaObject.currentSourceChanged.connect(self.songChanged)
        self.mediaObject.stateChanged.connect(self.stateChanged)
        self.mediaInformation.stateChanged.connect(self.mediaStateChanged)
        self.mediaObject.aboutToFinish.connect(self.Finishing)

        Phonon.createPath(self.mediaObject, self.audioOutput)

        self.songList()
        self.setupUi(self)
        self.connectActions()
        self.setupMenu()
        self.volumeSlider.setAudioOutput(self.audioOutput)
        self.volumeSlider.setMaximumVolume(0.8)
        self.seekSlider.setMediaObject(self.mediaObject)

        self.songs = []
        self.songlist = []
        self.loadSongList()
        self.refreshSongList()
        self.wasPlaying = False


    # 连接鼠标Action
    def connectActions(self):
        QtCore.QObject.connect(self.playButton, QtCore.SIGNAL('clicked()'), self.playSong)
        QtCore.QObject.connect(self.pauseButton, QtCore.SIGNAL('clicked()'), self.mediaObject.pause)
        QtCore.QObject.connect(self.stopButton,  QtCore.SIGNAL('clicked()'), self.stopSong)
        self.openAction = QtGui.QAction("Open", self, shortcut="Ctrl+O", triggered=self.addFiles)
        self.exitAction = QtGui.QAction("Exit", self, shortcut="Ctrl+E", triggered=self.close)

        # 连接DEL按钮
        QtCore.QObject.connect((QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self.listWidget)),QtCore.SIGNAL('activated()'), self.delFiles)

        self.listWidget.mouseDoubleClickEvent = self.doubleSelectSong

    def doubleSelectSong(self,a):
         index = self.listWidget.row(self.listWidget.selectedItems()[0])
         self.songSelected(index)

    # 通过list选择歌曲
    def songSelected(self,index):
        self.mediaObject.stop()
        #something seems need here

        self.mediaObject.setCurrentSource(self.songs[index])
        self.mediaObject.play()
        self.wasPlaying = True
        if self.wasPlaying:
            self.playButton.setStyleSheet(_fromUtf8("border-image: url(:/buttons/btn_pause.png);"))
            QtCore.QObject.connect(self.playButton, QtCore.SIGNAL('clicked()'), self.pauseSong)

    def loadSongList(self):
        '''reload(sys)
        sys.setdefaultencoding('utf-8')
        type = sys.getfilesystemencoding()'''
        if os.path.exists('playlist.lst') is True:
            try:
                f = open('playlist.lst', 'rb')
                self.songlist = pickle.load(f)
            except IOError:
                pass
            except EOFError:
                pass
            finally:
                f.close()

        for song in self.songlist:
            #print song
            self.songs.append(Phonon.MediaSource(song))

        self.songList = []


    def saveSongList(self):
        '''reload(sys)
        sys.setdefaultencoding('utf-8')
        type = sys.getfilesystemencoding()'''
        for song in self.songs:
            index = self.songs.index(song)
            self.mediaInformation.setCurrentSource(self.songs[index])
            path = self.mediaInformation.currentSource().fileName()
            #path = str(path).decode('utf-8').encode(type)
            #print path

            self.songlist.append(path)


        file = open('playlist.lst', 'wb')
        pickle.dump(self.songlist, file)
        file.close()

        self.songlist = []
    def addFiles(self):
        files = QtGui.QFileDialog.getOpenFileNames(self, "Please select songs", "", self.tr("Song Files(*.*)"))

        #index = len(self.songs)

        for file in files:
            #print file
            self.songs.append(Phonon.MediaSource(file))
        #print index
        #if self.songs:
        #    self.mediaInformation.setCurrentSource(self.songs[index])
        #   self.mediaObject.setCurrentSource(self.songs[0])
        self.refreshSongList()
        self.saveSongList()

    def delFilesFirst(self,selectedItems):
        index = []
        for item in selectedItems:
            index.append(self.listWidget.row(item))
        index = sorted(index, reverse=True)
        print index

        for num in index:
            self.songs.remove(self.songs[num])
        '''for item in selectedItems:
            index = self.listWidget.row(item)
            print len(self.songs)
            print index

            self.songs.remove(self.songs[index])'''


        self.refreshSongList()
        self.saveSongList()


    def delFiles(self):
        selectedItems = self.listWidget.selectedItems()

        if selectedItems:
            if self.wasPlaying:
                self.mediaObject.stop()
                self.delFilesFirst(selectedItems)
            else:
                self.delFilesFirst(selectedItems)
        else:
            warning = QMessageBox(self)
            warning.setWindowTitle('Warning!')
            warning.setText('NO ITEM SELECTED!')
            warning.show()


    def playSong(self):
        selectedSong = self.listWidget.selectedItems()
        if len(selectedSong) > 0:
            index = self.listWidget.row(self.listWidget.selectedItems()[0])
        else:
            index = 0

        if self.songs[index] == self.mediaObject.currentSource():
            if self.mediaObject.currentSource():
                self.mediaObject.play()
        else:
            self.mediaObject.setCurrentSource(self.songs[index])
            self.mediaObject.play()
        self.wasPlaying = True

        #play按钮变成pause
        if self.wasPlaying:
            self.playButton.setStyleSheet(_fromUtf8("border-image: url(:/buttons/btn_pause.png);"))
            QtCore.QObject.connect(self.playButton, QtCore.SIGNAL('clicked()'), self.pauseSong)
    def pauseSong(self):
        self.playButton.setStyleSheet(_fromUtf8("border-image: url(:/buttons/btn_play.png);"))
        QtCore.QObject.connect(self.playButton, QtCore.SIGNAL('clicked()'), self.playSong)
        self.wasPlaying = False
        self.mediaObject.pause()
    def stopSong(self):
        self.mediaObject.stop()
        QtCore.QObject.connect(self.playButton, QtCore.SIGNAL('clicked()'), self.playSong)
        self.playButton.setStyleSheet(_fromUtf8("border-image: url(:/buttons/btn_play.png);"))
        self.lcdNumber.display('00:00')
    # 如果改变了歌曲，在table上将之高亮，重设时间显示
    def songChanged(self,source):
        self.listWidget.setCurrentRow(self.songs.index(source))
        #self.listWidget.setItemSelected(self.listWidget.(self.songs.index(source)))
        self.lcdNumber.display('00:00')

    # 根据播放状态改变按钮状态
    def stateChanged(self, newState):
        pass
    # 播放将要结束时，将下一首歌曲排入播放队列
    def Finishing(self):
        index = self.songs.index(self.mediaObject.currentSource()) + 1  #播放序列+1
        if len(self.songs) > index:
            self.mediaObject.enqueue(self.songs[index])
        else:
            self.mediaObject.enqueue(self.songs[0])

    # 设置播放器时间
    def updateTick(self,time):
        songTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.lcdNumber.display(songTime.toString('mm:ss'))
    def songList(self):
        pass
    # 提取文件名
    def parseName(self,source):
        title =  source.split('/')[-1]
        title =  title.split('.')
        if len(title) == 2:
            return title[0]
        elif len(title) == 1:
            return title[0]
        else:
            return title[-2]

    def refreshSongList(self):
        self.listWidget.clear()

        for song in self.songs:
            index = self.songs.index(song)
            self.mediaInformation.setCurrentSource(self.songs[index])
            title = self.mediaInformation.currentSource().fileName()

            #print title
            title = self.parseName(title)
            #print title
            self.listWidget.addItem(title)
    # 在table上显示歌名
    def mediaStateChanged(self):
        # mediaData = self.mediaInformation.metaData()  # 找到media的元数据
        title = self.mediaInformation.currentSource().fileName()  # 文件名

        title = self.parseName(title)


        #titleItem = QtGui.QTableWidgetItem(title)
        #titleItem.setFlags(titleItem.flags() ^ QtCore.Qt.ItemIsEditable)

        #currentRow = self.tableWidget.rowCount()
        #self.tableWidget.insertRow(currentRow)
        #self.tableWidget.setItem(currentRow, 0,titleItem)
        #self.listWidget.addItem(title)

        #index = self.songs.index(self.mediaInformation.currentSource()) + 1
        #if len(self.songs) > index:
        #    self.mediaInformation.setCurrentSource(self.songs[index])
        #else:
        #    pass#self.tableWidget.resizeColumnsToContents()

    def setupMenu(self):
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.exitAction)
    def setupUi(self, Qmp3player):
        Qmp3player.setObjectName(_fromUtf8("Qmp3player"))
        Qmp3player.resize(342, 428)
        Qmp3player.setMinimumSize(QtCore.QSize(342, 428))
        Qmp3player.setMaximumSize(QtCore.QSize(342, 428))
        Qmp3player.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"
""))
        self.centralWidget = QtGui.QWidget(Qmp3player)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))

        self.lcdNumber = QtGui.QLCDNumber(self.centralWidget)
        self.lcdNumber.setGeometry(QtCore.QRect(250, 280, 64, 23))
        self.lcdNumber.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))

        self.seekSlider = phonon.Phonon.SeekSlider(self.centralWidget)
        self.seekSlider.setGeometry(QtCore.QRect(20, 280, 221, 19))
        self.seekSlider.setObjectName(_fromUtf8("seekSlider"))

        self.volumeSlider = phonon.Phonon.VolumeSlider(self.centralWidget)
        self.volumeSlider.setGeometry(QtCore.QRect(210, 340, 109, 22))
        self.volumeSlider.setStyleSheet(_fromUtf8(""))
        self.volumeSlider.setObjectName(_fromUtf8("volumeSlider"))

        self.playButton = QtGui.QPushButton(self.centralWidget)
        self.playButton.setGeometry(QtCore.QRect(20, 320, 51, 51))
        self.playButton.setStyleSheet(_fromUtf8("border-image: url(:/buttons/btn_play.png);"))
        self.playButton.setText(_fromUtf8(""))
        self.playButton.setObjectName(_fromUtf8("playButton"))

        self.pauseButton = QtGui.QPushButton(self.centralWidget)
        self.pauseButton.setGeometry(QtCore.QRect(80, 320, 51, 51))
        self.pauseButton.setStyleSheet(_fromUtf8("border-image: url(:/buttons/btn_pause.png);"))
        self.pauseButton.setText(_fromUtf8(""))
        self.pauseButton.setObjectName(_fromUtf8("pauseButton"))

        self.stopButton = QtGui.QPushButton(self.centralWidget)
        self.stopButton.setGeometry(QtCore.QRect(140, 320, 51, 51))
        self.stopButton.setStyleSheet(_fromUtf8("border-image: url(:/buttons/btn_stop.png);"))
        self.stopButton.setText(_fromUtf8(""))
        self.stopButton.setObjectName(_fromUtf8("stopButton"))

        self.listWidget = QtGui.QListWidget(self.centralWidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 20, 291, 241))

        self.listWidget.setObjectName(_fromUtf8("tableWidget"))
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)  # 设置多选模式，用于多文件删除


        Qmp3player.setCentralWidget(self.centralWidget)

        self.retranslateUi(Qmp3player)
        QtCore.QMetaObject.connectSlotsByName(Qmp3player)

    def retranslateUi(self, Qmp3player):
        Qmp3player.setWindowTitle(_translate("Qmp3player", "Qmp3player", None))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    QUI = QtGui.QMainWindow()
    ui = Qmp3player()
    ui.show()

    sys.exit(app.exec_())

