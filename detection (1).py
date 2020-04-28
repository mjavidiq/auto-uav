import torch
from detecto import core, utils, visualize
import pickle
import rospy
from geometry_msgs.msg import Pose
from sensor_msgs.msg import Image

class Obj_det():
    coor = Pose()
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
    print(torch.cuda.is_available())
    def __init__(self):
        img_coor_pub = rospy.Publisher('our_topic', Pose, queue_size=10)
        img_sub = rospy.Subscriber('/uav_camera_down/image_raw', Image, callback=self.img_sub_cb)
        rate = rospy.Rate(10)
        rate.sleep()

        while not rospy.is_shutdown():
            cur_img = utils.read_image(self.image)
            predictions = self.loaded_model.predict(cur_img)
            labels, boxes, scores = predictions
            self.coor.orientation.x = boxes[0][0]
            self.coor.orientation.y = boxes[0][1]
            self.coor.orientation.z = boxes[0][2]
            self.coor.orientation.w = boxes[0][3]
            img_coor_pub.publish(self.coor)
            rate.sleep()

    def img_sub_cb(self,msg):
        self.image = msg

if __name__ == "__main__":
    Obj_det()
