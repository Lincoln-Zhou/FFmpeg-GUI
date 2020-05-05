# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Desktop/license.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_License(object):
    def setupUi(self, License):
        License.setObjectName("License")
        License.resize(400, 300)
        self.label = QtWidgets.QLabel(License)
        self.label.setGeometry(QtCore.QRect(10, 10, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(License)
        self.textBrowser.setGeometry(QtCore.QRect(10, 50, 381, 221))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setOpenExternalLinks(True)

        self.retranslateUi(License)
        QtCore.QMetaObject.connectSlotsByName(License)

    def retranslateUi(self, License):
        _translate = QtCore.QCoreApplication.translate
        License.setWindowTitle(_translate("License", "License"))
        self.label.setText(_translate("License", "License Information"))
        self.textBrowser.setHtml(_translate("License", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">FFmpeg GUI is distributed under GNU GPLv3 license.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">FFmpeg is licensed under the GNU LGPL version 2.1 or later.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For more information, please refer to <a href=\"https://ffmpeg.org/legal.html\"><span style=\" text-decoration: underline; color:#0000ff;\">FFmpeg legal page.</span></a></p></body></html>"))
