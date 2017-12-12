# iai_manual_tool_calib
A ROS utility to manually calibrate a tool with respect to the end-effector of a robot.

![rviz view](https://raw.githubusercontent.com/code-iai/iai_manual_tool_calib/master/doc/pr2_spoon_calib.png)

## Value Proposition
Quickly calibrate a tool with respect to the end-effector of a robot!

When setting up experiments into robotic tool usage, we often want to calibrate a tool with respect to the end-effector of the robot that performs the experiment. A quick way to do this is to visualize both the current point cloud measurements of the robot and the tool mesh in RVIZ. Then, you can iteratively improve the transform between the end-effector and the tool mesh until both overlap nicely. 

We call this manual calibration because you, the human operator, are responsible for visually inspecting and adapting the tool transform. This tool helps you with this task by using ROS visualization markers and interactive markers.

## Example: Calibrating a cup within the left gripper of the PR2
This repository contains a simple example to show how to use this tool. You will calibrate a cup within the left gripper of the PR2.

First, start your real or simulated PR2 (either will be fine). Then, use this launch-file:

```shell
$ roslaunch iai_manual_tool_calib pr2_cup_example.launch
```

This bring up RVIZ with all necessary plugins loaded. You should see the PR2 and the interactive markers next to the left gripper. 

Pull on the interactive markers until you like the calibration.

Everytime you pull, the calibration tool will print the current transform on the terminal. You should see something like this:

```shell
[INFO] [1513065815.559363]: Current Marker Pose for package://iai_manual_tool_calib/meshes/cup_eco_orange.dae:
[INFO] [1513065815.560841]: 
header: 
  seq: 48
  stamp: 
    secs: 1513065815
    nsecs: 524611922
  frame_id: l_gripper_tool_frame
pose: 
  position: 
    x: 0.1144426018
    y: 0.00828198250383
    z: -0.0153962718323
  orientation: 
    x: 0.637363195419
    y: 0.00705598853528
    z: 0.00583671033382
    w: 0.770509362221
```
Copy the transform data wherever you need it.

## Generic Usage
There is a generic launch-file that you can use with your own robot/application:

```
$ roslaunch iai_manual_tool_calib tool_calib.launch
```
This launch file takes three arguments:
  * frame_id (no default): The frame w.r.t. which you want to calibrate. This is also the reference frame for all markers.
  * mesh_resource (no default): ROS resouce identifier for your mesh, e.g. ```package://my_pkg/my_mesh.dae```.
  * marker_scale (default: 1): A scaling factor to be used with your mesh.
