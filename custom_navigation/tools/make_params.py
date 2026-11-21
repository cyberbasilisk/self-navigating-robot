#!/usr/bin/env python3
"""Copy Nav2's default params for this ROS distro and adapt them to robot.

Run once (and again after any Nav2 update):
    python3 ~/ros2_ws/src/custom_navigation/tools/make_params.py
"""
import os
import sys

import yaml

SRC = os.environ.get(
    'NAV2_DEFAULT_PARAMS',
    '/opt/ros/jazzy/share/nav2_bringup/params/nav2_params.yaml')
DST = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '..', 'config', 'nav2_params.yaml')

ROBOT_RADIUS = 0.15      # chassis is 0.20 x 0.15 m, circumscribed radius ~0.13 m
INFLATION_RADIUS = 0.40  # default is larger than this room's gaps really need


def get(d, *keys):
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def main():
    if not os.path.exists(SRC):
        sys.exit(f'Default params not found at {SRC}')
    with open(SRC) as f:
        p = yaml.safe_load(f)

    changed = []
    for cm in ('local_costmap', 'global_costmap'):
        params = get(p, cm, cm, 'ros__parameters')
        if params is None:
            print(f'WARNING: {cm} not found')
            continue
        if 'robot_radius' in params:
            params['robot_radius'] = ROBOT_RADIUS
            changed.append(f'{cm}.robot_radius = {ROBOT_RADIUS}')
        else:
            print(f'NOTE: {cm} uses a footprint, not robot_radius; edit by hand')
        infl = params.get('inflation_layer')
        if isinstance(infl, dict):
            infl['inflation_radius'] = INFLATION_RADIUS
            changed.append(f'{cm}.inflation_radius = {INFLATION_RADIUS}')

    amcl = get(p, 'amcl', 'ros__parameters')
    if amcl is not None:
        amcl['set_initial_pose'] = True
        amcl['initial_pose'] = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'yaw': 0.0}
        changed.append('amcl initial pose = (0, 0, 0)')

    with open(DST, 'w') as f:
        yaml.safe_dump(p, f, sort_keys=False)
    print('Wrote', os.path.normpath(DST))
    print('Changed:')
    for c in changed:
        print('  ', c)


if __name__ == '__main__':
    main()
