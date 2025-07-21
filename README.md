# Differential Drive and camera simulation with Gazebo
This repo contains the urdf and gazebo plugin for gazebpo simulation. 

## Control with gazebo bridge:
```
ros2 launch my_robot_gazebo.launch.xml
```
Note: There is a robot arm for practice. To enable robot arm, uncomment arm
     in my_robot.urdf.xml and joint in mobile_base.

https://github.com/user-attachments/assets/a09042b4-92fb-42aa-a899-aa9f6484632f

## Change control to ros2_control:
First run command to start simulation.
```
ros2 launch my_robot_ros_control.launch.xml
```
Second, spawn controllers: (joint_broad and diff_cont)
```
ros2 run controller_manager spawner joint_broad
ros2 run controller_manager spawner diff_cont
```

After spawn controllers successful, run the following code to control differential drive in gazebo.
Note: The diff_cont is listen to topic diff_cont/cmd_vel.
      The params use_stamped_vel cannot be set, so please directly publish stamped twist to control the robot.

```
ros2 topic pub /diff_cont/cmd_vel_unstamped geometry_msgs/msg/Twist "{
  linear: {x: 0.5},
  angular: {z: 0.1}
}" -1
```

