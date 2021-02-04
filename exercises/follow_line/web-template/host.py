#!/usr/bin/env python

from __future__ import print_function

from websocket_server import WebsocketServer
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

from gui import GUI, ThreadGUI
from hal import HAL
import console

class Template:
    # Initialize class variables
    # self.time_cycle to run an execution for atleast 1 second
    # self.process for the current running process
    def __init__(self):
        self.brain_process = None
        self.frequency_message = {'brain': '', 'gui': ''}
                
        # Shared variables
        self.time_cycle = multiprocessing.Value('d', 80)
        self.ideal_cycle = multiprocessing.Value('d', 80)
        self.reload = multiprocessing.Value('i', 0)
        
        self.server = None
        self.client = None
        self.host = sys.argv[1]

        # Initialize the GUI, HAL and Console behind the scenes
        self.console = console.Console()
        self.hal = HAL()
        self.gui = GUI(self.host, self.console, self.hal)

    # Function to generate and send frequency messages
    def send_frequency_message(self):
        # This function generates and sends frequency measures of the brain and gui
        brain_frequency = 0; gui_frequency = 0
        
        with self.ideal_cycle.get_lock():
            try:
                brain_frequency = round(1000 / self.ideal_cycle.value, 1)
            except ZeroDivisionError:
                brain_frequency = 0

        try:
            gui_frequency = round(1000 / self.thread_gui.ideal_cycle, 1)
        except ZeroDivisionError:
            gui_frequency = 0

        self.frequency_message["brain"] = brain_frequency
        self.frequency_message["gui"] = gui_frequency

        message = "#freq" + json.dumps(self.frequency_message)
        self.server.send_message(self.client, message)
    
    # Function to maintain thread execution
    def execute_process(self, source_code):
        with self.reload.get_lock():
            self.reload.value = 1
        # Keep checking until the thread is alive
        # The thread will die when the coming iteration reads the flag
        if(self.brain_process != None):
            self.brain_process.terminate()
            self.brain_process.join()

        # Turn the flag down, the iteration has successfully stopped!
        with self.reload.get_lock():
            self.reload.value = 0
        # New process execution
        self.brain_process = BrainProcess(source_code, self.gui, self.hal, self.console,
                                          self.reload, self.time_cycle, self.ideal_cycle)
        self.brain_process.start()
        print("New Process Started!")

    # Function to read and set frequency from incoming message
    def read_frequency_message(self, message):
        frequency_message = json.loads(message)

        # Set brain frequency
        frequency = float(frequency_message["brain"])
        with self.time_cycle.get_lock():
            self.time_cycle.value = 1000.0 / frequency

        # Set gui frequency
        frequency = float(frequency_message["gui"])
        self.thread_gui.time_cycle = 1000.0 / frequency

        return

    # The websocket function
    # Gets called when there is an incoming message from the client
    def handle(self, client, server, message):
        if(message[:5] == "#freq"):
            frequency_message = message[5:]
            self.read_frequency_message(frequency_message)
            self.send_frequency_message()
            return
        
        try:
            # Once received turn the reload flag up and send it to execute_thread function
            code = message
            self.execute_process(code)
        except:
            pass

    # Function that gets called when the server is connected
    def connected(self, client, server):
    	self.client = client
    	# Start the GUI update thread
    	self.thread_gui = ThreadGUI(self.gui)
    	self.thread_gui.start()

        # Initialize the ping message
        self.send_frequency_message()
    	
    	print(client, 'connected')
    	
    # Function that gets called when the connected closes
    def handle_close(self, client, server):
    	print(client, 'closed')
    	
    def run_server(self):
    	self.server = WebsocketServer(port=1905, host=self.host)
    	self.server.set_fn_new_client(self.connected)
    	self.server.set_fn_client_left(self.handle_close)
    	self.server.set_fn_message_received(self.handle)
    	self.server.run_forever()
    

