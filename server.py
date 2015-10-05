__author__ = 'hibiki'

import eventlet

import packet

import getopt
import sys


def handler(s, addr):

    print("Handling request")

    # get request packet
    request_packet = packet.read_command(s)

    packet_reader = packet.CommandPacketReader(request_packet)

    # extract information
    type    = packet_reader.get_type()
    id      = packet_reader.get_id()
    command = packet_reader.get_command()
    value   = packet_reader.get_value()

    packet_reader.report()

    # Todo : Pass to robot handler

    # send ACK and mirror request message
    packet_builder = packet.CommandPacketBuilder()
    packet_builder.set_type(packet.ACK_TYPE)
    packet_builder.set_id(id)
    packet_builder.set_command(command)
    packet_builder.set_value(value)

    # create respond packet
    reply_packet = packet_builder.create()

    # send acknowledge packet back to phone
    s.sendall(bytes((reply_packet[0], reply_packet[1])))

    packet_builder.report()

    # close socket
    s.close()



def start_server(HOST, PORT):
    server_socket = eventlet.listen((HOST, PORT))
    thread_pool = eventlet.GreenPool(10)
    while True:
        clientsocket, addr = server_socket.accept()
        thread_pool.spawn_n(handler, clientsocket, addr)

def usage():
    print("Usage ...")
    print("python3 server.py -h <host> -p <port>")
    print("Example: python3 server.py -h 0.0.0.0 -p 5000")

def main(argv):

    HOST = '0.0.0.0'
    PORT = 5000

    try:
        opts, args = getopt.getopt(argv, "h:p:", ['host=', 'port='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # Use user specified host and port if exist
    for opt, arg in opts:
        if opt in ('-h', '--host'):
            HOST = arg
        elif opt in ('-p', '--port'):
            PORT = arg

    # Start our server
    start_server(HOST, PORT)


if __name__ == '__main__':
    main(sys.argv[1:])

