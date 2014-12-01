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
from PyQt4.QtCore import *
from PyQt4.phonon import *
import sys
import os

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

    # 连接鼠标Action
    def connectActions(self):
        self.connect(self.playButton, SIGNAL('clicked()'), self.mediaObject.play)
        self.connect(self.pauseButton, SIGNAL('clicked()'), self.mediaObject.pause)
        self.connect(self.stopButton, SIGNAL('clicked()'), self.mediaObject.stop)
        self.openAction = QtGui.QAction("Open", self, shortcut="Ctrl+O", triggered=self.addFiles)
        self.exitAction = QtGui.QAction("Exit", self, shortcut="Ctrl+E", triggered=self.close)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.cellPressed.connect(self.songSelected)

    # 通过table选择歌曲
    def songSelected(self,row,column):
        self.mediaObject.stop()
        #something seems need here

        self.mediaObject.setCurrentSource(self.songs[row])
        self.mediaObject.play()

    def addFiles(self):
        files = QtGui.QFileDialog.getOpenFileNames(self, "Please select songs", "", self.tr("Song Files(*.mp3)"))

        index = len(self.songs)

        for file in files:
            self.songs.append(Phonon.MediaSource(file))

        print index
        if self.songs:
            self.mediaInformation.setCurrentSource(self.songs[index])
            self.mediaObject.setCurrentSource(self.songs[0])
    def playSong(self):
        pass
    def pauseSong(self):
        pass
    def stopSong(self):
        pass
    # 如果改变了歌曲，在table上将之高亮，重设时间显示
    def songChanged(self,source):
        self.tableWidget.selectRow(self.songs.index(source))
        self.lcdNumber.display('00:00')

    def stateChanged(self):
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
        else:
            return title[-2]

    # 在table上显示歌名
    def mediaStateChanged(self):
        # mediaData = self.mediaInformation.metaData()  # 找到media的元数据
        title = self.mediaInformation.currentSource().fileName()  # 文件名

        title = self.parseName(title)

        titleItem = QtGui.QTableWidgetItem(title)
        titleItem.setFlags(titleItem.flags() ^ QtCore.Qt.ItemIsEditable)

        currentRow = self.tableWidget.rowCount()
        self.tableWidget.insertRow(currentRow)
        self.tableWidget.setItem(currentRow, 0,titleItem)

        index = self.songs.index(self.mediaInformation.currentSource()) + 1
        if len(self.songs) > index:
            self.mediaInformation.setCurrentSource(self.songs[index])
        else:
            self.tableWidget.resizeColumnsToContents()

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

        self.tableWidget = QtGui.QTableWidget(self.centralWidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 291, 241))
        self.tableWidget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        header = ('Title',)
        self.tableWidget.setHorizontalHeaderLabels(header)

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

