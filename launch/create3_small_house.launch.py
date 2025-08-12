#!/usr/bin/env python3
# Launch Create3 robot in the small house world using the official Create3 Gazebo launch files

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

ARGUMENTS = [
    DeclareLaunchArgument('x', default_value='-1.0',
                          description='Initial X position'),
    DeclareLaunchArgument('y', default_value='1.0',
                          description='Initial Y position'),
    DeclareLaunchArgument('z', default_value='0.1',
                          description='Initial Z position'),
    DeclareLaunchArgument('yaw', default_value='0.0',
                          description='Initial yaw angle'),
    DeclareLaunchArgument('use_rviz', default_value='false',
                          description='Start rviz'),
    DeclareLaunchArgument('namespace', default_value='',
                          description='Robot namespace'),
]


def generate_launch_description():
    
    # Directories
    pkg_small_house_world = get_package_share_directory('small_house_world')
    
    # Launch configurations
    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    yaw = LaunchConfiguration('yaw')
    robot_name = LaunchConfiguration('robot_name')
    
    # Launch the small house world
    small_house_world_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            pkg_small_house_world, '/launch/small_house_gz.launch.py'
        ])
    )
    
    # Simple robot description - Create3-like robot
    robot_description_content = """<?xml version="1.0"?>
<robot name="create3">
  <link name="base_link">
    <inertial>
      <mass value="3.5"/>
      <origin xyz="0.0 0.0 0.0" rpy="0 0 0"/>
      <inertia ixx="0.06" ixy="0.0" ixz="0.0" iyy="0.06" iyz="0.0" izz="0.12"/>
    </inertial>
    <visual>
      <geometry>
        <cylinder radius="0.17" length="0.10"/>
      </geometry>
      <material name="grey">
        <color rgba="0.5 0.5 0.5 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.17" length="0.10"/>
      </geometry>
    </collision>
  </link>
  
  <link name="left_wheel_link">
    <inertial>
      <mass value="0.1"/>
      <origin xyz="0.0 0.0 0.0" rpy="0 0 0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
    <visual>
      <geometry>
        <cylinder radius="0.036" length="0.027"/>
      </geometry>
      <material name="black">
        <color rgba="0.0 0.0 0.0 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.036" length="0.027"/>
      </geometry>
    </collision>
  </link>
  
  <link name="right_wheel_link">
    <inertial>
      <mass value="0.1"/>
      <origin xyz="0.0 0.0 0.0" rpy="0 0 0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.001"/>
    </inertial>
    <visual>
      <geometry>
        <cylinder radius="0.036" length="0.027"/>
      </geometry>
      <material name="black">
        <color rgba="0.0 0.0 0.0 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.036" length="0.027"/>
      </geometry>
    </collision>
  </link>
  
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel_link"/>
    <origin xyz="0.0 0.12 -0.036" rpy="-1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>
  
  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel_link"/>
    <origin xyz="0.0 -0.12 -0.036" rpy="-1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>
  
  <!-- Gazebo differential drive plugin -->
  <gazebo>
    <plugin filename="gz-sim-diff-drive-system" name="gz::sim::systems::DiffDrive">
      <left_joint>left_wheel_joint</left_joint>
      <right_joint>right_wheel_joint</right_joint>
      <wheel_separation>0.24</wheel_separation>
      <wheel_radius>0.036</wheel_radius>
      <odom_publish_frequency>30</odom_publish_frequency>
      <max_linear_velocity>0.3</max_linear_velocity>
      <min_linear_velocity>-0.3</min_linear_velocity>
      <max_angular_velocity>1.9</max_angular_velocity>
      <min_angular_velocity>-1.9</min_angular_velocity>
      <topic>cmd_vel</topic>
      <odom_topic>odom</odom_topic>
      <frame_id>odom</frame_id>
      <child_frame_id>base_link</child_frame_id>
    </plugin>
  </gazebo>
</robot>"""

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'robot_description': robot_description_content
        }],
    )

    # Spawn robot in Gazebo with delay to ensure world is loaded
    spawn_robot = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='ros_gz_sim',
                executable='create',
                arguments=[
                    '-name', robot_name,
                    '-x', x,
                    '-y', y,
                    '-z', z,
                    '-Y', yaw,
                    '-topic', 'robot_description'
                ],
                output='screen',
            )
        ]
    )

    # ROS-Gazebo bridge for cmd_vel
    cmd_vel_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='cmd_vel_bridge',
        arguments=[
            'cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist'
        ],
        output='screen',
    )

    # ROS-Gazebo bridge for odom
    odom_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='odom_bridge',
        arguments=[
            'odom@nav_msgs/msg/Odometry@gz.msgs.Odometry'
        ],
        output='screen',
    )

    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(small_house_world_launch)
    ld.add_action(robot_state_publisher)
    ld.add_action(spawn_robot)
    ld.add_action(cmd_vel_bridge)
    ld.add_action(odom_bridge)
    
    return ld
