__author__ = 'hibiki'


# Define constants for packet type
REQ_TYPE = 0
ACK_TYPE = 1

# Define constants for IDs
ID_0 = 0
ID_1 = 1
ID_2 = 2
ID_3 = 3

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

    def _read(self):

        # handle Packet types
        # Perform AND operation with received high-byte
        # and check for equality
        if self.high_byte & int('10000000', 2) == int('10000000', 2):
            self.type = REQ_TYPE
        elif self.high_byte & int('01000000', 2) == int('01000000', 2):
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

