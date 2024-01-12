#!/usr/bin/env python
from __future__ import division
import rospy
import math
import numpy as np
import random
import time
import sympy as sym
from optparse import OptionParser
from std_msgs.msg import UInt8MultiArray
import numpy as np

class FanArray(object):
    def __init__(self, board_mapping, pin_mapping, avg_speed,Npulse,To, topic='/one_fan_at_a_time'):
        '''
        FanArray is a class to control an array of fans through an arduino. 
        Requires "rosrun rosserial_python serial_node.py /dev/ttyACM0" to communicate with arduino

        Inputs
        ======
        board_mapping: NxM numpy.ndarray with integer values corresponding to the PWM extender board number
                       for each fan in the array
        pin_mapping: NxM numpy.ndarray with integer values corresponding to the PWM pin number on the board

        '''
        assert board_mapping.shape == pin_mapping.shape
        assert board_mapping.dtype == np.uint8
        assert pin_mapping.dtype == np.uint8

        self.board_mapping = board_mapping
        self.pin_mapping = pin_mapping
        self.nfans=36
        self.avg_speed = avg_speed
        self.Npulse=Npulse
        self.To=To
        
        self.Fi=np.linspace(0,self.To,self.To+1)/self.To
         # code from board and pin maping 

        self.publisher = rospy.Publisher(topic, UInt8MultiArray, queue_size=100)
        rospy.on_shutdown(self.turn_off_all_fans)

    def update_single_fan_board_pin(self, board, pin, speed):
        '''
        board - PWM extender board number (from 0 to however many board extenders you have)
        pin - PWM pin number (from 0 to 15)
        speed - speed in PWM (from 0 to 100)
        '''
        if speed is None:
            speed = self.avg_speed


        msg = UInt8MultiArray()
        msg.data = [board, pin, speed]
        self.publisher.publish(msg)

    def get_speed(self,avg_speed,To,TI,phi):
        # create frequencies
        # F=1/To
        # Fi=np.linspace(0,To,To+1)*F
        Fi=self.Fi
        # print(Fi)

        nspeed=0
        # t=sym.Symbol('t')

        # Generate function
        for i in range(0,To):
            nspeed+=5*np.sin(2*np.pi*Fi[i]*TI +phi[i])
        # input time and update new speed
        S=int(nspeed+self.avg_speed)
        # limit the input speed to be between 20 and 100
        if S >100:
            S = 100
        elif S< 20:
            S = 20
        # return the speed
        return (S)



    def update_sine_wave(self,GG,phi,To,T1):


        # To=len(phi)
                # get time
        TI =rospy.get_time()

        # Generate a speed for each fan 
        NS=[]
        for i in range(1,self.nfans+1):
            ns=self.get_speed(self.avg_speed,To,TI+To*(i-1)/36,phi)

            NS.append(ns)
        
        # [pin , board , speed]
        ZZ=[]
        for i in range(0,36):
            zz= [GG[i][0],GG[i][1],NS[i]]
            ZZ.append(zz)
        print(ZZ,np.round((TI-T1),2))
        # print(ZZ[0][0])


        # msg = UInt8MultiArray()
        # msg.data = ZZ
        # self.publisher.publish(msg)
        # publish fan board, pin, and speed to arduino
        for i in range (0,36):
            self.update_single_fan_board_pin(ZZ[i][1], ZZ[i][0],ZZ[i][2])

        

    def update_single_row(self, row, speed):
        '''
        updates the speed of all fans in a row at the same value
        '''
        board_numbers = np.unique(self.board_mapping)
        pin_numbers = np.unique(self.pin_mapping)

        if speed is None:
            speed = self.avg_speed

        # msg = UInt8MultiArray()
        # msg.data = [row, speed]
        # self.publisher.publish(msg)

        
        if row == 0:
            for n in range(0,6):
                self.update_single_fan_board_pin(0,n,speed)
                # print('0 on')

        if row == 1:
            for n in range(6,12):
                self.update_single_fan_board_pin(0,n,speed)
                # print('1 on')

        if row == 2:
            for n in range(0,6):
                self.update_single_fan_board_pin(1,n,speed)
                # print('2 on')

        if row == 3:
            for n in range(6,12):
                self.update_single_fan_board_pin(1,n,speed)
                # print('3 on')

        if row == 4:
            for n in range(0,6):
                self.update_single_fan_board_pin(2,n,speed)
                # print('4 on')

        if row == 5:
            for n in range(6,12):
                self.update_single_fan_board_pin(2,n,speed)
                # print('5 on')




    def update_all_fans(self,speed=None):
        '''
        updates the speed of all fans in the array to the same value
        '''
        board_numbers = np.unique(self.board_mapping)
        pin_numbers = np.unique(self.pin_mapping)

        if speed is None:
            speed = self.avg_speed

        msg = UInt8MultiArray()
        msg.data = [speed]
        self.publisher.publish(msg)

        for board_number in board_numbers:
            for pin_number in pin_numbers:
                self.update_single_fan_board_pin(board_number, pin_number,speed)

    def set_step_pattern (self):

        self.update_all_fans(10)
        # print('start fans')
        # rospy.sleep(2)
        # TI=rospy.get_time()
        T1=rospy.get_time()
        print('start loop at T=0')

        for i in range (1,11):
            if i == 2:
                self.update_all_fans(i*10)
                print(i*10) 
                rospy.sleep(75)
                print('20--->30',np.round((rospy.get_time()-T1),0))
            elif i==10:
                self.update_all_fans(i*10)
                print(i*10)
                rospy.sleep(60)
                print('100--->off',np.round((rospy.get_time()-T1),0))
            elif i == 1:
                self.update_all_fans(i*10)
                print(i*10) 
                rospy.sleep(5)
                print('off--->20',np.round((rospy.get_time()-T1),0))

            else:
                self.update_all_fans(i*10)
                print(i*10)
                rospy.sleep(60)
                print(str(i*10)+'--->'+str((i+1)*10),np.round((rospy.get_time()-T1),0))

    def set_impulse (self,Npulse):
        Npulse=self.Npulse

        T1=rospy.get_time()
        print('0ff')
        self.update_all_fans(10)
        rospy.sleep(1)
        for i in range (1,Npulse+1):
            if i == 1:
                # print(20,np.round((rospy.get_time()-T1),0))
                print('on')
                self.update_all_fans(20)
                rospy.sleep(55)
                print(np.round((rospy.get_time()-T1),0),'pulse'+str(i))
                self.update_all_fans(100)
                rospy.sleep(1)
                # print(20,np.round((rospy.get_time()-T1),0))
                self.update_all_fans(20)
                rospy.sleep(20)
            elif i==Npulse:
                # print(20,np.round((rospy.get_time()-T1),0))
                self.update_all_fans(20)
                rospy.sleep(10)
                print(np.round((rospy.get_time()-T1),0),'pulse'+str(i))
                self.update_all_fans(100)
                rospy.sleep(1)
                # print(20,np.round((rospy.get_time()-T1),0))
                self.update_all_fans(20)
                rospy.sleep(30)
            else:
                # print(20,np.round((rospy.get_time()-T1),0))
                self.update_all_fans(20)
                rospy.sleep(10)
                print(np.round((rospy.get_time()-T1),0),'pulse'+str(i))
                self.update_all_fans(100)
                rospy.sleep(1)
                # print(20,np.round((rospy.get_time()-T1),0))
                self.update_all_fans(20)
                rospy.sleep(20)

    def set_frequency(self,HZ):
        T1=rospy.get_time()
        HZ=HZ
        AS=self.avg_speed

        WS=int(np.round(AS+30*np.sin(2*np.pi*HZ*T1),0))
        if WS >100:
            WS = 100
        elif WS< 20:
            WS = 20
        print(WS)

        self.update_single_row(2,WS)
        self.update_single_row(3,WS)
        self.update_single_row(4,WS)
        # return(WS)

        

            
            



    def update_single_fan_row_col(self, row, col, speed=None):
        '''
        row and col correspond to the row and col of the physical fan array
        '''
        if speed is None:
            speed = self.avg_speed

        board = self.board_mapping[row, col]
        pin = self.pin_mapping[row, col]
        self.update_single_fan_board_pin(board, pin, speed)

    def update_fan_speeds(self, fan_speed_array):
        '''
        Given an NxM array of PWM speeds for each fan, set the fan speeds.
        '''
        assert fan_speed_array.shape == self.board_mapping.shape
        assert fan_speed_array.dtype == np.uint8

        for row in range(fan_speed_array.shape[0]):
            for col in range(fan_speed_array.shape[1]):
                self.update_single_fan_row_col(row, col, fan_speed_array[row, col])

    def turn_off_all_fans(self):
        board_numbers = np.unique(self.board_mapping)
        pin_numbers = np.unique(self.pin_mapping)

        for board_number in board_numbers:
            for pin_number in pin_numbers:
                self.update_single_fan_board_pin(board_number, pin_number, 0)

    def main(self):
        rospy.spin()

    def turbulence (self):
        # generate all combinations of fans and board
        T1=rospy.get_time()

        GG=[]
        for i in range(0,3):
            for j in range(0,12):
                G=[j,i]
                GG.append(G)
        # put the fans in a random order
        random.shuffle(GG)

        To=self.To
        # Generate a phase shift
        phi=np.ones(To)
        for i in range(0,To):
            phi[i]=random.uniform(-math.pi,math.pi)
            # append
        # print(phi)

        # Update the arduino in Hz 
        r = rospy.Rate(5)
        # print(self.nfans)
        while not rospy.is_shutdown():
            self.update_sine_wave(GG,phi,To,T1)
            r.sleep()

    def laminar (self):
        r = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.update_all_fans(self.avg_speed)
            r.sleep()


    def shear (self):
        r = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.update_single_row(0,self.avg_speed)
            self.update_single_row(1,self.avg_speed)
            self.update_single_row(2,self.avg_speed)
            r.sleep()

    def step (self):
        r = rospy.Rate(1)
        while not rospy.is_shutdown():

            self.set_step_pattern()
            r.sleep()

    def impulse (self):

        self.set_impulse(self.Npulse)
        print('off')

    def hz (self):
        # HZspeed=self.avg_speed

        HZ_array=[0.01, 0.1, 1, 10, 100]

        # r = rospy.Rate(5)
        # # print(self.nfans)
        # for i in range (0,5):

        #     while not rospy.is_shutdown():
        #         self.set_frequency(HZ_array[i],HZspeed)
        #         r.sleep()
        i=0
        T1=rospy.get_time()
        r = rospy.Rate(12)
        self.update_single_row(2,10)
        self.update_single_row(3,10)
        self.update_single_row(4,10)
        rospy.sleep(1)
        self.update_single_row(2,20)
        self.update_single_row(3,20)
        self.update_single_row(4,20)
        rospy.sleep(10)

        while not rospy.is_shutdown():
            self.set_frequency(HZ_array[i])
            TZ=rospy.get_time()
            THZ=np.round(TZ-T1,1)+1
            print(HZ_array[i],THZ)
            if THZ % 300 == 0:
                i+=1
                TZ=0
            # print('1off')
            r.sleep()
        # print('2off')






        
            


        
        

