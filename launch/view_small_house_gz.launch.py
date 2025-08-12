from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    ld = LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                get_package_share_directory('small_house_world'),
                '/launch/small_house_gz.launch.py'
            ]),
            launch_arguments={
                'gui': 'true'
            }.items()
        )
    ])
    return ld


if __name__ == '__main__':
    generate_launch_description()
