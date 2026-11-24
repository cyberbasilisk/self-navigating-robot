## Self-Navigating Differential-Drive Robot

A custom differential-drive robot that builds a map of a room with SLAM, localizes on that map and drives itself to goal points using Nav2. Everything runs in Gazebo Harmonic with ROS2 Jazzy.

### Steps

1. **Mapping**: Drive the robot through the room with keyboard teleop while `slam_toolbox` builds a map from LIDAR scans.
2. **Localization**: AMCL (particle-filter localization) matches live scans against the saved map to estimate where the robot is.
3. **Navigation**: Give Nav2 a goal in RViz. It plans a route on the map, follows it, and avoids obstacles on the way.

<img width="1000" height="500" alt="nav_slam" src="https://github.com/user-attachments/assets/831b9121-01d1-4f4e-bd41-cb1cd302f1c7" />

### Architecture

Two phases, run separately:

- **Mapping**: `slam_toolbox` publishes the map and the `map → odom` transform.
- **Navigation**: `map_server` loads the saved map, AMCL publishes `map → odom`, and Nav2 plans and drives.

SLAM and AMCL should not run at the same time because they both publish `map → odom`, which could create conflict.

### Packages

| Package | Purpose |
|---|---|
| `diff_drive_bringup` | Robot URDF/xacro, the room world, the Gazebo to ROS2 bridge config, saved maps, RViz configs, sim launch file |
| `custom_navigation` | Nav2 launch file and a script that generates the Nav2 parameter file for this robot |

### Tuning

Nav2's defaults are tuned for a TurtleBot3, which is larger than this robot. `custom_navigation/tools/make_params.py` copies the default parameter file from the installed Nav2 and adjusts it.

| Parameter | Value | Reason |
|---|---|---|
| `robot_radius` (both costmaps) | 0.15 m | Chassis is 0.20 × 0.15 m, so the circumscribed radius is about 0.13 m, plus margin |
| `inflation_radius` (both costmaps) | 0.4 m | Keeps a safe distance from walls without closing off the narrower parts of the room |
| AMCL initial pose | (0, 0, 0) | The map origin is where the robot started when mapping, which is its spawn point |

Generating the file from the installed defaults, instead of hand-writing one, keeps it consistent with whichever Nav2 version is installed.



