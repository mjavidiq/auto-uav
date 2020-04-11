"""
testing offboard positon control with a simple takeoff script
"""

import rospy
import mavros
from mavros import command
from mavros_msgs.msg import *
from mavros_msgs.srv import *
from geometry_msgs.msg import PoseStamped, Point, Quaternion , PoseArray
import math
import numpy

class OffbPosCtl:
    curr_pose = PoseStamped()
    des_pose = PoseStamped()
    isReadyToFly = False
    tagDetected = False
    x_cam = 0
    y_cam = 0

    def __init__(self):
        rospy.init_node('offboard_test', anonymous=True)
        pose_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)
        tag_pose = rospy.Subscriber('/tag_detections_pose', PoseArray, callback=self.tag_pose_cb)
        mocap_sub = rospy.Subscriber('/mavros/local_position/pose', PoseStamped, callback=self.mocap_cb)
        state_sub = rospy.Subscriber('/mavros/state', State, callback=self.state_cb)

        rate = rospy.Rate(10)  # Hz
        rate.sleep()
        self.des_pose = self.copy_pose(self.curr_pose)
	current_x = self.curr_pose.pose.position.x
	current_y = self.curr_pose.pose.position.y
	distThreshold = 0.2
	del_val = 0.2
	pre_z =8
	flag = False
        while not rospy.is_shutdown():
            if self.isReadyToFly:
		des_z =  pre_z  
		if self.tagDetected:		
			if abs(self.x_cam) > 0.2:
				des_y = current_y - del_val*self.x_cam
				print "Correcting..",self.x_cam, self.y_cam, des_z
			if abs(self.y_cam) > 0.2:
				des_x = current_x - del_val*self.y_cam
				print "Correcting..",self.x_cam, self.y_cam, des_z
			if abs(self.x_cam)<0.2 and abs(self.y_cam)<0.2 and flag == False:
				#self.tagDetected = False
				pre_z = des_z - 0.03*des_z
				des_y = current_y
				des_x = current_x
				des_z = pre_z 		
				if pre_z<0.25:
					flag = True
					self.setLandMode()
					#self.setDisarm()
					self.tagDetected = False
					print "Arming",pre_z

				print "Corrected", des_z
		else:
			if pre_z <0.25 and not flag:
				print "Landing undetected"
				self.setLandMode()
				flag = True
				print self.tagDetected ,pre_z
			if pre_z < 0.75 and not flag:
				distThreshold = 0.01
				pre_z = pre_z - 0.02
				des_z = pre_z

			des_y = current_y
			des_x = current_x
			
                self.des_pose.pose.position.x = des_x
                self.des_pose.pose.position.y = des_y
                self.des_pose.pose.position.z = des_z

                curr_x = self.curr_pose.pose.position.x
                curr_y = self.curr_pose.pose.position.y
                curr_z = self.curr_pose.pose.position.z

                dist = math.sqrt((curr_x - des_x)*(curr_x - des_x) + (curr_y - des_y)*(curr_y - des_y) + (curr_z - des_z)*(curr_z - des_z))
                if dist < distThreshold:
                    current_x = curr_x
                    current_y = curr_y
		    
            pose_pub.publish(self.des_pose)
            rate.sleep()

    def tag_pose_cb(self,msg):
	if msg.poses != []:
		self.tagDetected = True
		self.x_cam = msg.poses[0].position.x
		self.y_cam = msg.poses[0].position.y
	else:
		self.tagDetected = False

#################DO NOT TOUCH BELOW #########################
    def copy_pose(self, pose):
        pt = pose.pose.position
        quat = pose.pose.orientation
        copied_pose = PoseStamped()
        copied_pose.header.frame_id = pose.header.frame_id
        copied_pose.pose.position = Point(pt.x, pt.y, pt.z)
        copied_pose.pose.orientation = Quaternion(quat.x, quat.y, quat.z, quat.w)
        return copied_pose

    def mocap_cb(self, msg):
        # print msg
        self.curr_pose = msg

    def state_cb(self,msg):
        print msg.mode
        if(msg.mode=='OFFBOARD'):
            self.isReadyToFly = True
            print "readyToFly"

    def setDisarm(self):
   	rospy.wait_for_service('/mavros/cmd/arming')
   	try:
       		armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
       		armService(False)
   	except rospy.ServiceException, e:
    		print "Service arm call failed: %s"%e

    def setLandMode(self):
   	rospy.wait_for_service('/mavros/cmd/land')
   	try:
       		landService = rospy.ServiceProxy('/mavros/cmd/land', mavros_msgs.srv.CommandTOL)
       		#http://wiki.ros.org/mavros/CustomModes for custom modes
       		isLanding = landService(altitude = 0, latitude = 0, longitude = 0, min_pitch = 0, yaw = 0)
   	except rospy.ServiceException, e:
       		print "service land call failed: %s. The vehicle cannot land "%e

if __name__ == "__main__":
    OffbPosCtl()
