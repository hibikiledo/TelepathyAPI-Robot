__author__ = 'hibiki'

import dispatcher
import server
import packet
import robot

# Create a dispatcher
d = dispatcher.Dispatcher()

# Perform registration here
d.register(packet.COMMAND_NONE, robot.stop)
d.register(packet.COMMAND_UP, robot.move_forward)
d.register(packet.COMMAND_UPRIGHT, robot.move_forward_servo_right)
d.register(packet.COMMAND_RIGHT, robot.turn_servo_right)
d.register(packet.COMMAND_DOWNRIGHT, robot.move_backward_servo_left)
d.register(packet.COMMAND_DOWN, robot.move_backward)
d.register(packet.COMMAND_DOWNLEFT, robot.move_backward_servo_left)
d.register(packet.COMMAND_LEFT, robot.turn_servo_left)
d.register(packet.COMMAND_UPLEFT, robot.move_forward_servo_left)

# Create a server
s = server.CommandServer('0.0.0.0', 5000, dispatcher=d)
s.start_server()


