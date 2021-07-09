import rospy
import threading
from math import asin, atan2, pi
from nav_msgs.msg import Odometry

def quat2Yaw(qw, qx, qy, qz):
    '''
    Translates from Quaternion to Yaw. 

    @param qw,qx,qy,qz: Quaternion values

    @type qw,qx,qy,qz: float

    @return Yaw value translated from Quaternion

    '''
    rotateZa0=2.0*(qx*qy + qw*qz)
    rotateZa1=qw*qw + qx*qx - qy*qy - qz*qz
    rotateZ=0.0
    if(rotateZa0 != 0.0 and rotateZa1 != 0.0):
        rotateZ=atan2(rotateZa0,rotateZa1)
    return rotateZ

def quat2Pitch(qw, qx, qy, qz):
    '''
    Translates from Quaternion to Pitch. 

    @param qw,qx,qy,qz: Quaternion values

    @type qw,qx,qy,qz: float

    @return Pitch value translated from Quaternion

    '''

    rotateYa0=-2.0*(qx*qz - qw*qy)
    rotateY=0.0
    if(rotateYa0 >= 1.0):
        rotateY = pi/2.0
    elif(rotateYa0 <= -1.0):
        rotateY = -pi/2.0
    else:
        rotateY = asin(rotateYa0)

    return rotateY

def quat2Roll (qw, qx, qy, qz):
    '''
    Translates from Quaternion to Roll. 

    @param qw,qx,qy,qz: Quaternion values

    @type qw,qx,qy,qz: float

    @return Roll value translated from Quaternion

    '''
    rotateXa0=2.0*(qy*qz + qw*qx)
    rotateXa1=qw*qw - qx*qx - qy*qy + qz*qz
    rotateX=0.0

    if(rotateXa0 != 0.0 and rotateXa1 != 0.0):
        rotateX=atan2(rotateXa0, rotateXa1)
    return rotateX


def odometry2Pose3D(odom):
    '''
    Translates from ROS Odometry to JderobotTypes Pose3d. 

    @param odom: ROS Odometry to translate

    @type odom: Odometry

    @return a Pose3d translated from odom

    '''
    pose = Pose3d()
    ori = odom.pose.pose.orientation

    pose.x = odom.pose.pose.position.x
    pose.y = odom.pose.pose.position.y
    pose.z = odom.pose.pose.position.z
    #pose.h = odom.pose.pose.position.h
    pose.yaw = quat2Yaw(ori.w, ori.x, ori.y, ori.z)
    pose.pitch = quat2Pitch(ori.w, ori.x, ori.y, ori.z)
    pose.roll = quat2Roll(ori.w, ori.x, ori.y, ori.z)
    pose.q = [ori.w, ori.x, ori.y, ori.z]
    pose.timeStamp = odom.header.stamp.secs + (odom.header.stamp.nsecs *1e-9)

    return pose
    
class Pose3d ():

	def __init__(self):

		self.x = 0 # X coord [meters]
		self.y = 0 # Y coord [meters]
		self.z = 0 # Z coord [meters]
		self.h = 1 # H param
		self.yaw = 0 #Yaw angle[rads]
		self.pitch = 0 # Pitch angle[rads]
		self.roll = 0 # Roll angle[rads]
		self.q = [0,0,0,0] # Quaternion
		self.timeStamp = 0 # Time stamp [s]


	def __str__(self):
		s = "Pose3D: {\n   x: " + str(self.x) + "\n   Y: " + str(self.y)
		s = s + "\n   Z: " + str(self.z) + "\n   H: " + str(self.h) 
		s = s + "\n   Yaw: " + str(self.yaw) + "\n   Pitch: " + str(self.pitch) + "\n   Roll: " + str(self.roll)
		s = s + "\n   quaternion: " + str(self.q) + "\n   timeStamp: " + str(self.timeStamp)  + "\n}"
		return s 


class ListenerPose3d:
    '''
        ROS Pose3D Subscriber. Pose3D Client to Receive pose3d from ROS nodes.
    '''
    def __init__(self, topic):
        '''
        ListenerPose3d Constructor.

        @param topic: ROS topic to subscribe
        
        @type topic: String

        '''
        self.topic = topic
        self.data = Pose3d()
        self.sub = None
        self.lock = threading.Lock()
        self.start()
 
    def __callback (self, odom):
        '''
        Callback function to receive and save Pose3d. 

        @param odom: ROS Odometry received
        
        @type odom: Odometry

        '''
        pose = odometry2Pose3D(odom)

        self.lock.acquire()
        self.data = pose
        self.lock.release()
        
    def stop(self):
        '''
        Stops (Unregisters) the client.

        '''
        self.sub.unregister()

    def start (self):
        '''
        Starts (Subscribes) the client.

        '''
        self.sub = rospy.Subscriber(self.topic, Odometry, self.__callback)
        
    def getPose3d(self):
        '''
        Returns last Pose3d. 

        @return last JdeRobotTypes Pose3d saved

        '''
        self.lock.acquire()
        pose = self.data
        self.lock.release()
        
        return pose

