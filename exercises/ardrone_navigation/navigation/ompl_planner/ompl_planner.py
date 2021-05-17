#!/usr/bin/env python
from ompl import util as ou
from ompl import base as ob
from ompl import control as oc
from ompl import geometric as og
from os.path import abspath, dirname, join
import sys
from functools import partial

import numpy as np
from math import sin, cos, tan
import matplotlib.pyplot as plt

from RigidBodyPlanning import RigidBodyPlanning
from RigidBodyPlanningWithControls import RigidBodyPlanningWithControls
from RigidBodyPlanningWithODESolverAndControls import RigidBodyPlanningWithODESolverAndControls


class ompl_planner:
    def __init__(self, costMap, dimension, start, start_yaw, goal, goal_yaw, plannerType, control = True, ODESolver = False):
        self.costMap = costMap
        self.dimension = dimension

        self.start = start
        self.start_yaw = start_yaw
        self.goal = goal
        self.goal_yaw = goal_yaw

        self.plannerType = plannerType
        self.control = control
        self.ODESolver = ODESolver
    
    def setMap(self, costMap):
        self.costMap = costMap

    def setPose(self,start, start_yaw, goal, goal_yaw):
        self.start = start
        self.start_yaw = start_yaw
        self.goal = goal
        self.goal_yaw = goal_yaw

    def setPlannerType(self, plannerType):
        self.plannerType = plannerType
    
    def setControl(self, control):
        self.control = control

    def setODESolver(self, ODESolver):
        self.ODESolver = ODESolver
    
    def omplRunOnce(self, runtime=None):
        if self.dimension == 3:
            planner = RigidBodyPlanning(self.costMap,self.dimension, self.start, self.start_yaw, self.goal, self.goal_yaw, self.plannerType)
        elif self.dimension == 2:
            if self.control :
                if self.ODESolver:
                    planner = RigidBodyPlanningWithODESolverAndControls(self.costMap, self.dimension, self.start, self.start_yaw, self.goal, self.goal_yaw, self.plannerType)
                else:
                    planner = RigidBodyPlanningWithControls(self.costMap, self.dimension, self.start, self.start_yaw, self.goal, self.goal_yaw, self.plannerType)
            else:
                planner = RigidBodyPlanning(self.costMap,self.dimension, self.start, self.start_yaw, self.goal, self.goal_yaw, self.plannerType)
            #costMap, dimension, start, start_yaw, goal, goal_yaw, plannerType
        if not runtime:
            pathlist = planner.solve()
        else:
            pathlist = planner.solve(runtime)
        
        return pathlist
        