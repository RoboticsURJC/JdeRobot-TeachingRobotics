import numpy as np
import math
from math import pi as pi
import cv2

class Map:
    def __init__(self, pose3d):
        self.pose3d = pose3d
    
    def RTx(self, angle, tx, ty, tz):
        RT = np.matrix([[1, 0, 0, tx], [0, math.cos(angle), -math.sin(angle), ty], 
                        [0, math.sin(angle), math.cos(angle), tz], [0, 0, 0, 1]])
        return RT
        
    def RTy(self, angle, tx, ty, tz):
        RT = np.matrix([[math.cos(angle), 0, math.sin(angle), tx], [0, 1, 0, ty],
                        [-math.sin(angle), 0, math.cos(angle), tz], [0, 0, 0, 1]])
        return RT
        
    def RTz(self, angle, tx, ty, tz):
        RT = np.matrix([[math.cos(angle), -math.sin(angle), 0, tx], [math.sin(angle), math.cos(angle), 0, ty],
                        [0, 0, 1, tz], [0, 0, 0, 1]])
        return RT
        
    def RTFormula(self):
        RTz = self.RTz(pi/2, 50, 70, 0)
        return RTz
        
    def getFormulaCoordinates(self):
        
        pose = self.pose3d.getPose3d()
        x = pose.x
        y = pose.y
        
        scale_y = 1.25; offset_y = 77
        y = scale_y * y + offset_y
        
        scale_x = -2.6; offset_x = 151
        x = scale_x * x + offset_x
        
        return x, y

    # Function to reset
    def reset(self):
        # Nothing to do, service takes care!
        pass
    
