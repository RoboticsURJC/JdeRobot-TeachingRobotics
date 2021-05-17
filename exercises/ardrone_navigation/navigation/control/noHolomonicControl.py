import numpy as np
import time
import math

class noHolomonicControl:
    def __init__(self, show = False):
        #self.pathlist = pathlist
        self.find_path = False
        self.PathId = 0
        self.getTarget = False
        self.v_old = 0
        self.w_old = 0
        self.v = 0
        self.w = 0
        self.e_old = [0,0,0]
        self.e = [0,0,0]
        self.controlYaw = True
        self.getFinal = False
        self.show = show

    def restart(self):
        #self.pathlist = pathlist
        self.find_path = False
        self.PathId = 0
        self.getTarget = False
        self.v_old = 0
        self.w_old = 0
        self.v = 0
        self.w = 0
        self.e_old = [0,0,0]
        self.e = [0,0,0]
        self.controlYaw = True
        self.getFinal = False
        self.show = show

    def setPath(self, pathlist):
        self.pathlist = pathlist
    
    def getPath(self):
        return self.pathlist
    
    def setControlYaw(self, controlYaw):
        #self.controlYaw = False
        self.controlYaw = controlYaw

    def findTarget(self,Pose,id):
        X = Pose[0]
        Y = Pose[1]
        Yaw = Pose[2]
        num = len(self.pathlist[0])-1
        TargetNowX = self.pathlist[0][self.PathId]
        TargetNowY = self.pathlist[1][self.PathId]
        dis = math.sqrt(pow(X-TargetNowX,2)+pow(Y-TargetNowY,2))
        if dis < 1:
            if num == self.PathId:
                if id==1:
                    if math.fabs(self.e[0]) < 0.1 and math.fabs(self.e[1])<0.5 and math.fabs(self.e[2])<0.1:
                        self.getTarget = True
            else:
                self.PathId += 1
        #elif(math.fabs(self.e[0]) < 0.01 and math.fabs(self.e[1])<1.5 and math.fabs(self.e[2])<0.01):
        #    self.PathId += 1

        print ("path",self.PathId)
        target = [X,Y,Yaw]
        target[0] = self.pathlist[0][self.PathId]
        target[1] = self.pathlist[1][self.PathId]
        target[2] = self.pathlist[2][self.PathId]
        return target
    
    def isGetTarget(self):
        return self.getTarget

    def control(self, Pose, id):
        # id = 1, pid
        # id = 2, direct
        TargetPose = self.findTarget(Pose,id)
        num = len(self.pathlist[0])-1
        if self.show:
            print ("pose", Pose)
            print ("target", TargetPose)
        if id==1:
            self.e[0] = math.cos(Pose[2])*(TargetPose[0] - Pose[0]) + math.sin(Pose[2])*(TargetPose[1] - Pose[1])
            self.e[1] = -math.sin(Pose[2])*(TargetPose[0] - Pose[0]) + math.cos(Pose[2])*(TargetPose[1] - Pose[1])
            self.e[2] = TargetPose[2] - Pose[2]
            #print ("e:",self.e)
            #print ("e_old:",self.e_old)
            self.v = self.v_old + 0.2*(self.e[0] - self.e_old[0]) + 0.01*self.e[0]
            self.w = self.w_old + 0.5*self.v*(self.e[1] - self.e_old[1])  + 0.001*self.e[1] + 0.2*(self.e[2] - self.e_old[2]) + 0.01*self.e[2]
            #self.pathlist
            #print ("v w: ",self.v,self.w)
            #print ("v w old: ",self.v_old,self.w_old)
            if self.v > 0.5:
                self.w = self.w*0.5/self.v
                self.v = 0.5
            if self.v < -0.5:
                self.w = self.w*-0.5/self.v
                self.v = -0.5 
            self.v_old = self.v
            self.w_old = self.w
            self.e_old[0] = self.e[0]
            self.e_old[1] = self.e[1]
            self.e_old[2] = self.e[2]
        else:
            if self.controlYaw:
                theta = math.atan2((TargetPose[1] - Pose[1]),(TargetPose[0] - Pose[0]))
                theta_01 = theta - Pose[2]
                theta_21 = TargetPose[2] - theta
                theta_20 = TargetPose[2] - Pose[2]
                dis = math.sqrt(math.pow((TargetPose[1] - Pose[1]),2)+math.pow((TargetPose[0] - Pose[0]),2))
                if self.show:
                    
                    print ("theta_01 ",theta_01)
                    print ("theta_21 ",theta_21)
                    print ("dis ",dis)
                if math.fabs(theta_01) > 0.2 and dis > 0.1 and ~self.getFinal:
                    self.v = 0
                    if theta_01 > 0:
                        self.w = max(0.2, theta_01)
                    else:
                        self.w = min(-0.2, theta_01)
                elif dis > 0.1 and ~self.getFinal:
                    self.v = max(0.2, dis) 
                    self.w = 0
                elif math.fabs(theta_20) > 0.2 and num == self.PathId:
                    self.v = 0
                    if theta_21 > 0:
                        self.w = max(0.2, theta_20)
                    else:
                        self.w = min(-0.2, theta_20)
                    self.getFinal = True
                # elif math.fabs(theta_21) > 0.2:
                #     self.v = 0
                #     if theta_21 > 0:
                #         self.w = max(0.2, theta_21)
                #     else:
                #         self.w = min(-0.2, theta_21)
                else:
                    print ("get target")
                    self.v = 0
                    self.w = 0
            else:
                theta = math.atan2((TargetPose[1] - Pose[1]),(TargetPose[0] - Pose[0]))
                theta_01 = theta - Pose[2]
                dis = math.sqrt(math.pow((TargetPose[1] - Pose[1]),2)+math.pow((TargetPose[0] - Pose[0]),2))
                if math.fabs(theta_01) > 0.05:
                    self.v = 0
                    self.w = 0.5*theta_01
                elif dis > 0.1:
                    self.v = max(0.1, 0.5*dis)
                    self.w = 0
                else:
                    print ("get target")
                    self.v = 0
                    self.w = 0
        if self.show:
            print ('v, w ', self.v, self.w)

        return [self.v, self.w]
