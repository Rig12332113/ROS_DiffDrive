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

## Load map to rviz
To load map constructed by slam toolbox, use the following code and run rviz and gazebo.
<img width="3840" height="2160" alt="Screenshot from 2025-07-21 21-46-32" src="https://github.com/user-attachments/assets/39993459-ee78-4a25-b504-7db2d6002006" />

```
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/my_robot_bringup/config/mapper_params_online_async.yaml use_sim_time:=true
```
## amcl
Start map server (through nav2)
```
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=map_save.yaml -p use_sim_time:=true
ros2 run nav2_util lifecycle_bringup map_server
```
If rviz doesn't show up map, change map->topic->Durability policy to transient local.

Start amcl (adaptive monte carlo localization)
```
ros2 run nav2_amcl amcl --ros-args -p use_sim_time:=true
ros2 run nav2_util lifecycle_bringup amcl
```

## Navigation with nav2
Run simulation and load map in previous step first, and launch nav2 for cost_map and navigation.
```
ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true
```
Note: If you can't navigate the robot with goal pose in rviz because of transform rate, try to set transform_timeout in mapper_params_online_async.yaml to higher value.
