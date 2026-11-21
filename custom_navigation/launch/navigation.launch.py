import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    nav_share = get_package_share_directory('custom_navigation')
    bringup_share = get_package_share_directory('diff_drive_bringup')
    nav2_share = get_package_share_directory('nav2_bringup')

    default_map = os.path.join(bringup_share, 'maps', 'room_map.yaml')
    default_params = os.path.join(nav_share, 'config', 'nav2_params.yaml')
    rviz_config = os.path.join(nav2_share, 'rviz', 'nav2_default_view.rviz')

    map_arg = DeclareLaunchArgument(
        'map', default_value=default_map, description='Path to map yaml')
    params_arg = DeclareLaunchArgument(
        'params_file', default_value=default_params, description='Nav2 params')

    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_share, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': LaunchConfiguration('map'),
            'params_file': LaunchConfiguration('params_file'),
            'use_sim_time': 'true',
            'autostart': 'true',
        }.items(),
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
        output='screen',
    )

    return LaunchDescription([map_arg, params_arg, nav2, rviz])
