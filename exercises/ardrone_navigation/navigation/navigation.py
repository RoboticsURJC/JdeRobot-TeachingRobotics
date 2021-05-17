
from ompl_planner.ompl_planner import ompl_planner
from control.noHolomonicControl import noHolomonicControl
from control.ardroneControl import ardroneControl
from path_processing.smoothPath import smooth
from map.occGridMap import occGridMap,costmap_2d,costmap_3d

import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from math import cos,sin,tan,pow,pi,sqrt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class navigation:
    def __init__(self, files, origin, resolution, dimension = 2):
        
        self.smooth = smooth()
        #self.occGridMap = occGridMap()

        self.dimension = dimension
        origin_x = origin[0]
        origin_y = origin[1]
        if dimension == 3:
            origin_z = origin[2]

        if dimension == 2:
            self.control = noHolomonicControl()
            if files:
                self.have_map = True
                self.init_img = cv2.imread(files)
                size = self.init_img.shape
                self.gridMap = costmap_2d(size[0],size[1],resolution, origin_x, origin_y)
                for i in range(size[0]):
                    for j in range(size[1]):
                        data = (np.sum(self.init_img[i,j]))/3
                        self.gridMap.setCost(i,j,data)
            else:
                self.have_map = False
                self.gridMap = costmap_2d(100,100,resolution, origin_x, origin_y)


        elif dimension == 3:
            self.control = ardroneControl()
            self.have_map = False
            self.gridMap = costmap_3d(100, 100, 50, 0.2, origin_x = -10, origin_y = -10, origin_z = 0)
            #cells_size_x, cells_size_y, cells_sise_z, resolution, origin_x = 0, origin_y = 0,origin_z = 0, default_value = 0
        
        self.getTarget = False

    def update_map_autopark(self,car_pose,target_pose):
        #car [6,3]
        #target [8,5]
        p1 = self.move_pose(car_pose,[12,-3])
        p2 = self.move_pose(car_pose,[-12,-3])
        p3 = self.move_pose(car_pose,[12,3])
        p4 = self.move_pose(car_pose,[-12,3])
        p5 = self.move_pose(target_pose,[4,2.5])
        p6 = self.move_pose(target_pose,[-4,2.5])

        self.gridMap.resizeMapCheckPoint(p1)
        self.gridMap.resizeMapCheckPoint(p2)
        self.gridMap.resizeMapCheckPoint(p3)
        self.gridMap.resizeMapCheckPoint(p4)
        self.gridMap.resizeMapCheckPoint(p5)
        self.gridMap.resizeMapCheckPoint(p6)

        m_p1 = self.gridMap.worldToMapEnforceBounds(p1[0],p1[1])
        m_p2 = self.gridMap.worldToMapEnforceBounds(p2[0],p2[1])
        m_p3 = self.gridMap.worldToMapEnforceBounds(p3[0],p3[1])
        m_p4 = self.gridMap.worldToMapEnforceBounds(p4[0],p4[1])
        m_p5 = self.gridMap.worldToMapEnforceBounds(p5[0],p5[1])
        m_p6 = self.gridMap.worldToMapEnforceBounds(p6[0],p6[1])

        print ("getSizeInCellsX",self.gridMap.getSizeInCellsX())
        print ("getSizeInCellsY",self.gridMap.getSizeInCellsY())
        print ("getOriginX",self.gridMap.getOriginX())
        print ("getOriginY",self.gridMap.getOriginY())
        print ("p1",p1,m_p1)
        print ("p2",p2,m_p2)
        print ("p3",p3,m_p3)
        print ("p4",p4,m_p4)
        print ("p5",p5,m_p5)
        print ("p6",p6,m_p6)
        h = self.gridMap.size_x_
        w = self.gridMap.size_y_
        for i in range(h):
            for j in range(w):
                self.gridMap.setCost(i,j,-10)

        if m_p1[1] == m_p2[1]:
            #scene like autopark.world
            print ("update map")
            num_x_1 = m_p1[0] - m_p2[0]
            num_y_1 = m_p1[1] - m_p3[1]
            for i in range(num_x_1):
                for j in range(num_y_1):
                    self.gridMap.setCost(i+m_p4[0],j+m_p4[1],15)
            num_x_2 = m_p5[0] - m_p6[0]
            num_y_2 = m_p3[1] - m_p5[1]
            for i in range(num_x_2):
                for j in range(num_y_2):
                    self.gridMap.setCost(i+m_p6[0],j+m_p6[1],15)
            self.gridMap.drawMap()

    def move_pose(self,pose,move):
        assert len(pose) == 3
        assert len(move) == 2
        dx = move[1]*sin(pose[2]) + move[0]*cos(pose[2])
        dy = -move[1]*cos(pose[2]) + move[0]*sin(pose[2])
        x = pose[0] + dx
        y = pose[1] + dy
        return [x,y]

    def path_planning_2d(self,current_pose,goal_pose):
        startX = current_pose[0]
        startY = current_pose[1]
        startYaw = current_pose[2]
        goalX = goal_pose[0]
        goalY = goal_pose[1]
        goalYaw = goal_pose[2]
        print ("pose",startX, startY, startYaw, goalX, goalY, goalYaw)

        start_pose_map = self.gridMap.worldToMap(startX,startY)
        goal_pose_map = self.gridMap.worldToMap(goalX, goalY)

        ompl_control = True
        ompl_sol = ompl_planner(self.gridMap, startX, startY, startYaw, goalX, goalY, goalYaw, "rrt", ompl_control, False)
        path_list = ompl_sol.omplRunOnce(50)
        #print self.pathlist
        if path_list :
            if ompl_control:
                path_list = self.path_smooth(path_list,current_pose)

                self.control.setPath(path_list)
                return True
            else:
                self.control.setControlYaw(False)
                self.control.setPath(path_list)
                return True
        else:
            return False
    
    def path_smooth_2d(self,path_list,current_pose):
        plt.figure(1)
        plt.plot(path_list[0], path_list[1])
        num = len(path_list[0])
        for i in range(num):
            x1 = path_list[0][i]
            y1 = path_list[1][i]
            yaw = path_list[2][i]
            x2 = x1 + math.cos(yaw)
            y2 = y1 + math.sin(yaw)
            plt.plot([x1,x2],[y1,y2])
        plt.savefig("figure1.jpg") 
        self.smooth.setPath(path_list)
        path_list = self.smooth.Floyd(path_list)
        path_list = self.smooth.checkYaw(path_list, current_pose)

        plt.figure(2)
        plt.plot(path_list[0], path_list[1])

        num = len(path_list[0])
        for i in range(num):
            x1 = path_list[0][i]
            y1 = path_list[1][i]
            yaw = path_list[2][i]
            x2 = x1 + math.cos(yaw)
            y2 = y1 + math.sin(yaw)
            plt.plot([x1,x2],[y1,y2])
        plt.savefig("figure2.jpg")

        return path_list

    def path_following_2d(self, current_pose):
        if self.getTarget:
            print "get Target"
            print self.control.getPath()
            return [0,0]
            
        Pose = [0,0,0]
        Pose[0] = current_pose[0]
        Pose[1] = current_pose[1]
        Pose[2] = current_pose[2]

        data = self.control.control(Pose,2)
        self.getTarget = self.control.isGetTarget()
        return data

    def path_check(self,path_smooth, costmap):
        print ('todo')

    def update_map_laser_2d(self, laser, id, pose):
        self.occGridMap.registerScan(pose,id,laser)
        self.occGridMap.drawMap()

    def update_map_3d(self):
        lx = self.gridMap.size_x_
        ly = self.gridMap.size_y_
        lz = self.gridMap.size_z_
        for i in range(lx):
            for j in range(ly):
                for k in range(lz):
                    self.gridMap.setCost(i,j,k,15)

        pillar_box = [0.2, 0.2, 4.0]
        pillar_swell = [1, 1, 0]

        floor_box = [5,5,0.2]
        floor_swell = [1,1,1]

        wall1_box = [5,0.2,5]
        wall2_box = [0.2,5,5]
        wall_swell = [1,1,0]

        # pillar_pose = []
        # floor_pose = []
        # wall1_pose = []
        # wall2_pose = []
        
        for i in range(5):
            for j in range(5):
                x = i*5-10
                y = j*5-10
                z = 2
                #pillar_pose.append([x,y,z])
                self.add_box_map(pillar_box,[x,y,z],pillar_swell)
        
        for i in range(4):
            for j in range(4):
                x = i*5-7.5
                y = j*5-7.5
                z = 4
                if (x==2.5 and y==2.5) or (x==-7.5 and y==-2.5):
                    print ('no floor')
                else:
                    #floor_pose.append([x,y,z])
                    self.add_box_map(floor_box,[x,y,z],floor_swell)
        
        for i in range(4):
            for j in range(2):
                x = i*5-7.5
                y = j*20-10
                z = 6.5
                self.add_box_map(wall1_box,[x,y,z],wall_swell)

        for i in range(4):
            for j in range(2):
                y = i*5-7.5
                x = j*20-10
                z = 6.5
                self.add_box_map(wall2_box,[x,y,z],wall_swell)

        wall1_pose = [[7.5,5,6.5],[-7.5,0,6.5]]
        wall2_pose = [[5,2.5,6.5],[5,-2.5,6.5],[0,7.5,6.5],[0,2.5,6.5],[0,-2.5,6.5],[-5,-7.5,6.5]]

        l1 = len(wall1_pose)
        l2 = len(wall2_pose)
        for i in range(l1):
            self.add_box_map(wall1_box,wall1_pose[i],wall_swell)
        for i in range(l2):
            self.add_box_map(wall2_box,wall2_pose[i],wall_swell)

        self.gridMap.drawMap()
    
    def add_box_map(self, box, pose, swell):
        box_sum = []
        for i,j in zip(box, swell):
            summ = i+j
            box_sum.append(summ)
        
        start = []
        for i,j in zip(box_sum, pose):
            tmp = j - i/2
            start.append(tmp)
        
        cell_size = self.gridMap.getSize(0,0,0,box_sum[0],box_sum[1],box_sum[2])
        cell_start = self.gridMap.worldToMapEnforceBounds(start[0],start[1],start[2])

        for i in range(cell_size[0]):
            for j in range(cell_size[1]):
                for k in range(cell_size[2]):
                    self.gridMap.setCost(i+cell_start[0], j+cell_start[1], k+cell_start[2], -10)


    def path_planning_3d(self,current_pose,goal_pose):
        startX = current_pose[0]
        startY = current_pose[1]
        startZ = current_pose[2]
        goalX = goal_pose[0]
        goalY = goal_pose[1]
        goalZ = goal_pose[2]
        print ("pose",startX, startY, startZ, goalX, goalY, goalZ)
        #bitstar rrtstar fmtstar
        ompl_sol = ompl_planner(self.gridMap, 3, current_pose, 0,  goal_pose,  0, "fmtstar", False, False)
        path_list = ompl_sol.omplRunOnce(10)
        #print path_list
        if path_list :
            self.control.restart()
            self.control.setPath(path_list)
            tmpmap = self.gridMap.getMap()
            lx = self.gridMap.size_x_
            ly = self.gridMap.size_y_
            lz = self.gridMap.size_z_

            x = []
            y = []
            z = []
            d = 0
            for i in range(lx):
                for j in range(ly):
                    for k in range(lz):
                        if tmpmap[i,j,k] < -5:
                            tmp = self.gridMap.mapToWorld(i,j,k)
                            d = d+1
                            if ( d ==10  ):
                                x.append(tmp[0])
                                y.append(tmp[1])
                                z.append(tmp[2])
                                d = 0
                            
            x2 = path_list[0]
            y2 = path_list[1]
            z2 = path_list[2]
            ax = plt.subplot(111, projection='3d')
            ax.scatter(x, y, z, c='b')
            ax.scatter(x2, y2, z2, c='r')
            plt.show()
            return True
        else:
            return False

    def path_following_3d(self, current_pose):
        if self.getTarget:
            print "get Target"
            print self.control.getPath()

        data = self.control.control(current_pose)
        self.getTarget = self.control.isGetTarget()
        return [self.getTarget,data]