def get_interactive_fan_array_controller():
    rospy.init_node('fan_array_control', anonymous=True)

    board_1 = 0*np.ones([2,6]).astype('uint8')
    board_2 = 1*np.ones([2,6]).astype('uint8')
    board_3 = 2*np.ones([2,6]).astype('uint8')
    board_mapping = np.vstack((board_1, board_2, board_3))

    pins = np.arange(0, 12).reshape([2,6])
    pin_mapping = np.vstack([pins]*3)
    pin_mapping = pin_mapping.astype('uint8')

    fanarray = FanArray(board_mapping, pin_mapping,speed, topic='/one_fan_at_a_time')    

    return fanarray 


if __name__ == '__main__':
    rospy.init_node('fan_array_control', anonymous=True)
    parser = OptionParser()
    parser.add_option("--topic", type="str", dest="topic", default='/one_fan_at_a_time',
                        help="rostopic to publish to")
    parser.add_option("--program", type="str", dest="program", default='laminar',
                        help="program to run (main, turbulence, laminar , shear, step, impulse, or hz )")
    parser.add_option("--avg_speed", type="int", dest="avg_speed", default=70,
                        help="mean fan speed between 0 and 100")
    parser.add_option("--Npulse", type="int", dest="Npulse", default=3,
                        help="number of pulses")
    parser.add_option("--To", type="int", dest="To", default=10,
                        help="To frequency")
    # add option to descide which to run 
    (options, args) = parser.parse_args()

    


    board_1 = 0*np.ones([2,6]).astype('uint8')
    board_2 = 1*np.ones([2,6]).astype('uint8')
    board_3 = 2*np.ones([2,6]).astype('uint8')
    board_mapping = np.vstack((board_1, board_2, board_3))

    pins = np.arange(0, 12).reshape([2,6])
    pin_mapping = np.vstack([pins]*3).astype('uint8')

    fanarray = FanArray(board_mapping, pin_mapping, options.avg_speed, options.Npulse, options.To, topic=options.topic)

    if options.program == 'main':    
        fanarray.main()
    elif options.program == 'turbulence':
        fanarray.turbulence()
    elif options.program == 'laminar':
        fanarray.laminar()
    elif options.program == 'shear':
        fanarray.shear()
    elif options.program == 'step':
        fanarray.step()
    elif options.program == 'impulse':
        fanarray.impulse()
    elif options.program == 'hz':
        fanarray.hz()

    # fanarray.mainrurb()
    # fanarray.update_single_fan_board_pin()

