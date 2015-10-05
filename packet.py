__author__ = 'hibiki'

import struct

'''
 Provide Builder and Reader for reading and creting packets.

 Compose of ..
  - Utility functions
  - Builder class
  - Reader class

'''

# Define constants for packet type
REQ_TYPE = 0
ACK_TYPE = 1

TYPES = {
    0: 'REQ_TYPE',
    1: 'ACK_TYPE'
}

# Define constants for IDs
ID_0 = 0
ID_1 = 1
ID_2 = 2
ID_3 = 3

IDS = {
    0: 'ID_0',
    1: 'ID_1',
    2: 'ID_2',
    3: 'ID_3',
}

# Define constants for Commands
COMMAND_NONE = 0
COMMAND_UP = 1
COMMAND_UPRIGHT = 2
COMMAND_RIGHT = 3
COMMAND_DOWNRIGHT = 4
COMMAND_DOWN = 5
COMMAND_DOWNLEFT = 6
COMMAND_LEFT = 7
COMMAND_UPLEFT = 8

COMMANDS = {
    0: 'COMMAND_NONE',
    1: 'COMMAND_UP',
    2: 'COMMAND_UPRIGHT',
    3: 'COMMAND_RIGHT',
    4: 'COMMAND_DOWNRIGHT',
    5: 'COMMAND_DOWN',
    6: 'COMMAND_DOWNLEFT',
    7: 'COMMAND_LEFT',
    8: 'COMMAND_UPLEFT'
}


'''
    Utility function
    [0] Continue reading for command until get the complete one.
'''
def read_command(s):
    byte_count = 0
    command_packet = bytearray()
    # keep reading until get 2 byte (complete command packet)
    while byte_count < 2:
        partial = s.recv(1)
        if len(partial) == 1:
            command_packet.append(byte_to_int(partial))
            byte_count += 1
    # return
    return command_packet


'''
    Utility function
    [1] Convert byte into integer
'''
def byte_to_int(byte):
    return struct.unpack("B", byte)[0]


class CommandPacketBuilder:

    def __init__(self):
        self.type = None
        self.id = None
        self.command = None
        self.value = None

    def set_type(self, type):
        self.type = type

    def set_id(self, id):
        self.id = id

    def set_command(self, command):
        self.command = command

    def set_value(self, value):
        self.value = value

    def report(self):
        print(': '.join([
            TYPES.get(self.type), IDS.get(self.id),
            COMMANDS.get(self.command), str(self.value)
        ]))

    def create(self):

        high_byte = int('00000000', 2)
        low_byte  = int('00000000', 2)

        # handle packet types
        # 10XXXXXX - REQ
        # 01XXXXXX - ACK
        if self.type == REQ_TYPE:
            high_byte |= int('10000000', 2)
        elif self.type == ACK_TYPE:
            high_byte |= int('01000000', 2)

        # handle IDs
        # This is done by using shifting 4 position
        high_byte |= self.id << 4

        # handle Commands
        # Perform OR operation with command constant
        high_byte |= self.command

        # handle Values
        # Perform OR operation to set value
        low_byte |= self.value

        # return high_byte and low_byte
        return (high_byte, low_byte)


class CommandPacketReader:

    def __init__(self, packet):
        self.high_byte = packet[0]
        self.low_byte  = packet[1]

        self.type = None
        self.id = None
        self.command = None
        self.value = None

        self._read()

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id

    def get_command(self):
        return self.command

    def get_value(self):
        return self.value

    def report(self):
        print(': '.join([
            TYPES.get(self.type), IDS.get(self.id),
            COMMANDS.get(self.command), str(self.value)
        ]))


    def _read(self):

        # handle Packet types
        # Perform AND operation with received high-byte
        # and check for equality
        if self.high_byte & int('11000000', 2) == int('10000000', 2):
            self.type = REQ_TYPE
        elif self.high_byte & int('11000000', 2) == int('01000000', 2):
            self.type = ACK_TYPE

        # handle IDs
        # Mask other bits except id bits and perform 4 shift right
        self.id = (self.high_byte & int('00110000', 2)) >> 4

        # handle Commands
        # Mask other bits except last 4 LSB bits
        self.command = self.high_byte & int('00001111', 2)

        # handle Value
        # Copy value over
        self.value = self.low_byte
