import threading
import time
from datetime import datetime

import math
import jderobot

from parallelIce.cameraClient import CameraClient
from parallelIce.navDataClient import NavDataClient
from parallelIce.cmdvel import CMDVel
from parallelIce.extra import Extra
from parallelIce.pose3dClient import Pose3DClient

from navigation.navigation import navigation
from navigation.control.ardroneControl import ardroneControl

time_cycle = 80

class MyAlgorithm(threading.Thread):

    def __init__(self, camera, navdata, pose, cmdvel, extra):
        self.camera = camera
        self.navdata = navdata
        self.pose = pose
        self.cmdvel = cmdvel
        self.extra = extra

        self.minError=0.01

        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)

        self.navigation = navigation(None,[0,0,0],0.2,3)
        
        self.find_path = False
        self.get_point = True
        #self.goal_point = [[7.5,7.5,1],[-5,-7.5,1],[-7.5,-7.5,5],[-7.5,7.5,5],[7.5,-7.5,5]]
        self.goal_point = [[7.5, 0 ,6], [7.5,7.5,2],[-7.5, 7.5, 2],[-7.5,7.5,6]]
        self.num = 0

    def run (self):

        self.stop_event.clear()

        while (not self.kill_event.is_set()):
           
            start_time = datetime.now()

            if not self.stop_event.is_set():
                self.execute()

            finish_Time = datetime.now()

            dt = finish_Time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            #print (ms)
            if (ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

    def stop (self):
        self.stop_event.set()

    def play (self):
        if self.is_alive():
            self.stop_event.clear()
        else:
            self.start()

    def kill (self):
        self.kill_event.set()


    def execute(self):
        # Add your code here
        # use: self.pose.getPose3d().x
        #      self.pose.getPose3d().y
        # to get the coordinates of the drone in the x,y plane
        pose_n = [self.pose.getPose3d().x, self.pose.getPose3d().y, self.pose.getPose3d().z, self.pose.getPose3d().yaw]
        print (pose_n)

        if not self.find_path and self.get_point and self.num < len(self.goal_point):
            self.cmdvel.setVX(0)
            self.cmdvel.setVY(0)
            self.cmdvel.setVZ(0)
            self.cmdvel.setYaw(0)
            self.cmdvel.sendVelocities()
            if self.num == 0:
                self.navigation.update_map_3d()
            goal_pose = self.goal_point[self.num]
            print ("goal", goal_pose)            
            self.find_path = self.navigation.path_planning_3d(pose_n,goal_pose)
        else:
            [self.get_point, data] = self.navigation.path_following_3d(pose_n)
            if self.get_point:
                self.find_path = False
                self.num += 1
            self.cmdvel.setVX(data[0])
            self.cmdvel.setVY(data[1])
            self.cmdvel.setVZ(data[2])
            self.cmdvel.setYaw(data[3])
            self.cmdvel.sendVelocities()
