import sys
import config
#import comm
from PyQt5.QtWidgets import QApplication
from gui.GUI import MainWindow
from gui.threadGUI import ThreadGUI
from MyAlgorithm import MyAlgorithm

import rospy
import threading
from jderobotTypes import LaserData, CMDVel, Pose3d, SonarData
from gui.threadPublisher import ThreadPublisher
sys.path.append('/home/vladkrav/TFM/AmigoBot/web-template')
from interfaces.motors import PublisherMotors
from interfaces.pose3d import ListenerPose3d
from interfaces.laser import ListenerLaser
from interfaces.sonar import ListenerSonar

if __name__ == "__main__":

    motors = PublisherMotors("/robot0/cmd_vel", 0.2, 0.2)
    pose3d = ListenerPose3d("/robot0/odom")
    laser = ListenerLaser("/robot0/laser_1")
    sonar_0 = ListenerSonar("/robot0/sonar_0")
    sonar_1 = ListenerSonar("/robot0/sonar_1")
    sonar_2 = ListenerSonar("/robot0/sonar_2")
    sonar_3 = ListenerSonar("/robot0/sonar_3")
    sonar_4 = ListenerSonar("/robot0/sonar_4")
    sonar_5 = ListenerSonar("/robot0/sonar_5")
    sonar_6 = ListenerSonar("/robot0/sonar_6")
    sonar_7 = ListenerSonar("/robot0/sonar_7")
    sonar = [sonar_0, sonar_1, sonar_2, sonar_3, sonar_4, sonar_5, sonar_6, sonar_7]
    
    #Run your Algorithm with your solution
    algorithm=MyAlgorithm(pose3d, motors, laser, sonar)

    #app = QApplication(sys.argv)
    #myGUI = MainWindow(pose3d)
    #myGUI.setMotors(motors)
    #myGUI.setPose3D(pose3d)
    #myGUI.setLaser(laser)
    #myGUI.setAlgorithm(algorithm)
    #myGUI.show()

    #t2 = ThreadGUI(myGUI)
    #t2.daemon = True
    #t2.start()
    #sys.exit(app.exec_())