#!/usr/bin/python
#-*- coding: utf-8 -*-

import numpy as np
import threading
import time
from datetime import datetime
import jderobot
import math
import cv2
from math import pi as pi
import random

time_cycle = 80


class MyAlgorithm(threading.Thread):
    
    def __init__(self, pose3d, motors, laser, sonar):

        self.pose3d = pose3d
        self.motors = motors
        self.laser = laser
        self.sonar = sonar
        self.stop_event = threading.Event()
        self.kill_event = threading.Event()
        self.lock = threading.Lock()
        threading.Thread.__init__(self, args=self.stop_event)
        self.start()

    def parse_laser_data(self,laser_data):
        laser = []
        for i in range(400):
            dist = laser_data.values[i]
            angle = math.radians(i)
            laser += [(dist, angle)]
        return laser

    def laser_vector(self,laser_array):
        laser_vectorized = []
        for d,a in laser_array:
            x = d * math.cos(a) * -1
            y = d * math.sin(a) * -1
            v = (x, y)
            laser_vectorized += [v]
        return laser_vectorized
        
    def run (self):
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
        self.motors.sendV(0)
        self.motors.sendAZ(0)
        self.stop_event.set()

    def play (self):
        if self.is_alive():
            self.stop_event.clear()
        else:
            self.start()

    def kill (self):
        self.kill_event.set()

    def execute(self):

        print ('Execute')
        # TODO
        print ("Posicion X del robot: ", self.pose3d.getPose3d().x)
        print ("Posicion Y del robot: ", self.pose3d.getPose3d().y)
        print ("Giro del AmigoBot: ", self.pose3d.getPose3d().yaw)
        print ("Distancia del sonar_0: ", self.sonar[0].getSonarData().distances)
        print ("Distancia del sonar_1: ", self.sonar[1].getSonarData().distances)
        print ("Distancia del sonar_3: ", self.sonar[3].getSonarData().distances)
        print ("Distancia del sonar_2: ", self.sonar[2].getSonarData().distances)
        print ("Distancia del sonar_4: ", self.sonar[4].getSonarData().distances)
        print ("Distancia del sonar_5: ", self.sonar[5].getSonarData().distances)
        print ("Distancia del sonar_6: ", self.sonar[6].getSonarData().distances)
        print ("Distancia del sonar_7: ", self.sonar[7].getSonarData().distances)
        print ("Distancia del laser: ", self.laser.getLaserData().values)
        self.motors.sendW(0.2)
        self.motors.sendV(0)