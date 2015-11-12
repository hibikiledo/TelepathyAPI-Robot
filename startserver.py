import threading

from cores import dispatcher
from cores import servers
from cores import ipc
from cores import packet

import robot
#import Automate

# Create an instance of RobotIPC for communication between command & heartbeat server
robot_ipc = ipc.RobotIPC('/dev/shm/rr-ipc')
robot_ipc.write("WORKING")

# Initialize robot script
robot.init_gpio()
# Automate.init_gpio(robot_ipc)

# Create a dispatcher
m_dispatcher = dispatcher.Dispatcher()
a_dispatcher = dispatcher.Dispatcher()

# Register function handlers for manual control
m_dispatcher.register(packet.COMMAND_NONE, robot.stop)
m_dispatcher.register(packet.COMMAND_UP, robot.move_forward)
m_dispatcher.register(packet.COMMAND_UPRIGHT, robot.move_forward_servo_right)
m_dispatcher.register(packet.COMMAND_RIGHT, robot.turn_servo_right)
m_dispatcher.register(packet.COMMAND_DOWNRIGHT, robot.move_backward_servo_right)
m_dispatcher.register(packet.COMMAND_DOWN, robot.move_backward)
m_dispatcher.register(packet.COMMAND_DOWNLEFT, robot.move_backward_servo_left)
m_dispatcher.register(packet.COMMAND_LEFT, robot.turn_servo_left)
m_dispatcher.register(packet.COMMAND_UPLEFT, robot.move_forward_servo_left)

'''
# Register function handlers for automate control
a_dispatcher.register(packet.COMMAND_UP, Automate.move_forward)
a_dispatcher.register(packet.COMMAND_LEFT, Automate.turn_left)
a_dispatcher.register(packet.COMMAND_RIGHT, Automate.turn_right)
a_dispatcher.register(packet.COMMAND_DOWN, Automate.move_backward)
'''

# Create server processes
command_thread = threading.Thread(target=servers.command_server, args=(m_dispatcher, a_dispatcher, robot_ipc))
heartbeat_thread = threading.Thread(target=servers.heartbeat_server, args=(robot_ipc, )) 

# Start processes
command_thread.start()
heartbeat_thread.start()

# Join back all processes
command_thread.join()
heartbeat_thread.join()
