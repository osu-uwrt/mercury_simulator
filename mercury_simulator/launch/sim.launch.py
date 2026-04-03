import os
from launch.launch_description import LaunchDescription
from launch.substitutions import LaunchConfiguration as LC
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import AnyLaunchDescriptionSource
from ament_index_python import get_package_share_directory

DEFAULT_ROBOT_NAME = "mercury"
DEFAULT_ACTIVE_CONTROL_MODEL = "hybrid"

def generate_launch_description():

    vehicle_config_path = get_package_share_directory("mercury_descriptions") + "/" + LC("robot")
    simulation_config = get_package_share_directory("mercury_simulator") + "/config/simulator.yaml"



    return LaunchDescription([
        DeclareLaunchArgument(
            'robot',
            default_value=DEFAULT_ROBOT_NAME,
            description="Name of the robot to use."
        ),
        
        launch.actions.GroupAction([
            launch_ros.actions.PushRosNamespace(
                LC("robot")
            ),

            # Launch simulator
            launch_ros.actions.Node(
                package="mercurcy_simulator",
                executable="physics_simulator",
                name="physics_simulator",
                output="screen",
                parameters=[
                    {"vehicle_config_path", get_package_share_directory("mercury_descriptions") + "/" + LC("robot")},
                    {"simulator_config", get_package_share_directory("mercury_simulator") + "/config/simulator.yaml"},
                    {"robot", LC("robot")},
                ]
            ),
        ], scoped=True)
    ])
