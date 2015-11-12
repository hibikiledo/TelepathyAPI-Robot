import eventlet

import packet

'''
  Client class (Outdated)
  No longer work with current implementation of packet.
'''

HOST = '127.0.0.1'
PORT = 5000

socket = eventlet.connect((HOST, PORT))

# build a packet

packet_builder = packet.CommandPacketBuilder()
packet_builder.set_type(packet.REQ_TYPE)
packet_builder.set_id(packet.ID_3)
packet_builder.set_command(packet.COMMAND_DOWN)
packet_builder.set_value(50)

# report
packet_builder.report()

# craft a packet
request_packet = packet_builder.create()

# send it to robot
socket.send(bytes((request_packet[0], )))
socket.send(bytes((request_packet[1], )))

# read response back .. looking for ACK
response = socket.recv(2)

packet_reader = packet.CommandPacketReader(response)

packet_reader.report()

