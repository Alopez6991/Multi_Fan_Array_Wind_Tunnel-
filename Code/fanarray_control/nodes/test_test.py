#!/usr/bin/env python
import rospy
from optparse import OptionParser
import numpy as np
from std_msgs.msg import UInt8MultiArray

class FanArray(object):
    def __init__(self, board_mapping, pin_mapping, avg_speed, topic='/one_fan_at_a_time'):
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
         # code from board and pin maping 

        self.publisher = rospy.Publisher(topic, UInt8MultiArray, queue_size=100)


    def main(self):
    	print('one')
        rospy.spin()
        print('two')


    def turbulence (self):
        r = rospy.Rate(.001)
        print('outside')
        while not rospy.is_shutdown():
            print('hello world') 
            r.sleep()



        
        


if __name__ == '__main__':
    rospy.init_node('fan_array_control', anonymous=True)
    parser = OptionParser()
    parser.add_option("--topic", type="str", dest="topic", default='/one_fan_at_a_time',
                        help="rostopic to publish to")
    parser.add_option("--program", type="str", dest="program", default='main',
                        help="program to run (main or turbulence)")
    parser.add_option("--avg_speed", type="int", dest="avg_speed", default=70,
                        help="mean fan speed between 0 and 100")
    # add option to descide which to run 
    (options, args) = parser.parse_args()

    


    board_1 = 0*np.ones([2,6]).astype('uint8')
    board_2 = 1*np.ones([2,6]).astype('uint8')
    board_3 = 2*np.ones([2,6]).astype('uint8')
    board_mapping = np.vstack((board_1, board_2, board_3))

    pins = np.arange(0, 12).reshape([2,6])
    pin_mapping = np.vstack([pins]*3).astype('uint8')

    fanarray = FanArray(board_mapping, pin_mapping, options.avg_speed, topic=options.topic)

    if options.program == 'main':    
        fanarray.main()
    elif options.program == 'turbulence':
        fanarray.turbulence()
    # fanarray.mainrurb()
    # fanarray.update_single_fan_board_pin()

