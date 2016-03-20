# -*- coding: utf-8 -*-
# Python 2.7
# PyQt4

'''
Music player.
Supports .mp3, .wav, .Flac, .ape formats.
'''

__author__ = "MarcoQin <qyyfy2009@gmail/163.com>"
__version__ = "1.2"


from PyQt4 import QtCore, QtGui
from images import images_rc  # noqa init resource
import sys
import time
from core.file_manager import FileManager
from core.model import Song
from core.player import Player
from threading import Thread
import Queue


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
        self.queue = Queue.Queue(maxsize=10)
        self.player_core = Player(self.song_data, self.queue, self)

        self.setupUi(self)
        self.connectActions()

        self.refreshSongList()
        self.quit = False
        self.wasPlaying = False
        self.is_paused = False
        self.totalTime = '00:00'
        self.total_int_time = 0
        self.update_tick_process_start = False
        self.slider_in_pressed_value = 0  # seekslider first value
        Thread(target=self.about_to_stop).start()

    def closeEvent(self, *args, **kwargs):
        # catch exit sinal and stop the subprocess
        self.queue.put(None)
        if self.wasPlaying:
            self.wasPlaying = False
            self.stopSong()
        self.freePlayer()
        self.quit = True
        super(Ui_Form, self).closeEvent(*args, **kwargs)

    def keyPressEvent(self, event):
        key = event.key()
        print key
        #  if key == QtCore.Qt.Key_Left:
        #  print('Left Arrow Pressed')

    # 连接鼠标Action
    def connectActions(self):
        QtCore.QObject.connect(
            self.playButton,
            QtCore.SIGNAL('clicked()'),
            self.playSong)
        QtCore.QObject.connect(
            self.stopButton,
            QtCore.SIGNAL('clicked()'),
            self.stopSong)
        QtCore.QObject.connect(
            self.addFilesButton,
            QtCore.SIGNAL('clicked()'),
            self.addFiles)
        QtCore.QObject.connect(
            self.delFilesButton,
            QtCore.SIGNAL('clicked()'),
            self.delFiles)
        QtCore.QObject.connect(
            self.nextButton,
            QtCore.SIGNAL('clicked()'),
            self.nextSong)
        QtCore.QObject.connect(
            self.previousButton,
            QtCore.SIGNAL('clicked()'),
            self.previousSong)
        QtCore.QObject.connect(
            self.seekSlider,
            QtCore.SIGNAL('sliderPressed()'),
            self.slider_pressed)
        QtCore.QObject.connect(
            self.seekSlider,
            QtCore.SIGNAL('sliderReleased()'),
            self.slider_released)
        # 连接DEL按钮
        QtCore.QObject.connect(
            (QtGui.QShortcut(
                QtGui.QKeySequence( QtCore.Qt.Key_Delete), self.listWidget)), QtCore.SIGNAL('activated()'),
            self.delFiles)

        self.listWidget.mouseDoubleClickEvent = self.doubleSelectSong

    def doubleSelectSong(self, a):
        self.wasPlaying = False
        song_id = unicode(self.listWidget.selectedItems()[
                          0].text()).split('#')[0].strip()
        self.songSelected(song_id)

    # 通过list选择歌曲
    def songSelected(self, song_id):
        self.player_core.double_select_song(
            self.song_data.get_song_by_id(song_id).path)
        self.getTotalTime()
        self.updateMetaInfo()
        self.wasPlaying = True
        self.buttonChange(self.wasPlaying)
        self.set_update_tick_sub_process()

    def set_list_widget_selected(self, song_id):
        for item in self.iter_all_list_items():
            if str(song_id) in unicode(item[1].text()):
                self.listWidget.setCurrentRow(item[0])
                break

    def iter_all_list_items(self):
        for i in range(self.listWidget.count()):
            yield i, self.listWidget.item(i)

    def addFiles(self):
        files = QtGui.QFileDialog.getOpenFileNames(
            self, "Please select songs", "", self.tr("Song Files(*.*)"))
        new = []
        for file in files:
            print unicode(file)
            new.append(unicode(file).encode('utf-8'))
        self.file_manager.add_files(new)
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
            self.playButton.setStyleSheet(
                _fromUtf8("border-image: url(:/btn/btn_pause.png);"))
            self.playButton.clicked.disconnect()
            QtCore.QObject.connect(
                self.playButton,
                QtCore.SIGNAL('clicked()'),
                self.pauseSong)
        else:
            self.playButton.setStyleSheet(
                _fromUtf8("border-image: url(:/btn/btn_play.png);"))
            self.playButton.clicked.disconnect()
            QtCore.QObject.connect(
                self.playButton,
                QtCore.SIGNAL('clicked()'),
                self.playSong)

    def set_update_tick_sub_process(self):
        if not self.update_tick_process_start:
            Thread(target=self.updateTick).start()
            self.update_tick_process_start = True

    def playSong(self):
        if not self.wasPlaying and self.is_paused:
            self.is_paused = False
            self.player_core.pause()
            self.wasPlaying = True
            self.buttonChange(self.wasPlaying)
            return
        else:
            self.player_core.play()
            self.getTotalTime()
            self.updateMetaInfo()
            self.set_list_widget_selected(self.song_data.current_song_id)
            self.wasPlaying = True
            self.set_update_tick_sub_process()
            self.buttonChange(self.wasPlaying)

    def pauseSong(self):
        self.wasPlaying = False
        self.is_paused = True
        self.player_core.pause()
        self.buttonChange(self.wasPlaying)

    def stopSong(self):
        self.wasPlaying = False
        self.is_paused = False
        self.player_core.stop()
        self.totalTime = '00:00'
        self.buttonChange(self.wasPlaying)
        self.setLabelText(1, True)

    def freePlayer(self):
        self.player_core.free_player()

    def nextSong(self):
        self.is_paused = False
        self.wasPlaying = False
        self.player_core.next()
        self.getTotalTime()
        self.updateMetaInfo()
        self.set_list_widget_selected(self.song_data.current_song_id)
        self.wasPlaying = True
        self.buttonChange(self.wasPlaying)
        self.set_update_tick_sub_process()

    def previousSong(self):
        self.is_paused = False
        self.wasPlaying = False
        self.player_core.previous()
        self.getTotalTime()
        self.updateMetaInfo()
        self.set_list_widget_selected(self.song_data.current_song_id)
        self.wasPlaying = True
        self.buttonChange(self.wasPlaying)
        self.set_update_tick_sub_process()

    def slider_pressed(self):
        self.slider_in_pressed_value = self.seekSlider.value()

    def slider_released(self):
        seek_time = (self.seekSlider.value() -
                     self.slider_in_pressed_value) * self.total_int_time / 100
        if seek_time != 0:
            self.player_core.seek(seek_time)

    def setLabelText(self, text, default=True):
        if default:
            self.label.setText(
                _translate(
                    "Form",
                    "QPlayer\nAuthor：MarcoQin <qyyfy2009@gmail.com>",
                    None))
        else:
            self.label.setText(text)

    def updateMetaInfo(self):
        info = self.file_info
        tp = ('album', 'artist', 'genre', 'title')
        if not info['title']:
            info['title'] = info['name'].split('.')[0]
        if not info['genre']:
            info['genre'] = 'ACG'
        string = '\n'.join(
            '{0}: {1}'.format(
                k,
                v.encode('utf-8')) for k,
            v in info.items() if k in tp)
        string = QtCore.QString.fromUtf8(string)
        self.setLabelText(string, False)

    # 设置播放器时间
    def getTotalTime(self):
        print 'get_total time'
        self.file_info = self.player_core.file_info
        t = self.file_info['length']
        print t
        int_t = int(float(t))
        m, s = divmod(int(float(t)), 60)
        if m < 10:
            m = '0{0}'.format(m)
        if s < 10:
            s = '0{0}'.format(s)
        t = '{0}:{1}'.format(m, s)
        self.totalTime = t
        self.total_int_time = int_t

    def about_to_stop(self):
        while True:
            if self.quit:
                break
            cmd = self.queue.get()
            print "self.queue.get(): ", cmd
            if not cmd:
                break
            if cmd:
                self.wasPlaying = False
                self.is_paused = False
                event = self.nextButton.click()
                try:
                    QtGui.QApplication.sendEvent(event)
                except Exception:
                    pass

    def updateTick(self):
        while True:
            try:
                if self.quit:
                    self.update_tick_process_start = False
                    break
                if not self.wasPlaying and not self.is_paused:
                    time.sleep(1)
                    continue
                songTime = int(self.player_core.time_pos)
                self.total_int_time = self.player_core.total_length
                persent = (songTime * 1.0 / self.total_int_time) * 100
                m, s = divmod(songTime, 60)
                if m < 10:
                    m = '0{0}'.format(m)
                if s < 10:
                    s = '0{0}'.format(s)
                songTime = '{0}:{1}'.format(m, s)
                m, s = divmod(int(self.total_int_time), 60)
                if m < 10:
                    m = '0{0}'.format(m)
                if s < 10:
                    s = '0{0}'.format(s)
                t = '{0}:{1}'.format(m, s)
                self.totalTime = t
                tick = songTime + '/' + self.totalTime
                self.lcdNumber.display(tick)
                self.seekSlider.setValue(persent)
                time.sleep(1)
            except Exception as e:
                print e
                time.sleep(1)
                continue

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
        # 用“#name{语句}来限定form的背景，不会改变form上的别的widget的背景。
        Form.setStyleSheet(
            _fromUtf8("#Form{background-image: url(:/bg/bg2.jpg)}"))
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
        self.stopButton.setStyleSheet(
            _fromUtf8("border-image: url(:/btn/btn_stop.png);"))
        self.stopButton.setText(_fromUtf8(""))
        self.stopButton.setIconSize(QtCore.QSize(35, 35))
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.gridLayout_3.addWidget(self.stopButton, 0, 1, 1, 1)
        self.playButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.playButton.setMinimumSize(QtCore.QSize(35, 35))
        self.playButton.setMaximumSize(QtCore.QSize(35, 35))
        self.playButton.setBaseSize(QtCore.QSize(35, 35))
        self.playButton.setWhatsThis(_fromUtf8(""))
        self.playButton.setStyleSheet(
            _fromUtf8("border-image: url(:/btn/btn_play.png);"))
        self.playButton.setText(_fromUtf8(""))
        self.playButton.setObjectName(_fromUtf8("playButton"))
        self.gridLayout_3.addWidget(self.playButton, 0, 0, 1, 1)
        self.nextButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.nextButton.setMinimumSize(QtCore.QSize(35, 35))
        self.nextButton.setMaximumSize(QtCore.QSize(35, 35))
        self.nextButton.setStyleSheet(
            _fromUtf8("border-image: url(:/btn/btn_next.png);"))
        self.nextButton.setText(_fromUtf8(""))
        self.nextButton.setObjectName(_fromUtf8("nextButton"))
        self.gridLayout_3.addWidget(self.nextButton, 0, 3, 1, 1)
        self.previousButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.previousButton.setMinimumSize(QtCore.QSize(35, 35))
        self.previousButton.setMaximumSize(QtCore.QSize(35, 35))
        self.previousButton.setStyleSheet( _fromUtf8("border-image: url(:/btn/btn_previous.png);"))
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
        #  self.seekSlider.setEnabled(False)
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 419, 301, 41))
        self.horizontalLayoutWidget.setObjectName(
            _fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.addFilesButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.addFilesButton.setMinimumSize(QtCore.QSize(35, 35))
        self.addFilesButton.setMaximumSize(QtCore.QSize(35, 35))
        self.addFilesButton.setStyleSheet(
            _fromUtf8("border-image: url(:/btn/btn_add.png);"))
        self.addFilesButton.setText(_fromUtf8(""))
        self.addFilesButton.setObjectName(_fromUtf8("addFilesButton"))
        self.horizontalLayout.addWidget(self.addFilesButton)
        self.delFilesButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.delFilesButton.setMinimumSize(QtCore.QSize(35, 35))
        self.delFilesButton.setMaximumSize(QtCore.QSize(35, 35))
        self.delFilesButton.setStyleSheet(
            _fromUtf8("border-image: url(:/btn/btn_del.png);"))
        self.delFilesButton.setText(_fromUtf8(""))
        self.delFilesButton.setObjectName(_fromUtf8("delFilesButton"))
        self.horizontalLayout.addWidget(self.delFilesButton)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(20, 213, 301, 192))
        self.listWidget.setStyleSheet(
            _fromUtf8(
                "background-color: rgb(189, 213, 231);\n"
                "background-color: qlineargradient(spread:reflect, x1:0.358, y1:0.880682, x2:1, y2:0, stop:0.244318 rgba(125, 178, 236, 255), stop:1 rgba(255, 255, 255, 255));"))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.listWidget.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)  # 设置多选模式，用于多文件删除
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 10, 301, 110))
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet(
            _fromUtf8(
                "border-image: url(:/bg/lable.png);\n"
                "background-image: url(:/bg/bg.png);"))
        self.label.setFrameShadow(QtGui.QFrame.Plain)
        self.label.setLineWidth(1)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "QPlayer", None))
        self.label.setText(
            _translate(
                "Form",
                "QPlayer\nAuthor：MarcoQin <qyyfy2009@gmail.com>",
                None))

    def hide_ui(self):
        items = [
            'label',
            'listWidget',
            'delFilesButton',
            'addFilesButton',
            'neteasePlayListButton',
            'normalPlayListButton',
            'seekSlider',
            'previousButton',
            'nextButton',
            'playButton',
            'stopButton',
            'lcdNumber',
            'horizontalLayoutWidget']
        self.setMaximumSize(QtCore.QSize(1280, 720))
        self.setMinimumSize(QtCore.QSize(1280, 720))
        self.resize(640, 480)
        for item in items:
            getattr(self, item).hide()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    QUI = QtGui.QMainWindow()
    ui = Ui_Form()
    ui.show()
    sys.exit(app.exec_())
