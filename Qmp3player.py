# -*- coding: utf-8 -*-
# Python 2.7
# PyQt4

'''
Music player.
Supports .mp3, .wav formats.
With an id3v1.0 tag reader.
'''

__author__ = "MarcoQin <qyyfy2009@gmail/163.com>"
__version__ = "1.1"


from PyQt4 import QtCore, QtGui
from PyQt4 import phonon
from PyQt4.phonon import Phonon
from images import images_rc
import sys
import os
import cPickle as pickle
from MediaInfo import MediaInfo

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



class Ui_Form(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_Form, self).__init__()
        self.mediaInfo = MediaInfo()
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
        self.mediaObject = Phonon.MediaObject(self)
        self.mediaInformation = Phonon.MediaObject(self)
        self.mediaObject.setTickInterval(100)
        self.mediaObject.tick.connect(self.updateTick)
        self.mediaObject.currentSourceChanged.connect(self.songChanged)
        self.mediaObject.stateChanged.connect(self.stateChanged)
        self.mediaObject.aboutToFinish.connect(self.Finishing)
        Phonon.createPath(self.mediaObject, self.audioOutput)

        self.setupUi(self)
        self.connectActions()
        self.volumeSlider.setAudioOutput(self.audioOutput)
        self.volumeSlider.setMaximumVolume(0.8)
        self.seekSlider.setMediaObject(self.mediaObject)

        self.songs = []
        self.songlist = []
        self.allsongsinfo = []
        self.loadSongList()
        self.refreshSongList()
        self.wasPlaying = False
        self.totalTime = '00:00'


    # 连接鼠标Action
    def connectActions(self):
        QtCore.QObject.connect(self.playButton, QtCore.SIGNAL('clicked()'), self.playSong)
        QtCore.QObject.connect(self.stopButton,  QtCore.SIGNAL('clicked()'), self.stopSong)
        QtCore.QObject.connect(self.addFilesButton, QtCore.SIGNAL('clicked()'), self.addFiles)
        QtCore.QObject.connect(self.delFilesButton, QtCore.SIGNAL('clicked()'), self.delFiles)
        QtCore.QObject.connect(self.nextButton, QtCore.SIGNAL('clicked()'), self.nextSong)
        QtCore.QObject.connect(self.previousButton, QtCore.SIGNAL('clicked()'), self.previousSong)
        # 连接DEL按钮
        QtCore.QObject.connect((QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self.listWidget)),QtCore.SIGNAL('activated()'), self.delFiles)

        self.listWidget.mouseDoubleClickEvent = self.doubleSelectSong


    def doubleSelectSong(self,a):
         index = self.listWidget.row(self.listWidget.selectedItems()[0])
         self.songSelected(index)

    # 通过list选择歌曲
    def songSelected(self,index):
        self.mediaObject.stop()
        self.mediaObject.clearQueue()
        self.mediaObject.setCurrentSource(self.songs[index])
        self.mediaObject.play()
        self.wasPlaying = True

        self.buttonChange(self.wasPlaying)
        self.updateMetaInfo()


    def loadSongList(self):
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

        self.getSongPath()
        self.mediaInfo.parseAllSongs(self.songlist)


    def getSongPath(self):
        self.songlist = []
        for song in self.songs:
            self.mediaInformation.setCurrentSource(song)
            path = self.mediaInformation.currentSource().fileName()

            self.songlist.append(path)
            self.mediaInformation.clearQueue()


    def saveSongList(self):
        self.getSongPath()
        file = open('playlist.lst', 'wb')
        pickle.dump(self.songlist, file)
        file.close()
        self.mediaInfo.parseAllSongs(self.songlist)


    def addFiles(self):
        files = QtGui.QFileDialog.getOpenFileNames(self, "Please select songs", "", self.tr("Song Files(*.mp3;*.wav)"))

        for file in files:
            self.songs.append(Phonon.MediaSource(file))

        self.saveSongList()
        self.refreshSongList()


    def delFilesFirst(self,index):
        for num in index:
            self.songs.remove(self.songs[num])

        self.buttonChange(self.wasPlaying)
        self.saveSongList()
        self.refreshSongList()
        self.totalTime = '00:00'


    def delFiles(self):
        selectedItems = self.listWidget.selectedItems()
        index = []
        selectedSongs = []

        for item in selectedItems:
            index.append(self.listWidget.row(item))

        index = sorted(index, reverse=True)

        for num in index:
            selectedSongs.append(self.songs[num])

        if selectedItems:
            if self.wasPlaying:
                if self.mediaObject.currentSource() in selectedSongs:
                    self.mediaObject.stop()
                    self.wasPlaying = False
                    self.delFilesFirst(index)
                    self.setLabelText(1,True)
                else:
                    self.delFilesFirst(index)
            else:
                self.delFilesFirst(index)
        else:
            warning = QtGui.QMessageBox(self)
            warning.setWindowTitle('Warning!')
            warning.setText('NO ITEM SELECTED!')
            warning.show()


    def buttonChange(self, playState):
        if playState:
            self.playButton.setStyleSheet(_fromUtf8("border-image: url(:/btn/btn_pause.png);"))
            QtCore.QObject.connect(self.playButton, QtCore.SIGNAL('clicked()'), self.pauseSong)
        else:
            self.playButton.setStyleSheet(_fromUtf8("border-image: url(:/btn/btn_play.png);"))
            QtCore.QObject.connect(self.playButton, QtCore.SIGNAL('clicked()'), self.playSong)


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
            self.buttonChange(self.wasPlaying)
            self.updateMetaInfo()


    def pauseSong(self):
        self.wasPlaying = False
        self.mediaObject.pause()
        self.buttonChange(self.wasPlaying)


    def stopSong(self):
        self.totalTime = '00:00'
        self.mediaObject.stop()
        self.wasPlaying = False
        self.buttonChange(self.wasPlaying)
        self.setLabelText(1,True)


    def nextSong(self):
        self.mediaObject.stop()
        self.mediaObject.clearQueue()
        if self.wasPlaying:
            if not self.listWidget.selectedItems():
                index = self.songs.index(self.mediaObject.currentSource()) + 1
                try:
                    self.mediaObject.setCurrentSource(self.songs[index])
                except:
                    self.mediaObject.setCurrentSource(self.songs[0])
            else:
                index = self.listWidget.row(self.listWidget.selectedItems()[0]) + 1
                try:
                    self.mediaObject.setCurrentSource(self.songs[index])
                except:
                    self.mediaObject.setCurrentSource(self.songs[0])
        else:
            if not self.listWidget.selectedItems():
                self.mediaObject.setCurrentSource(self.songs[0])
            else:
                index = self.listWidget.row(self.listWidget.selectedItems()[0]) + 1
                try:
                    self.mediaObject.setCurrentSource(self.songs[index])
                except:
                    self.mediaObject.setCurrentSource(self.songs[0])

        self.mediaObject.play()
        self.wasPlaying = True
        self.buttonChange(self.wasPlaying)
        self.updateMetaInfo()


    def previousSong(self):
        self.mediaObject.stop()
        self.mediaObject.clearQueue()
        if self.wasPlaying:
            if not self.listWidget.selectedItems():
                index = self.songs.index(self.mediaObject.currentSource()) - 1
                try:
                    self.mediaObject.setCurrentSource(self.songs[index])
                except:
                    self.mediaObject.setCurrentSource(self.songs[len(self.songs) - 1])
            else:
                index = self.listWidget.row(self.listWidget.selectedItems()[0]) - 1
                try:
                    self.mediaObject.setCurrentSource(self.songs[index])
                except:
                    self.mediaObject.setCurrentSource(self.songs[len(self.songs) - 1])
        else:
            if not self.listWidget.selectedItems():
                self.mediaObject.setCurrentSource(self.songs[len(self.songs) - 1])
            else:
                index = self.listWidget.row(self.listWidget.selectedItems()[0]) - 1
                try:
                    self.mediaObject.setCurrentSource(self.songs[index])
                except:
                    self.mediaObject.setCurrentSource(self.songs[len(self.songs) - 1])

        self.mediaObject.play()
        self.wasPlaying = True
        self.buttonChange(self.wasPlaying)
        self.updateMetaInfo()


    def songChanged(self,source):
        self.listWidget.setCurrentRow(self.songs.index(source))
        self.lcdNumber.display('00:00/00:00')


    def setLabelText(self,text,default = True):
        if default:
            self.label.setText(_translate("Form", "QMusicPlayer\nAuthor：MarcoQin <qyyfy2009@gmail.com>", None))
        else:
            self.label.setText(text)


    def getMetaData(self):
        self.mediaInformation.setCurrentSource(self.mediaObject.currentSource())
        title = self.mediaObject.currentSource().fileName()
        title = self.parseName(title)
        text = 'Title:' + title + '\n' + 'Artist:N/A' + '\n' + 'Album:M/A'
        self.setLabelText(text,False)


    def updateMetaInfo(self):
        index = self.songs.index(self.mediaObject.currentSource())
        string = self.mediaInfo.getFileInfo(index)
        if string:
            self.setLabelText(string, False)
        else:
            self.getMetaData()


    def stateChanged(self, newState,oldState):
        self.getTotalTime()

    # 播放将要结束时，将下一首歌曲排入播放队列
    def Finishing(self):
        index = self.songs.index(self.mediaObject.currentSource()) + 1
        if len(self.songs) > index:
            self.mediaObject.enqueue(self.songs[index])
        else:
            self.mediaObject.enqueue(self.songs[0])

    # 设置播放器时间
    def getTotalTime(self):
        totalTime = self.mediaObject.totalTime()
        totalTime = QtCore.QTime(0, (totalTime / 60000) % 60, (totalTime / 1000) % 60)
        totalTime =totalTime.toString('mm:ss')
        self.totalTime = totalTime


    def updateTick(self,time):
        songTime = QtCore.QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        songTime = songTime.toString('mm:ss')
        tick = songTime + '/' + self.totalTime
        self.lcdNumber.display(tick)

    # 提取文件名
    def parseName(self,source):
        title =  source.split('/')[-1]
        title =  title.split('.')
        return title[-2]


    def refreshSongList(self):
        self.listWidget.clear()
        for song in self.songs:
            index = self.songs.index(song)
            self.mediaInformation.setCurrentSource(self.songs[index])
            title = self.mediaInformation.currentSource().fileName()
            title = self.parseName(title)
            self.listWidget.addItem(title)


    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(337, 475)
        Form.setMinimumSize(QtCore.QSize(337, 475))
        Form.setMaximumSize(QtCore.QSize(337, 475))
        Form.setStyleSheet(_fromUtf8("#Form{background-image: url(:/bg/bg2.jpg)}"))  # 用“#name{语句}来限定form的背景，不会改变form上的别的widget的背景。
        self.gridLayoutWidget = QtGui.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 127, 301, 41))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lcdNumber = QtGui.QLCDNumber(self.gridLayoutWidget)
        self.lcdNumber.setFrameShadow(QtGui.QFrame.Plain)
        self.lcdNumber.setLineWidth(1)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setNumDigits(11)
        self.lcdNumber.setObjectName(_fromUtf8("lcdNumber"))
        self.gridLayout_3.addWidget(self.lcdNumber, 0, 5, 1, 1)
        self.stopButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.stopButton.setMinimumSize(QtCore.QSize(35, 35))
        self.stopButton.setMaximumSize(QtCore.QSize(35, 35))
        self.stopButton.setStyleSheet(_fromUtf8("border-image: url(:/btn/btn_stop.png);"))
        self.stopButton.setText(_fromUtf8(""))
        self.stopButton.setIconSize(QtCore.QSize(35, 35))
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.gridLayout_3.addWidget(self.stopButton, 0, 1, 1, 1)
        self.playButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.playButton.setMinimumSize(QtCore.QSize(35, 35))
        self.playButton.setMaximumSize(QtCore.QSize(35, 35))
        self.playButton.setBaseSize(QtCore.QSize(35, 35))
        self.playButton.setWhatsThis(_fromUtf8(""))
        self.playButton.setStyleSheet(_fromUtf8("border-image: url(:/btn/btn_play.png);"))
        self.playButton.setText(_fromUtf8(""))
        self.playButton.setObjectName(_fromUtf8("playButton"))
        self.gridLayout_3.addWidget(self.playButton, 0, 0, 1, 1)
        self.nextButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.nextButton.setMinimumSize(QtCore.QSize(35, 35))
        self.nextButton.setMaximumSize(QtCore.QSize(35, 35))
        self.nextButton.setStyleSheet(_fromUtf8("border-image: url(:/btn/btn_next.png);"))
        self.nextButton.setText(_fromUtf8(""))
        self.nextButton.setObjectName(_fromUtf8("nextButton"))
        self.gridLayout_3.addWidget(self.nextButton, 0, 3, 1, 1)
        self.previousButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.previousButton.setMinimumSize(QtCore.QSize(35, 35))
        self.previousButton.setMaximumSize(QtCore.QSize(35, 35))
        self.previousButton.setStyleSheet(_fromUtf8("border-image: url(:/btn/btn_previous.png);"))
        self.previousButton.setText(_fromUtf8(""))
        self.previousButton.setIconSize(QtCore.QSize(35, 35))
        self.previousButton.setObjectName(_fromUtf8("previousButton"))
        self.gridLayout_3.addWidget(self.previousButton, 0, 2, 1, 1)
        self.seekSlider = phonon.Phonon.SeekSlider(Form)
        self.seekSlider.setGeometry(QtCore.QRect(20, 181, 301, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.seekSlider.setFont(font)
        self.seekSlider.setMouseTracking(False)
        self.seekSlider.setAutoFillBackground(False)
        self.seekSlider.setIconVisible(False)
        self.seekSlider.setObjectName(_fromUtf8("seekSlider"))
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 419, 301, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.volumeSlider = phonon.Phonon.VolumeSlider(self.horizontalLayoutWidget)
        self.volumeSlider.setObjectName(_fromUtf8("volumeSlider"))
        self.horizontalLayout.addWidget(self.volumeSlider)
        self.addFilesButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.addFilesButton.setMinimumSize(QtCore.QSize(35, 35))
        self.addFilesButton.setMaximumSize(QtCore.QSize(35, 35))
        self.addFilesButton.setStyleSheet(_fromUtf8("border-image: url(:/btn/btn_add.png);"))
        self.addFilesButton.setText(_fromUtf8(""))
        self.addFilesButton.setObjectName(_fromUtf8("addFilesButton"))
        self.horizontalLayout.addWidget(self.addFilesButton)
        self.delFilesButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.delFilesButton.setMinimumSize(QtCore.QSize(35, 35))
        self.delFilesButton.setMaximumSize(QtCore.QSize(35, 35))
        self.delFilesButton.setStyleSheet(_fromUtf8("border-image: url(:/btn/btn_del.png);"))
        self.delFilesButton.setText(_fromUtf8(""))
        self.delFilesButton.setObjectName(_fromUtf8("delFilesButton"))
        self.horizontalLayout.addWidget(self.delFilesButton)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(20, 213, 301, 192))
        self.listWidget.setStyleSheet(_fromUtf8("background-color: rgb(189, 213, 231);\n"
"background-color: qlineargradient(spread:reflect, x1:0.358, y1:0.880682, x2:1, y2:0, stop:0.244318 rgba(125, 178, 236, 255), stop:1 rgba(255, 255, 255, 255));"))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)  # 设置多选模式，用于多文件删除
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 17, 301, 91))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet(_fromUtf8("border-image: url(:/bg/lable.png);\n"
"background-image: url(:/bg/bg.png);"))
        self.label.setFrameShadow(QtGui.QFrame.Plain)
        self.label.setLineWidth(1)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "QMusicPlayer", None))
        self.label.setText(_translate("Form", "QMusicPlayer\nAuthor：MarcoQin <qyyfy2009@gmail.com>", None))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    QUI = QtGui.QMainWindow()
    ui = Ui_Form()
    ui.show()
    sys.exit(app.exec_())
