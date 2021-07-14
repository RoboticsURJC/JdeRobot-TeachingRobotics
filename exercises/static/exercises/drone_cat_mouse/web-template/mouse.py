import threading
import rospy

from drone_wrapper import DroneWrapper
from interfaces.autonomous_mouse import path_obfuscated
from interfaces.threadStoppable import StoppableThread
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState


class Mouse:
    def __init__(self):
        self.mouse = DroneWrapper(name="rqt", ns="mouse/")
        self.reset_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

    # Explicit initialization functions
    # Class method, so user can call it without instantiation
    @classmethod
    def initRobot(cls):
        new_instance = cls()
        return new_instance

    def takeoff(self):
        self.mouse.takeoff(h=5)

    def start_mouse(self, path_level):
        self.takeoff()
        self.thread = StoppableThread(target=self.autonomous_mouse, args=[path_level])
        self.thread.start()

    def land(self):
        self.mouse.land()

    def stop_mouse(self):
        self.thread.stop()
        self.mouse.set_cmd_mix(vx=0, vy=0, z=self.mouse.get_position()[2], az=0)

    def reset_mouse(self):
        self.thread.stop()
        self.mouse.land()

        req = ModelState()
        req.model_name = "iris_red"
        req.pose.position.x = 2.0
        req.pose.position.y = 0.0
        req.pose.position.z = 0.05
        req.pose.orientation.x = 0.0
        req.pose.orientation.y = 0.0
        req.pose.orientation.z = 0.0
        req.pose.orientation.w = 1.0
        req.twist.linear.x = 0.0
        req.twist.linear.y = 0.0
        req.twist.linear.z = 0.0
        req.twist.angular.x = 0.0
        req.twist.angular.y = 0.0
        req.twist.angular.z = 0.0
        self.reset_state(req)

    def autonomous_mouse(self, path_level):
        v = path_obfuscated(path_level)
        if v is not None:
            vx, vy, vz, yaw = v
            self.mouse.set_cmd_vel(vx, vy, vz, yaw)
        else:
            print("[Mouse] Path {} not available".format(path_level))

    def get_position(self):
        pos = self.mouse.get_position()
        return pos