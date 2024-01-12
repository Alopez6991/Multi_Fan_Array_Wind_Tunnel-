#!/usr/bin/env python
import rospy
import math
import numpy as np
import random
import time
import sympy as sym
from optparse import OptionParser
from std_msgs.msg import UInt32MultiArray
from std_msgs.msg import UInt8
import numpy as np

class trig_sig:
	def __init__ (self, topic):
		self.pub_trig_sig=rospy.Publisher('SIG',UInt8,queue_size=100)

	def Pub_sig(self):
		r = rospy.Rate(1)
		sig1=0
		sig2=1
		msg=UInt8()
		msg.data=sig1
		msg2=UInt8()
		msg2.data=sig2
		while not rospy.is_shutdown():
			self.pub_trig_sig.publish(msg)
			T=random.randint(6, 15)
			rospy.sleep(T)
			self.pub_trig_sig.publish(msg2)
			rospy.sleep(.1)
			r.sleep()

if __name__ == '__main__':
    # rospy.init_node('read_motor', anonymous=True)
    parser = OptionParser()
    parser.add_option("--topic", type="str", dest="topic", default='',
                    help="ros topic with Float32 message for velocity control")
    (options, args) = parser.parse_args()
    rospy.init_node('SIG', anonymous=True)
    PUB = trig_sig(options.topic)
    PUB.Pub_sig()