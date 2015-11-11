import accelerometer
import gyro
import math
import time

#import compass


class ComplementaryFilter:
    def __init__(self):
        # init variable for our sensors
        self.accelerometer = accelerometer.Accelerometer()
        self.gyro = gyro.Gyro()

        # may ve used later
        #self.compass = compass.Compass()

        # init equation constant
        self.now = time.time()
        self.K = 0.98
        self.K1 = 1 - self.K
        self.time_diff = 0.01

    # this function read all data from device
    def read_data(self):
        accel_x1, accel_y1, accel_z1 = self.accelerometer.getCurrentAcceleroValue()
        gyro_x1, gyro_y1, gyro_z1 = self.gyro.getCurrentGyroValue()
        return accel_x1, accel_y1, accel_z1, gyro_x1, gyro_y1, gyro_z1

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    # get the rotation angle respect to x axis
    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)

    # get the rotation angle respect to y axis
    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.dist(y, z))
        return math.degrees(radians)

    # set initual value to compute complemetary filter
    def initual_filter_compute(self):

        accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = self.read_data()

        # init angle value from accelerometer alone
        self.last_x = self.get_x_rotation(accel_x, accel_y, accel_z)
        self.last_y = self.get_y_rotation(accel_x, accel_y, accel_z)

        # init offset for gyro ---> think of it as a starting value when gyro is flat
        self.gyro_offset = gyro_x
        self.gyro_offset_y = gyro_y

        self.gyro_total = self.last_x - self.gyro_offset

        #print ("respect to x", int(self.last_x), "respect to y", int(self.last_y))

        return int(self.last_x), int(self.last_y)

    # compute complementary value
    def filter_compute(self):
        time.sleep(self.time_diff - 0.005)

        accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = self.read_data()

        # current gyro value is reduced from the offset
        gyro_x -= self.gyro_offset
        gyro_y -= self.gyro_offset_y

        gyro_delta = (gyro_x*self.time_diff)
        self.gyro_total += gyro_delta

        gyro_delta_y = (gyro_y*self.time_diff)

        rotation_x = self.get_x_rotation(accel_x, accel_y, accel_z)
        rotation_y = self.get_y_rotation(accel_x, accel_y, accel_z)

        self.last_x = self.K * (self.last_x + gyro_delta) + (self.K1 * rotation_x)
        self.last_y = self.K * (self.last_y + gyro_delta_y) + (self.K1 * rotation_y)
        #print ("respect to x", int(self.last_x), "respect to y", int(self.last_y))

        return int(self.last_x), int(self.last_y)

# simulate main
#myFilter = ComplementaryFilter()
#myFilter.initual_filter_compute()

#while True:
#    myFilter.filter_compute()
    
