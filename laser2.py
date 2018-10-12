#!/usr/bin/env python

import rospy
from subsomption.msg import Channel 
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

import random
import numpy as np

bumper_l=0
bumper_r=0
lasers=LaserScan()
speed=10
threshold=50
timer=10
count_backward=0
count_turn=0


def callback_right_bumper(data):
    global bumper_r
    bumper_r=data.data
    #rospy.loginfo(rospy.get_caller_id()+"Right bumper %d",data.data)

def callback_left_bumper(data):
    global bumper_l
    bumper_l=data.data
    #rospy.loginfo(rospy.get_caller_id()+"Left bumper %d",data.data)


def callback_lasers(data):
    global lasers
    lasers=data
#    rospy.loginfo(rospy.get_caller_id()+" Lasers %s"," ".join(map(str,lasers)))


# replace 'my_behavior' by the name of your behavior
def my_behavior():
    global bumper_r
    global bumper_l
    global count_backward
    global count_turn
    rospy.init_node('my_behavior', anonymous=True)

    # remove the subscriptions you don't need.
    rospy.Subscriber("/simu_fastsim/laser_scan", LaserScan, callback_lasers)
    rospy.Subscriber("/simu_fastsim/right_bumper", Bool, callback_right_bumper)
    rospy.Subscriber("/simu_fastsim/left_bumper", Bool, callback_left_bumper)
 
    # replace /subsomption/channel0 by /subsomption/channeli where i is the number of the channel you want to publish in
    pub = rospy.Publisher('/subsomption/channel1', Channel , queue_size=10)
    r = rospy.Rate(10) # 10hz
    v=Channel()
    v.activated=True
    v.speed_left=0
    v.speed_right=0
    count_backward=0
    count=0
	 
    range_threshold = 20
	
    while not rospy.is_shutdown():
	# print(" ".join([str(int(x)) for x in lasers.ranges]))
	angle = 0
	if (lasers.ranges):	
		laser_min = min(lasers.ranges)
		laser_index = lasers.ranges.index(laser_min)	
		laser_angle = lasers.angle_min + laser_index * lasers.angle_increment

		# print("min, index", laser_min, laser_index, laser_angle)

		if laser_min < range_threshold:
			v.speed_left = 1 * np.sign(laser_angle)
			v.speed_right = -1 * np.sign(laser_angle)
			pub.publish(v)
	
        # compute the value of v that will be sent to the subsomption channel. 
        r.sleep()   


if __name__ == '__main__':
    random.seed()
    try:
        my_behavior()
    except rospy.ROSInterruptException: pass
