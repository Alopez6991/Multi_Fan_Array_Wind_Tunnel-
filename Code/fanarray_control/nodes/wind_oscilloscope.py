#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib.animation as animate
from mpl_toolkits.mplot3d import Axes3D
import roslib
import numpy as np
import rospy
from std_msgs.msg import Float32, Float64MultiArray
import time

fig = plt.figure()
ax = plt.axes()
x_vec = []
y_vec = []
#z_vec = []

tcall = time.time()
def trigger_callback(analog_data):
        tcall = time.time()
        obj_ids = []
        x_vec.append(analog_data.data[0])
        y_vec.append(analog_data.data[1])




def braid_sub():
	rospy.init_node("Oscilloscope", anonymous = True)
	rospy.Subscriber("/analog_output",Float64MultiArray, trigger_callback)
	#rospy.spin()
	plt.show(block = True)
	
def animate_(i, x_vec, y_vec):
		plt.style.use('seaborn-white')
		x_vec = x_vec[-1000:]
		y_vec = y_vec[-1000:]
		#z_vec = z_vec[-1000:]
		ax.clear()
		#ax.set_ylim(-.3,.3)
		#ax.set_xlim(-.5,.5)
		#ax.set_zlim(0,.5)
		ax.spines["top"].set_visible(False)
		ax.spines["right"].set_visible(False)
		ax.plot(x_vec, label = "Volt 1", color = "blue")
		ax.plot(y_vec, label = "Volt 2", color = "orange")	
		ax.legend()

ani = animate.FuncAnimation(fig, animate_, fargs=(x_vec, y_vec), interval=10)
#plt.show()
if __name__ == "__main__":
	braid_sub()

