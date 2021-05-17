#!/usr/bin/env python

######################################################################
# Software License Agreement (BSD License)
#
#  Copyright (c) 2010, Rice University
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#   * Neither the name of the Rice University nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
######################################################################

# Author: Mark Moll

from math import sin, cos
from functools import partial

from ompl import util as ou
from ompl import base as ob
from ompl import control as oc
from ompl import geometric as og

from os.path import abspath, dirname, join
import numpy as np
import math

import matplotlib.pyplot as plt
## @cond IGNORE
# a decomposition is only needed for SyclopRRT and SyclopEST
class RigidBodyPlanningWithControls:
    def __init__(self, costMap, dimension, start, start_yaw, goal, goal_yaw, plannerType):
        self.costMap = costMap
        self.start_x = start[0]
        self.start_y = start[1]
        self.start_yaw = start_yaw
        self.goal_x = goal[0]
        self.goal_y = goal[1]
        self.goal_yaw = goal_yaw
        self.plannerType = plannerType
        self.simpleSetupControl()
    
    def propagate(self, start, control, duration, state):
        state.setX( start.getX() + control[0] * duration * math.cos(start.getYaw()) )
        state.setY( start.getY() + control[0] * duration * math.sin(start.getYaw()) )
        state.setYaw(start.getYaw() + control[1] * duration)

    def isStateValid(self, spaceInformation, state):
        # perform collision checking or check if other constraints are
        # satisfied
        wx = state.getX()
        wy = state.getY()
        if not self.costMap:
            tmp = True
            if wy < -4 and wy > 5:
                tmp = False
            elif wy < -0.5:
                if wx > 12 or wx < 5.5:
                    tmp = False 
        else:
            mPoint = self.costMap.worldToMap(wx, wy)
            cost = self.costMap.getCost(mPoint[0],mPoint[1])
            if cost < -5:
                tmp = False
            else:
                tmp = True
        return spaceInformation.satisfiesBounds(state) and tmp
    
    def simpleSetupControl(self):
        self.setSpace()
        self.setProblem()
        self.setPlanner()

    def setSpace(self):
        # construct the state space we are planning in
        self.space = ob.SE2StateSpace()
        # set the bounds for the R^2 part of SE(2)
        self.bounds = ob.RealVectorBounds(2)
        if not self.costMap:
            self.bounds.setLow(-8)
            self.bounds.setHigh(20)
        else:
            ox = self.costMap.getOriginX()
            oy = self.costMap.getOriginY()
            size_x = self.costMap.getSizeInMetersX()
            size_y = self.costMap.getSizeInMetersY()
            low = min(ox, oy)
            high = max(ox+size_x, oy+size_y)
            print ("low",low)
            print ("high",high)
            #self.bounds.setLow(low)
            #self.bounds.setHigh(high)
            self.bounds.setLow(0,ox)
            self.bounds.setHigh(0,ox+size_x)
            self.bounds.setLow(1,oy)
            self.bounds.setHigh(1,oy+size_y)

        self.space.setBounds(self.bounds)

        # create a control space
        self.cspace = oc.RealVectorControlSpace(self.space, 2)
        # set the bounds for the control space
        cbounds = ob.RealVectorBounds(2)
        cbounds.setLow(0,-1.5)
        cbounds.setHigh(0,1.5)
        cbounds.setLow(1,-3)
        cbounds.setHigh(1,3)
        self.cspace.setBounds(cbounds)

        # define a simple setup class
        self.ss = oc.SimpleSetup(self.cspace)
        self.ss.setStateValidityChecker(ob.StateValidityCheckerFn(partial(self.isStateValid, self.ss.getSpaceInformation())))
        self.ss.setStatePropagator(oc.StatePropagatorFn(self.propagate))
    
    def setProblem(self):
        # create a start state
        start = ob.State(self.space)
        start().setX(self.start_x)
        start().setY(self.start_y)
        start().setYaw(self.start_yaw)
        # create a goal state
        goal = ob.State(self.space)
        goal().setX(self.goal_x)
        goal().setY(self.goal_y)
        goal().setYaw(self.goal_yaw)

        # set the start and goal states
        self.ss.setStartAndGoalStates(start, goal, 0.05)
    
    def setPlanner(self):
        # (optionally) set planner
        self.si = self.ss.getSpaceInformation()

        if self.plannerType.lower() == "rrt":
            planner = oc.RRT(self.si)
        elif self.plannerType.lower() == "est":
            planner = oc.EST(self.si)
        elif self.plannerType.lower() == "kpiece1":
            planner = oc.KPIECE1(self.si)
        elif self.plannerType.lower() == "syclopest":
            # SyclopEST and SyclopRRT require a decomposition to guide the search
            decomp = MyDecomposition(32, self.bounds)
            planner = oc.SyclopEST(self.si, decomp)
        elif self.plannerType.lower() == "sycloprrt":
            # SyclopEST and SyclopRRT require a decomposition to guide the search
            decomp = MyDecomposition(32, self.bounds)
            planner = oc.SyclopRRT(self.si, decomp)
        else:
            OMPL_ERROR("Planner-type is not implemented in ompl control function.")
            decomp = MyDecomposition(32, self.bounds)
            planner = oc.SyclopEST(self.si, decomp)

        self.ss.setPlanner(planner)
        # (optionally) set propagation step size
        self.si.setPropagationStepSize(.05)

    def solve(self, runtime=None):
        if not runtime:
            runtime = 10
        # attempt to solve the problem
        solved = self.ss.solve(runtime)

        if solved:
            # print the path to screen
            p = self.ss.getSolutionPath()
            print("Found solution:\n%s" % self.ss.getSolutionPath().printAsMatrix())
            #p.interpolate()
            pathlist = [[] for i in range(6)]
            #print p.getControlCount() 
            for i in range(p.getControlCount()):
                x = p.getState(i+1).getX()
                y = p.getState(i+1).getY()
                yaw = p.getState(i+1).getYaw()
                pathlist[0].append(x)
                pathlist[1].append(y)
                pathlist[2].append(yaw)
                # print ('x = %f, y = %f, yaw = %f ' %(x,y,yaw))
                v = p.getControl(i)[0]
                w = p.getControl(i)[1]
                t = p.getControlDuration(i)
                pathlist[3].append(v)
                pathlist[4].append(w)
                pathlist[5].append(t)
                # print ('v = %f, w = %f, t = %f ' %(v,w,x))
            return pathlist
        else:
            print ("can't find path")
            return False
    
    def updateMap(self, costMap):
        self.costMap = costMap

    def updatePose(self,start_x, start_y, start_yaw, goal_x, goal_y, goal_yaw):
        self.start_x = start_x
        self.start_y = start_y
        self.start_yaw = start_yaw
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.goal_yaw = goal_yaw
    
    def updatePlannerType(self, plannerType):
        self.plannerType = plannerType

class MyDecomposition(oc.GridDecomposition):
    def __init__(self, length, bounds):
        super(MyDecomposition, self).__init__(length, 2, bounds)
    def project(self, s, coord):
        coord[0] = s.getX()
        coord[1] = s.getY()
    def sampleFullState(self, sampler, coord, s):
        sampler.sampleUniform(s)
        s.setXY(coord[0], coord[1])
## @endcond


if __name__ == "__main__":
    
    
    planner = RigidBodyPlanningWithControls(None, 6,3,0,7.25,-3,0, 'syclopest')

    pathlist = planner.solve()
    print pathlist
    plt.figure(1)
    plt.plot(pathlist[0], pathlist[1])
    num = len(pathlist[0])
    for i in range(num):
        x1 = pathlist[0][i]
        y1 = pathlist[1][i]
        yaw = pathlist[2][i]
        x2 = x1 + 0.5*cos(yaw)
        y2 = y1 + 0.5*sin(yaw)
        plt.plot([x1,x2],[y1,y2])
    plt.show()