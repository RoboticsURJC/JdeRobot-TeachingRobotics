import numpy as np
import time
import math

class ardroneControl:
    def __init__(self, show = False):
        #self.pathlist = pathlist
        self.getTarget = False
        self.controlYaw = False
        self.getFinal = False
        self.show = show
        self.PathId = 0

    def restart(self):
        self.getTarget = False
        self.controlYaw = False
        self.getFinal = False
        self.PathId = 0

    def setPath(self, pathlist):
        self.pathlist = pathlist
    
    def getPath(self):
        return self.pathlist
    
    def setControlYaw(self, controlYaw):
        #self.controlYaw = False
        self.controlYaw = controlYaw

    def findTarget(self,Pose):
        X = Pose[0]
        Y = Pose[1]
        Z = Pose[2]
        num = len(self.pathlist[0])-1
        TargetNowX = self.pathlist[0][self.PathId]
        TargetNowY = self.pathlist[1][self.PathId]
        TargetNowZ = self.pathlist[2][self.PathId]

        dis = math.sqrt(pow(X-TargetNowX,2)+pow(Y-TargetNowY,2)+pow(Z-TargetNowZ,2))
        if dis < 1:
            if num == self.PathId:
                if dis < 0.2:
                    self.getTarget = True
            else:
                self.PathId += 1
        #elif(math.fabs(self.e[0]) < 0.01 and math.fabs(self.e[1])<1.5 and math.fabs(self.e[2])<0.01):
        #    self.PathId += 1
        print ("path",self.PathId)
        target = [0, 0, 0]
        target[0] = self.pathlist[0][self.PathId]
        target[1] = self.pathlist[1][self.PathId]
        target[2] = self.pathlist[2][self.PathId]
        return target
    
    def isGetTarget(self):
        return self.getTarget

    def control(self, Pose):
        # id = 1, pid
        # id = 2, direct
        TargetPose = self.findTarget(Pose)
        if self.show:
            print ("pose", Pose)
            print ("target", TargetPose)
        
        vx = TargetPose[0] - Pose[0]
        vy = TargetPose[1] - Pose[1]
        vz = TargetPose[2] - Pose[2]
        az = 0  - Pose[3]

        vx = self.limiting(vx, 1, -1)
        vy = self.limiting(vy, 1, -1)
        vz = self.limiting(vz, 1, -1)
        az = self.limiting(az, 1, -1)

        if self.show:
            print("v", vx,vy,vz,az)

        return [vx,vy,vz,az]

    def limiting(self, num, max, min):
        if num > max:
            num = max
        if num < min:
            num = min

        return num

