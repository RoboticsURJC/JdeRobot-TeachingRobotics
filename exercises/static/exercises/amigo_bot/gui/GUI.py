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

from gui.widgets.teleopWidget import TeleopWidget
from gui.widgets.mapWidget import MapWidget
from gui.widgets.mapWidget import LogoWidget
from gui.widgets.graphicPercentageWidget import PercentageWidget
from gui.widgets.communicator import Communicator
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow
from gui.form import Ui_MainWindow
from jderobotTypes import CMDVel

class MainWindow(QMainWindow, Ui_MainWindow):

    updGUI=pyqtSignal()
    def __init__(self, pose3d, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.teleop=TeleopWidget(self)
        self.map=MapWidget(self)
        self.logo = LogoWidget(self)
        self.tlLayout.addWidget(self.teleop)
        self.teleop.setVisible(True)
        self.mapLayout.addWidget(self.map)
        self.logoLayout.addWidget(self.logo)
        self.map.setVisible(True)
        self.logo.setVisible(True)

        self.percentageCheck.stateChanged.connect(self.showPercentageWidget)
        self.percentageWidget=PercentageWidget(self, pose3d)
        self.percentageCommunicator=Communicator()

        self.pushButton.clicked.connect(self.playClicked)
        self.pushButton.setCheckable(True)
        self.updGUI.connect(self.updateGUI)

        self.stopButton.clicked.connect(self.stopClicked)

    def updateGUI(self):
        laserdata = self.laser.getLaserData()
        if (laserdata):
            self.map.setLaserValues(laserdata)
        self.map.update()

    def getPose3D(self):
        return self.pose3d

    def setPose3D(self,pose3d):
        self.pose3d=pose3d

    def getLaser(self):
        return self.laser

    def setLaser(self,laser):
        self.laser=laser

    def getMotors(self):
        return self.motors

    def setMotors(self,motors):
        self.motors=motors

    def getBumper(self):
        return self.bumper

    def setBumper(self,bumper):
        self.bumper=bumper

    def showPercentageWidget(self,state):
        if state == Qt.Checked:
            self.percentageWidget.show()
        else:
            self.percentageWidget.close()

    def closePercentageWidget(self):
        self.percentageCheck.setChecked(False)

    def playClicked(self):
        if self.pushButton.isChecked():
            self.pushButton.setText('RUNNING')
            self.pushButton.setStyleSheet("background-color: #ec7063")
            self.algorithm.play()
        else:
            self.pushButton.setText('STOPPED')
            self.pushButton.setStyleSheet("background-color: #7dcea0")
            self.algorithm.stop()

    def setAlgorithm(self, algorithm ):
        self.algorithm=algorithm

    def getAlgorithm(self):
        return self.algorithm

    def setXYValues(self,newX,newY):
        vel = CMDVel()
        myW=-newX*(self.motors.getMaxW())*2
        myV=-newY*(self.motors.getMaxV())
        vel.vx = myV
        vel.az = myW
        self.motors.sendVelocities(vel)

    def stopClicked(self):
        self.motors.sendV(0)
        self.motors.sendW(0)
        self.teleop.returnToOrigin()

    def closeEvent(self, event):
        self.algorithm.kill()
        event.accept()
