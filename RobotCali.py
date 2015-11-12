import ComplementaryFilter
import time
from RPIO import PWM


def setup():
    global current_ms
    global servo
    global servo_port
    # init servo value
    servo_port = 18
    servo = PWM.Servo()

    # assume we set servo at the middle which is 1500 ms
    current_ms = 1500
    servo.set_servo(servo_port, current_ms)


#####################################################
def calibrate(x_value):
    global servo
    global current_ms
    global servo_port
    # case one servo shift left
    if x_value < -1:
        current_ms -= 10
        print ("shift left -- > right", current_ms)
        servo.set_servo(servo_port,current_ms)

    # case two servo shift right
    elif x_value > 1:
        current_ms += 10
        print ("shift right --> left", current_ms)
        servo.set_servo(servo_port,current_ms)


