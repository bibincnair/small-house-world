# /*******************************************************************************
# * Copyright 2019 ROBOTIS CO., LTD.
# * Copyright 2024 AWS RoboMaker (Modified for Gazebo)
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *     http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# *******************************************************************************/

# /* Author: Darby Lim, Modified for Gazebo (Ionic) */

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    world_file_name = 'small_house_gz.world'
    package_dir = get_package_share_directory('small_house_world')
    world_path = os.path.join(package_dir, 'worlds', world_file_name)
    bridge_config = os.path.join(package_dir, 'param', 'gz_bridge_config.yaml')
    
    # Set Gazebo resource path to include our models
    gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=os.path.join(package_dir, 'models')
    )
    
    # Gazebo sim launch
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('ros_gz_sim'),
            '/launch/gz_sim.launch.py'
        ]),
        launch_arguments={
            'gz_args': ['-r -v 4 ', world_path],
            'on_exit_shutdown': 'true'
        }.items()
    )
    
    # ROS-Gazebo bridge for clock (essential)
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )
    
    # Optional: Full bridge configuration (uncomment if needed)
    # full_bridge = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=['--ros-args', '-p', f'config_file:={bridge_config}'],
    #     output='screen'
    # )
    
    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value=world_path,
            description='SDF world file'
        ),
        DeclareLaunchArgument(
            'gui',
            default_value='true',
            description='Set to "false" to run headless.'
        ),
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation time'
        ),
        gz_resource_path,
        gz_sim,
        clock_bridge,
    ])


if __name__ == '__main__':
    generate_launch_description()
