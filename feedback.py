# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Desktop/feedback.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Feedbacks(object):
    def setupUi(self, Feedbacks):
        Feedbacks.setObjectName("Feedbacks")
        Feedbacks.resize(400, 300)
        self.label = QtWidgets.QLabel(Feedbacks)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Feedbacks)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 381, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Feedbacks)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 361, 21))
        self.label_3.setObjectName("label_3")
        self.label_3.setOpenExternalLinks(True)
        self.label_4 = QtWidgets.QLabel(Feedbacks)
        self.label_4.setGeometry(QtCore.QRect(10, 130, 211, 16))
        self.label_4.setObjectName("label_4")
        self.label_4.setOpenExternalLinks(True)

        self.retranslateUi(Feedbacks)
        QtCore.QMetaObject.connectSlotsByName(Feedbacks)

    def retranslateUi(self, Feedbacks):
        _translate = QtCore.QCoreApplication.translate
        Feedbacks.setWindowTitle(_translate("Feedbacks", "Dialog"))
        self.label.setText(_translate("Feedbacks", "Feedback"))
        self.label_2.setText(_translate("Feedbacks", "Feedback is welcomed through GitHub issues or E-mail"))
        self.label_3.setText(_translate("Feedbacks", "<a href=\"https://github.com/Lang-Zhou/FFmpeg-GUI\">GitHub Project: FFmpeg GUI</a>"))
        self.label_4.setText(_translate("Feedbacks", "E-mail: LincolnZh@protonmail.com"))
