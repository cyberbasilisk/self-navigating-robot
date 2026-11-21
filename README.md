## Self Navigating Differential-Drive Robot

A custom differential-drive robot that builds a map of a room with SLAM, localizes on that map and drives itself to goal points using Nav2. Everything runs in Gazebo Harmonic on ROS2 Jazzy.

### Steps

1. **Mapping**: Drive the robot through the room with keyboard teleop while `slam_toolbox` builds a map from LIDAR scans.
2. **Localization**: AMCL (particle-filter localization) matches live scans against the saved map to estimate where the robot is.
3. **Navigation**: Give Nav2 a goal in RViz. It plans a route on the map, follows it, and avoids obstacles on the way.

### Architecture

Two phases, run separately:

- **Mapping**: `slam_toolbox` publishes the map and the `map → odom` transform.
- **Navigation**: `map_server` loads the saved map, AMCL publishes `map → odom`, and Nav2 plans and drives.

SLAM and AMCL should not run at the same time because they both publish `map → odom`, which could create conflict.

### Packages

| Package | Purpose |
|---|---|
| `diff_drive_bringup` | Robot URDF/xacro, the room world, the Gazebo ↔ ROS2 bridge config, saved maps, RViz configs, sim launch file |
| `custom_navigation` | Nav2 launch file and a script that generates the Nav2 parameter file for this robot |



