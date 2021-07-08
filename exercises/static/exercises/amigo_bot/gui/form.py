# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '3d_reconstructrionui_smaller.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(936, 469)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tlLayout = QtWidgets.QVBoxLayout()
        self.tlLayout.setContentsMargins(0, -1, 1, -1)
        self.tlLayout.setObjectName("tlLayout")
        self.horizontalLayout_2.addLayout(self.tlLayout)
        self.mapLayout = QtWidgets.QVBoxLayout()
        self.mapLayout.setContentsMargins(1, -1, 0, -1)
        self.mapLayout.setObjectName("mapLayout")
        self.horizontalLayout_2.addLayout(self.mapLayout)
        self.logoLayout = QtWidgets.QVBoxLayout()
        self.logoLayout.setContentsMargins(1, -1, 0, -1)
        self.logoLayout.setObjectName("logoLayout")
        self.horizontalLayout_2.addLayout(self.logoLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.percentageCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.percentageCheck.setGeometry(QtCore.QRect(540, 220, 94, 26))
        self.percentageCheck.setObjectName("percentageCheck")
        self.verticalLayout_2.addWidget(self.percentageCheck)
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.stopButton.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopButton.setIcon(icon)
        self.stopButton.setObjectName("stopButton")
        self.verticalLayout_2.addWidget(self.stopButton)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 936, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.percentageCheck.setText(_translate("MainWindow", "Percentage Graphic"))
        self.stopButton.setText(_translate("MainWindow", "Stop Code"))
        self.pushButton.setText(_translate("MainWindow", "Run my algorithm"))
