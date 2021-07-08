import json
import math
import rospy
from std_msgs.msg import Int32
from interfaces.pose3d import ListenerPose3d
import os

class Config:
    def __init__(self):
        with open('config_sim.json') as file:
            self.config = json.load(file)
        self.pos_x = self.config['CONFIGURATION']['POS_X']
        self.pos_y = self.config['CONFIGURATION']['POS_Y']
        self.max_velV = self.config['CONFIGURATION']['MAX_VEL_V']
        self.max_velW = self.config['CONFIGURATION']['MAX_VEL_W']
        self.orientation = math.radians(self.config['CONFIGURATION']['ORIENTATION'])
        self.sonar_0 = self.config['CONFIGURATION']['SONAR_0']
        self.sonar_1 = self.config['CONFIGURATION']['SONAR_1']
        self.sonar_2 = self.config['CONFIGURATION']['SONAR_2']
        self.sonar_3 = self.config['CONFIGURATION']['SONAR_3']
        self.sonar_4 = self.config['CONFIGURATION']['SONAR_4']
        self.sonar_5 = self.config['CONFIGURATION']['SONAR_5']
        self.sonar_6 = self.config['CONFIGURATION']['SONAR_6']
        self.sonar_7 = self.config['CONFIGURATION']['SONAR_7']
        self.laser = self.config['CONFIGURATION']['LASER']
        self.topic_pose = self.config['CONFIGURATION']['TOPIC_POSE']
        self.topic_motors = self.config['CONFIGURATION']['TOPIC_MOTOR']
        self.topic_laser = self.config['CONFIGURATION']['TOPIC_LASER']
        self.topic_sonar_0 = self.config['CONFIGURATION']['TOPIC_SONAR0']
        self.topic_sonar_1 = self.config['CONFIGURATION']['TOPIC_SONAR1']
        self.topic_sonar_2 = self.config['CONFIGURATION']['TOPIC_SONAR2']
        self.topic_sonar_3 = self.config['CONFIGURATION']['TOPIC_SONAR3']
        self.topic_sonar_4 = self.config['CONFIGURATION']['TOPIC_SONAR4']
        self.topic_sonar_5 = self.config['CONFIGURATION']['TOPIC_SONAR5']
        self.topic_sonar_6 = self.config['CONFIGURATION']['TOPIC_SONAR6']
        self.topic_sonar_7 = self.config['CONFIGURATION']['TOPIC_SONAR7']
        rospy.init_node("AmigoBot")
        # If the robot is the real, we need to enable the motors
        if(os.path.basename(file.name) == 'config_real.json'):
            self.topic_enable_motors = self.config['CONFIGURATION']['TOPIC_ENABLE_MOTORS']
            self.msg = 0
            self.pub_motors = rospy.Publisher(self.topic_enable_motors, Int32, queue_size=1)
            self.pub_motors.publish(self.msg)
        else:
            pass
            # self.pos_x = ListenerPose3d.getPose3d.x
            # self.pos_y = ListenerPose3d.getPose3d.y
            # self.orientation = ListenerPose3d.getPose3d.yaw
