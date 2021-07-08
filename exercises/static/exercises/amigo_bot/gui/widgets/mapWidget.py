#
#  Copyright (C) 1997-2016 JDE Developers Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
#  Authors :
#       Irene Lope Rodriguez<irene.lope236@gmail.com>
#       Vanessa Fernandez Martinez<vanessa_1895@msn.com>


from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtCore import QPoint, QPointF, pyqtSignal, Qt
from PyQt5 import QtGui, QtCore
import numpy as np
import math
from math import pi as pi
import cv2


class MapWidget(QWidget):

    stopSIG=pyqtSignal()

    def __init__(self,winParent):
        super(MapWidget, self).__init__()
        self.winParent=winParent
        self.initUI()
        self.laser = []
        self.trail = []


    def initUI(self):
        self.map = cv2.imread("resources/images/robocup.png", cv2.IMREAD_GRAYSCALE)
        self.map = cv2.resize(self.map, (500, 500))
        image = QtGui.QImage(self.map.data, self.map.shape[1], self.map.shape[0], self.map.shape[1], QtGui.QImage.Format_Indexed8);
        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.height = self.pixmap.height()
        self.width = self.pixmap.width()
        self.mapWidget = QLabel(self)
        self.mapWidget.setPixmap(self.pixmap)
        self.mapWidget.resize(self.width, self.height)

        self.resize(300,300)
        self.setMinimumSize(500,500)


    def setLaserValues(self, laser_data):
        # Init laser array
        if len(self.laser) == 0:
            for i in range(400):
                self.laser.append((0,0))

        for i in range(400):
            dist = laser_data.values[i]
            angle = -math.pi/2 + math.radians(i)
            self.laser += [(dist, angle)]


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
        RTy = self.RTy(pi, 0.6, -1, 0)
        return RTy


    def drawVacuum(self, painter):
        scale = 50

        pose = self.winParent.getPose3D().getPose3d()
        x = pose.x
        y = pose.y
        yaw = pose.yaw

        final_poses = self.RTVacuum() * np.matrix([[x], [y], [1], [1]]) * scale

        triangle = QtGui.QPolygon()
        triangle.append(QtCore.QPoint(final_poses.flat[0]-50/9, final_poses.flat[1]+50/7))
        triangle.append(QtCore.QPoint(final_poses.flat[0]+50/3, final_poses.flat[1]-10+50/7))
        triangle.append(QtCore.QPoint(final_poses.flat[0]+50/3, final_poses.flat[1]+10+50/7))
        matrix = QtGui.QTransform()
        matrix.rotate(-180*yaw/pi)
        triangle = matrix.map(triangle)
        # The center of triangle is (final_poses.flat[0]+50/9, final_poses.flat[1]+50/7)
        center = matrix.map(QtCore.QPoint(final_poses.flat[0]+50/9, final_poses.flat[1]+50/7))
        xDif = final_poses.flat[0]+50/9 - center.x()
        yDif = final_poses.flat[1] +50/7- center.y()

        triangle.translate(xDif, yDif)

        pen = QPen(Qt.red, 2)
        painter.setPen(pen)
        painter.drawPolygon(triangle)


    def drawCircle(self, painter, centerX, centerY):
        pen = QPen(Qt.blue, 2)
        painter.setPen(pen)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        brush.setColor(QtGui.QColor(Qt.blue))
        painter.setBrush(brush)
        painter.drawEllipse(centerX, centerY, 50/3, 50/3)


    def drawTrail(self, painter):
        pose = self.winParent.getPose3D().getPose3d()
        x = pose.x
        y = pose.y
        scale = 50

        final_poses = self.RTVacuum() * np.matrix([[x], [y], [1], [1]]) * scale

        # Vacuum's way
        self.trail.append([final_poses.flat[0], final_poses.flat[1]])

        for i in range(0, len(self.trail)):
            self.drawCircle(painter, self.trail[i][0], self.trail[i][1])


    def paintEvent(self, e):

        copy = self.pixmap.copy()
        painter = QtGui.QPainter(copy)

        painter.translate(QPoint(self.width/2, self.height/2))
        self.drawTrail(painter)
        self.drawVacuum(painter)

        self.mapWidget.setPixmap(copy)
        painter.end()


class LogoWidget(QWidget):
    stopSIG=pyqtSignal()

    def __init__(self,winParent):
        super(LogoWidget, self).__init__()
        self.winParent=winParent
        self.initUI()


    def initUI(self):
        self.logo = cv2.imread("resources/logo_jderobot1.png", cv2.IMREAD_UNCHANGED)
        self.logo = cv2.resize(self.logo, (100, 100))
        image = QtGui.QImage(self.logo.data, self.logo.shape[1], self.logo.shape[0], QtGui.QImage.Format_ARGB32);
        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.height = self.pixmap.height()
        self.width = self.pixmap.width()
        self.logoWidget = QLabel(self)
        self.logoWidget.setPixmap(self.pixmap)
        self.logoWidget.resize(self.width, self.height)

        self.resize(300,300)
        self.setMinimumSize(100,100)
