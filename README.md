# auto-uav
Autonomous drone for site analysis

rosservice call /mavros/set_mode "base_mode: 0"__
rosservice call /mavros/set_mode "custom_mode: 'OFFBOARD'"__
rosservice call /mavros/cmd/arming "value: true"__

ROS_NAMESPACE=/uav_cam_down/ rosrun image_proc image_proc__
roslaunch apriltags_ros example.launch

rqt
