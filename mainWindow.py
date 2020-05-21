# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Desktop/GUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from about import Ui_About
from license import Ui_License
from feedback import Ui_Feedbacks
from model import Model
import ffmpy
import sys
import os
import json
import subprocess


class Ui_ffmpegGUI(object):
    def __init__(self):
        # Initialize the super class
        super().__init__()
        self.model = Model()

    def openAbout(self):
        self.aboutWindow = QtWidgets.QMainWindow()
        self.ui = Ui_About()
        self.ui.setupUi(self.aboutWindow)
        self.aboutWindow.setWindowTitle('About')
        self.aboutWindow.show()

    def openFeedbacks(self):
        self.feedbackWindow = QtWidgets.QMainWindow()
        self.ui = Ui_Feedbacks()
        self.ui.setupUi(self.feedbackWindow)
        self.feedbackWindow.setWindowTitle('Feedbacks')
        self.feedbackWindow.show()
        
    def openLicense(self):
        self.licenseWindow = QtWidgets.QMainWindow()
        self.ui = Ui_License()
        self.ui.setupUi(self.licenseWindow)
        self.licenseWindow.setWindowTitle('License')
        self.licenseWindow.show()

    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                            options=options)
        if fileName:
            self.model.setFileName(fileName)
            self.refresh()
            self.showProperty()

    def refresh(self):
        self.fileNameShow.setText(self.model.getFileName())

    def showProperty(self):
        # Show input video property in text browser
        self.fileProperty.clear()
        # Refresh fileProperty widget each time openFile() is called
        meta = ffmpy.FFprobe(executable='ffprobe', inputs={
            self.model.getFileName(): ' -v error -print_format json -show_format -show_streams'}).run(
            stdout=subprocess.PIPE)
        output = json.loads(meta[0].decode('utf-8'))
        data = ['Media Name: ' + output['format']['filename'], 'Media Duration: ' + output['format']['duration'] + ' s',
                'Media Size: ' + str(eval(output['format']['size'] + '/1048576')) + ' MB']
        try:
            data.append('Media Encoder: ' + output['format']['tags']['encoder'])
        except:
            data.append('Media Encoder: undefined')
        # In some situations ffprobe cannot get Media encoder in 'tags', use 'except' to avoid return error

        try:
            data.append('Video Codec Name: ' + output['streams'][0]['codec_name'])
        except:
            try:
                data.append('Video Codec Name: ' + output['streams'][1]['codec_name'])
            except:
                data.append('Video Codec Name: undefined')

        try:
            data.append('Video Codec Long Name: ' + output['streams'][0]['codec_long_name'])
        except:
            try:
                data.append('Video Codec Long Name: ' + output['streams'][1]['codec_long_name'])
            except:
                data.append('Video Codec Long Name: undefined')

        try:
            data.append('Resolution: ' + str(output['streams'][0]['width']) + 'x' + str(output['streams'][0]['height']))
        except:
            try:
                data.append(
                    'Resolution: ' + str(output['streams'][1]['width']) + 'x' + str(output['streams'][1]['height']))
            except:
                data.append('Resolution: undefined')

        try:
            data.append('FPS: ' + str(eval(output['streams'][0]['avg_frame_rate'])))
        except:
            try:
                data.append('FPS: ' + str(eval(output['streams'][1]['avg_frame_rate'])))
            except:
                data.append('FPS: undefined')

        try:
            data.append('Audio Codec Name: ' + output['streams'][1]['codec_name'])
        except:
            try:
                data.append('Audio Codec Name: ' + output['streams'][0]['codec_name'])
            except:
                data.append('Audio Codec Name: undefined')

        try:
            data.append('Audio Codec Long Name: ' + output['streams'][1]['codec_long_name'])
        except:
            try:
                data.append('Audio Codec Long Name: ' + output['streams'][0]['codec_long_name'])
            except:
                data.append('Audio Codec Long Name: undefined')

        try:
            data.append('Bit Rate: ' + str(eval(output['streams'][1]['bit_rate'] + '/1000')) + ' kb')
        except:
            try:
                data.append('Bit Rate: ' + str(eval(output['streams'][0]['bit_rate'] + '/1000')) + ' kb')
            except:
                data.append('Bit Rate: undefined')
        # Extract other important properties

        for element in data:
            self.fileProperty.append(element)

    def mainprocess(self):
        videoQuality = 1
        audioQuality = 1
        # The default quality is Original
        if self.vqO.isChecked():
            videoQuality = 1
        elif self.vqH.isChecked():
            videoQuality = 'veryslow'
        elif self.vqM.isChecked():
            videoQuality = 'medium'
        elif self.vqL.isChecked():
            videoQuality = 'veryfast'
        elif self.vqD.isChecked():
            videoQuality = 0
        # Video quality control uses -preset parameter

        if self.aqO.isChecked():
            audioQuality = 1
        elif self.aqH.isChecked():
            audioQuality = '5'
        elif self.aqM.isChecked():
            audioQuality = '3'
        elif self.aqL.isChecked():
            audioQuality = '1'
        elif self.aqD.isChecked():
            audioQuality = 0
        # Audio quality control uses VBR mode

        videoEncoding = 1
        audioEncoding = 1
        # Audio encoding is currently not supported but source code is kept for further updates
        if self.vEncoding.currentIndex() == 0:
            videoEncoding = 1
        elif self.vEncoding.currentIndex() == 1:
            videoEncoding = 'libx264'
        elif self.vEncoding.currentIndex() == 2:
            videoEncoding = 'libx265'

        vqCmd = ' -c:v'
        aqCmd = ' -c:a'
        if videoQuality == 1:
            vqCmd += ' copy'
        else:
            if videoQuality == 0:
                vqCmd = ' -vn'
            else:
                vqCmd += f' {videoEncoding} -preset {videoQuality}'

        if audioQuality == 1:
            aqCmd += ' copy'
        else:
            if audioQuality == 0:
                aqCmd = ' -an'
            else:
                aqCmd += f' libfdk_aac -vbr {audioQuality}'
        # Please notice currently any adjust to audio quality (that is, not using original) will force audio encoding using libfdk_aac
        # Generate ffmpeg codec and quality parameter string

        fpsCmd = ''
        if self.FPS.isEnabled():
            fpsCmd = f' -framerate {self.FPS.value()}'
        # Generate ffmpeg FPS parameter string

        trimCmd = ''
        if self.isTrim.isChecked():
            startTime = 3600 * self.sH.value() + 60 * self.sM.value() + self.sS.value()
            endTime = 3600 * self.eH.value() + 60 * self.eM.value() + self.eS.value()
            if startTime >= endTime:
                errorMsg = QtWidgets.QMessageBox()
                errorMsg.setText('Parameter Error.')
                errorMsg.setWindowTitle('Error')
                errorMsg.setDetailedText('Contradicted parameter, please check input.')
                errorMsg.exec()
                return
            else:
                trimCmd = ' -ss ' + str(startTime) + ' -to ' + str(endTime)
        # For convenience, time is formatted as seconds, decimal: 3
        # Generate ffmpeg trim parameter string

        fileName, fileExt = os.path.splitext(self.model.getFileName())
        # Get fileName and fileExt to generate output parameters
        outputName = fileName + '-processed'
        outputExt = fileExt
        if self.formatChoose.currentIndex() != 0:
            outputExt = self.formatChoose.currentText()

        command = vqCmd + aqCmd + fpsCmd + trimCmd
        outputFullName = outputName + outputExt
        # Generate final parameters command

        process = ffmpy.FFmpeg(inputs={self.model.getFileName(): None},
                               outputs={outputFullName: command})
        try:
            process.run()
            self.progressBar.setValue(100)
            # In this alpha version progress bar isn't in function, only present in GUI, further updates needed
            succeedMsg = QtWidgets.QMessageBox()
            succeedMsg.setText('Processing Complete.')
            succeedMsg.setWindowTitle('Success')
            succeedMsg.setDetailedText(f'Successfully executed FFmpeg command ffmpeg -i {self.model.getFileName()}{command} {outputFullName}')
            succeedMsg.exec()
        except:
            failMsg = QtWidgets.QMessageBox()
            failMsg.setText('Fatal Error')
            failMsg.setInformativeText('An error happened and command cannot be executed. For more information, go to Show Details.')
            failMsg.setDetailedText(f'{sys.exc_info()[0]}')
            failMsg.exec()

    def setupUi(self, ffmpegGUI):
        ffmpegGUI.setObjectName("ffmpegGUI")
        ffmpegGUI.setEnabled(True)
        ffmpegGUI.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ffmpegGUI)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(680, 510, 113, 32))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(self.mainprocess)
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 20, 781, 33))
        self.layoutWidget.setObjectName("layoutWidget")
        self.fileInputWidget = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.fileInputWidget.setContentsMargins(0, 0, 0, 0)
        self.fileInputWidget.setObjectName("fileInputWidget")
        self.fileNameTitle = QtWidgets.QLabel(self.layoutWidget)
        self.fileNameTitle.setObjectName("fileNameTitle")
        self.fileInputWidget.addWidget(self.fileNameTitle)
        self.fileNameShow = QtWidgets.QLineEdit(self.layoutWidget)
        self.fileNameShow.setObjectName("fileNameShow")
        self.fileNameShow.setEnabled(False)
        self.fileInputWidget.addWidget(self.fileNameShow)
        self.chooseFile = QtWidgets.QPushButton(self.layoutWidget)
        self.chooseFile.setObjectName("chooseFile")
        self.chooseFile.clicked.connect(self.openFile)
        self.fileInputWidget.addWidget(self.chooseFile)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(257, 71, 170, 205))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.aPreference = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.aPreference.setContentsMargins(0, 0, 0, 0)
        self.aPreference.setObjectName("aPreference")
        self.apTitle = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.apTitle.setFont(font)
        self.apTitle.setObjectName("apTitle")
        self.aPreference.addWidget(self.apTitle)
        self.aQuality = QtWidgets.QVBoxLayout()
        self.aQuality.setObjectName("aQuality")
        self.aqTitle = QtWidgets.QLabel(self.layoutWidget1)
        self.aqTitle.setObjectName("aqTitle")
        self.aQuality.addWidget(self.aqTitle)
        self.aqO = QtWidgets.QRadioButton(self.layoutWidget1)
        self.aqO.setChecked(True)
        self.aqO.setObjectName("aqO")
        self.aQuality.addWidget(self.aqO)
        self.aqH = QtWidgets.QRadioButton(self.layoutWidget1)
        self.aqH.setObjectName("aqH")
        self.aQuality.addWidget(self.aqH)
        self.aqM = QtWidgets.QRadioButton(self.layoutWidget1)
        self.aqM.setObjectName("aqM")
        self.aQuality.addWidget(self.aqM)
        self.aqL = QtWidgets.QRadioButton(self.layoutWidget1)
        self.aqL.setObjectName("aqL")
        self.aQuality.addWidget(self.aqL)
        self.aqD = QtWidgets.QRadioButton(self.layoutWidget1)
        self.aqD.setObjectName("aqD")
        self.aQuality.addWidget(self.aqD)
        self.aPreference.addLayout(self.aQuality)
        self.aePreference = QtWidgets.QVBoxLayout()
        self.aePreference.setObjectName("aePreference")
        self.aeTitle = QtWidgets.QLabel(self.layoutWidget1)
        self.aeTitle.setObjectName("aeTitle")
        self.aePreference.addWidget(self.aeTitle)
        self.aEncoding = QtWidgets.QComboBox(self.layoutWidget1)
        self.aEncoding.setObjectName("aEncoding")
        self.aEncoding.addItem("")
        self.aePreference.addWidget(self.aEncoding)
        self.aPreference.addLayout(self.aePreference)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(11, 71, 170, 266))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.vPreference = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.vPreference.setContentsMargins(0, 0, 0, 0)
        self.vPreference.setObjectName("vPreference")
        self.vpTitle = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.vpTitle.setFont(font)
        self.vpTitle.setObjectName("vpTitle")
        self.vPreference.addWidget(self.vpTitle)
        self.vQuality = QtWidgets.QVBoxLayout()
        self.vQuality.setObjectName("vQuality")
        self.vqTitle = QtWidgets.QLabel(self.layoutWidget2)
        self.vqTitle.setObjectName("vqTitle")
        self.vQuality.addWidget(self.vqTitle)
        self.vqO = QtWidgets.QRadioButton(self.layoutWidget2)
        self.vqO.setChecked(True)
        self.vqO.setObjectName("vqO")
        self.vQuality.addWidget(self.vqO)
        self.vqH = QtWidgets.QRadioButton(self.layoutWidget2)
        self.vqH.setObjectName("vqH")
        self.vQuality.addWidget(self.vqH)
        self.vqM = QtWidgets.QRadioButton(self.layoutWidget2)
        self.vqM.setObjectName("vqM")
        self.vQuality.addWidget(self.vqM)
        self.vqL = QtWidgets.QRadioButton(self.layoutWidget2)
        self.vqL.setObjectName("vqL")
        self.vQuality.addWidget(self.vqL)
        self.vqD = QtWidgets.QRadioButton(self.layoutWidget2)
        self.vqD.setObjectName("vqD")
        self.vQuality.addWidget(self.vqD)
        self.vPreference.addLayout(self.vQuality)
        self.vePreference = QtWidgets.QVBoxLayout()
        self.vePreference.setObjectName("vePreference")
        self.veTitle = QtWidgets.QLabel(self.layoutWidget2)
        self.veTitle.setObjectName("veTitle")
        self.vePreference.addWidget(self.veTitle)
        self.vEncoding = QtWidgets.QComboBox(self.layoutWidget2)
        self.vEncoding.setEditable(False)
        self.vEncoding.setObjectName("vEncoding")
        self.vEncoding.addItem("")
        self.vEncoding.addItem("")
        self.vEncoding.addItem("")
        self.vEncoding.addItem("")
        self.vEncoding.addItem("")
        self.vEncoding.addItem("")
        self.vePreference.addWidget(self.vEncoding)
        self.vPreference.addLayout(self.vePreference)
        self.vFPS = QtWidgets.QVBoxLayout()
        self.vFPS.setObjectName("vFPS")
        self.isSetFPS = QtWidgets.QCheckBox(self.layoutWidget2)
        self.isSetFPS.setObjectName("isSetFPS")
        self.vFPS.addWidget(self.isSetFPS)
        self.FPS = QtWidgets.QDoubleSpinBox(self.layoutWidget2)
        self.FPS.setEnabled(False)
        self.FPS.setWrapping(False)
        self.FPS.setFrame(True)
        self.FPS.setMaximum(199.99)
        self.FPS.setObjectName("FPS")
        self.vFPS.addWidget(self.FPS)
        self.vPreference.addLayout(self.vFPS)
        self.layoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(10, 360, 123, 49))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.formatSetWidget = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.formatSetWidget.setContentsMargins(0, 0, 0, 0)
        self.formatSetWidget.setObjectName("formatSetWidget")
        self.formatTitle = QtWidgets.QLabel(self.layoutWidget3)
        self.formatTitle.setObjectName("formatTitle")
        self.formatSetWidget.addWidget(self.formatTitle)
        self.formatChoose = QtWidgets.QComboBox(self.layoutWidget3)
        self.formatChoose.setObjectName("formatChoose")
        self.formatChoose.addItem("")
        self.formatChoose.addItem("")
        self.formatChoose.addItem("")
        self.formatChoose.addItem("")
        self.formatChoose.addItem("")
        self.formatChoose.addItem("")
        self.formatChoose.addItem("")
        self.formatChoose.addItem("")
        self.formatChoose.addItem("")
        self.formatChoose.addItem("")
        self.formatSetWidget.addWidget(self.formatChoose)
        self.layoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(260, 320, 231, 89))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.trimWidget = QtWidgets.QGridLayout(self.layoutWidget4)
        self.trimWidget.setContentsMargins(0, 0, 0, 0)
        self.trimWidget.setObjectName("trimWidget")
        self.startTime = QtWidgets.QHBoxLayout()
        self.startTime.setObjectName("startTime")
        self.sH = QtWidgets.QSpinBox(self.layoutWidget4)
        self.sH.setEnabled(False)
        self.sH.setMaximum(99)
        self.sH.setObjectName("sH")
        self.startTime.addWidget(self.sH)
        self.sM = QtWidgets.QSpinBox(self.layoutWidget4)
        self.sM.setEnabled(False)
        self.sM.setMaximum(59)
        self.sM.setObjectName("sM")
        self.startTime.addWidget(self.sM)
        self.sS = QtWidgets.QDoubleSpinBox(self.layoutWidget4)
        self.sS.setEnabled(False)
        self.sS.setDecimals(3)
        self.sS.setMaximum(59.999)
        self.sS.setObjectName("sS")
        self.startTime.addWidget(self.sS)
        self.trimWidget.addLayout(self.startTime, 1, 1, 1, 1)
        self.startTitle = QtWidgets.QLabel(self.layoutWidget4)
        self.startTitle.setObjectName("startTitle")
        self.trimWidget.addWidget(self.startTitle, 1, 0, 1, 1)
        self.endTitle = QtWidgets.QLabel(self.layoutWidget4)
        self.endTitle.setObjectName("endTitle")
        self.trimWidget.addWidget(self.endTitle, 2, 0, 1, 1)
        self.endTime = QtWidgets.QHBoxLayout()
        self.endTime.setObjectName("endTime")
        self.eH = QtWidgets.QSpinBox(self.layoutWidget4)
        self.eH.setEnabled(False)
        self.eH.setObjectName("eH")
        self.endTime.addWidget(self.eH)
        self.eM = QtWidgets.QSpinBox(self.layoutWidget4)
        self.eM.setEnabled(False)
        self.eM.setMaximum(59)
        self.eM.setObjectName("eM")
        self.endTime.addWidget(self.eM)
        self.eS = QtWidgets.QDoubleSpinBox(self.layoutWidget4)
        self.eS.setEnabled(False)
        self.eS.setDecimals(3)
        self.eS.setMaximum(59.999)
        self.eS.setObjectName("eS")
        self.endTime.addWidget(self.eS)
        self.trimWidget.addLayout(self.endTime, 2, 1, 1, 1)
        self.isTrim = QtWidgets.QCheckBox(self.layoutWidget4)
        self.isTrim.setObjectName("isTrim")
        self.trimWidget.addWidget(self.isTrim, 0, 0, 1, 2)
        self.layoutWidget5 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget5.setGeometry(QtCore.QRect(10, 470, 781, 21))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.progressWidget = QtWidgets.QHBoxLayout(self.layoutWidget5)
        self.progressWidget.setContentsMargins(0, 0, 0, 0)
        self.progressWidget.setObjectName("progressWidget")
        self.progressTitle = QtWidgets.QLabel(self.layoutWidget5)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.progressTitle.setFont(font)
        self.progressTitle.setObjectName("progressTitle")
        self.progressWidget.addWidget(self.progressTitle)
        self.progressBar = QtWidgets.QProgressBar(self.layoutWidget5)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressWidget.addWidget(self.progressBar)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(500, 70, 291, 341))
        self.widget.setObjectName("widget")
        self.filePropertyWidget = QtWidgets.QGridLayout(self.widget)
        self.filePropertyWidget.setContentsMargins(0, 0, 0, 0)
        self.filePropertyWidget.setObjectName("filePropertyWidget")
        self.filePropertyTitle = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.filePropertyTitle.setFont(font)
        self.filePropertyTitle.setObjectName("filePropertyTitle")
        self.filePropertyWidget.addWidget(self.filePropertyTitle, 0, 0, 1, 1)
        self.fileProperty = QtWidgets.QTextBrowser(self.widget)
        self.fileProperty.setObjectName("fileProperty")
        self.filePropertyWidget.addWidget(self.fileProperty, 1, 0, 1, 1)
        ffmpegGUI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ffmpegGUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        ffmpegGUI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ffmpegGUI)
        self.statusbar.setObjectName("statusbar")
        ffmpegGUI.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(ffmpegGUI)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.triggered['bool'].connect(self.openAbout)
        self.actionFeedbacks = QtWidgets.QAction(ffmpegGUI)
        self.actionFeedbacks.setObjectName("actionFeedbacks")
        self.actionFeedbacks.triggered['bool'].connect(self.openFeedbacks)
        self.actionLicense = QtWidgets.QAction(ffmpegGUI)
        self.actionLicense.setObjectName("actionLicense")
        self.actionLicense.triggered['bool'].connect(self.openLicense)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionFeedbacks)
        self.menuAbout.addAction(self.actionLicense)
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(ffmpegGUI)
        self.isSetFPS.toggled['bool'].connect(self.FPS.setEnabled)
        self.isTrim.toggled['bool'].connect(self.sH.setEnabled)
        self.isTrim.toggled['bool'].connect(self.sM.setEnabled)
        self.isTrim.toggled['bool'].connect(self.sS.setEnabled)
        self.isTrim.toggled['bool'].connect(self.eH.setEnabled)
        self.isTrim.toggled['bool'].connect(self.eM.setEnabled)
        self.isTrim.toggled['bool'].connect(self.eS.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ffmpegGUI)

    def retranslateUi(self, ffmpegGUI):
        _translate = QtCore.QCoreApplication.translate
        ffmpegGUI.setWindowTitle(_translate("ffmpegGUI", "MainWindow"))
        self.startButton.setText(_translate("ffmpegGUI", "Start"))
        self.fileNameTitle.setText(_translate("ffmpegGUI", "File Name"))
        self.chooseFile.setText(_translate("ffmpegGUI", "Choose File"))
        self.apTitle.setText(_translate("ffmpegGUI", "Audio Output Preferences"))
        self.aqTitle.setText(_translate("ffmpegGUI", "Quality"))
        self.aqO.setText(_translate("ffmpegGUI", "Original"))
        self.aqH.setText(_translate("ffmpegGUI", "High"))
        self.aqM.setText(_translate("ffmpegGUI", "Medium"))
        self.aqL.setText(_translate("ffmpegGUI", "Low"))
        self.aqD.setText(_translate("ffmpegGUI", "Detach Audio"))
        self.aeTitle.setText(_translate("ffmpegGUI", "Encoding"))
        self.aEncoding.setItemText(0, _translate("ffmpegGUI", "Original"))
        self.vpTitle.setText(_translate("ffmpegGUI", "Video Output Preferences"))
        self.vqTitle.setText(_translate("ffmpegGUI", "Quality"))
        self.vqO.setText(_translate("ffmpegGUI", "Original"))
        self.vqH.setText(_translate("ffmpegGUI", "High"))
        self.vqM.setText(_translate("ffmpegGUI", "Medium"))
        self.vqL.setText(_translate("ffmpegGUI", "Low"))
        self.vqD.setText(_translate("ffmpegGUI", "Detach Video"))
        self.veTitle.setText(_translate("ffmpegGUI", "Encoding"))
        self.vEncoding.setItemText(0, _translate("ffmpegGUI", "Original"))
        self.vEncoding.setItemText(1, _translate("ffmpegGUI", "H.264"))
        self.vEncoding.setItemText(2, _translate("ffmpegGUI", "H.265/HEVC"))
        self.isSetFPS.setText(_translate("ffmpegGUI", "Custom FPS"))
        self.formatTitle.setText(_translate("ffmpegGUI", "File Output Format:"))
        self.formatChoose.setItemText(0, _translate("ffmpegGUI", "Original"))
        self.formatChoose.setItemText(1, _translate("ffmpegGUI", ".ape"))
        self.formatChoose.setItemText(2, _translate("ffmpegGUI", ".avi"))
        self.formatChoose.setItemText(3, _translate("ffmpegGUI", ".flac"))
        self.formatChoose.setItemText(4, _translate("ffmpegGUI", ".mov"))
        self.formatChoose.setItemText(5, _translate("ffmpegGUI", ".mp3"))
        self.formatChoose.setItemText(6, _translate("ffmpegGUI", ".mp4"))
        self.formatChoose.setItemText(7, _translate("ffmpegGUI", ".rmvb"))
        self.formatChoose.setItemText(8, _translate("ffmpegGUI", ".wav"))
        self.formatChoose.setItemText(9, _translate("ffmpegGUI", ".wmv"))
        self.startTitle.setText(_translate("ffmpegGUI", "From"))
        self.endTitle.setText(_translate("ffmpegGUI", "To"))
        self.isTrim.setText(_translate("ffmpegGUI", "Trim"))
        self.progressTitle.setText(_translate("ffmpegGUI", "Processing Progress"))
        self.filePropertyTitle.setText(_translate("ffmpegGUI", "File Property"))
        self.fileProperty.setHtml(_translate("ffmpegGUI",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'.AppleSystemUIFont\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
                                             "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.menuAbout.setTitle(_translate("ffmpegGUI", "ffmpeg GUI"))
        self.actionAbout.setText(_translate("ffmpegGUI", "About"))
        self.actionFeedbacks.setText(_translate("ffmpegGUI", "Feedbacks"))
        self.actionLicense.setText(_translate("ffmpegGUI", "License"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ffmpegGUI = QtWidgets.QMainWindow()
    ui = Ui_ffmpegGUI()
    ui.setupUi(ffmpegGUI)
    ffmpegGUI.setWindowTitle('FFmpeg GUI')
    ffmpegGUI.show()
    sys.exit(app.exec_())
