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
#       Alberto Martin Florido <almartinflorido@gmail.com>
#       Aitor Martinez Fernandez <aitor.martinez.fernandez@gmail.com>
#

import sys
import config
import comm
from MyAlgorithm import MyAlgorithm
import easyiceconfig as EasyIce
from gui.threadGUI import ThreadGUI
from parallelIce.cameraClient import CameraClient
from parallelIce.navDataClient import NavDataClient
from parallelIce.cmdvel import CMDVel
from parallelIce.extra import Extra
from parallelIce.pose3dClient import Pose3DClient
from gui.GUI import MainWindow
from PyQt5.QtWidgets import QApplication

import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == '__main__':

    cfg = config.load(sys.argv[1])

    #starting comm
    jdrc= comm.init(cfg, 'Introrob')

    camera = jdrc.getCameraClient("Introrob.Camera")
    navdata = jdrc.getNavdataClient("Introrob.Navdata")
    pose = jdrc.getPose3dClient("Introrob.Pose3D")
    cmdvel = jdrc.getCMDVelClient("Introrob.CMDVel")
    extra = jdrc.getArDroneExtraClient("Introrob.Extra")


    algorithm=MyAlgorithm(camera, navdata, pose, cmdvel, extra)

    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.setCamera(camera)
    frame.setNavData(navdata)
    frame.setPose3D(pose)
    frame.setCMDVel(cmdvel)
    frame.setExtra(extra)
    frame.setAlgorithm(algorithm)
    frame.show()
    
    

    t2 = ThreadGUI(frame)  
    t2.daemon=True
    t2.start()
    
    sys.exit(app.exec_())  
