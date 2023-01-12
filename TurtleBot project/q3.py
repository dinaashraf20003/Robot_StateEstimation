#! /usr/bin/env python

import rospy
import numpy as np
import tf
import matplotlib.pyplot as plt
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

rospy.init_node('q3')
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
noisy_heading_pub= rospy.Publisher('/noisy_state',Float32MultiArray,queue_size=1)
rate = rospy.Rate(2)
move = Twist()
move.linear.x = 0.2
move.angular.z = 0.5  
odom=0
noise_yaw = []
noise_angular = []

def callback(msg):
	odom= msg
	explicit_quat = [msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w]
	(roll, pitch, yaw) = tf.transformations.euler_from_quaternion(explicit_quat)
	yaw = np.random.normal(yaw,0.25,1)[0]	
	angular_rotation = msg.twist.twist.angular.z
	angular_rotation  = np.random.normal(angular_rotation,0.3,1)[0]
	rospy.loginfo("roll: ")
	rospy.loginfo(roll)
	rospy.loginfo("pitch: ")
	rospy.loginfo(pitch)
	rospy.loginfo("yaw: ")
	rospy.loginfo(yaw)
	global noise_yaw, noise_angular
	noisy_state = []
	noisy_state.append(yaw)
	noisy_state.append(angular_rotation)
	noise_yaw.append(yaw)
	noise_angular.append(angular_rotation)
	noisy_heading_pub.publish(Float32MultiArray(data = noisy_state))
       

rospy.Subscriber("/odom",Odometry,callback)

while not rospy.is_shutdown(): 
  plt.plot(noise_yaw)
  plt.plot(noise_angular)
  plt.show()
  pub.publish(move)
  rate.sleep()
