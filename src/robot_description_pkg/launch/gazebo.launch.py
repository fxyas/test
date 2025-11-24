from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    pkg_name = 'robot_description_pkg'

    # Path to URDF
    urdf_path = os.path.join(
        get_package_share_directory(pkg_name),
        'urdf',
        'amr.urdf'
    )

    # Path to custom world file
    world_path = os.path.join(
        get_package_share_directory(pkg_name),
        'worlds',
        'custom_world.world'
    )

    # Path to models directory
    models_path = os.path.join(
        get_package_share_directory(pkg_name),
        'models'
    )

    # Set GAZEBO_MODEL_PATH to include custom models
    set_gazebo_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=models_path + ':' + os.environ.get('GAZEBO_MODEL_PATH', '')
    )

    #  Launch Gazebo with custom world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ),
        launch_arguments={'world': world_path}.items()
    )

    # Publish robot state
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': open(urdf_path).read()}],
        output='screen'
    )

    #  Spawn the robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'amr',
            '-file', urdf_path,
            '-x', '0', '-y', '0', '-z', '0.1'
        ],
        output='screen'
    )

    return LaunchDescription([
        set_gazebo_model_path,
        gazebo,
        rsp_node,
        spawn_entity
    ])
