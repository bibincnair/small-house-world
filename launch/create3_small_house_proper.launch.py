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
    pkg_irobot_create_gz_bringup = get_package_share_directory('irobot_create_gz_bringup')
    pkg_small_house_world = get_package_share_directory('small_house_world')
    
    # First, we need to make our world available to the Create3 launcher
    # The create3_gz.launch.py expects to find worlds in specific locations
    # We'll create a custom world file that references our small house world
    
    # We need to modify the approach slightly because the Create3 launcher expects
    # world files in a specific format. Let's create a combined launch that:
    # 1. Starts our world
    # 2. Then spawns the Create3 in it
    
    # Launch the small house world first
    small_house_world_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            pkg_small_house_world, '/launch/small_house_gz.launch.py'
        ])
    )
    
    # Then spawn the Create3 robot using the official spawn launch
    create3_spawn_launch = PathJoinSubstitution([
        pkg_irobot_create_gz_bringup, 'launch', 'create3_spawn.launch.py'
    ])
    
    create3_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([create3_spawn_launch]),
        launch_arguments=[
            ('x', LaunchConfiguration('x')),
            ('y', LaunchConfiguration('y')),
            ('z', LaunchConfiguration('z')),
            ('yaw', LaunchConfiguration('yaw')),
            ('namespace', LaunchConfiguration('namespace')),
            ('use_rviz', LaunchConfiguration('use_rviz')),
        ]
    )
    
    # Start the Create3 nodes (sensors, controllers, etc.)
    create3_nodes_launch = PathJoinSubstitution([
        pkg_irobot_create_gz_bringup, 'launch', 'create3_gz_nodes.launch.py'
    ])
    
    create3_nodes = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([create3_nodes_launch]),
        launch_arguments=[
            ('namespace', LaunchConfiguration('namespace')),
        ]
    )

    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(small_house_world_launch)
    ld.add_action(create3_spawn)
    ld.add_action(create3_nodes)
    
    return ld
