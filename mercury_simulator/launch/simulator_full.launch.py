from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.launch_description import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration as LC
import os

DEFAULT_ROBOT_NAME = "mercury"
DEFAULT_ACTIVE_CONTROL_MODEL = "hybrid"


def determine_launch_files(context, *args, **kwargs):
    # all of the robot namespaced launch files to start
    ns_launch_files: 'list[str]' = []
    ns_launch_file_args: 'list[list[tuple]]' = []
    
    def add_launch_file(file: str, args: 'list[tuple]' = []):
        ns_launch_files.append(file)
        ns_launch_file_args.append(args)
        
    #
    # ADD LAUNCHES HERE. THEY CAN BE CONDITIONAL
    #

    add_launch_file (
        os.path.join(
            get_package_share_directory('mercury_controller'),
            'launch',
            'controller.launch.py'),
        
        #launch args
        [
            ('active_control_enabled', LC('active_control_enabled')),
            ('active_control_model', LC('active_control_model'))
        ]
    )
    
    add_launch_file (
        os.path.join(
            get_package_share_directory('mercury_hardware'),
            'launch',
            'navigation.launch.py'),

        [
            ('sim_enabled', LC('sim_enabled'))
        ]
        
    )
    
    
    add_launch_file (
        os.path.join(
            get_package_share_directory('mercury_mapping'),
            'launch',
            'mapping.launch.py'),
    )

    add_launch_file(
        os.path.join(
            get_package_share_directory('mercury_simulator'),
            'launch',
            'simulator.launch.py'
        ),

        [
            ('robot', LC('robot'))
        ]
    )
    
    #add_launch_file (
    #    os.path.join(
    #        get_package_share_directory('mercury_autonomy'),
    #        'launch',
    #        'autonomy.launch.py') 
    #)
    
    robot_name = LC('robot')
    
    if len(ns_launch_files) != len(ns_launch_file_args):
        print("--------------------------------------------------------")
        print("Launch file list is not the same length as args list!")
        print("This means that someone did something bad!")
        print("Please ensure that launch files are added to")
        print("the description using add_launch_file")
        print("--------------------------------------------------------")
        return []
    
    # set up a list to collect launch descriptions
    ns_descrips = []
    
    # iterate the list of launch files we were given to start
    for i in range(0, len(ns_launch_files)):
        launch_file = ns_launch_files[i]
        args = ns_launch_file_args[i]
        
        ns_descrips.append(
            IncludeLaunchDescription(
                AnyLaunchDescriptionSource(launch_file),
                launch_arguments=[
                    ('namespace', robot_name),
                    ('robot', robot_name)
                ] + args
            )
        )
    
    return ns_descrips
    

def generate_launch_description():
    # create the launch description 
    return LaunchDescription([
        DeclareLaunchArgument(
            'robot',
            default_value=DEFAULT_ROBOT_NAME, 
            description='name of the robot to spawn'),

        DeclareLaunchArgument(
            'active_control_enabled',
            default_value='True',
            description="Whether or not active control is launched with the rest of the system",
        ),
        
        DeclareLaunchArgument(
            'active_control_model',
            default_value=DEFAULT_ACTIVE_CONTROL_MODEL,
            description="The default active control model to use"
        ),

        DeclareLaunchArgument(
            'sim_enabled',
            default_value='True',
            description="Enable simulator to read proper xacro"
        ),
        
        OpaqueFunction(function=determine_launch_files),
    ])
