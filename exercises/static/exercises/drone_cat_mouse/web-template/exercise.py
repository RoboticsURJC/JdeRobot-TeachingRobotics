#!/usr/bin/env python

from __future__ import print_function

from websocket_server import WebsocketServer
import time
import threading
import subprocess
import sys
from datetime import datetime
import re
import json
import importlib
import numpy as np

import rospy
from std_srvs.srv import Empty

from gui import GUI, ThreadGUI
from hal import HAL
from mouse import Mouse
from console import start_console, close_console


class Template:
    # Initialize class variables
    # self.time_cycle to run an execution for at least 1 second
    # self.process for the current running process
    def __init__(self):
        self.thread = None
        self.reload = False

        # Time variables
        self.time_cycle = 80
        self.ideal_cycle = 80
        self.iteration_counter = 0
        self.real_time_factor = 0
        self.score = 0
        self.dist = 0
        self.frequency_message = {'brain': '', 'gui': '', 'rtf': '', 'score': '', 'dist': ''}

        self.server = None
        self.client = None
        self.host = sys.argv[1]

        # Initialize the GUI, HAL and Console behind the scenes
        self.hal = HAL()
        self.mouse = Mouse()
        self.gui = GUI(self.host, self.hal, self.mouse)

    # Function to parse the code
    # A few assumptions:
    # 1. The user always passes sequential and iterative codes
    # 2. Only a single infinite loop
    def parse_code(self, source_code):
        if source_code[:5] == "#resu":
                restart_simulation = rospy.ServiceProxy('/gazebo/unpause_physics', Empty)
                restart_simulation()

                return "", ""

        elif source_code[:5] == "#paus":
                pause_simulation = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
                pause_simulation()

                return "", ""

        elif source_code[:5] == "#rest":
            reset_simulation = rospy.ServiceProxy('/gazebo/reset_world', Empty)
            reset_simulation()
            self.gui.reset_gui()
            if self.hal.get_landed_state() ==2 : self.hal.land()

            return "", ""

        else:
            # Pause and unpause
            sequential_code, iterative_code = self.seperate_seq_iter(source_code)
            return iterative_code, sequential_code

    # Function to separate the iterative and sequential code
    def seperate_seq_iter(self, source_code):
        if source_code == "":
            return "", ""

        # Search for an instance of while True
        infinite_loop = re.search(r'[^ \t]while\(True\):|[^ \t]while True:', source_code)

        # Separate the content inside while True and the other
        # (Separating the sequential and iterative part!)
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
        # Redirect the information to console
        start_console()

        iterative_code, sequential_code = self.parse_code(source_code)

        # print(sequential_code)
        # print(iterative_code)

        # The Python exec function
        # Run the sequential part
        gui_module, hal_module = self.generate_modules()
        reference_environment = {"GUI": gui_module, "HAL": hal_module}
        exec(sequential_code, reference_environment)

        # Run the iterative part inside template
        # and keep the check for flag
        while self.reload == False:
            start_time = datetime.now()

            # Execute the iterative portion
            exec(iterative_code, reference_environment)

            # Template specifics to run!
            finish_time = datetime.now()
            dt = finish_time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0

            # Keep updating the iteration counter
            if (iterative_code == ""):
                self.iteration_counter = 0
            else:
                self.iteration_counter = self.iteration_counter + 1

            # The code should be run for atleast the target time step
            # If it's less put to sleep
            if (ms < self.time_cycle):
                time.sleep((self.time_cycle - ms) / 1000.0)

        close_console()
        print("Current Thread Joined!")

    # Function to generate the modules for use in ACE Editor
    def generate_modules(self):
        # Define HAL module
        hal_module = importlib.util.module_from_spec(importlib.machinery.ModuleSpec("HAL", None))
        hal_module.HAL = importlib.util.module_from_spec(importlib.machinery.ModuleSpec("HAL", None))
        # hal_module.drone = imp.new_module("drone")
        # motors# hal_module.HAL.motors = imp.new_module("motors")

        # Add HAL functions
        hal_module.HAL.get_frontal_image = self.hal.get_frontal_image
        hal_module.HAL.get_ventral_image = self.hal.get_ventral_image
        hal_module.HAL.get_position = self.hal.get_position
        hal_module.HAL.get_velocity = self.hal.get_velocity
        hal_module.HAL.get_yaw_rate = self.hal.get_yaw_rate
        hal_module.HAL.get_orientation = self.hal.get_orientation
        hal_module.HAL.get_roll = self.hal.get_roll
        hal_module.HAL.get_pitch = self.hal.get_pitch
        hal_module.HAL.get_yaw = self.hal.get_yaw
        hal_module.HAL.get_landed_state = self.hal.get_landed_state
        hal_module.HAL.set_cmd_pos = self.hal.set_cmd_pos
        hal_module.HAL.set_cmd_vel = self.hal.set_cmd_vel
        hal_module.HAL.set_cmd_mix = self.hal.set_cmd_mix
        hal_module.HAL.takeoff = self.hal.takeoff
        hal_module.HAL.land = self.hal.land

        # Define GUI module
        gui_module = importlib.util.module_from_spec(importlib.machinery.ModuleSpec("GUI", None))
        gui_module.GUI = importlib.util.module_from_spec(importlib.machinery.ModuleSpec("GUI", None))

        # Add GUI functions
        gui_module.GUI.showImage = self.gui.showImage
        gui_module.GUI.showLeftImage = self.gui.showLeftImage

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
        while not self.reload:
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
                self.ideal_cycle = ms / self.iteration_counter
            except:
                self.ideal_cycle = 0

            # Reset the counter
            self.iteration_counter = 0

            # Send to client
            self.send_frequency_message()

    # Function to generate and send frequency messages
    def send_frequency_message(self):
        # This function generates and sends frequency measures of the brain and gui
        brain_frequency = 0; gui_frequency = 0
        try:
            brain_frequency = round(1000 / self.ideal_cycle, 1)
        except ZeroDivisionError:
            brain_frequency = 0

        try:
            gui_frequency = round(1000 / self.thread_gui.ideal_cycle, 1)
        except ZeroDivisionError:
            gui_frequency = 0

        self.frequency_message["brain"] = brain_frequency
        self.frequency_message["gui"] = gui_frequency
        self.frequency_message["rtf"] = self.real_time_factor
        self.frequency_message["score"] = self.score
        self.frequency_message["dist"] = self.dist

        message = "#freq" + json.dumps(self.frequency_message)
        self.server.send_message(self.client, message)

    # Function to track the real time factor from Gazebo statistics
    # https://stackoverflow.com/a/17698359
    # (For reference, Python3 solution specified in the same answer)
    def track_stats(self):
        args = ["gz", "stats", "-p"]
        # Prints gz statistics. "-p": Output comma-separated values containing-
        # real-time factor (percent), simtime (sec), realtime (sec), paused (T or F)
        stats_process = subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
        # bufsize=1 enables line-bufferred mode (the input buffer is flushed
        # automatically on newlines if you would write to process.stdin )
        with stats_process.stdout:
            for line in iter(stats_process.stdout.readline, ''):
                stats_list = [x.strip() for x in line.split(',')]
                self.real_time_factor = stats_list[0]

    # Function to calculate score for evaluation
    def calc_score(self):
        point_cnt = 0
        max_score = 100
        max_points = 240
        self.score = 0

        while not self.reload:
            # Get position of cat drone
            x1, y1, z1 = self.hal.get_position()
            # Get position of mouse drone
            x2, y2, z2 = self.mouse.get_position()

            # Calculate distance between cat and mouse drones
            self.dist = np.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
            # Rounding upto 2 decimal
            self.dist = int(self.dist*100)/100

            # Calculate score only when both the drones are in air 
            # and score is less than maximum score
            # and raise score upto maximum of 2 mins that is 240 measuring points
            if z1 > 0.25 and z2 > 0.25 and self.score < max_score and point_cnt <= max_points:
                # Calculate score
                if self.dist < 2.0:
                    self.score = self.score + 0.5
                elif self.dist >= 2.0 and self.dist < 3.0:
                    self.score = self.score + 0.25
                elif self.dist >= 3.0 and self.dist < 4.0:
                    self.score = self.score + 0.12

                # Rounding upto 2 decimal
                self.score = int(self.score*100)/100

            point_cnt = point_cnt + 1
            time.sleep(0.5)

    # Function to maintain thread execution
    def execute_thread(self, source_code):
        # Keep checking until the thread is alive
        # The thread will die when the coming iteration reads the flag
        if self.thread is not None:
            while self.thread.is_alive() or self.measure_thread.is_alive():
                pass

        # Turn the flag down, the iteration has successfully stopped!
        self.reload = False
        # New thread execution
        self.measure_thread = threading.Thread(target=self.measure_frequency)
        self.thread = threading.Thread(target=self.process_code, args=[source_code])
        self.eval_thread = threading.Thread(target=self.calc_score)
        self.thread.start()
        self.measure_thread.start()
        self.eval_thread.start()
        print("New Thread Started!")

    # Function to read and set frequency from incoming message
    def read_frequency_message(self, message):
        frequency_message = json.loads(message)

        # Set brain frequency
        frequency = float(frequency_message["brain"])
        self.time_cycle = 1000.0 / frequency

        # Set gui frequency
        frequency = float(frequency_message["gui"])
        self.thread_gui.time_cycle = 1000.0 / frequency

        return

    # The websocket function
    # Gets called when there is an incoming message from the client
    def handle(self, client, server, message):
        if message[:5] == "#freq":
            frequency_message = message[5:]
            self.read_frequency_message(frequency_message)
            return

        try:
            # Once received turn the reload flag up and send it to execute_thread function
            code = message
            # print(repr(code))
            self.reload = True
            self.execute_thread(code)
        except:
            pass

    # Function that gets called when the server is connected
    def connected(self, client, server):
        self.client = client
        # Start the GUI update thread
        self.thread_gui = ThreadGUI(self.gui)
        self.thread_gui.start()

        # Start the real time factor tracker thread
        self.stats_thread = threading.Thread(target=self.track_stats)
        self.stats_thread.start()

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


# Execute!
if __name__ == "__main__":
    server = Template()
    server.run_server()
