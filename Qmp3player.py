# -*- coding: utf-8 -*-

#
#
# Created: Wed Nov 26 10:19:46 2014
#
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4 import phonon
from PyQt4.phonon import Phonon
from images import images_rc
import sys

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

class Ui_Qmp3player(object):
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
        self.play = QtGui.QPushButton(self.centralWidget)
        self.play.setGeometry(QtCore.QRect(20, 320, 51, 51))
        self.play.setStyleSheet(_fromUtf8("border-image: url(:/buttons/btn_play.png);"))
        self.play.setText(_fromUtf8(""))
        self.play.setObjectName(_fromUtf8("play"))
        self.pause = QtGui.QPushButton(self.centralWidget)
        self.pause.setGeometry(QtCore.QRect(80, 320, 51, 51))
        self.pause.setStyleSheet(_fromUtf8("border-image: url(:/buttons/btn_pause.png);"))
        self.pause.setText(_fromUtf8(""))
        self.pause.setObjectName(_fromUtf8("pause"))
        self.stop = QtGui.QPushButton(self.centralWidget)
        self.stop.setGeometry(QtCore.QRect(140, 320, 51, 51))
        self.stop.setStyleSheet(_fromUtf8("border-image: url(:/buttons/btn_stop.png);"))
        self.stop.setText(_fromUtf8(""))
        self.stop.setObjectName(_fromUtf8("stop"))
        self.tableWidget = QtGui.QTableWidget(self.centralWidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 291, 241))
        self.tableWidget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        Qmp3player.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(Qmp3player)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 342, 23))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        Qmp3player.setMenuBar(self.menuBar)
        self.actionOpen = QtGui.QAction(Qmp3player)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionExit = QtGui.QAction(Qmp3player)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionOpen_2 = QtGui.QAction(Qmp3player)
        self.actionOpen_2.setObjectName(_fromUtf8("actionOpen_2"))
        self.actionExit_2 = QtGui.QAction(Qmp3player)
        self.actionExit_2.setObjectName(_fromUtf8("actionExit_2"))
        self.menuFile.addAction(self.actionOpen_2)
        self.menuFile.addAction(self.actionExit_2)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(Qmp3player)
        QtCore.QMetaObject.connectSlotsByName(Qmp3player)

    def retranslateUi(self, Qmp3player):
        Qmp3player.setWindowTitle(_translate("Qmp3player", "Qmp3player", None))
        self.menuFile.setTitle(_translate("Qmp3player", "File", None))
        self.actionOpen.setText(_translate("Qmp3player", "Open", None))
        self.actionExit.setText(_translate("Qmp3player", "Exit", None))
        self.actionOpen_2.setText(_translate("Qmp3player", "Open", None))
        self.actionExit_2.setText(_translate("Qmp3player", "Exit", None))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Qmp3player = QtGui.QMainWindow()
    ui = Ui_Qmp3player()
    ui.setupUi(Qmp3player)
    Qmp3player.show()
    sys.exit(app.exec_())

