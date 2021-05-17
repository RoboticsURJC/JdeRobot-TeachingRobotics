import numpy as np
import math
from math import cos,sin,tan,pow,pi
from costmap_2d import costmap_2d
from costmap_3d import costmap_3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2

class occGridMap:
    def __init__(self, lo_occ = -10, lo_free = 5,lo_max = 15,lo_min = -15, dimension = 2):
        self.dimension = dimension
        self.lo_occ = lo_occ
        self.lo_free = lo_free
        self.lo_max = lo_max
        self.lo_min = lo_min
        if self.dimension == 2:
            self.map = costmap_2d(100, 100, 0.2)
            self.m_laserpose = []
            self.m_laserpose.append( [2,0,0] )
            self.m_laserpose.append( [-1.9,0,pi] )
            self.m_laserpose.append( [0.3,-1,-pi/2] )
            self.m_laserMaxRange = 11
            self.m_usableRange = 9
        elif self.dimension == 3:
            self.map = costmap_3d(100, 100, 100, 0.2, origin_x = -10, origin_y = -10, origin_z = 0)
            #cells_size_x, cells_size_y, cells_sise_z, resolution, origin_x = 0, origin_y = 0,origin_z = 0, default_value = 0

    def registerScan(self, pose, laserNum, laserData):
        laserPose = [0,0,0]
        laserPose[0] = pose[0] + cos(pose[2]) * self.m_laserpose[laserNum][0] - sin(pose[2]) * self.m_laserpose[laserNum][1]
        laserPose[1] = pose[1] + sin(pose[2]) * self.m_laserpose[laserNum][0] + cos(pose[2]) * self.m_laserpose[laserNum][1] 
        laserPose[2] = pose[2] + self.m_laserpose[laserNum][2]

        self.computerActiveArea(laserPose, laserData)
    
        P0 = self.map.worldToMapEnforceBounds(laserPose[0],laserPose[1])
        #print ("P0 = ", P0, laserPose)

        for i in range(180):
            r = laserData[i][0]
            if r > self.m_laserMaxRange:
                continue
            if r > self.m_usableRange:
                r = self.m_usableRange
            phit = [0,0]
            angle = math.radians(180 - i) - pi/2
            phit[0] = laserPose[0] + r * cos(laserPose[2] - angle)
            phit[1] = laserPose[1] + r * sin(laserPose[2] - angle)
            P1 = self.map.worldToMapEnforceBounds(phit[0],phit[1])
            #print ("P1 = ", P1, phit, i, "P0 = ", P0, laserPose)
            line = self.map.drawBresenham(P0[0],P0[1],P1[0],P1[1])
            #print ("line = " , line )
            lenLine = len(line)
            for i in range(lenLine):
                x = line[i][0]
                y = line[i][1]
                self.map.costmap_[x,y] += self.lo_free
            
            if r < self.m_usableRange:
                self.map.costmap_[P1[0],P1[1]] += self.lo_occ
        
        self.map.updateWeight(self.lo_max, self.lo_min)

        
    def computerActiveArea(self, laserPose, laserData):
        #P0 = self.worldToMapNoBounds(laserPose[0], laserPose[1])

        minP = self.map.mapToWorld(0,0)
        maxP = self.map.mapToWorld(self.map.size_x_ - 1, self.map.size_y_ - 1)

        minP = self.map.min_pose(laserPose, minP)
        maxP = self.map.max_pose(laserPose, maxP)

        # laser angle 0~180
        for i in range(180):
            r = laserData[i][0]
            if r > self.m_laserMaxRange:
                continue
            if r > self.m_usableRange:
                r = self.m_usableRange
            phit = [0,0]
            angle = math.radians(i) - pi/2
            phit[0] = laserPose[0] + r * cos(laserPose[2] - angle)
            phit[1] = laserPose[1] + r * sin(laserPose[2] - angle)
            #print ("P1 = ", phit, i)
            #P1 = self.worldToMapNoBounds(phit[0],phit[1])
            minP = self.map.min_pose(phit, minP)
            maxP = self.map.max_pose(phit, maxP)
            

        iMinP = self.map.worldToMapNoBounds(minP[0], minP[1])
        iMaxP = self.map.worldToMapNoBounds(maxP[0], maxP[1])
        if iMinP != [0, 0] or iMaxP != [self.map.size_x_ - 1, self.map.size_y_ - 1]:
            minP = [minP[0] - 1,minP[1] - 1]
            maxP = [maxP[0] + 1,maxP[1] + 1]
            self.map.resizeMap(minP, maxP)
            #print ("minp = ",minP, "maxP = ", maxP )


    def drawMap(self):
        if self.dimension == 2:
            h = self.map.size_x_
            w = self.map.size_y_
            mapppm = np.zeros((h,w,3))
            
            for i in range(h):
                for j in range(w):
                    mapppm[i,j,0] = (self.map.costmap_[i,j]+ 15)*255/30
                    mapppm[i,j,1] = (self.map.costmap_[i,j]+ 15)*255/30
                    mapppm[i,j,2] = (self.map.costmap_[i,j]+ 15)*255/30
                    # if self.map.costmap_[i,j] != 0:
                    #     print self.map.costmap_[i,j]
            #print self.map.costmap_
            cv2.imwrite('map_image.ppm',mapppm)
        elif self.dimension == 3:
            lx = self.map.size_x_
            ly = self.map.size_y_
            lz = self.map.size_z_

            x = np.array([])
            y = np.array([])
            z = np.array([])

            for i in range(lx):
                for j in range(ly):
                    for k in range(lz):
                        if self.map.costmap_[i,j,k] > 0:
                            x = np.append(x,i)
                            y = np.append(y,j)
                            z = np.append(z,k)

            ax = plt.subplot(111, projection='3d')
            ax.scatter(x, y, z, c='b')
            plt.savefig('map_image.png') 
