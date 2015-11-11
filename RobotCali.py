import ComplementaryFilter
import time
from RPIO import PWM

# init object from complementaryfilter class
myFilter = ComplementaryFilter.ComplementaryFilter()
myFilter.initual_filter_compute()

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
 
    # case one servo shift left
    if x_value > 5:
        current_ms -= 10
        print ("shift left -- > right", current_ms)
        servo.set_servo(servo_port,current_ms)

    # case two servo shift right
    elif x_value < -5:
        current_ms += 10
        print ("shift right --> left", current_ms)
        servo.set_servo(servo_port,current_ms)


####################################################
counter = 0
while True: 
    # note in the case we are not using y_value
    x_value, y_value = myFilter.filter_compute()
    #print ("x val", x_value)

    if counter == 0:

        print("here is my x", x_value)
       
        if x_value > 8 or x_value < -8:           
         # we have to calibrate the robot
            calibrate(x_value)

    counter += 1

    if counter == 10:
        counter = 0
