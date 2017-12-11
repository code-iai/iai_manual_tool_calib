#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Quaternion, Vector3
from geometry_msgs.msg._PoseStamped import PoseStamped
from interactive_markers.interactive_marker_server import InteractiveMarkerServer
from std_msgs.msg import ColorRGBA
from visualization_msgs.msg import InteractiveMarker, InteractiveMarkerControl, InteractiveMarkerFeedback, Marker


class ToolCalib(object):
    def __init__(self):
        rospy.loginfo("Constructor got called")

        self.frame_id = rospy.get_param("~frame_id")
        self.mesh_resource = rospy.get_param("~mesh_resource")

        self.server = InteractiveMarkerServer("tool_calib")
        self.server.insert(self.create_6dof_marker(), self.marker_callback)
        self.server.applyChanges()

        self.tool_marker = Marker()
        self.tool_marker.header.frame_id = self.frame_id
        self.tool_marker.header.stamp = rospy.get_rostime()
        self.tool_marker.pose.orientation.w = 1
        self.tool_marker.ns = "tool_marker"
        self.tool_marker.id = 1
        self.tool_marker.action = Marker.ADD
        self.tool_marker.type = Marker.MESH_RESOURCE
        self.tool_marker.color = ColorRGBA(1.0, 1.0, 1.0, 1.0)
        self.tool_marker.scale = Vector3(1.0, 1.0, 1.0)
        self.tool_marker.frame_locked = True
        self.tool_marker.mesh_resource = self.mesh_resource
        self.tool_marker.mesh_use_embedded_materials = True

        self.marker_pub = rospy.Publisher("/visualization_marker", Marker, queue_size=1)

    def create_6dof_marker(self):
        imarker = InteractiveMarker()
        imarker.header.frame_id = self.frame_id
        imarker.pose.orientation.w = 1
        imarker.name = "tool_calib"
        imarker.name = "Tool Calibration"
        imarker.scale = 0.2

        control = InteractiveMarkerControl()
        control.orientation = Quaternion(0, 0, 0, 1)
        control.name = "rotate_x"
        control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        imarker.controls.append(control)

        control = InteractiveMarkerControl()
        control.orientation = Quaternion(0, 0, 0, 1)
        control.name = "move_x"
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        imarker.controls.append(control)

        control = InteractiveMarkerControl()
        control.orientation = Quaternion(0, 1, 0, 1)
        control.name = "rotate_z"
        control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        imarker.controls.append(control)

        control = InteractiveMarkerControl()
        control.orientation = Quaternion(0, 1, 0, 1)
        control.name = "move_z"
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        imarker.controls.append(control)

        control = InteractiveMarkerControl()
        control.orientation = Quaternion(0, 0, 1, 1)
        control.name = "rotate_y"
        control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
        imarker.controls.append(control)

        control = InteractiveMarkerControl()
        control.orientation = Quaternion(0, 0, 1, 1)
        control.name = "move_y"
        control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
        imarker.controls.append(control)

        return imarker


    def marker_callback(self, data):
        if data.event_type == InteractiveMarkerFeedback.MOUSE_UP:
            rospy.loginfo("Current Marker Pose for %s:", self.mesh_resource)
            self.tool_marker.header = data.header
            self.tool_marker.pose = data.pose
            self.marker_pub.publish(self.tool_marker)
            rospy.loginfo("\n%s", PoseStamped(data.header, data.pose))
        self.server.applyChanges()

if __name__ == '__main__':
    rospy.init_node("tool_calib")
    my_tool_calib = ToolCalib()
    rospy.spin()