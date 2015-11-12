import struct
from cores import exceptions

'''
 Provide Builder and Reader for reading and creting packets.

 Compose of ..
  - Utility functions
  - Builder class
  - Reader class
'''

# Define constants for packet type
REQ_M_TYPE = int('00000000', 2)
ACK_M_TYPE = int('01000000', 2)
REQ_A_TYPE = int('10000000', 2)
ACK_A_TYPE = int('11000000', 2)
TYPES_MASK  = int('11000000', 2)

TYPES = {
    REQ_M_TYPE: 'REQ_M_TYPE',
    ACK_M_TYPE: 'ACK_M_TYPE',
    REQ_A_TYPE: 'REQ_A_TYPE',
    ACK_A_TYPE: 'ACK_A_TYPE'
}

# Define constants for IDs
ID_0 = int('00000000', 2)
ID_1 = int('00010000', 2)
ID_2 = int('00100000', 2)
ID_3 = int('00110000', 2)
IDS_MASK = int('00110000', 2)

IDS = {
    ID_0: 'ID_0',
    ID_1: 'ID_1',
    ID_2: 'ID_2',
    ID_3: 'ID_3'
}

# Define constants for Commands
COMMAND_NONE        = int('00000000', 2)
COMMAND_UP          = int('00000001', 2)
COMMAND_UPRIGHT     = int('00000010', 2)
COMMAND_RIGHT       = int('00000011', 2)
COMMAND_DOWNRIGHT   = int('00000100', 2)
COMMAND_DOWN        = int('00000101', 2)
COMMAND_DOWNLEFT    = int('00000110', 2)
COMMAND_LEFT        = int('00000111', 2)
COMMAND_UPLEFT      = int('00001000', 2)
COMMANDS_MASK = int('00001111', 2)

COMMANDS = {
    COMMAND_NONE: 'COMMAND_NONE',
    COMMAND_UP: 'COMMAND_UP',
    COMMAND_UPRIGHT: 'COMMAND_UPRIGHT',
    COMMAND_RIGHT: 'COMMAND_RIGHT',
    COMMAND_DOWNRIGHT: 'COMMAND_DOWNRIGHT',
    COMMAND_DOWN: 'COMMAND_DOWN',
    COMMAND_DOWNLEFT: 'COMMAND_DOWNLEFT',
    COMMAND_LEFT: 'COMMAND_LEFT',
    COMMAND_UPLEFT: 'COMMAND_UPLEFT'
}

# Define constans for HeartBeat
HEART_REQ = int('00000000', 2)
HEART_ACK = int('01000000', 2)
HEART_DONE  = int('10000000', 2)
HEART_ERR = int('11000000', 2)

HEARTS = {
    HEART_REQ: 'HEART_REQ',
    HEART_ACK: 'HEART_ACK',
    HEART_DONE: 'HEART_DONE',
    HEART_ERR: 'HEART_ERR'
}

MAX_FAILURES = 10


'''
    Utility function
    [0] Continue reading for command until get the complete one.    
'''
def read_command(s, size):
    byte_count = 0
    failure_count = 0
    command_packet = bytearray()
    # keep reading until get 2 byte (complete command packet)
    while byte_count < size:        
        partial = s.recv(1)
        # we got something from socket
        if len(partial) == 1:
            command_packet.append(byte_to_int(partial))
            byte_count += 1
        # ops! we got nothing
        if len(partial) == 0:
            failure_count += 1
        # threat as failure ! .. raise exception
        if failure_count > MAX_FAILURES:
            raise exceptions.IncompletePacketError(size)
    # return
    return command_packet


'''
    Utility function
    [1] Convert byte into integer
'''
def byte_to_int(byte):
    return struct.unpack("B", byte)[0]


'''
 Build HeartBeat Packet in a single byte.
 Return type is integer
'''
class HeartBeatPacketBuilder:

    def __init__(self):
        self.type = None

    def set_type(self, type):
        if type not in TYPES.keys():
            raise exceptions.UnknowPacketTypeError()
        self.type = type

    def create(self):
        # create an empty byte output
        abyte = int('00000000', 2)
        abyte |= self.type

        return abyte

    def report(self):
        print(': '.join([
            HEARTS.get(self.type)]))

'''
 Read HeartBeat Packet from a single byte
 Return a type as an integer
'''
class HeartBeatPacketReader:

    def __init__(self, packet):
        self.packet = packet[0]
        self.type = None
        self._read()

    def _read(self):
        self.type = (self.packet & TYPES_MASK)

    def get_type(self):
        return self.type

    def report(self):
        print(': '.join([
            HEARTS.get(self.type)]))

'''
 Build command as a tuple of high byte and low byte
 Return type is integer
'''
class CommandPacketBuilder:

    def __init__(self):
        self.type = None
        self.id = None
        self.command = None
        self.value = None

    def set_type(self, type):
        if type not in TYPES.keys():
            raise exceptions.UnknowPacketTypeError()
        self.type = type

    def set_id(self, id):
        if id not in IDS.keys():
            raise exceptions.UnknownIdError()
        self.id = id

    def set_command(self, command):
        if command not in COMMANDS.keys():
            raise exceptions.UnknownCommandError()
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
        high_byte |= self.type

        # handle IDs
        high_byte |= self.id

        # handle Commands
        high_byte |= self.command

        # handle Values
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
        self.type = self.high_byte & TYPES_MASK

        # handle IDs
        # Mask other bits except id bits and perform 4 shift right
        self.id = self.high_byte & IDS_MASK

        # handle Commands
        # Mask other bits except last 4 LSB bits
        self.command = self.high_byte & COMMANDS_MASK

        # handle Value
        # Copy value over
        self.value = self.low_byte