class BrainProcess(multiprocessing.Process):
    def __init__(self, code, gui, hal, console, reload, time_cycle, ideal_cycle, **kwargs):
        self.thread = None
        self.source_code = code

        self.gui = gui
        self.hal = hal
        self.console = console

        self.reload = reload
        self.time_cycle = time_cycle
        self.ideal_cycle = ideal_cycle
        self.iteration_counter = 0

        multiprocessing.Process.__init__(self)

    def start(self):
        self.measure_thread = threading.Thread(target=self.measure_frequency)
        self.thread = threading.Thread(target=self.process_code, args=[self.source_code, ])

        self.thread.start()
        self.measure_thread.start()

    # Function to parse the code
    # A few assumptions: 
    # 1. The user always passes sequential and iterative codes
    # 2. Only a single infinite loop
    def parse_code(self, source_code):
        if(source_code[:5] == "#resu"):
                restart_simulation = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
                restart_simulation()

                return "", "", 1

        elif(source_code[:5] == "#paus"):
                pause_simulation = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
                pause_simulation()

                return "", "", 1
    		
    	elif(source_code[:5] == "#rest"):
    		reset_simulation = rospy.ServiceProxy('/gazebo/reset_world', Empty)
    		reset_simulation()
    		self.gui.reset_gui()
    		return "", "", 1
    		
    	else:
    		# Get the frequency of operation, convert to time_cycle and strip
    		try:
        		# Get the debug level and strip the debug part
        		debug_level = int(source_code[5])
        		source_code = source_code[12:]
        	except:
        		debug_level = 1
        		source_code = ""
    		
    		source_code = self.debug_parse(source_code, debug_level)
    		# Pause and unpause
    		if(source_code == ""):
    		    self.gui.lap.pause()
    		else:
    		    self.gui.lap.unpause()
    		sequential_code, iterative_code = self.seperate_seq_iter(source_code)
    		return iterative_code, sequential_code, debug_level
			
        
    # Function to parse code according to the debugging level
    def debug_parse(self, source_code, debug_level):
    	if(debug_level == 1):
    		# If debug level is 0, then all the GUI operations should not be called
    		source_code = re.sub(r'GUI\..*', '', source_code)
    		
    	return source_code
    
    # Function to seperate the iterative and sequential code
    def seperate_seq_iter(self, source_code):
    	if source_code == "":
            return "", ""

        # Search for an instance of while True
        infinite_loop = re.search(r'[^ \t]while\(True\):|[^ \t]while True:', source_code)

        # Seperate the content inside while True and the other
        # (Seperating the sequential and iterative part!)
        try:
            start_index = infinite_loop.start()
            iterative_code = source_code[start_index:]
            sequential_code = source_code[:start_index]

            # Remove while True: syntax from the code
            # And remove the the 4 spaces indentation before each command
            iterative_code = re.sub(r'[^ ]while\(True\):|[^ ]while True:', '', iterative_code)
            iterative_code = re.sub(r'^[ ]{4}', '', iterative_code, flags=re.M)

        except:
            sequential_code = source_code
            iterative_code = ""
            
        return sequential_code, iterative_code


    # The process function
    def process_code(self, source_code):
        # Reference Environment for the exec() function
        reference_environment = {'console': self.console, 'print': print_function}
        iterative_code, sequential_code, debug_level = self.parse_code(source_code)
        
        # print("The debug level is " + str(debug_level)
        # print(sequential_code)
        # print(iterative_code)
        
        # Whatever the code is, first step is to just stop!
        self.hal.resetHAL()

        try:
            # The Python exec function
            # Run the sequential part
            gui_module, hal_module = self.generate_modules()
            exec(sequential_code, {"GUI": gui_module, "HAL": hal_module, "time": time}, reference_environment)

            # Run the iterative part inside template
            # and keep the check for flag
            with self.reload.get_lock():
                reload = self.reload.value

            while reload == 0:
                start_time = datetime.now()
                
                # Execute the iterative portion
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
                with self.time_cycle.get_lock():
                    time_cycle = self.time_cycle.value

                if(ms < time_cycle):
                    time.sleep((time_cycle - ms) / 1000.0)

                with self.reload.get_lock():
                    reload = self.reload.value

            print("Current Process Joined!")

        # To print the errors that the user submitted through the Javascript editor (ACE)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.console.print(exc_value)

    # Function to generate the modules for use in ACE Editor
    def generate_modules(self):
        # Define HAL module
        hal_module = imp.new_module("HAL")
        hal_module.HAL = imp.new_module("HAL")
        hal_module.HAL.motors = imp.new_module("motors")

        # Add HAL functions
        hal_module.HAL.getImage = self.hal.getImage
        hal_module.HAL.motors.sendV = self.hal.motors.sendV
        hal_module.HAL.motors.sendW = self.hal.motors.sendW

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
        with self.reload.get_lock():
            reload = self.reload.value

        while reload == 0:
            # Sleep for 2 seconds
            time.sleep(2)
            
            # Measure the current time and subtract from the previous time to get real time interval
            current_time = datetime.now()
            dt = current_time - previous_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            previous_time = current_time
            
            # Get the time period
            with self.ideal_cycle.get_lock():
                try:
                    # Division by zero
                    self.ideal_cycle.value = ms / self.iteration_counter
                except:
                    self.ideal_cycle.value = 0
            
            # Reset the counter
            self.iteration_counter = 0

            # Update reload variable
            with self.reload.get_lock():
                reload = self.reload.value

# Execute!
if __name__ == "__main__":
    server = Template()
    server.run_server()
