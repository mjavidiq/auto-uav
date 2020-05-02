#!/usr/bin/env python3
import torch
from detecto import core, utils, visualize
import pickle
import rospy
import cv2
from geometry_msgs.msg import Pose
from sensor_msgs.msg import Image
#from cv_bridge.boost.cv_bridge_boost import getCvType 
from cv_bridge import CvBridge
import numpy as np

print ("import Complete")
class Obj_det():
    #bridge = CvBridge()
    print ("Class Entered")
    coor = Pose()
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
    print("model loaded")
    flag = False
    def __init__(self):
        rospy.init_node('offboard_test', anonymous=True)
        img_coor_pub = rospy.Publisher('our_topic', Pose, queue_size=10)
        img_sub = rospy.Subscriber('/uav_cam_down/image_raw', Image, self.callback)
        rate = rospy.Rate(10)
        rate.sleep()
        counter = 0
        while not rospy.is_shutdown():
            if self.flag == True:
               #cur_img = utils.read_image(self.image)
               cur_img = self.image
               #frame = self.bridge.imgmsg_to_cv2(cur_img,"bgr8")
               frame = np.frombuffer(self.image.data,np.uint8).reshape(self.image.height,self.image.width, -1)
               #print(type(frame))
               #print(frame.shape)
               #current = cv2.imread(frame,1)

               predictions = self.loaded_model.predict(frame)
               labels, boxes, scores = predictions
               #print(scores , boxes , boxes.tolist())
 
               if boxes.tolist() == []:

                   print("##############################################")
                   #print(self.coor)
                   self.coor.position.x = 0
               else:
                   box = boxes[0].tolist()
                   if scores.tolist()[0]>0.85:
                       counter+=1
                       if counter>=3:
                           self.coor.position.x = 1
                           counter = 0
                   else:
                       self.coor.position.x = 0
                       counter = 0
                   print(scores.tolist()[0])
                   self.coor.orientation.x = box[0]
                   self.coor.orientation.y = box[1]
                   self.coor.orientation.z = box[2]
                   self.coor.orientation.w = box[3]
                   # print(scores)
               img_coor_pub.publish(self.coor)
               rate.sleep()

    def callback(self,msg):
        #print("hi")
        self.flag = True
        self.image = msg
        # print(self.image.height, self.image.width)

if __name__ == "__main__":
    Obj_det()
