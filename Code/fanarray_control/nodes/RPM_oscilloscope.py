#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.animation as animate
from mpl_toolkits.mplot3d import Axes3D
import roslib
import numpy as np
import rospy
from std_msgs.msg import Float32, Float64MultiArray,UInt16MultiArray
import time

fig = plt.figure()
ax = plt.axes()
R0 = []
R1 = []
R2 = []
R3 = []
R4 = []
R5 = []
#z_vec = []

tcall = time.time()
def trigger_callback(analog_data):
        tcall = time.time()
        obj_ids = []
        R0.append(analog_data.data[0])
        R1.append(analog_data.data[7])
        R2.append(analog_data.data[14])
        R3.append(analog_data.data[21])
        R4.append(analog_data.data[28])
        R5.append(analog_data.data[35])




def braid_sub():
	rospy.init_node("Oscilloscope", anonymous = True)
	rospy.Subscriber("/faststuff",UInt16MultiArray, trigger_callback)
	#rospy.spin()
	plt.show(block = True)
	
def animate_(i, R0, R1, R2, R3, R4, R5):
		plt.style.use('seaborn-white')
		R0 = R0[-100:]
		R1 = R1[-100:]
		R2 = R2[-100:]
		R3 = R3[-100:]
		R4 = R4[-100:]
		R5 = R5[-100:]
		#z_vec = z_vec[-1000:]
		ax.clear()
		#ax.set_ylim(-.3,.3)
		#ax.set_xlim(-.5,.5)
		#ax.set_zlim(0,.5)
		ax.spines["top"].set_visible(False)
		ax.spines["right"].set_visible(False)
		ax.plot(R0, label = "row0", color = "blue")
		ax.plot(R1, label = "row1", color = "red")
		ax.plot(R2, label = "row2", color = "orange")
		ax.plot(R3, label = "row3", color = "green")
		# ax.plot(R4, label = "row4", color = "purple")
		ax.plot(R5, label = "row5", color = "black")	
		ax.set_ylabel('RPMs')
		ax.legend()

ani = animate.FuncAnimation(fig, animate_, fargs=(R0, R1, R2, R3, R4, R5), interval=10)
#plt.show()
if __name__ == "__main__":
	braid_sub()

