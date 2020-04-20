#!/usr/bin/python3
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
#       Eduardo Perdices <eperdices@gsyc.es>	
#       Aitor Martinez Fernandez <aitor.martinez.fernandez@gmail.com>	
#  Rosified by:
#       Shyngyskhan Abilkassov <s.abilkassov@gmail.com>

# General imports
import sys
import config
import rospy
import comm

# Practice imports
from gui.GUI import MainWindow
from gui.threadGUI import ThreadGUI
from MyAlgorithm import MyAlgorithm
from PyQt5.QtWidgets import QApplication
from interfaces.motors import PublisherMotors

if __name__ == "__main__":

    cfg = config.load(sys.argv[1])
    jdrc = comm.init(cfg, 'Stop')
    pose3d = jdrc.getPose3dClient("Stop.Pose3D")
    cameraC = jdrc.getCameraClient("Stop.CameraC")
    cameraL = jdrc.getCameraClient("Stop.CameraL")
    cameraR = jdrc.getCameraClient("Stop.CameraR")

    print("Publishing "+  "Stop.Motors" + " with ROS messages")
    topicM = cfg.getProperty("Stop.Motors"+".Topic")
    maxW = cfg.getPropertyWithDefault("Stop.Motors"+".maxW", 4)
    if not maxW:
        maxW = 5
        print ("Stop.Motors"+".maxW not provided, the default value is used: "+ repr(maxW))

    maxV = cfg.getPropertyWithDefault("Stop.Motors"+".maxV", 5)
    if not maxV:
        maxV = 10
        print ("Stop.Motors"+".maxV not provided, the default value is used: "+ repr(maxV))
    
    motors = PublisherMotors(topicM, maxV, maxW)

    print("Starting movement of dummy cars")
    topicM_Dummy1 = cfg.getProperty("Stop.DummyMotors1"+".Topic")
    topicM_Dummy2 = cfg.getProperty("Stop.DummyMotors2"+".Topic")
    motorsDummy1 = PublisherMotors(topicM_Dummy1, maxV, maxW)
    motorsDummy2 = PublisherMotors(topicM_Dummy2, maxV, maxW)

    motorsDummy1.sendV(3.5)
    motorsDummy2.sendV(4)

    algorithm = MyAlgorithm(pose3d, cameraC, cameraL, cameraR, motors)

    app = QApplication(sys.argv)
    myGUI = MainWindow()
    myGUI.setMotors(motors)
    myGUI.setCameraC(cameraC)
    myGUI.setCameraL(cameraL)
    myGUI.setCameraR(cameraR)
    myGUI.setPose3D(pose3d)
    myGUI.setAlgorithm(algorithm)
    myGUI.show()

    t2 = ThreadGUI(myGUI)
    t2.daemon=True
    t2.start()

    sys.exit(app.exec_())
