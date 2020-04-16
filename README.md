# auto-uav
Autonomous drone for site analysis

rosservice call /mavros/set_mode "base_mode: 0"
rosservice call /mavros/set_mode "custom_mode: 'OFFBOARD'"
rosservice call /mavros/cmd/arming "value: true"

ROS_NAMESPACE=/uav_cam_down/ rosrun image_proc image_proc
roslaunch apriltags_ros example.launch

rqt

