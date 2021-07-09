import rospy
import cv2
import threading
import time
from datetime import datetime

from interfaces.camera import ListenerCamera
from interfaces.motors import PublisherMotors
from shared.image import SharedImage
from shared.value import SharedValue

# Hardware Abstraction Layer
class HAL:
    IMG_WIDTH = 320
    IMG_HEIGHT = 240
    
    def __init__(self):
    	rospy.init_node("HAL")
    
        # Shared memory variables
    	self.shared_image = SharedImage("halimage")
        self.shared_v = SharedValue("velocity")
        self.shared_w = SharedValue("angular")

        # ROS Topics
    	self.camera = ListenerCamera("/F1ROS/cameraL/image_raw")
    	self.motors = PublisherMotors("/F1ROS/cmd_vel", 4, 0.3)

        # Update thread
        self.thread = ThreadHAL(self.update_hal)

    # Function to start the update thread
    def start_thread(self):
        self.thread.start()
    
    # Get Image from ROS Driver Camera
    def getImage(self):
        image = self.camera.getImage().data
        self.shared_image.add(image)

    # Set the velocity
    def setV(self):
        velocity = self.shared_v.get()
        self.motors.sendV(velocity)

    # Get the velocity
    def getV(self):
        velocity = self.shared_v.get()
        return velocity

    # Get the angular velocity
    def getW(self):
        angular = self.shared_w.get()
        return angular

    # Set the angular velocity
    def setW(self):
        angular = self.shared_w.get()
        self.motors.sendW(angular)

    def update_hal(self):
        self.getImage()
        self.setV()
        self.setW()

    # Destructor function to close all fds
    def __del__(self):
        self.shared_image.close()
        self.shared_v.close()
        self.shared_w.close()

class ThreadHAL(threading.Thread):
    def __init__(self, update_function):
        super(ThreadHAL, self).__init__()
        self.time_cycle = 80
        self.update_function = update_function

    def run(self):
        while(True):
            start_time = datetime.now()

            self.update_function()

            finish_time = datetime.now()

            dt = finish_time - start_time
            ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0

            if(ms < self.time_cycle):
                time.sleep((self.time_cycle - ms) / 1000.0)