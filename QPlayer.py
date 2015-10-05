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
#  from PyQt4 import phonon
#  from PyQt4.phonon import Phonon
from images import images_rc
import sys
import os
import time
import cPickle as pickle
from MediaInfo import MediaInfo
from core.file_manager import FileManager
from core.model import Song
from core.player import Player
from threading import Thread


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
        self.file_manager = FileManager()
        self.song_data = Song()
        self.player_core = Player(self.song_data)
        self.mediaInfo = MediaInfo()
        #  self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
        #  self.mediaObject = Phonon.MediaObject(self)
        #  self.mediaInformation = Phonon.MediaObject(self)
        #  self.mediaObject.setTickInterval(100)
        #  self.mediaObject.tick.connect(self.updateTick)
        #  self.mediaObject.currentSourceChanged.connect(self.songChanged)
        #  self.mediaObject.stateChanged.connect(self.stateChanged)
        #  self.mediaObject.aboutToFinish.connect(self.Finishing)
        #  Phonon.createPath(self.mediaObject, self.audioOutput)

        self.setupUi(self)
        self.connectActions()
        #  self.volumeSlider.setAudioOutput(self.audioOutput)
        #  self.volumeSlider.setMaximumVolume(0.8)
        #  self.seekSlider.setMediaObject(self.mediaObject)

        self.songs = []
        self.songlist = []
        self.allsongsinfo = []
        self.loadSongList()
        self.refreshSongList()
        self.wasPlaying = False
        self.totalTime = '00:00'
        self.total_int_time = 0
        self.update_tick_process_start = False

    def closeEvent(self, *args, **kwargs):
        # catch exit sinal and stop the subprocess
        if self.wasPlaying:
            self.wasPlaying = False
            self.stopSong()


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
        QtCore.QObject.connect(self, QtCore.SIGNAL("finished()"), self.stopSong)
        QtCore.QObject.connect(self, QtCore.SIGNAL("terminated()"), self.stopSong)
        QtCore.QObject.connect(self, QtCore.SIGNAL('quit'), self.stopSong)

        self.listWidget.mouseDoubleClickEvent = self.doubleSelectSong


    def doubleSelectSong(self,a):
        self.wasPlaying = False
        song_id = unicode(self.listWidget.selectedItems()[0].text()).split('#')[0].strip()
        self.songSelected(song_id)

    # 通过list选择歌曲
    def songSelected(self, song_id):
        self.player_core.double_select_song(self.song_data.get_song_by_id(song_id).path)
        self.getTotalTime()
        self.updateMetaInfo()
        self.buttonChange(self.wasPlaying)
        self.wasPlaying = True
        self.set_update_tick_sub_process()

    def set_list_widget_selected(self, song_id):
        for item in self.iter_all_list_items():
            if str(song_id) in unicode(item[1].text()):
                self.listWidget.setCurrentRow(item[0])
                break

    def iter_all_list_items(self):
        for i in range(self.listWidget.count()):
            yield i, self.listWidget.item(i)



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
            pass
            #print song
            #  self.songs.append(Phonon.MediaSource(song))

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
        files = QtGui.QFileDialog.getOpenFileNames(self, "Please select songs", "", self.tr("Song Files(*.*)"))

        new = []
        for file in files:
            print unicode(file)
            new.append(unicode(file).encode('utf-8'))
        self.file_manager.add_files(new)
            #  self.songs.append(Phonon.MediaSource(file))

        self.refreshSongList()

    def delFiles(self):
        selectedItems = self.listWidget.selectedItems()
        if selectedItems:
            ids = [int(unicode(s.text()).split('#')[0]) for s in selectedItems]
            if self.song_data.current_song_id in ids:
                self.stopSong()
            self.file_manager.del_files(ids)
            self.refreshSongList()
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

    def set_update_tick_sub_process(self):
        if not self.update_tick_process_start:
            Thread(target=self.updateTick).start()
            self.update_tick_process_start = True


    def playSong(self):
        self.wasPlaying = False
        self.player_core.play()
        if self.wasPlaying:
            self.buttonChange(self.wasPlaying)
        self.getTotalTime()
        self.updateMetaInfo()
        self.set_list_widget_selected(self.song_data.current_song_id)
        self.wasPlaying = True
        self.set_update_tick_sub_process()

    def pauseSong(self):
        self.wasPlaying = False
        self.player_core.pause()
        self.buttonChange(self.wasPlaying)


    def stopSong(self):
        self.wasPlaying = False
        self.player_core.stop()
        self.totalTime = '00:00'
        self.buttonChange(self.wasPlaying)
        self.setLabelText(1,True)


    def nextSong(self):
        self.wasPlaying = False
        self.player_core.next()
        self.buttonChange(self.wasPlaying)
        self.getTotalTime()
        self.updateMetaInfo()
        self.set_list_widget_selected(self.song_data.current_song_id)
        self.wasPlaying = True
        self.set_update_tick_sub_process()

    def previousSong(self):
        self.wasPlaying = False
        self.player_core.previous()
        self.buttonChange(self.wasPlaying)
        self.getTotalTime()
        self.updateMetaInfo()
        self.set_list_widget_selected(self.song_data.current_song_id)
        self.wasPlaying = True
        self.set_update_tick_sub_process()


    def songChanged(self,source):
        self.listWidget.setCurrentRow(self.songs.index(source))
        self.lcdNumber.display('00:00/00:00')


    def setLabelText(self,text,default = True):
        if default:
            self.label.setText(_translate("Form", "QMusicPlayer\nAuthor：MarcoQin <qyyfy2009@gmail.com>", None))
        else:
            self.label.setText(text)


    def updateMetaInfo(self):
        tp = ('album', 'artist', 'genre', 'title')
        if not self.file_info['title'] or self.file_info['title'] == "''":
            self.file_info['title'] = self.file_info['file_name'].split('.')[0]
        if not self.file_info['genre'] or self.file_info['genre'] == "''":
            self.file_info['genre'] = 'ACG'
        string = '\n'.join('{0}: {1}'.format(k, v).replace("'", '') for k, v in self.file_info.items() if k in tp)
        string = QtCore.QString.fromUtf8(string)
        self.setLabelText(string, False)


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
        self.file_info = self.player_core.file_info
        t = self.file_info['length']
        int_t = int(float(t))
        m, s = divmod(int(float(t)), 60)
        if m < 10:
            m = '0{0}'.format(m)
        if s < 10:
            s = '0{0}'.format(s)
        t = '{0}:{1}'.format(m, s)
        self.totalTime = t
        self.total_int_time = int_t


    def updateTick(self):
        while 1:
            try:
                if not self.wasPlaying:
                    self.lcdNumber.display('00:00/00:00')
                    self.seekSlider.setValue(0)
                    self.update_tick_process_start = False
                    break
                songTime = self.player_core.time_pos
                persent = (songTime*1.0/self.total_int_time)*100
                m, s = divmod(songTime, 60)
                if m < 10:
                    m = '0{0}'.format(m)
                if s < 10:
                    s = '0{0}'.format(s)
                songTime = '{0}:{1}'.format(m, s)
                tick = songTime + '/' + self.totalTime
                self.lcdNumber.display(tick)
                self.seekSlider.setValue(persent)
                time.sleep(1)
            except Exception:
                break

    # 提取文件名
    def parseName(self,source):
        title =  source.split('/')[-1]
        title =  title.split('.')
        return title[-2]


    def refreshSongList(self):
        self.listWidget.clear()
        song_data = self.song_data.get_all_songs()
        for song in song_data:
            self.listWidget.addItem(u'{0}# {1}'.format(song.id, song.name))


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
        self.seekSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.seekSlider.setGeometry(QtCore.QRect(20, 181, 301, 20))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.seekSlider.setFont(font)
        self.seekSlider.setMouseTracking(False)
        self.seekSlider.setAutoFillBackground(False)
        self.seekSlider.setObjectName(_fromUtf8("seekSlider"))
        self.seekSlider.setEnabled(False)
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 419, 301, 41))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        #  self.volumeSlider = phonon.Phonon.VolumeSlider(self.horizontalLayoutWidget)
        #  self.volumeSlider.setObjectName(_fromUtf8("volumeSlider"))
        #  self.horizontalLayout.addWidget(self.volumeSlider)
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
        self.label.setGeometry(QtCore.QRect(20, 10, 301, 110))
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
    def sign_action():
        ui.stopSong()

    sys.exit(app.exec_())
