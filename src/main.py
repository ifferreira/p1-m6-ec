from collections import deque
import argparse
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from time import sleep

parser = argparse.ArgumentParser(description='p1-m6-ec')
parser.add_argument('vx', metavar='vx', type=float, help='x axis vel for the turtle')
parser.add_argument('vy', metavar='vy', type=float, help='y axis vel for the turtle')
parser.add_argument('vt', metavar='vt', type=float, help='rotational vel for the turtle')
parser.add_argument('ms', metavar='ms', type=int, help='mili seconds to run the command')
arguments = parser.parse_args()


#TurtleController retirado da atividade ponderada
class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.velocities = deque([arguments.vx, arguments.vy, arguments.vt])
        timer = self.create_timer(0.1, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = self.velocities.popleft()
        msg.linear.y = self.velocities.popleft()
        msg.angular.z = self.velocities.popleft()
        self.publisher_.publish(msg)
        self.get_logger().info('Publicando velocidades para a tartaruga')
        self.i += 1
        if self.i == arguments.ms:
            self.destroy_node()
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    tc = TurtleController()
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()



