import numpy as np
import math
from math import cos,sin,tan,pow,pi,sqrt

class laser_handle:
    def autopark_place(self, laser_data, pose):
        #assert len(laser_data) == len(laser_angle)
        assert len(pose) == 3
        car_x = pose[0]
        car_y = pose[1]
        car_yaw = pose[2]
        num = len(laser_data)
        tmp = 0
        right_angle = 90
        left_angle = 90
        for i in range(num/2):
            if laser_data[num/2 - i][0] == 10:
                tmp += 1
                right_angle = 90 - i 
            else:
                # print ("laser_data",laser_data[num/2 - i])
                break
            
        
        for i in range(num/2):
            if laser_data[num/2 + i][0] == 10:
                tmp += 1
                left_angle = 90 + i
            else:
                # print ("laser_data",laser_data[num/2 - i])
                break
        if right_angle == left_angle:
            print ("not free place")
            return None
        else:
            print ("left_angle",left_angle,"right_angle",right_angle)
            len_angle = left_angle - right_angle
            print ("len_angle ",len_angle, ", tmp_length = ",tmp)
            max_length = sqrt(pow(10,2)-pow(5,2))
            left_park_len = min(tan((left_angle - 90)*pi/180) * 5.5, max_length)
            right_park_len = min(tan((90 - right_angle)*pi/180) * 5.5, max_length)
            park_len = left_park_len + right_park_len
            print ("park_len",park_len)
            
            if park_len > 8:
                print ("find park place")
                car_head_len = (left_park_len-right_park_len)/2
                print ("car_head_len",car_head_len)
                print ("pose",pose)
                x_tmp = 5.5*sin(car_yaw) + car_head_len * cos(car_yaw)
                y_tmp = - 5.5*cos(car_yaw) + car_head_len * sin(car_yaw)
            
                park_x = x_tmp + car_x
                park_y = y_tmp + car_y
                park_yaw = car_yaw
                print ("park place = ", park_x, park_y, park_yaw)
                return [park_x, park_y, park_yaw]
            else: 
                return None
