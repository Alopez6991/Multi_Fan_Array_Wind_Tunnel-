#!/usr/bin/env python
import rospy
from optparse import OptionParser
from std_msgs.msg import UInt8MultiArray
import numpy as np

class FanArray(object):
    def __init__(self, board_mapping, pin_mapping, topic='/fanarrayNxM'):
        '''
        FanArray is a class to control an array of fans through an arduino. 
        Requires "rosrun rosserial_python serial_node.py /dev/ttyACM0" to communicate with arduino

        Inputs
        ======
        board_mapping: NxM numpy.ndarray with integer values corresponding to the PWM extender board number
                       for each fan in the array
        pin_mapping: NxM numpy.ndarray with integer values corresponding to the PWM pin number on the board

        '''
        # assert board_mapping.shape == pin_mapping.shape
        # assert board_mapping.dtype == np.uint8
        # assert pin_mapping.dtype == np.uint8

        self.board_mapping = board_mapping
        self.pin_mapping = pin_mapping

        self.publisher = rospy.Publisher(topic, UInt8MultiArray, queue_size=100)
        rospy.on_shutdown(self.turn_off_all_fans)

    def update_single_fan_board_pin(self, board, pin, speed):
        '''
        board - PWM extender board number (from 0 to however many board extenders you have)
        pin - PWM pin number (from 0 to 15)
        speed - speed in PWM (from 0 to 100)
        '''
        msg = UInt8MultiArray()
        msg.data = [board, pin, speed]
        self.publisher.publish(msg)

    def update_all_fans(self,speed):
        '''
        updates the speed of all fans in the array to the same value
        '''
        board_numbers = np.unique(self.board_mapping)
        pin_numbers = np.unique(self.pin_mapping)

        msg = UInt8MultiArray()
        msg.data = [speed]
        self.publisher.publish(msg)

        for board_number in board_numbers:
            for pin_number in pin_numbers:
                self.update_single_fan_board_pin(board_number, pin_number,speed)


    def update_single_fan_row_col(self, row, col, speed):
        '''
        row and col correspond to the row and col of the physical fan array
        '''
        board = self.board_mapping[row, col]
        pin = self.pin_mapping[row, col]
        self.update_single_fan(board, pin, speed)

    def update_fan_speeds(self, fan_speed_array):
        '''
        Given an NxM array of PWM speeds for each fan, set the fan speeds.
        '''
        assert fan_speed_array.shape == self.board_mapping.shape
        assert fan_speed_array.dtype == np.uint8

        for row in range(fan_speed_array.shape[0]):
            for col in range(fan_speed_array.shape[1]):
                self.update_single_fan_row_col(row, col, speed)

    def turn_off_all_fans(self):
        board_numbers = np.unique(self.board_mapping)
        pin_numbers = np.unique(self.pin_mapping)

        for board_number in board_numbers:
            for pin_number in pin_numbers:
                self.update_single_fan_board_pin(board_number, pin_number, 0)

    def main(self):
        rospy.spin()

def get_interactive_fan_array_controller():
    rospy.init_node('fan_array_control', anonymous=True)

    board_1 = 0*np.ones([2,6]).astype('uint8')
    board_2 = 1*np.ones([2,6]).astype('uint8')
    board_3 = 2*np.ones([2,6]).astype('uint8')
    board_mapping = np.vstack((board_1, board_2, board_3))

    pins = np.arange(0, 12).reshape([2,6])
    pin_mapping = np.vstack([pins]*3)
    pin_mapping = pin_mapping.astype('uint8')

    fanarray = FanArray(board_mapping, pin_mapping, topic='/fanarrayNxM')    

    return fanarray 


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--topic", type="str", dest="topic", default='/fanarrayNxM',
                        help="rostopic to publish to")
    (options, args) = parser.parse_args()

    rospy.init_node('fanarray_control', anonymous=True)
    # rospy.init_node('one_fan_at_a_time', anonymous=True)


    board_1 = 0*np.ones([2,6]).astype('uint8')
    board_2 = 1*np.ones([2,6]).astype('uint8')
    board_3 = 2*np.ones([2,6]).astype('uint8')
    board_mapping = np.vstack((board_1, board_2, board_3))

    pins = np.arange(0, 12).reshape([2,6])
    pin_mapping = np.vstack([pins]*3).astype('uint8')

    fanarray = FanArray(board_mapping, pin_mapping, topic=options.topic)    
    fanarray.main()
    # fanarray.update_single_fan_board_pin()

