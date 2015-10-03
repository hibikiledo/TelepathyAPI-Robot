__author__ = 'hibiki'

import unittest

import packet

class PacketBuilderReader(unittest.TestCase):

    def test_build_and_read(self):

        # Create test data
        types = [packet.REQ_TYPE, packet.ACK_TYPE]
        ids = [packet.ID_0, packet.ID_1, packet.ID_2, packet.ID_3]
        commands = [
            packet.COMMAND_NONE, packet.COMMAND_UP, packet.COMMAND_UPRIGHT,
            packet.COMMAND_RIGHT, packet.COMMAND_DOWNRIGHT, packet.COMMAND_DOWN,
            packet.COMMAND_DOWNLEFT, packet.COMMAND_LEFT, packet.COMMAND_UPLEFT
        ]
        values = range(255)

        # Try all combinations of 4 values to check that
        # reader and builder can build and read the same thing
        for type in types:
            for id in ids:
                for command in commands:
                    for value in values:
                        # get builder and set data in packet
                        builder = packet.CommandPacketBuilder()
                        builder.set_type(type)
                        builder.set_id(id)
                        builder.set_command(command)
                        builder.set_value(value)
                        # create packet
                        output = builder.create()
                        # get reader and read the data
                        reader = packet.CommandPacketReader(output)
                        # check if created data and readed data are matched
                        self.assertEqual(type, reader.get_type())
                        self.assertEqual(id, reader.get_id())
                        self.assertEqual(command, reader.get_command())
                        self.assertEqual(value, reader.get_value())

if __name__ == '__main__':
    unittest.main()
