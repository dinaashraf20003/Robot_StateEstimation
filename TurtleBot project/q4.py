#! /usr/bin/env python

import rospy
import numpy as np
import tf
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import Imu
import time
from IPython.display import clear_output

rospy.init_node('q4')
filtered_heading_pub= rospy.Publisher('/filtered_heading',Float32MultiArray,queue_size=1)
rate = rospy.Rate(2)
odom=0
noise_yaw = []
noise_angular = []
filtered_yaw = []
filtered_angular = []
yaw_imu = 0
angular_imu =0
yaw_odom = 0
angular_odom =0
x_k = np.array([0.073183581233, 0.173288971186])
p_k = ([[0.25**2,0],[0,0.5]])
seconds = time.time()
f= np.array([[1,seconds],[0,1]])
w= np.array([0.25**2,0.3**2])
q= np.array([[0.25**2,0],[0,0.3**2]])
r= np.array([0.5])
v= np.array([0.5])
h= np.array([[1,0],[0,1]])
z_k=np.array([0.000827047832819])
I=np.eye(2,2)
counter = 0

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def imu_callback(msg):
	explicit_quat = [msg.orientation.x,msg.orientation.y,msg.orientation.z,msg.orientation.w]
	global yaw_imu	
	(roll_imu, pitch_imu, yaw_imu) = tf.transformations.euler_from_quaternion(explicit_quat)
	global angular_imu 
	angular_imu = msg.angular_velocity.z
	global z_k
	z_k[0] = yaw_imu
	#print(z_k)
	#rospy.loginfo("yaw imu: ")
	#rospy.loginfo(yaw_imu)
	#rospy.loginfo("vel imu: ")
	#rospy.loginfo(angular_imu )

def noise_callback(msg):
	yaw_odom= msg.data[0]
	angular_odom = msg.data[1]
	global noise_yaw, noise_angular, filtered_yaw, filtered_angular
	noise_yaw.append(yaw_odom)
	noise_angular.append(angular_odom)
	global x_k
	x_k[0] = yaw_odom
	x_k[1] = angular_odom
	#print(x_k)
	#rospy.loginfo("yaw odom: ")
	#rospy.loginfo(yaw_odom)
	#rospy.loginfo("vel odom: ")
	#rospy.loginfo(angular_odom)
	now = time.time()
        global f, p_k, w, q, h, I, v, r, p_est, x_res
        f= np.array([[1, 0.01],[0,1]])
        x_est= np.dot(f,x_k)+w 
        #print(x_est)
        p_est= np.dot(np.dot(f, p_k), f.T) + q
        #print(p_est)
        y= z_k-np.dot(h,x_est)
        s= np.dot(np.dot(h, p_k), h.T) + r
        s_inv = np.array([[s[0][0], s[1][0]], [s[0][1], s[1][1]]])
        #print(s)
        k= np.dot(p_est,np.dot(h.T,s_inv))
        x_res=x_est+np.dot(k,y)
        p_k=np.dot((I- np.dot(k,h)),p_est)
	print(x_res)
        filtered_yaw.append(x_res[0])
        filtered_angular.append(x_res[1])
        filtered_heading_pub.publish(Float32MultiArray(data = x_res))
	
	#plt.plot(noise_yaw)
        #plt.plot(noise_angular)	
        #plt.plot(filtered_yaw)
        #plt.plot(filtered_angular)
        #plt.show()
	#plt.close()
	#plt.show()
def animate(i):
	global noise_yaw, noise_angular, filtered_yaw, filtered_angular
	ax1.clear()
	ax1.plot(noise_yaw, 'b')
	ax1.plot(noise_angular, 'orange')
	ax1.plot(filtered_yaw, 'g')
	ax1.plot(filtered_angular, 'r')
while not rospy.is_shutdown(): 
  
  rospy.Subscriber("/imu",Imu,imu_callback)
  rospy.Subscriber('/noisy_state',Float32MultiArray,noise_callback)
  ani = animation.FuncAnimation(fig, animate, interval=100)
  plt.show()
  rate.sleep()
