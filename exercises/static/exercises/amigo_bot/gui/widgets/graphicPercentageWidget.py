import sys, math
from math import pi as pi
import numpy as np
import cv2
from PyQt5.QtCore import QPoint, QRect, QSize, Qt, QPointF, QRectF, pyqtSignal, QTimer
from PyQt5.QtGui import (QBrush, QConicalGradient, QLinearGradient, QPainter, QPainterPath, QPalette, QPen, QPixmap, QPolygon, QRadialGradient, QColor, QTransform, QPolygonF, QKeySequence, QIcon)
from PyQt5.QtWidgets import (QApplication, QProgressBar, QCheckBox, QComboBox, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QSpinBox, QWidget, QPushButton, QSpacerItem, QSizePolicy, QLCDNumber)
from PyQt5 import QtGui, QtCore
from parallelIce.pose3dClient import Pose3DClient
import easyiceconfig as EasyIce
from gui.threadGUI import ThreadGUI
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class PercentageWidget(QWidget):
    def __init__(self,winParent, pose3d):
        super(PercentageWidget, self).__init__()
        self.winParent=winParent
        self.map = cv2.imread("resources/images/robocup.png", cv2.IMREAD_GRAYSCALE)
        self.map = cv2.resize(self.map, (500, 500))
        self.pose3d = pose3d
        self.percentageHouse = 0
        self.numPixels = self.calculatePixelsWhite()
        self.numPixelsWalked = 0
        self.numPixelInit = 656

        layout = QGridLayout()

        self.seconds = 0
        self.MAXseconds = 900
        self.contSeconds = 0
        self.secondsArray = [0]

        self.devPercentages = [0]
        self.percentagePrev = 0
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout.addWidget(self.canvas)

        vSpacer = QSpacerItem(30, 50, QSizePolicy.Ignored, QSizePolicy.Ignored)
        layout.addItem(vSpacer,1,0)

        self.setFixedSize(1200,500);

        self.setLayout(layout)

        timer = QTimer(self)
        timer.start(1000)
        timer.timeout.connect(self.accountantTime)


    def accountantTime(self):
        if self.seconds < self.MAXseconds:
            self.updateG()
            self.seconds += 1
            if self.seconds % 100 == 0:
                self.contSeconds += 1
                dif = float(float(self.percentageHouse) - float(self.percentagePrev))
                self.devPercentages.append(dif)
                self.secondsArray.append(self.contSeconds)
                self.percentagePrev = self.percentageHouse

            ax = self.figure.add_subplot(111)
            ax.set_xlabel('Time')
            ax.set_ylabel('Percentage Derivative')
            ax.set_xlim([0, 9]);
            ax.set_ylim([0, 10]);
            ax.plot(self.secondsArray, self.devPercentages,'r')
            self.canvas.draw()


    def RTx(self, angle, tx, ty, tz):
        RT = np.matrix([[1, 0, 0, tx], [0, math.cos(angle), -math.sin(angle), ty], [0, math.sin(angle), math.cos(angle), tz], [0,0,0,1]])
        return RT

    def RTy(self, angle, tx, ty, tz):
        RT = np.matrix([[math.cos(angle), 0, math.sin(angle), tx], [0, 1, 0, ty], [-math.sin(angle), 0, math.cos(angle), tz], [0,0,0,1]])
        return RT

    def RTz(self, angle, tx, ty, tz):
        RT = np.matrix([[math.cos(angle), -math.sin(angle), 0, tx], [math.sin(angle), math.cos(angle),0, ty], [0, 0, 1, tz], [0,0,0,1]])
        return RT

    def RTVacuum(self):
        RTy = self.RTy(pi, 1, -1, 0)
        return RTy


    def calculatePixelsWhite(self):
        # Calculating the 100% of the pixels that can be traversed
        numPixels = 0
        for i in range(0, self.map.shape[1]):
            for j in range(0, self.map.shape[0]):
                if self.map[i][j] == 255:
                    numPixels = numPixels + 1
        return numPixels

    def calculatePercentage(self):
        percentage = float(self.numPixelsWalked * 100) / float(self.numPixels)
        # If vacuum is stopped, the percentage is zero
        if self.numPixelsWalked == self.numPixelInit:
            percentage = 0.0
        return percentage


    def percentageWalked(self):
        pose = self.winParent.getPose3D().getPose3d()
        x = pose.x
        y = pose.y
        scale = 30

        final_poses = self.RTVacuum() * np.matrix([[x], [y], [1], [1]]) * scale

        i_init = int(-50/4+final_poses.flat[0] + self.map.shape[1]/2)
        i_finish = int(50/4+final_poses.flat[0] + self.map.shape[1]/2)
        j_init = int(-50/4+final_poses[1] + self.map.shape[0]/2)
        j_finish = int(50/4+final_poses[1] + self.map.shape[0]/2)
        for k in range(i_init, i_finish+1):
            for l in range(j_init, j_finish+1):
                if (self.map[k][l] == 255):
                    self.numPixelsWalked = self.numPixelsWalked + 1
                    self.map[k][l] = 128

        self.percentageHouse = self.calculatePercentage()


    def updateG(self):
        self.percentageWalked()
        self.update()
