from multiprocessing import Process

import dispatcher
import servers
import ipc
#import robot

import packet

# Initialize robot script
#robot.init_gpio(robot_ipc)

# Create an instance of RobotIPC for communication between command & heartbeat server
robot_ipc = ipc.RobotIPC('rr-shm')
robot_ipc.write("WORKING")

# Create a dispatcher
m_dispatcher = dispatcher.Dispatcher()
a_dispatcher = dispatcher.Dispatcher()

# Perform registration here
d.register(packet.COMMAND_NONE, robot.stop)
d.register(packet.COMMAND_UP, robot.move_forward)
d.register(packet.COMMAND_UPRIGHT, robot.move_forward_servo_right)
d.register(packet.COMMAND_RIGHT, robot.turn_servo_right)
d.register(packet.COMMAND_DOWNRIGHT, robot.move_backward_servo_right)
d.register(packet.COMMAND_DOWN, robot.move_backward)
d.register(packet.COMMAND_DOWNLEFT, robot.move_backward_servo_left)
d.register(packet.COMMAND_LEFT, robot.turn_servo_left)
d.register(packet.COMMAND_UPLEFT, robot.move_forward_servo_left)

# TODO : Register function handlers for automate control
# ----

