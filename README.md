# auto-uav
Autonomous drone for site analysis

roslaunch px4 openuav.launch vehicle:=iris <br />

rosservice call /mavros/set_mode "base_mode: 0" <br />
rosservice call /mavros/set_mode "custom_mode: 'OFFBOARD'" <br />
rosservice call /mavros/cmd/arming "value: true"

ROS_NAMESPACE=/uav_cam_down/ rosrun image_proc image_proc <br />
roslaunch apriltags_ros example.launch

rqt
