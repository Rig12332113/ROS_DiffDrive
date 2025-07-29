from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # declare path from share directory
    urdf_path = PathJoinSubstitution([
        FindPackageShare("my_robot_description"),
        "urdf",
        "my_robot.urdf.xacro"
    ])
    gazebo_config_path = PathJoinSubstitution([
        FindPackageShare("my_robot_bringup"),
        "config",
        "gazebo_bridge.yaml"
    ])
    rviz_path = PathJoinSubstitution([
        FindPackageShare("my_robot_description"),
        "rviz",
        "sensor_config.rviz"
    ])

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{
                "robot_description": Command([
                    PathJoinSubstitution([FindExecutable(name="xacro")]),
                    ' ',
                    urdf_path
                ])
            }]
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution([
                FindPackageShare("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            ])),
            launch_arguments={
                "gz_args": PathJoinSubstitution([
                    FindPackageShare("my_robot_bringup"),
                    "worlds",
                    "test_world.sdf -r"
                ])
            }.items()
        ),

        Node(
            package="ros_gz_sim",
            executable="create",
            arguments=["-topic", "robot_description"]
        ),
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            parameters=[
                {"config_file": gazebo_config_path}
            ]
        ),
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", rviz_path],
            output="screen"
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution([
                FindPackageShare("slam_toolbox"),
                "launch",
                "online_async_launch.py"
            ])),
            launch_arguments={
                "slam_params_file": PathJoinSubstitution([
                    FindPackageShare("my_robot_bringup"),
                    "config",
                    "mapper_params_online_async.yaml"
                ]),
                "use_sim_time": "true"
            }.items()
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(PathJoinSubstitution([
                FindPackageShare("nav2_bringup"),
                "launch",
                "navigation_launch.py"
            ])),
            launch_arguments={
                "use_sim_time": "true"
            }.items()
        ),
    ])