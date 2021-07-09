import logging
import time
import threading
import multiprocessing
import sys
from datetime import datetime
import re
import json
import traceback
import imp

import rospy
from std_srvs.srv import Empty
import cv2

from user_functions import GUIFunctions, HALFunctions
from console import start_console, close_console

from shared.value import SharedValue

# The brain process class
class BrainProcess(multiprocessing.Process):
    def __init__(self, code, exit_signal):
        super(BrainProcess, self).__init__()

        # Initialize exit signal
        self.exit_signal = exit_signal

        # Function definitions for users to use
        self.hal = HALFunctions()
        self.gui = GUIFunctions()

        # Time variables
        self.time_cycle = SharedValue('brain_time_cycle')
        self.ideal_cycle = SharedValue('brain_ideal_cycle')
        self.iteration_counter = 0

        # Get the sequential and iterative code
        # Something wrong over here! The code is reversing
        # Found a solution but could not find the reason for this
        self.sequential_code = code[1]
        self.iterative_code = code[0]

    # Function to run to start the process
    def run(self):
        # Two threads for running and measuring
        self.measure_thread = threading.Thread(target=self.measure_frequency)
        self.thread = threading.Thread(target=self.process_code)

        self.measure_thread.start()
        self.thread.start()

        print("Brain Process Started!")

        self.exit_signal.wait()

    # The process function
    def process_code(self):
        # Redirect information to console
        start_console()

        # Reference Environment for the exec() function
        iterative_code, sequential_code = self.iterative_code, self.sequential_code
        
        # print(sequential_code)
        # print(iterative_code)
        
        # Whatever the code is, first step is to just stop!
        self.hal.sendV(0)
        self.hal.sendW(0)


        # The Python exec function
        # Run the sequential part
        gui_module, hal_module = self.generate_modules()
        if sequential_code != "":
            reference_environment = {"GUI": gui_module, "HAL": hal_module}
            exec(sequential_code, reference_environment)

        # Run the iterative part inside template
        # and keep the check for flag
        while not self.exit_signal.is_set():
            start_time = datetime.now()
            
            # Execute the iterative portion
            if iterative_code != "":
                exec(iterative_code, reference_environment)

            # Template specifics to run!
            finish_time = datetime.now()
            dt = finish_time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            
            # Keep updating the iteration counter
            if(iterative_code == ""):
                self.iteration_counter = 0
            else:
                self.iteration_counter = self.iteration_counter + 1
        
            # The code should be run for atleast the target time step
            # If it's less put to sleep
            # If it's more no problem as such, but we can change it!
            time_cycle = self.time_cycle.get()

            if(ms < time_cycle):
                time.sleep((time_cycle - ms) / 1000.0)

        close_console()
        print("Current Thread Joined!")


    # Function to generate the modules for use in ACE Editor
    def generate_modules(self):
        # Define HAL module
        hal_module = imp.new_module("HAL")
        hal_module.HAL = imp.new_module("HAL")
        hal_module.HAL.motors = imp.new_module("motors")

        # Add HAL functions
        hal_module.HAL.getImage = self.hal.getImage
        hal_module.HAL.motors.sendV = self.hal.sendV
        hal_module.HAL.motors.sendW = self.hal.sendW

        # Define GUI module
        gui_module = imp.new_module("GUI")
        gui_module.GUI = imp.new_module("GUI")

        # Add GUI functions
        gui_module.GUI.showImage = self.gui.showImage

        # Adding modules to system
        # Protip: The names should be different from
        # other modules, otherwise some errors
        sys.modules["HAL"] = hal_module
        sys.modules["GUI"] = gui_module

        return gui_module, hal_module
            
    # Function to measure the frequency of iterations
    def measure_frequency(self):
        previous_time = datetime.now()
        # An infinite loop
        while not self.exit_signal.is_set():
            # Sleep for 2 seconds
            time.sleep(2)
            
            # Measure the current time and subtract from the previous time to get real time interval
            current_time = datetime.now()
            dt = current_time - previous_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            previous_time = current_time
            
            # Get the time period
            try:
            	# Division by zero
            	self.ideal_cycle.add(ms / self.iteration_counter)
            except:
            	self.ideal_cycle.add(0)
            
            # Reset the counter
            self.iteration_counter = 0