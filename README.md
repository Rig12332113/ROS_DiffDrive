# Differential Drive and camera simulation with Gazebo
This repo contains the urdf and gazebo plugin for gazebpo simulation. 

https://github.com/user-attachments/assets/a09042b4-92fb-42aa-a899-aa9f6484632f

# Change to ros2_control:
Note: The diff_cont is listen to topic diff_cont/cmd_vel.
      The params use_stamped_vel cannot be set, so please directly publish stamped twist to control the robot.

'''
ros2 topic pub /diff_cont/cmd_vel_unstamped geometry_msgs/msg/Twist "{
  linear: {x: 0.5},
  angular: {z: 0.1}
}" -1
'''

