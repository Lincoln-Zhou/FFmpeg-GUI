# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Desktop/About.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(400, 300)
        self.name = QtWidgets.QLabel(About)
        self.name.setGeometry(QtCore.QRect(130, 30, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.version = QtWidgets.QLabel(About)
        self.version.setGeometry(QtCore.QRect(140, 90, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.version.setFont(font)
        self.version.setObjectName("version")
        self.intro1 = QtWidgets.QLabel(About)
        self.intro1.setGeometry(QtCore.QRect(100, 150, 191, 51))
        self.intro1.setObjectName("intro1")
        self.intro2 = QtWidgets.QLabel(About)
        self.intro2.setGeometry(QtCore.QRect(120, 200, 151, 16))
        self.intro2.setObjectName("intro2")
        self.copyright = QtWidgets.QLabel(About)
        self.copyright.setGeometry(QtCore.QRect(99, 240, 191, 20))
        self.copyright.setObjectName("copyleft")

        self.retranslateUi(About)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "Dialog"))
        self.name.setText(_translate("About", "ffmpeg GUI"))
        self.version.setText(_translate("About", "Version 0.1 Alpha"))
        self.intro1.setText(_translate("About", "A simple video processing tool"))
        self.intro2.setText(_translate("About", "Based on FFmpeg project"))
        self.copyright.setText(_translate("About", "CopyLeft 2020 Lincoln Zhou"))
