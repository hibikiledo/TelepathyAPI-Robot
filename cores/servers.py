import eventlet

from cores import packet

import getopt
import sys


'''
 Define top-level functions for each process to call
   command_server : start a command server
   heartbeat_server : start a heartbeat server
'''
def command_server(m_dispatcher, a_dispatcher, robot_ipc):
    print("Starting command server")
    command_server = CommandServer('0.0.0.0', 5000, m_dispatcher, a_dispatcher)
    command_server.start_server()

def heartbeat_server(robot_ipc):
    print("Starting heartbeat server")
    heartbeat_server = HeartBeatServer('0.0.0.0', 5001, robot_ipc)
    heartbeat_server.start_server()

'''
 Define classes for servers
 including HeartBeat and Command servers
'''

class HeartBeatServer:

    def __init__(self, host, port, robot_ipc):
        self.host = host
        self.port = port
        self.ipc = robot_ipc

    def handler(self, client_socket, address):        

        print("Handling HeartBeat")

        # Get packet
        request_packet = packet.read_command(client_socket, 1)

        packet_reader = packet.HeartBeatPacketReader(request_packet)

        # Extract information
        type = packet_reader.get_type()

        # Read from shared-memory region and replay with data
        content = self.ipc.read()

        # Handle values and set proper packet type
        packet_builder = packet.HeartBeatPacketBuilder()

        # packet_builder.set_type(packet.HEART_ACK)

        # handle DONE | WORKING
        if content == 'ERROR':
            packet_builder.set_type(packet.HEART_ERR)
        elif content == 'DONE':
            packet_builder.set_type(packet.HEART_DONE)
        elif content == 'HEALTHY':
            packet_builder.set_type(packet.HEART_ACK)

        # Create packet
        reply_packet = packet_builder.create()

        # send acknowledge packet back to phone
        client_socket.sendall(bytes((reply_packet, )))

        packet_builder.report()

        # close socket
        client_socket.close()
      

    def start_server(self):        
        self.server_socket = eventlet.listen((self.host, self.port))
        thread_pool = eventlet.GreenPool(10)
        while True:
            clientsocket, addr = self.server_socket.accept()
            thread_pool.spawn_n(self.handler, clientsocket, addr)


class CommandServer:

    def __init__(self, host, port, m_dispatcher, a_dispatcher):
        self.m_dispatcher = m_dispatcher
        self.a_dispatcher = a_dispatcher
        self.host = host
        self.port = port


    def handler(self, client_socket, address):

        print("Handling request")

        # get request packet
        request_packet = packet.read_command(client_socket, 2)

        print("Command Packet", request_packet)

        packet_reader = packet.CommandPacketReader(request_packet)

        # extract information
        type    = packet_reader.get_type()
        id      = packet_reader.get_id()
        command = packet_reader.get_command()
        value   = packet_reader.get_value()

        packet_reader.report()

        
        # Let dispatcher dispatch command
        if type == packet.REQ_M_TYPE:
            self.m_dispatcher.handle(command, value)
        if type == packet.REQ_A_TYPE:
            self.a_dispatcher.handle(command, value)
        

        # send ACK and mirror request message        
        packet_builder = packet.CommandPacketBuilder()

        # handle M_TYPE and A_TYPE separately
        if type == packet.REQ_M_TYPE:
            packet_builder.set_type(packet.ACK_M_TYPE)
        if type == packet.REQ_A_TYPE:
            packet_builder.set_type(packet.ACK_A_TYPE)

        # handle id, command, and value normally
        packet_builder.set_id(id)
        packet_builder.set_command(command)
        packet_builder.set_value(value)

        # create respond packet
        reply_packet = packet_builder.create()

        # send acknowledge packet back to phone
        client_socket.sendall(bytes((reply_packet[0], reply_packet[1])))

        packet_builder.report()

        # close socket
        client_socket.close()


    def start_server(self):
        self.server_socket = eventlet.listen((self.host, self.port))
        thread_pool = eventlet.GreenPool(10)
        while True:
            clientsocket, addr = self.server_socket.accept()
            thread_pool.spawn_n(self.handler, clientsocket, addr)
