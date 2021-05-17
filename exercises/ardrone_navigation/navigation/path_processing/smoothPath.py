import numpy as np
import time
import math
from scipy import interpolate  
import matplotlib.pyplot as plt

class smooth:
    #def __init__(self):

    def setPath(self, pathlist):
        self.pathlist = pathlist
    
    def getPath(self):
        return self.pathlist

    def inter(self,pathlist):
        self.pathlist = pathlist
        x = self.pathlist[0]
        y = self.pathlist[1]
        xnew=np.linspace(min(x),max(x),201)
        #plt.figure(3)
        #plt.plot(x,y,"ro")  
  
        for kind in ["nearest","zero","slinear","quadratic","cubic"]:
            #"nearest","zero"
            #slinear
            #"quadratic","cubic"
            f=interpolate.interp1d(x,y,kind=kind)  
            ynew=f(xnew)
            #plt.plot(xnew,ynew,label=str(kind))
            #plt.savefig("figure3.jpg") 

    def Floyd(self,pathlist):
        self.pathlist = pathlist
        numLen = len(self.pathlist[0])
        if (numLen > 2):
            
            vector = [self.pathlist[0][numLen -1] - self.pathlist[0][numLen - 2], self.pathlist[1][numLen -1] - self.pathlist[1][numLen - 2],self.pathlist[2][numLen -1] - self.pathlist[2][numLen - 2]]
            tempvector = [0,0,0]
            #for (int i = numLen - 3; i>= 0; i--)
            i = numLen - 3
            while (i >= 0):
                tempvector = [self.pathlist[0][i+1] - self.pathlist[0][i], self.pathlist[1][i+1] - self.pathlist[1][i],self.pathlist[2][i+1] - self.pathlist[2][i]]
                if math.fabs(math.atan2(vector[1],vector[0])-math.atan2(tempvector[1],tempvector[0])) < 0.001:
                    del self.pathlist[0][i+1]
                    del self.pathlist[1][i+1]
                    del self.pathlist[2][i+1]
                else:
                    vector = tempvector
                i -= 1
        numLen = len(self.pathlist[0])
        #for (int i = numLen-1; i >= 0; i--) 
        i = numLen-1
        while(i>=0):
            j = 0
            while (j<=i-1):
            #for (int j = 0; j<= i-1; j++)
            
                if (self.CheckCrossNoteWalkable(i,j)):
                    k = i-1
                    while(k>=j):
                    #for (int k = i-1; k>=j; k--):
                        del self.pathlist[0][k]
                        del self.pathlist[1][k]
                        del self.pathlist[2][k]
                        k -= 1
                    i=j
                    break
                j += 1
            i -= 1

        return self.pathlist
    
    def CheckCrossNoteWalkable(self, i ,j):
        x1 = self.pathlist[0][i]
        y1 = self.pathlist[1][i]
        x2 = self.pathlist[0][j]
        y2 = self.pathlist[1][j]
        dis = math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))
        return dis < 1

    def checkYaw(self,pathlist, start):
        self.pathlist = pathlist
        num = len(self.pathlist[0])
        for i in range(num-1):
            if (i == 0):
                x0 = start[0]
                y0 = start[1]
            else:
                x0 = self.pathlist[0][i-1]
                y0 = self.pathlist[1][i-1]
            x1 = self.pathlist[0][i]
            y1 = self.pathlist[1][i]
            x2 = self.pathlist[0][i+1]
            y2 = self.pathlist[1][i+1]
            vector1 = [x1-x0,y1-y0]
            vector2 = [x2-x1,y2-y1]
            yaw1 = math.atan2(vector1[1],vector1[0])
            yaw2 = math.atan2(vector2[1],vector2[0])
            # print ("yaw1")
            # print (yaw1)
            # print ("yaw2")
            # print (yaw2)
            yawtmp = (yaw2+yaw1)/2
            if (i==0):
                yawtmp = self.setYaw(yawtmp,start[2])
            else:
                yawtmp = self.setYaw(yawtmp,self.pathlist[2][i-1])
            print ("yawtmp",yawtmp)
            self.pathlist[2][i] = yawtmp
        return self.pathlist
    
    def setYaw(self, newYaw, lastYaw):
        dis = newYaw - lastYaw
        if math.fabs(dis) > 1.57:
            if newYaw >= 0:
                newYaw = -(3.14 - newYaw)
            else:
                newYaw = 3.147 + newYaw 
        return newYaw