# Small House World - Gazebo Migration

This directory contains the migrated version of the Small House World package, updated to work with Gazebo (formerly Ignition) instead of Gazebo Classic.

## Migration Changes

### Dependencies Updated
- **From**: `gazebo_ros`, `gazebo`, `gazebo_plugins` 
- **To**: `ros_gz_sim`, `ros_gz_bridge`, `gz-sim`

### Package Name
- **From**: `aws_robomaker_small_house_world`
- **To**: `small_house_world`

### Key Files

#### Original Files (Gazebo Classic)
- `launch/small_house.launch.py` - Uses `gazebo_ros`
- `launch/view_small_house.launch.py` - GUI version for Gazebo Classic
- `worlds/small_house.world` - Original SDF 1.6 world file

#### New Files (Gazebo)
- `launch/small_house_gz.launch.py` - Uses `ros_gz_sim`
- `launch/view_small_house_gz.launch.py` - GUI version for Gazebo
- `worlds/small_house_gz.world` - Updated SDF 1.8 world file with Gazebo plugins
- `param/gz_bridge_config.yaml` - ROS-Gazebo bridge configuration

### World File Improvements

The new `small_house_gz.world` includes:
- Updated SDF version (1.8)
- Gazebo system plugins:
  - `gz-sim-physics-system` - Physics simulation
  - `gz-sim-user-commands-system` - User commands (play/pause/reset)
  - `gz-sim-scene-broadcaster-system` - Scene management
- Enhanced camera configuration
- Improved physics settings
- Better lighting (shadows enabled)

### ROS-Gazebo Bridge

The package includes a comprehensive bridge configuration (`param/bridge_config.yaml`) that supports:
- Clock synchronization (`/clock`)
- Sensor data (cameras, lidar, IMU)
- Robot control (`/cmd_vel`)
- Odometry and joint states
- Transform data (`/tf`, `/tf_static`)

## Usage

### Launch Gazebo World (Headless)
```bash
ros2 launch small_house_world small_house_gz.launch.py gui:=false
```

### Launch Gazebo World (with GUI)
```bash
ros2 launch small_house_world view_small_house_gz.launch.py
```

### Custom Bridge Configuration
To use the full bridge configuration for robot integration:

1. Edit `launch/small_house_gz.launch.py`
2. Uncomment the `full_bridge` node
3. Customize `param/bridge_config.yaml` for your specific robot topics

### Integration with Navigation

For Nav2 integration, ensure:
1. Your robot model includes appropriate sensors (lidar, cameras, etc.)
2. The bridge is configured for your robot's topics
3. Use `use_sim_time:=true` in your navigation launch files

## Backwards Compatibility

Both versions are maintained:
- Use `*_gz.launch.py` files for Gazebo (recommended)
- Use original `*.launch.py` files for Gazebo Classic (legacy)

## Benefits of Migration

1. **Modern Simulation**: Latest Gazebo with better performance and features
2. **Better Integration**: Improved ROS 2 integration via `ros_gz_bridge`
3. **Future-Proof**: Gazebo Classic is deprecated, Gazebo is actively developed
4. **Enhanced Graphics**: Better rendering and visual quality
5. **Modular Architecture**: Cleaner plugin system and better extensibility

## Troubleshooting

### Common Issues

1. **Models not loading**: Ensure `GZ_SIM_RESOURCE_PATH` includes the models directory
2. **Bridge not working**: Check that topic names match between ROS and Gazebo
3. **Performance issues**: Adjust physics settings in the world file

### Dependencies
Make sure you have installed:
```bash
sudo apt install ros-${ROS_DISTRO}-ros-gz-sim ros-${ROS_DISTRO}-ros-gz-bridge
```

For development builds, the package is configured to build with the Docker environment in this repository.
