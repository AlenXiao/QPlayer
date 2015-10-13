# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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


class Ui_MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1280, 720)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.centralwidget.setStyleSheet('background: black; border-width: 0px; border-style: solid')
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.centralwidget)
        print self.centralwidget.winId()
        parent = self.parentWidget()
        #  parent.listWidget.hide()
        #  parent.addFilesButton.hide()
        #  parent.lcdNumber.hide()
        #  parent.stopButton.hide()
        #  parent.nextButton.hide()
        #  parent.addFilesButton.hide()
        #  parent.delFilesButton.hide()
        #  parent.label.hide()
        #  parent.neteasePlayListButton.hide()
        #  parent.normalPlayListButton.hide()
        #  parent.seekSlider.hide()
        #  parent.playButton.hide()
        #  parent.previousButton.hide()
        parent.hide_ui()
        #  self.horizontalSlider = QtGui.QSlider(self.centralwidget)
        #  self.horizontalSlider.setGeometry(QtCore.QRect(30, 400, 581, 29))
        #  self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        #  self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        #  self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        #  self.graphicsView.setGeometry(QtCore.QRect(40, 40, 571, 321))
        #  self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        #  print self.graphicsView.winId()
        #  MainWindow.setCentralWidget(self.centralwidget)
        #  self.menubar = QtGui.QMenuBar(MainWindow)
        #  self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 28))
        #  self.menubar.setObjectName(_fromUtf8("menubar"))
        #  MainWindow.setMenuBar(self.menubar)
        #  self.statusbar = QtGui.QStatusBar(MainWindow)
        #  self.statusbar.setObjectName(_fromUtf8("statusbar"))
        #  MainWindow.setStatusBar(self.statusbar)

        #  self.retranslateUi(MainWindow)
        #  QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

