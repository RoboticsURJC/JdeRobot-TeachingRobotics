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
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
######################################################################

# Author: Ioan Sucan, Mark Moll


from ompl import util as ou
from ompl import base as ob
from ompl import geometric as og
from os.path import abspath, dirname, join
import sys
from functools import partial

class Plane2DEnvironment:
    def __init__(self, ppm_file):
        self.ppm_ = ou.PPM()
        self.ppm_.loadFile(ppm_file)
        self.space = ob.RealVectorStateSpace()
        self.space.addDimension(0.0, self.ppm_.getWidth())
        self.space.addDimension(0.0, self.ppm_.getHeight())
        self.maxWidth_ = self.ppm_.getWidth() - 1
        self.maxHeight_ = self.ppm_.getHeight() - 1

        self.si = ob.SpaceInformation(self.space)

        # set state validity checking for this space
        self.si.setStateValidityChecker(ob.StateValidityCheckerFn(
            partial(Plane2DEnvironment.isStateValid, self)))
        self.si.setup()
        self.si.setStateValidityCheckingResolution(1.0 / self.space.getMaximumExtent())
        #self.ss_.setPlanner(og.RRTConnect(self.ss_.getSpaceInformation()))

    def plan(self, start_row, start_col, goal_row, goal_col,plannerType,runtime):
        if not self.si:
            return False
        start = ob.State(self.space)
        start()[0] = start_row
        start()[1] = start_col
        goal = ob.State(self.space)
        goal()[0] = goal_row
        goal()[1] = goal_col
        # Create a problem instance

        self.pdef = ob.ProblemDefinition(self.si)
        # Set the start and goal states
        self.pdef.setStartAndGoalStates(start, goal)

        self.planner = self.allocatePlanner(self.si, plannerType)
        self.planner.setProblemDefinition(self.pdef)
        # perform setup steps for the planner
        self.planner.setup()
        # print the settings for this space
        print(self.si.settings())
        # generate a few solutions; all will be added to the goal
        for i in range(5):
            self.solved = self.planner.solve(runtime)
            p = self.pdef.getSolutionPath()
            print("Found solution:\n%s" % p)
        ns = self.planner.getProblemDefinition().getSolutionCount()
        print("Found %d solutions" % ns)

        if self.solved:
            # get the goal representation from the problem definition (not the same as the goal state)
            # and inquire about the found path
            path = self.pdef.getSolutionPath()
            print("Found solution:\n%s" % path)
            return True
        else:
            print("No solution found")
            return False

        
    def allocatePlanner(self,si,plannerType):
        if plannerType.lower() == "bitstar":
            return og.BITstar(si)
        elif plannerType.lower() == "fmtstar":
            return og.FMT(si)
        elif plannerType.lower() == "informedrrtstar":
            return og.InformedRRTstar(si)
        elif plannerType.lower() == "prmstar":
            return og.PRMstar(si)
        elif plannerType.lower() == "rrtstar":
            return og.RRTstar(si)
        elif plannerType.lower() == "sorrtstar":
            return og.SORRTstar(si)
        else:
            OMPL_ERROR("Planner-type is not implemented in allocation function.");


    def recordSolution(self):
        if not self.si:
            return
        p = self.pdef.getSolutionPath()
        print("Found solution:\n%s" % p)
        p.interpolate()
        for i in range(p.getStateCount()):
            w = min(self.maxWidth_, int(p.getState(i)[0]))
            h = min(self.maxHeight_, int(p.getState(i)[1]))
            c = self.ppm_.getPixel(h, w)
            c.red = 255
            c.green = 0
            c.blue = 0

    def getPath(self):
        # if not self.si:
        #     return
        p = self.pdef.getSolutionPath()
        p.interpolate()
        pathlist = [[] for i in range(2)]
        for i in range(p.getStateCount()):
            w = min(self.maxWidth_, int(p.getState(i)[0]))
            h = min(self.maxHeight_, int(p.getState(i)[1]))
            pathlist[0].append(w)
            pathlist[1].append(h)
        return pathlist

    def save(self, filename):
        if not self.si:
            return
        self.ppm_.saveFile(filename)

    def isStateValid(self, state):
        w = min(int(state[0]), self.maxWidth_)
        h = min(int(state[1]), self.maxHeight_)

        c = self.ppm_.getPixel(h, w)
        return c.red > 127 and c.green > 127 and c.blue > 127

