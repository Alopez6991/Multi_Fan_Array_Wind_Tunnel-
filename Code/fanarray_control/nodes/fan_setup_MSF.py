#!/usr/bin/env python
import rospy
import math
import numpy as np
import random
import time
import sympy as sym
from optparse import OptionParser
from std_msgs.msg import UInt32MultiArray
import numpy as np

class FanSetup(object):
    def __init__(self,speed,freq,topic='fan_setup_MSF'):

		self.speed=speed
		self.freq=freq
		self.publisher = rospy.Publisher(topic, UInt32MultiArray, queue_size=100)
		rospy.on_shutdown(self.turn_off_all_fans)

    def lam(self):
    	r = rospy.Rate(1)
    	mode=0
    	msg=UInt32MultiArray()
    	msg.data=[mode,self.speed,self.freq]
    	while not rospy.is_shutdown():
            self.publisher.publish(msg)
            r.sleep()
    	
        # rospy.spin()

    def shear(self):
    	r = rospy.Rate(1)
    	mode=1
    	msg=UInt32MultiArray()
    	msg.data=[mode,self.speed,self.freq]
    	while not rospy.is_shutdown():
            self.publisher.publish(msg)
            r.sleep()

    def check(self):
    	r = rospy.Rate(1)
    	mode=2
    	msg=UInt32MultiArray()
    	msg.data=[mode,self.speed,self.freq]
    	while not rospy.is_shutdown():
            self.publisher.publish(msg)
            r.sleep()

    def turb(self):
    	r = rospy.Rate(1)
    	mode=3
    	msg=UInt32MultiArray()
    	msg.data=[mode,self.speed,self.freq]
    	while not rospy.is_shutdown():
            self.publisher.publish(msg)
            r.sleep()

    def turn_off_all_fans(self):
    	# r = rospy.Rate(1)
    	mode=0
    	msg=UInt32MultiArray()
    	msg.data=[mode,0,0]
    	# while not rospy.is_shutdown():
        self.publisher.publish(msg)
            # r.sleep()

if __name__ == '__main__':
	rospy.init_node('fan_array_control', anonymous=True)
	parser = OptionParser()
	parser.add_option("--topic",type="str",dest="topic",default="fan_setup_MSF",help="rostopic to publish to")
	parser.add_option("--program", type="str", dest="program", default='lam',
                    help="program to run (turbulence, laminar , shear, check)")
	parser.add_option("--speed", type="int", dest="speed", default=70,
                    help="mean fan speed between 0 and 100")
	parser.add_option("--freq", type="int", dest="freq", default=10,
                    help="To frequency")
	(options,args) = parser.parse_args()

	fansetup=FanSetup(options.speed,options.freq,topic=options.topic)
	if options.program == 'lam':
		fansetup.lam()
	elif options.program == 'shear':
		fansetup.shear()
	elif options.program == 'check':
		fansetup.check()
	elif options.program == 'turb':
		fansetup.turb()