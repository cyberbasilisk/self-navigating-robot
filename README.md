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

### Debugging log

1. **Scan points missing in RViz.** Gazebo stamped each scan with its own scoped sensor name, which did not exist in the TF tree, so RViz and SLAM couldn't place the points. Fixed by setting `gz_frame_id` to `lidar_link` on the sensor.

2. **Wheel frames reported transform errors.** The wheel joints are continuous, so their transforms depend on joint angles that Gazebo knew but ROS2 didn't. Fixed by publishing joint states from Gazebo and bridging `/joint_states`.

3. **Map display showed an error in RViz.** `slam_toolbox` publishes the map with transient-local durability, and the display's QoS had to match, the same class of problem as the `BEST_EFFORT` scan topic in Project 1.

4. **Nav2 couldn't find its params file.** The generated file has to exist before `colcon build`, because the build copies it into the install directory. Therefore generate, before build.

5. **`use_sim_time` everywhere.** Every node touching timestamps or transforms needs it set, or messages stamped with sim time get rejected against wall-clock time.

### Running it

```bash
# 1. Generate Nav2 params, then build
python3 custom_navigation/tools/make_params.py
colcon build && source install/setup.bash

# 2. Start the simulation
ros2 launch diff_drive_bringup spawn_robot.launch.py

# 3. Mapping with teleop + SLAM
ros2 run teleop_twist_keyboard teleop_twist_keyboard
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true

# 4. Navigation (stop SLAM and teleop first)
ros2 launch custom_navigation navigation.launch.py
```

In RViz, use **2D Pose Estimate** if the robot looks misplaced, then **2D Goal Pose** to send a goal.

### Tech stack

![ROS2](https://img.shields.io/badge/ROS2-22314E?style=flat&logo=ros&logoColor=white)
![Gazebo](https://img.shields.io/badge/Gazebo-F58113?style=flat&logo=gazebo&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white)
![Nav2](https://img.shields.io/badge/Nav2-blue?style=flat&logo=ros&logoColor=white)


### What's next

- Multi-waypoint patrol using Nav2's waypoint follower.

- Port to real hardware (Raspberry Pi + LIDAR), comparing sim-to-real behavior.
