#!/usr/bin/env python3
# Launch Create3 robot in the small house world
# This approach copies the small house world to the expected location for Create3

import os
import shutil
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
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


def setup_world_for_create3(context, *args, **kwargs):
    """Copy the small house world to create3_gz expected location"""
    
    try:
        # Get package directories
        pkg_small_house_world = get_package_share_directory('small_house_world')
        pkg_create3_gz_bringup = get_package_share_directory('irobot_create_gz_bringup')
        
        # Source and destination paths
        src_world = os.path.join(pkg_small_house_world, 'worlds', 'small_house_gz.world')
        dest_worlds_dir = os.path.join(pkg_create3_gz_bringup, 'worlds')
        dest_world = os.path.join(dest_worlds_dir, 'small_house_gz.sdf')
        
        # Create destination directory if it doesn't exist
        os.makedirs(dest_worlds_dir, exist_ok=True)
        
        # Copy the world file
        if os.path.exists(src_world):
            shutil.copy2(src_world, dest_world)
            print(f"Copied world file from {src_world} to {dest_world}")
        
        # Now launch the Create3 with our world
        create3_gz_launch = PathJoinSubstitution([
            pkg_create3_gz_bringup, 'launch', 'create3_gz.launch.py'
        ])
        
        create3_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([create3_gz_launch]),
            launch_arguments=[
                ('world', 'small_house_gz'),  # Use our copied world
                ('x', LaunchConfiguration('x')),
                ('y', LaunchConfiguration('y')),
                ('z', LaunchConfiguration('z')),
                ('yaw', LaunchConfiguration('yaw')),
                ('use_rviz', LaunchConfiguration('use_rviz')),
                ('namespace', LaunchConfiguration('namespace')),
            ]
        )
        
        return [create3_launch]
        
    except Exception as e:
        print(f"Error setting up Create3 with small house world: {e}")
        # Fallback to our custom launch
        pkg_small_house_world = get_package_share_directory('small_house_world')
        
        small_house_world_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                pkg_small_house_world, '/launch/small_house_gz.launch.py'
            ])
        )
        
        return [small_house_world_launch]


def generate_launch_description():
    
    # Create launch description and add actions
    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(OpaqueFunction(function=setup_world_for_create3))
    
    return ld
