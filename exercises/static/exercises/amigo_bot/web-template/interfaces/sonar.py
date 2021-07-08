import rospy
from sensor_msgs.msg import Range
import threading 
from math import pi as PI

class SonarData ():

    def __init__(self):
        self.distances = []
        self.minRange = 0
        self.maxRange = 0
        self.timeStamp = 0
    
    def __str__(self):
        s = "SonarData: {\n minRange: " + str(self.minRange) + "\n maxRange: " + str(self.maxRange)
        s = s + "\n timeStamp: " + str(self.timeStamp) + "\n distances " + str(self.distances) + "\n}"
        return s

def SonarScan2SonarData (scan):
    '''
        Translates from ROS SonarScan to JderobotTypes SonarData.
        @param scan: ROS SonarScan to translate
        @type scan: SonarScan
        @return a SonarData translated from scan
    '''
    sonar = SonarData ()
    sonar.distances = scan.range
    sonar.minRange = scan.min_range
    sonar.maxRange = scan.max_range
    sonar.timeStamp = scan.header.stamp.secs + (scan.header.stamp.nsecs *1e-9)
    return sonar

class ListenerSonar:
    '''
        ROS Sonar Subsciber. Sonar client to receive sonar scans from ROS Nodes
    '''
    def __init__(self, topic):
        '''
            ListenerSonar Constructor.
            @param topic: Rostopic to subscribe
            @type topic: String
        '''
        self.topic = topic
        self.data = SonarData ()
        self.sub = None
        self.lock = threading.Lock()
        self.start()
        
    def __callback (self, scan):
        '''
            Callback function to receive and save Sonar Scans
            @param scan: ROS SonarScan received
            @type scan: SonarScan
        '''
        sonar = SonarScan2SonarData (scan)
        self.lock.acquire()
        self.data = sonar
        self.lock.release()
        
    def stop (self):
        '''
        Stops (Unregisters) the client.
        '''
        self.sub.unregister()

    def start(self):
        '''
        Starts (Subscribes) the client.
        '''
        self.sub = rospy.Subscriber(self.topic, Range, self.__callback)

    def getSonarData(self):
        '''
        Returns last SonarData
        @return last JdeRobotTypes SonarData saved
        '''
        self.lock.acquire()
        sonar = self.data
        self.lock.release()
        
        return sonar
