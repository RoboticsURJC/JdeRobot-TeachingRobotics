import rospy
from sensor_msgs.msg import LaserScan
import threading
from math import pi as PI

class LaserData ():

    def __init__(self):

        self.values = [] # meters
        self.minAngle = 0 # Angle of first value (rads)
        self.maxAngle = 0 # Angle of last value (rads)
        self.minRange = 0 # Max Range posible (meters)
        self.maxRange = 0 # Min Range posible (meters)
        self.timeStamp = 0 # seconds
        self.angleIncrement = 0 # Increment of angle


    def __str__(self):
        s = "LaserData: {\n   minAngle: " + str(self.minAngle) + "\n   maxAngle: " + str(self.maxAngle)
        s = s + "\n   minRange: " + str(self.minRange) + "\n   maxRange: " + str(self.maxRange) 
        s = s + "\n   timeStamp: " + str(self.timeStamp) + "\n   values: " + str(self.values) + "\n"
        s = s + "\n   angleIncrement: " + str(self.angleIncrement) + "\n}"
        return s 

def laserScan2LaserData(scan):
    '''
    Translates from ROS LaserScan to JderobotTypes LaserData. 

    @param scan: ROS LaserScan to translate

    @type scan: LaserScan

    @return a LaserData translated from scan

    '''
    laser = LaserData()
    laser.values = scan.ranges
    ''' 
          ROS Angle Map      JdeRobot Angle Map
                0                  PI/2
                |                   |
                |                   |
       PI/2 --------- -PI/2  PI --------- 0
                |                   |
                |                   |
    '''
    laser.minAngle = scan.angle_min  + PI/2
    laser.maxAngle = scan.angle_max  + PI/2
    laser.maxRange = scan.range_max
    laser.minRange = scan.range_min
    laser.timeStamp = scan.header.stamp.secs + (scan.header.stamp.nsecs *1e-9)
    laser.angleIncrement = scan.angle_increment
    return laser

class ListenerLaser:
    '''
        ROS Laser Subscriber. Laser Client to Receive Laser Scans from ROS nodes.
    '''
    def __init__(self, topic):
        '''
        ListenerLaser Constructor.

        @param topic: ROS topic to subscribe
        
        @type topic: String

        '''
        self.topic = topic
        self.data = LaserData()
        self.sub = None
        self.lock = threading.Lock()
        self.start()
 
    def __callback (self, scan):
        '''
        Callback function to receive and save Laser Scans. 

        @param scan: ROS LaserScan received
        
        @type scan: LaserScan

        '''
        laser = laserScan2LaserData(scan)

        self.lock.acquire()
        self.data = laser
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
        self.sub = rospy.Subscriber(self.topic, LaserScan, self.__callback)
        
    def getLaserData(self):
        '''
        Returns last LaserData. 

        @return last JdeRobotTypes LaserData saved

        '''
        self.lock.acquire()
        laser = self.data
        self.lock.release()
        
        return laser

