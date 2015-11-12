#!/usr/bin/python
import smbus
import time
import math


class compass_work:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x1e

    def set_value(self):
        self.write_byte(0, 0b01110000)  # Set to 8 samples @ 15Hz
        self.write_byte(1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (default)
        self.write_byte(2, 0b00000000)  # Continuous sampling

        self.scale = 0.92


    def read_byte(self,adr):
        return self.bus.read_byte_data(self.address, adr)


    def read_word(self,adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr + 1)
        val = (high << 8) + low
        return val


    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val


    def write_byte(self,adr, value):
        self.bus.write_byte_data(self.address, adr, value)



    def get_value(self):
        x_offset = 178
        y_offset = 4
        x_out = (self.read_word_2c(3) - x_offset) * self.scale
        y_out = (self.read_word_2c(7) - y_offset) * self.scale
        z_out = (self.read_word_2c(5)) * self.scale

        # print "xout", x_out, "yout", y_out
        # print "xout*scale", (x_out * scale),"yout*scale", (y_out * scale)
    
        bearing  = math.atan2(y_out * self.scale, x_out * self.scale) 
        if (bearing < 0):
            bearing += 2 * math.pi
        
        print("Bearing: ", math.degrees(bearing))
        return math.degrees(bearing)