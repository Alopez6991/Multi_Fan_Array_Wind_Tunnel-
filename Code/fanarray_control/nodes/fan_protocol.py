#!/usr/bin/env python
import rospy
import math
import numpy as np
import random
import time
import sympy as sym
from optparse import OptionParser
from std_msgs.msg import UInt32MultiArray,Float32
from std_msgs.msg import UInt8
import numpy as np

class FanSetup(object):
    def __init__(self,speed,freq,Time1,Time2,Npulse,Mode,topic='fan_setup_MSF'):

        self.speed=speed
        self.freq=freq
        self.Time1=Time1
        self.Time2=Time2
        self.Npulse=Npulse
        self.Mode=Mode
        self.publisher = rospy.Publisher(topic, UInt32MultiArray, queue_size=100)
        self.pub=rospy.Publisher('mode',UInt8,queue_size=100)
        rospy.Subscriber('braid_trigger_topic',Float32,self.callback)
        self.trig=None
        self.T=0
        rospy.on_shutdown(self.turn_off_all_fans)

    
    def lam2shear(self):
        r = rospy.Rate(1)
        mode=0
        M2=self.Mode
        if M2 == 'LR':
            mode2=11
        elif M2 == 'RL':
            mode2=111
        elif M2 == 'TL':
            mode2=1111
        elif M2 == 'TR':
            mode2=11111
        elif M2 == 'BL':
            mode2=10
        elif M2 == 'BR':
            mode2=100
        elif M2 == 'BT':
            mode2=1000
        else:
            mode2=1
        msg=UInt32MultiArray()
        msg.data=[mode,self.speed,self.freq]
        msg2=UInt32MultiArray()
        msg2.data=[mode2,self.speed,self.freq]
        msg3=UInt32MultiArray()
        msg3.data=[0,0,0]
        state=UInt8()

        # print ('start')
        while not rospy.is_shutdown():
            # print('loop start')
            rospy.sleep(1)
            state.data=0
            self.pub.publish(state)
            self.publisher.publish(msg)
            # print('first pub',self.Time1)
            rospy.sleep(self.Time1*60*60)
            # print('pause')
            self.publisher.publish(msg3)
            rospy.sleep(1)
            # print('shear')
            state.data=1
            self.pub.publish(state)
            self.publisher.publish(msg2)
            rospy.sleep(self.Time2*60*60)
            r.sleep()



    def lam2check(self):
            r = rospy.Rate(1)
            mode=0
            mode2=2
            msg=UInt32MultiArray()
            msg.data=[mode,self.speed,self.freq]
            msg2=UInt32MultiArray()
            msg2.data=[mode2,self.speed,self.freq]
            msg3=UInt32MultiArray()
            msg3.data=[0,0,0]
            state=UInt8()
            # print ('start')
            while not rospy.is_shutdown():
                # print('loop start')
                rospy.sleep(1)
                state.data=0
                self.pub.publish(state)
                self.publisher.publish(msg)
                # print('first pub',self.Time1)
                rospy.sleep(self.Time1)
                # print('pause')
                self.publisher.publish(msg3)
                rospy.sleep(1)
                # print('shear')
                state.data=2
                self.pub.publish(state)
                self.publisher.publish(msg2)
                rospy.sleep(self.Time2)
                r.sleep()

    def callback(self,dat):
        self.trig=dat.data
        print(self.trig)
        if self.trig==0.0:
            self.T=100
        else:
            self.T=200
        print(self.T,'T')
    def trigger(self):
        
        r = rospy.Rate(50)
        mode=0
        mode2=2
        msg=UInt32MultiArray()
        msg.data=[mode,self.speed,self.freq]
        msg2=UInt32MultiArray()
        msg2.data=[mode,100,self.freq]
        msg3=UInt32MultiArray()
        msg3.data=[0,0,0]
        state=UInt8()
        # print ('start')
        while not rospy.is_shutdown():
            # print(self.T,'loop')
            # self.publisher.publish(msg)
            if self.T ==200:
                print('pulse')
                # self.publisher.publish(msg3)
                # rospy.sleep(.1)
                state.data=2
                self.pub.publish(state)
                self.publisher.publish(msg2)
                rospy.sleep(5)
                self.publisher.publish(msg)
            r.sleep()



    def lam(self):
    	r = rospy.Rate(1)
    	mode=0
    	flag =0
    	msg=UInt32MultiArray()
    	msg.data=[mode,self.speed,self.freq]
    	#if flag =0
    	#self.publisher.publish(msg)
    	#print(flag)
    	while not rospy.is_shutdown():
            self.publisher.publish(msg)
            r.sleep()

    	#rospy.sleep()
        # rospy.spin()

    def shear(self):
    	r = rospy.Rate(1)
        if self.Mode == 'LR':
            mode=11
        elif self.Mode == 'RL':
            mode=111
        elif self.Mode == 'TL':
            mode=1111
        elif self.Mode == 'TR':
            mode=11111
        elif self.Mode == 'BL':
            mode=10
        elif self.Mode == 'BR':
            mode=100
        elif self.Mode == 'BT':
            mode=1000
        else:
            mode=1
        msg=UInt32MultiArray()
    	msg.data=[mode,self.speed,self.freq]
    	while not rospy.is_shutdown():
            self.publisher.publish(msg)
            r.sleep()

    # def shear_left_right(self):
    #         r = rospy.Rate(1)
    #         mode=11
    #         msg=UInt32MultiArray()
    #         msg.data=[mode,self.speed,self.freq]
    #         while not rospy.is_shutdown():
    #             self.publisher.publish(msg)
    #             r.sleep()

    # def shear_right_left(self):
    #         r = rospy.Rate(1)
    #         mode=111
    #         msg=UInt32MultiArray()
    #         msg.data=[mode,self.speed,self.freq]
    #         while not rospy.is_shutdown():
    #             self.publisher.publish(msg)
    #             r.sleep()

    def check(self):
    	r = rospy.Rate(1)
    	mode=2
    	msg=UInt32MultiArray()
    	msg.data=[mode,self.speed,self.freq]
    	while not rospy.is_shutdown():
            self.publisher.publish(msg)
            r.sleep()

    def check2(self):
        r = rospy.Rate(1)
        mode=22
        msg=UInt32MultiArray()
        msg.data=[mode,self.speed,self.freq]
        while not rospy.is_shutdown():
            self.publisher.publish(msg)
            r.sleep()

    def check3(self):
        r = rospy.Rate(1)
        mode=222
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

    def D_check(self):
        r = rospy.Rate(1)
        mode=4
        msg=UInt32MultiArray()
        msg.data=[mode,self.speed,self.freq]
        while not rospy.is_shutdown():
            self.publisher.publish(msg)
            r.sleep()

    def DD_check(self):
        r = rospy.Rate(1)
        mode=5
        msg=UInt32MultiArray()
        msg.data=[mode,self.speed,self.freq]
        while not rospy.is_shutdown():
            self.publisher.publish(msg)
            r.sleep()

    def crazy(self):
        r = rospy.Rate(1)
        mode=6
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
                    help="program to run (turbulence, laminar , shear, check,laminar to shear, shear_LR, Shear_RL)")
    parser.add_option("--speed", type="int", dest="speed", default=70,
                    help="mean fan speed between 0 and 100")
    parser.add_option("--freq", type="int", dest="freq", default=10,
                    help="To frequency")
    parser.add_option("--Time1", type="int", dest="Time1", default=1, help="how long is it laminar")
    parser.add_option("--Time2", type="int", dest="Time2", default=1, help="how long is it shear")
    # parser.add_option("--speed2", type="int", dest="speed2", default=, help="second speed when doing the lam2___ set ups")
    parser.add_option("--Npulse", type="int", dest="Npulse", default=1, help="how many pulses do you want")
    parser.add_option("--Mode", type="str", dest="Mode",default='LR', help="what set up do you want for shear, TB, LR, RL, TL, TR, BL, BR")

    (options,args) = parser.parse_args()

    fansetup=FanSetup(options.speed,options.freq,options.Time1,options.Time2,options.Npulse,options.Mode,topic=options.topic)
    if options.program == 'lam':
    	fansetup.lam()
    elif options.program == 'shear':
    	fansetup.shear()
    # elif options.program == 'shear_LR':
    #     fansetup.shear_left_right()
    # elif options.program == 'shear_RL':
        # fansetup.shear_right_left()
    elif options.program == 'check':
    	fansetup.check()
    elif options.program == 'check2':
        fansetup.check2()
    elif options.program == 'check3':
        fansetup.check3()
    elif options.program == 'turb':
    	fansetup.turb()
    elif options.program == 'Dcheck':
        fansetup.D_check()
    elif options.program == 'DDcheck':
        fansetup.DD_check()
    elif options.program == 'lam2shear':
        fansetup.lam2shear()
    elif options.program == 'lam2check':
        fansetup.lam2check()
    elif options.program == 'trigger':
        fansetup.trigger()
    elif options.program == 'crazy':
        fansetup.crazy()