import json
import rospy
import cv2
import sys
import base64
import threading
import time
import numpy as np
from datetime import datetime
from websocket_server import WebsocketServer
import multiprocessing
import logging

from interfaces.pose3d import ListenerPose3d
from shared.image import SharedImage
from shared.image import SharedImage
from shared.value import SharedValue

from lap import Lap
from map import Map

# Graphical User Interface Class
class GUI:
    # Initialization function
    # The actual initialization
    def __init__(self, host):
        rospy.init_node("GUI")

        self.payload = {'image': '','lap': '', 'map': '', 'v':'','w':''}
        self.server = None
        self.client = None
        
        self.host = host

        # Image variable
        self.shared_image = SharedImage("guiimage")
        
        # Get HAL variables
        self.shared_v = SharedValue("velocity")
        self.shared_w = SharedValue("angular")
        
        # Create the lap object
        pose3d_object = ListenerPose3d("/F1ROS/odom")
        self.lap = Lap(pose3d_object)
        self.map = Map(pose3d_object)

        # Event objects for multiprocessing
        self.ack_event = multiprocessing.Event()
        self.cli_event = multiprocessing.Event()

        # Start server thread
        t = threading.Thread(target=self.run_server)
        t.start()

    # Function to prepare image payload
    # Encodes the image as a JSON string and sends through the WS
    def payloadImage(self):
        image = self.shared_image.get()
        payload = {'image': '', 'shape': ''}
    	
    	shape = image.shape
        frame = cv2.imencode('.JPEG', image)[1]
        encoded_image = base64.b64encode(frame)
        
        payload['image'] = encoded_image.decode('utf-8')
        payload['shape'] = shape
        
        return payload

    # Function to get the client
    # Called when a new client is received
    def get_client(self, client, server):
        self.client = client
        self.cli_event.set()

        print(client, 'connected')
        
    # Update the gui
    def update_gui(self):
        # Payload Image Message
        payload = self.payloadImage()
        self.payload["image"] = json.dumps(payload)
        
        # Payload Lap Message
        lapped = self.lap.check_threshold()
        self.payload["lap"] = ""
        if(lapped != None):
            self.payload["lap"] = str(lapped)
            
        # Payload Map Message
        pos_message = str(self.map.getFormulaCoordinates())
        self.payload["map"] = pos_message

        # Payload V Message
        v_message = str(self.shared_v.get())
        self.payload["v"] = v_message

        # Payload W Message
        w_message = str(self.shared_w.get())
        self.payload["w"] = w_message
        
        message = "#gui" + json.dumps(self.payload)
        self.server.send_message(self.client, message)
            
    # Function to read the message from websocket
    # Gets called when there is an incoming message from the client
    def get_message(self, client, server, message):
        # Acknowledge Message for GUI Thread
        if(message[:4] == "#ack"):
            # Set acknowledgement flag
            self.ack_event.set()
        # Pause message
        elif(message[:5] == "#paus"):
            self.lap.pause()
        # Unpause message
        elif(message[:5] == "#resu"):
            self.lap.unpause()
        # Reset message
        elif(message[:5] == "#rest"):
            self.reset_gui()

    	
    # Function that gets called when the connected closes
    def handle_close(self, client, server):
        print(client, 'closed')

    # Activate the server
    def run_server(self):
        self.server = WebsocketServer(port=2303, host=self.host)
        self.server.set_fn_new_client(self.get_client)
        self.server.set_fn_message_received(self.get_message)
        self.server.set_fn_client_left(self.handle_close)
        self.server.run_forever()

    # Function to reset
    def reset_gui(self):
        self.lap.reset()
        self.map.reset()

        

# This class decouples the user thread
# and the GUI update thread
class ProcessGUI(multiprocessing.Process):
    def __init__(self):
        super(ProcessGUI, self).__init__()

        self.host = sys.argv[1]

        # Time variables
        self.time_cycle = SharedValue("gui_time_cycle")
        self.ideal_cycle = SharedValue("gui_ideal_cycle")
        self.iteration_counter = 0

    # Function to initialize events
    def initialize_events(self):
        # Events
        self.ack_event = self.gui.ack_event
        self.cli_event = self.gui.cli_event
        self.exit_signal = multiprocessing.Event()

    # Function to start the execution of threads
    def run(self):
        # Initialize GUI
        self.gui = GUI(self.host)
        self.initialize_events()

        # Wait for client before starting
        self.cli_event.wait()

        self.measure_thread = threading.Thread(target=self.measure_thread)
        self.thread = threading.Thread(target=self.run_gui)

        self.measure_thread.start()
        self.thread.start()

        print("GUI Process Started!")

        self.exit_signal.wait()

    # The measuring thread to measure frequency
    def measure_thread(self):
        previous_time = datetime.now()
        while(True):
            # Sleep for 2 seconds
            time.sleep(2)

            # Measure the current time and subtract from previous time to get real time interval
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

    # The main thread of execution
    def run_gui(self):
        while(True):
            start_time = datetime.now()
            # Send update signal
            self.gui.update_gui()

            # Wait for acknowldege signal
            self.ack_event.wait()
            self.ack_event.clear()
            
            finish_time = datetime.now()
            self.iteration_counter = self.iteration_counter + 1
            
            dt = finish_time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
            
            time_cycle = self.time_cycle.get()

            if(ms < time_cycle):
                time.sleep((time_cycle-ms) / 1000.0)

        self.exit_signal.set()

    # Functions to handle auxillary GUI functions
    def reset_gui():
        self.gui.reset_gui()
    
    def lap_pause():
        self.gui.lap.pause()
    
    def lap_unpause():
        self.gui.lap.unpause()


if __name__ == "__main__":
    gui = ProcessGUI()
    gui.start()