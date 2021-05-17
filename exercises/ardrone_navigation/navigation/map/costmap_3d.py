import numpy as np
import math
from math import cos,sin,tan,pow,pi
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class costmap_3d:
    def __init__(self,cells_size_x, cells_size_y, cells_sise_z, resolution, origin_x = 0, origin_y = 0,origin_z = 0, default_value = 0):
        self.size_x_ = cells_size_x
        self.size_y_ = cells_size_y
        self.size_z_ = cells_sise_z
        self.resolution_ = resolution # grid length
        self.origin_x_ = origin_x
        self.origin_y_ = origin_y
        self.origin_z_ = origin_z
        self.default_value_ = default_value

        self.initMaps(self.size_x_, self.size_y_, self.size_z_, self.default_value_)

    def initMaps(self, size_x, size_y, size_z, default_value):
        if (size_x>0 and size_y>0 and size_z>0):
            self.costmap_ = np.full((size_x, size_y, size_z), default_value, int)
        else:
            self.costmap_ = None
            print ("map's size error")

    def reinitMap(self, size_x, size_y, size_z, resolution, origin_x, origin_y, origin_z):
        self.size_x_ = size_x
        self.size_y_ = size_y
        self.size_z_ = size_z
        self.resolution_ = resolution
        self.origin_x_ = origin_x
        self.origin_y_ = origin_y
        self.origin_z_ = origin_z

        self.initMaps(self.size_x_, self.size_y_, self.size_z_, self.default_value_)
    
    def resetMap(self, x0, y0, z0, xn, yn, zn):
        if xn > self.size_x_:
            xn = self.size_x_
        if yn > self.size_y_:
            yn = self.size_y_
        if zn > self.size_z_:
            zn = self.size_z_
        lenx = xn - x0
        leny = yn - y0
        lenz = yn - z0
        for i in range(lenx):
            for j in range(leny):
                for k in range(lenz):
                    self.costmap_[i+x0,j+y0,k+z0] = self.default_value_

    def cellDistance(self, world_dist):
        cells_dist = max(0.0, math.ceil(world_dist / self.resolution_))
        return cells_dist
    
    def getMap(self):
        return self.costmap_
    
    def getCost(self, mx, my, mz):
        if mx < self.size_x_ and my < self.size_y_ and mz < self.size_z_:
            return self.costmap_[mx, my, mz]
        else:
            return None
        
    def setCost(self, mx, my, mz, cost):
        if mx < self.size_x_ and my < self.size_y_ and mz < self.size_z_:
            self.costmap_[mx, my, mz] = cost
        else:
            print("Over the border")
    
    def getSizeInCellsX(self):
        return self.size_x_
    
    def getSizeInCellsY(self):
        return self.size_y_
    
    def getSizeInCellsZ(self):
        return self.size_z_

    def getSizeInMetersX(self):
        return (self.size_x_ - 1 + 0.5) * self.resolution_
    
    def getSizeInMetersY(self):
        return (self.size_y_ - 1 + 0.5) * self.resolution_
    
    def getSizeInMetersZ(self):
        return (self.size_z_ - 1 + 0.5) * self.resolution_

    def getOriginX(self):
        return self.origin_x_

    def getOriginY(self):
        return self.origin_y_
    
    def getOriginZ(self):
        return self.origin_z_

    def getResolution(self):
        return self.resolution_

    def getSize(self, min_x, min_y, min_z, max_x, max_y, max_z):
        cell_size_x = (int)((max_x - min_x) / self.resolution_)
        cell_size_y = (int)((max_y - min_y) / self.resolution_)
        cell_size_z = (int)((max_z - min_z) / self.resolution_)
        return [cell_size_x, cell_size_y, cell_size_z]

    def mapToWorld(self, mx, my, mz):
        wx = self.origin_x_ + (mx + 0.5) * self.resolution_
        wy = self.origin_y_ + (my + 0.5) * self.resolution_
        wz = self.origin_z_ + (mz + 0.5) * self.resolution_
        return [wx, wy, wz]


    def worldToMap(self, wx, wy, wz):
        if (wx < self.origin_x_ or wy < self.origin_y_  or wz < self.origin_z_):
            return False

        mx = (int)((wx - self.origin_x_) / self.resolution_)
        my = (int)((wy - self.origin_y_) / self.resolution_)
        mz = (int)((wz - self.origin_z_) / self.resolution_)

        if (mx < self.size_x_ and my < self.size_y_ and mz < self.size_z_):
            return [mx, my, mz]
        else:
            return False

    def worldToMapNoBounds(self, wx, wy, wz):
        mx = (int)((wx - self.origin_x_) / self.resolution_)
        my = (int)((wy - self.origin_y_) / self.resolution_)
        mz = (int)((wz - self.origin_z_) / self.resolution_)
        return [mx, my, mz]

    def worldToMapEnforceBounds(self, wx, wy, wz):
        #   Here we avoid doing any math to wx,wy before comparing them to
        #   the bounds, so their values can go out to the max and min values
        #   of double floating point.
        if (wx < self.origin_x_):
            mx = 0
        elif (wx > self.resolution_ * self.size_x_ + self.origin_x_):
            mx = self.size_x_ - 1
        else:
            mx = (int)((wx - self.origin_x_) / self.resolution_)

        if (wy < self.origin_y_):
            my = 0
        elif (wy > self.resolution_ * self.size_y_ + self.origin_y_):
            my = self.size_y_ - 1
        else:
            my = (int)((wy - self.origin_y_) / self.resolution_)

        if (wz < self.origin_z_):
            mz = 0
        elif (wz > self.resolution_ * self.size_z_ + self.origin_z_):
            mz = self.size_z_ - 1
        else:
            mz = (int)((wz - self.origin_z_) / self.resolution_)
        return [mx, my, mz]
    

    def updateOrigin(self, new_origin_x, new_origin_y, new_origin_z):

        cell_ox = int((new_origin_x - self.origin_x_) / self.resolution_)
        cell_oy = int((new_origin_y - self.origin_y_) / self.resolution_)
        cell_oz = int((new_origin_z - self.origin_z_) / self.resolution_)

        new_grid_ox = self.origin_x_ + cell_ox * self.resolution_
        new_grid_oy = self.origin_y_ + cell_oy * self.resolution_
        new_grid_oz = self.origin_z_ + cell_oz * self.resolution_

        size_x = self.size_x_
        size_y = self.size_y_
        size_z = self.size_z_

        lower_left_x = min(max(cell_ox, 0), size_x)
        lower_left_y = min(max(cell_oy, 0), size_y)
        lower_left_z = min(max(cell_oz, 0), size_z)
        upper_right_x = min(max(cell_ox + size_x, 0), size_x)
        upper_right_y = min(max(cell_oy + size_y, 0), size_y)
        upper_right_z = min(max(cell_oz + size_z, 0), size_z)

        cell_size_x = upper_right_x - lower_left_x
        cell_size_y = upper_right_y - lower_left_y
        cell_size_z = upper_right_z - lower_left_z

        new_costmap = np.full((self.size_x_,self.size_y_,self.size_z_), self.default_value_, int)

        for i in range(cell_size_x):
            for j in range(cell_size_y):
                for k in range(cell_size_z):
                    tmp_x1 = lower_left_x - cell_ox + i
                    tmp_y1 = lower_left_y - cell_oy + j
                    tmp_z1 = lower_left_z - cell_oz + k
                    tmp_x2 = lower_left_x + i
                    tmp_y2 = lower_left_y + j
                    tmp_z2 = lower_left_z + k
                    new_costmap[tmp_x1, tmp_y1, tmp_z1] = self.costmap_[tmp_x2, tmp_y2, tmp_z2]

        self.costmap_ = new_costmap
        self.origin_x_ = new_grid_ox
        self.origin_y_ = new_grid_oy
        self.origin_z_ = new_grid_oz

    def updateSize(self, new_size_x, new_size_y, new_size_z):
        new_costmap = np.full((new_size_x, new_size_y, new_size_z), self.default_value_, int)

        cell_size_x = min(new_size_x, self.size_x_)
        cell_size_y = min(new_size_y, self.size_y_)
        cell_size_z = min(new_size_z, self.size_z_)

        for i in range(cell_size_x):
            for j in range(cell_size_y):
                for k in range(cell_size_z):
                    new_costmap[i,j,k] = self.costmap_[i,j,k]
            
        self.costmap_ = new_costmap
        self.size_x_ = new_size_x
        self.size_y_ = new_size_y
        self.size_z_ = new_size_z

    def resizeMap(self, minP, maxP):
        # max_cell_size = self.getSize(minP[0], minP[1], maxP[0], maxP[1])
        iMinP = self.worldToMapNoBounds(minP[0], minP[1], minP[2])
        iMaxP = self.worldToMapNoBounds(maxP[0], maxP[1], maxP[2])
        
        if iMinP[0] > 0 or iMinP[1] > 0 or iMinP[2] > 0 or iMaxP[0] < self.size_x_ - 1 or iMaxP[1] < self.size_y_ - 1 or iMaxP[2] < self.size_z_ - 1:
            print ("reszie map error")

        new_grid_ox = self.origin_x_ + iMinP[0] * self.resolution_
        new_grid_oy = self.origin_y_ + iMinP[1] * self.resolution_
        new_grid_oz = self.origin_z_ + iMinP[2] * self.resolution_

        new_size_x = iMaxP[0] - iMinP[0]
        new_size_y = iMaxP[1] - iMinP[1]
        new_size_z = iMaxP[2] - iMinP[2]

        self.updateSize(new_size_x,new_size_y,new_size_z)
        self.updateOrigin(new_grid_ox, new_grid_oy,new_grid_oz)
    
    def resizeMapCheckPoint(self,world_pose):
        map_pose = self.worldToMap(world_pose[0], world_pose[1], world_pose[2])
        if not map_pose:
            minP = self.mapToWorld(0,0,0)
            maxP = self.mapToWorld(self.size_x_ - 1, self.size_y_ - 1, self.size_z_ - 1)
            minP = self.min_pose(world_pose, minP)
            maxP = self.max_pose(world_pose, maxP)
            self.resizeMap(minP, maxP)
    
    def updateWeight(self, lo_max, lo_min):
        for i in range(self.size_x_):
            for j in range(self.size_y_):
                for k in range(self.size_z_):
                    if self.costmap_[i,j,k] > lo_max:
                        self.costmap_[i,j,k] = lo_max
                    if self.costmap_[i,j,k] < lo_min:
                        self.costmap_[i,j,k] = lo_min

    def min_pose(self, p1, p2):
        if p1[0] < p2[0]:
            p2[0] = p1[0]
        if p1[1] < p2[1]:
            p2[1] = p1[1]
        if p1[2] < p2[2]:
            p2[2] = p1[2]
        return p2
    
    def max_pose(self, p1, p2):
        if p1[0] > p2[0]:
            p2[0] = p1[0]
        if p1[1] > p2[1]:
            p2[1] = p1[1]
        if p1[2] > p2[2]:
            p2[2] = p1[2]
        return p2

    def drawMap(self):
        lx = self.size_x_
        ly = self.size_y_
        lz = self.size_z_

        x = np.array([])
        y = np.array([])
        z = np.array([])

        for i in range(self.size_x_):
            for j in range(self.size_y_):
                for k in range(self.size_z_):
                    if self.costmap_[i,j,k] < -5:
                        x = np.append(x,i)
                        y = np.append(y,j)
                        z = np.append(z,k)

        ax = plt.subplot(111, projection='3d')
        ax.scatter(x, y, z, c='b')
        plt.savefig('map_image.png')
        #plt.show()

