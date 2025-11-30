
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import math
import time


class FloatingPosePublisher(Node):

    def __init__(self):
        super().__init__('floating_pose_publisher')

        self.publisher_ = self.create_publisher(PoseStamped, 'floating_pose', 10)
        self.timer = self.create_timer(0.02, self.timer_callback)  # 50 Hz

        self.start_time = time.time()


    def timer_callback(self):
        now = time.time() - self.start_time

        # Floating along Z (sin wave)
        z = 1.0 + 0.5 * math.sin(now * 1.5)   # adjust amplitude + speed

        # Rotation around Z (yaw)
        yaw = now                              # 1 rad/sec
        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)

        # Build PoseStamped
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "map"

        # Position
        msg.pose.position.x = 0.0
        msg.pose.position.y = 0.0
        msg.pose.position.z = z

        # Orientation (only Z rotation)
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = qz
        msg.pose.orientation.w = qw

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FloatingPosePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
