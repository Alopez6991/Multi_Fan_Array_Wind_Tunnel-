#!/usr/bin/env python
from __future__ import print_function
from time import sleep
from os import system


from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                   AiInputMode, Range, AInFlag)

import rospy
import sys
from std_msgs.msg import String
from std_msgs.msg import Float64


def AnalogInputHandler():

    pub = rospy.Publisher('analog_output', Float64, queue_size=10)
    rate = rospy.Rate(500)
    daq_device = None
    try:
        # Get a list of available DAQ devices
        devices = get_daq_device_inventory(InterfaceType.USB)
        # Create a DaqDevice Object and connect to the device
        daq_device = DaqDevice(devices[0])
        daq_device.connect()
        # Get AiDevice and AiInfo objects for the analog input subsystem
        ai_device = daq_device.get_ai_device()
        ai_info = ai_device.get_info()

        #system('clear')      

        while not rospy.is_shutdown():
            try:
                
                # Display data for the specified analog input channels.
                for channel in range(0,1):
                    data = ai_device.a_in(channel, AiInputMode.SINGLE_ENDED, Range.BIP10VOLTS, AInFlag.DEFAULT)
                    
                    #pub.publish("Voltage = " + str(data))
                    pub.publish(float(data))
                rate.sleep()
            except (ValueError, NameError, SyntaxError):
                break
                    
    except RuntimeError as error:
        print('\n', error)

    finally:
        if daq_device:
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()


def reset_cursor():
    """Reset the cursor in the terminal window."""
    stdout.write('\033[1;1H')

    
if __name__ == '__main__':
    rospy.init_node('analog_handler', anonymous=True)
    
    try:
        ns=AnalogInputHandler()
    except rospy.ROSInterruptException: 
        pass
