__author__ = 'hibiki'

import eventlet

import packet

import getopt
import sys


class CommandServer:

    def __init__(self, host, port, dispatcher):
        self.dispatcher = dispatcher
        self.host = host
        self.port = port


    def handler(self, client_socket, address):

        print("Handling request")

        # get request packet
        request_packet = packet.read_command(client_socket)

        packet_reader = packet.CommandPacketReader(request_packet)

        # extract information
        type    = packet_reader.get_type()
        id      = packet_reader.get_id()
        command = packet_reader.get_command()
        value   = packet_reader.get_value()

        packet_reader.report()

        # Let dispatcher dispatch command
        self.dispatcher.handle(command, value)

        # send ACK and mirror request message
        packet_builder = packet.CommandPacketBuilder()
        packet_builder.set_type(packet.ACK_TYPE)
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
