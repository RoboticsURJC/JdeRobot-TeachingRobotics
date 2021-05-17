#
#  Copyright (C) 1997-2015 JDE Developers Team
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
#       Alberto Martin Florido <almartinflorido@gmail.com>
#
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
# from gui.speedoMeter import SpeedoMeter
# from gui.attitudeIndicator import AttitudeIndicator
from qfi import qfi_ADI, qfi_ALT, qfi_SI, qfi_HSI
import math


class SensorsWidget(QWidget):
    sensorsUpdate = pyqtSignal()

    def __init__(self, winParent):
        super(SensorsWidget, self).__init__()
        self.winParent = winParent
        self.sensorsUpdate.connect(self.updateSensors)
        self.initUI()

    def initUI(self):

        self.mainLayout = QGridLayout()
        self.horizonLayout = QVBoxLayout()
        self.horizonData = QGridLayout()
        self.compassLayout = QVBoxLayout()
        self.compassData = QGridLayout()
        self.altLayout = QVBoxLayout()
        self.altData = QGridLayout()

        self.setMinimumSize(660, 450)
        self.setMaximumSize(660, 450)

        self.setWindowTitle("Sensors")

        self.pitchLabel = QLabel('Pitch:', self)
        self.pitchValueLabel = QLabel('0', self)
        self.pitchValueLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.rollLabel = QLabel('Roll:', self)
        self.rollValueLabel = QLabel('0', self)
        self.rollValueLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.yawLabel = QLabel('Yaw:', self)
        self.yawValueLabel = QLabel('0', self)
        self.yawValueLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.altLabel = QLabel('Alt:', self)
        self.altValueLabel = QLabel('0', self)
        self.altValueLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.pitchgLabel = QLabel("\272", self)
        self.rollgLabel = QLabel("\272", self)
        self.yawgLabel = QLabel("\272", self)
        self.altmLabel = QLabel('m', self)

        hSpacer = QSpacerItem(100, 30, QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.horizonData.addItem(hSpacer, 0, 0, 1, 1, Qt.AlignLeft)
        self.horizonData.addWidget(self.pitchLabel, 0, 1, Qt.AlignCenter)
        self.horizonData.addWidget(self.pitchValueLabel, 0, 2, Qt.AlignCenter)
        self.horizonData.addWidget(self.pitchgLabel, 0, 3, Qt.AlignCenter)
        self.horizonData.addWidget(self.rollLabel, 0, 4, Qt.AlignCenter)
        self.horizonData.addWidget(self.rollValueLabel, 0, 5, Qt.AlignCenter)
        self.horizonData.addWidget(self.rollgLabel, 0, 6, Qt.AlignCenter)
        self.horizonData.addItem(hSpacer, 0, 7, 1, 1, Qt.AlignRight)

        self.compassData.addItem(hSpacer, 0, 0, 1, 1, Qt.AlignLeft)
        self.compassData.addWidget(self.yawLabel, 0, 1, Qt.AlignCenter)
        self.compassData.addWidget(self.yawValueLabel, 0, 2, Qt.AlignCenter)
        self.compassData.addWidget(self.yawgLabel, 0, 3, Qt.AlignCenter)
        self.compassData.addItem(hSpacer, 0, 4, 1, 1, Qt.AlignRight)

        self.altData.addItem(hSpacer, 0, 0, 1, 1, Qt.AlignLeft)
        self.altData.addWidget(self.altLabel, 0, 1, Qt.AlignCenter)
        self.altData.addWidget(self.altValueLabel, 0, 2, Qt.AlignCenter)
        self.altData.addWidget(self.altmLabel, 0, 3, Qt.AlignCenter)
        self.altData.addItem(hSpacer, 0, 4, 1, 1, Qt.AlignLeft)

        self.altd = qfi_ALT.qfi_ALT(self)

        self.altd.setFixedSize(QtCore.QSize(200,200))
        self.altLayout.addWidget(self.altd)
        self.altLayout.addLayout(self.altData)
        # self.altd.move(420,50)

        self.compass = qfi_HSI.qfi_HSI(self)
        self.compass.setFixedSize(QtCore.QSize(200, 200))
        self.compassLayout.addWidget(self.compass)
        self.compassLayout.addLayout(self.compassData)

        self.horizon = qfi_ADI.qfi_ADI(self)
        self.horizon.setFixedSize(QtCore.QSize(200, 200))
        self.horizonLayout.addWidget(self.horizon)
        self.horizonLayout.addLayout(self.horizonData)

        # self.battery=Qwt.QwtThermo(self)
        # self.battery.setMaxValue(100.0)
        # self.battery.setMinValue(0.0)
        # self.battery.setPipeWidth(10)

        # self.battery.move(580,10)
        # self.battery.resize(56,241)
        # self.batteryLabel=QLabel('Battery (%)',self)
        # self.batteryLabel.move(580,251)

        self.velLinX = qfi_SI.qfi_SI(self)
        self.velLinX.setFixedSize(QtCore.QSize(150, 150))
        # self.velLinX.move(60,270)
        self.velXLabel = QLabel('Linear X (m/s)', self)
        # self.velXLabel.move(95,420)


        self.velLinY = qfi_SI.qfi_SI(self)
        self.velLinY.setFixedSize(QtCore.QSize(150, 150))
        # self.velLinY.move(240,270)
        self.velYLabel = QLabel('Linear Y (m/s)', self)
        # self.velYLabel.move(275,420)

        self.velLinZ = qfi_SI.qfi_SI(self)
        self.velLinZ.setFixedSize(QtCore.QSize(150, 150))
        # self.velLinZ.setLabel("8 m/s")
        # self.velLinZ.move(420,270)
        self.velZLabel = QLabel('Linear Z (m/s)', self)
        # self.velZLabel.move(455,420)

        self.mainLayout.addLayout(self.horizonLayout, 0, 0, Qt.AlignCenter)
        self.mainLayout.addLayout(self.compassLayout, 0, 1, Qt.AlignCenter)
        self.mainLayout.addLayout(self.altLayout, 0, 2, Qt.AlignCenter)
        self.mainLayout.addWidget(self.velLinX, 1, 0, Qt.AlignCenter)
        self.mainLayout.addWidget(self.velLinY, 1, 1, Qt.AlignCenter)
        self.mainLayout.addWidget(self.velLinZ, 1, 2, Qt.AlignCenter)
        self.mainLayout.addWidget(self.velXLabel, 2, 0, Qt.AlignCenter)
        self.mainLayout.addWidget(self.velYLabel, 2, 1, Qt.AlignCenter)
        self.mainLayout.addWidget(self.velZLabel, 2, 2, Qt.AlignCenter)
        self.setLayout(self.mainLayout);

    def updateSensors(self):
        pose = self.winParent.getPose3D().getPose3d()

        if pose != None:
            qw = pose.q[0]
            qx = pose.q[1]
            qy = pose.q[2]
            qz = pose.q[3]
            self.drawAltd(pose.z)
            self.drawYawValues(self.quatToYaw(qw, qx, qy, qz) * 180 / math.pi)
            self.drawPitchRollValues(self.quatToPitch(qw, qx, qy, qz) * 180 / math.pi,
                                     self.quatToRoll(qw, qx, qy, qz) * 180 / math.pi)

        navdata = self.winParent.getNavData().getNavData()

        if navdata != None:
            # self.battery.setValue(navdata.batteryPercent)
            self.drawVelocities(navdata.vx, navdata.vy, navdata.vz)

    def drawYawValues(self, degress):
        value = "{0:.2f}".format(degress)
        self.yawValueLabel.setText(value)
        self.compass.setHeading(degress)
        self.compass.viewUpdate.emit()

    def drawAltd(self, meters):

        self.altd.setAltitude(meters * 10)
        self.altd.viewUpdate.emit()

        value = "{0:.0f}".format(meters)
        self.altValueLabel.setText(value)

    def drawPitchRollValues(self, pitch, roll):
        if (pitch > 0 and pitch <= 90):
            result = pitch / 90
            result = -result
        elif (pitch < 0 and pitch >= -90):
            result = pitch / -90
        else:
            result = 0.0

        self.horizon.setPitch(pitch)
        self.horizon.setRoll(-roll)
        self.horizon.viewUpdate.emit()
        pitchValue = "{0:.2f}".format(pitch)
        rollValue = "{0:.2f}".format(roll)
        self.pitchValueLabel.setText(pitchValue)
        self.rollValueLabel.setText(rollValue)

    def drawVelocities(self, vx, vy, vz):

        vx = math.fabs(vx)
        vx /= 1000.0
        self.velLinX.setSpeed(vx)
        self.velLinX.viewUpdate.emit()
        vx = math.fabs(vx)

        vy = math.fabs(vy)
        vy /= 1000.0
        self.velLinY.setSpeed(vy)
        self.velLinY.viewUpdate.emit()

        vz = math.fabs(vz)
        vz /= 1000.0
        self.velLinZ.setSpeed(vz)
        self.velLinZ.viewUpdate.emit()

    def quatToRoll(self, qw, qx, qy, qz):
        rotateXa0 = 2.0 * (qy * qz + qw * qx)
        rotateXa1 = qw * qw - qx * qx - qy * qy + qz * qz
        rotateX = 0.0

        if (rotateXa0 != 0.0 and rotateXa1 != 0.0):
            rotateX = math.atan2(rotateXa0, rotateXa1)

        return rotateX

    def quatToPitch(self, qw, qx, qy, qz):
        rotateYa0 = -2.0 * (qx * qz - qw * qy)
        rotateY = 0.0
        if (rotateYa0 >= 1.0):
            rotateY = math.pi / 2.0
        elif (rotateYa0 <= -1.0):
            rotateY = -math.pi / 2.0
        else:
            rotateY = math.asin(rotateYa0)

        return rotateY

    def quatToYaw(self, qw, qx, qy, qz):
        rotateZa0 = 2.0 * (qx * qy + qw * qz)
        rotateZa1 = qw * qw + qx * qx - qy * qy - qz * qz
        rotateZ = 0.0
        if (rotateZa0 != 0.0 and rotateZa1 != 0.0):
            rotateZ = math.atan2(rotateZa0, rotateZa1)

        return rotateZ

    def closeEvent(self, event):
        self.winParent.closeSensorsWidget()
