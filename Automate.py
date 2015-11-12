# __author__ = 'tappenisarn eiei'

##############################################################

# PLEASE NOTE THAT PARAMETER VALUE FOR EACH FUNCTION HERE
# WILL BE DISTANCE AND COMPASS DIRECTION NOT SPEED ANYMORE

##############################################################
print("I'm on the head of Automate.py")

import RPi.GPIO as GPIO
import time
import threading
import interupt
import interupt_turn
import interupt_cali
from sensors import compass_work
from RPIO import PWM


# same command set as nut's module
COMMAND_NONE = 0
COMMAND_UP = 1
COMMAND_UPRIGHT = 2
COMMAND_RIGHT = 3
COMMAND_DOWNRIGHT = 4
COMMAND_DOWN = 5
COMMAND_DOWNLEFT = 6
COMMAND_LEFT = 7
COMMAND_UPLEFT = 8

# set up gpio variable here

servo_port = 18
motor = 13
motor_control_a = 17
motor_control_b = 27

pwm = None
motor_pwm = None
servo = None
current_ms = None
# init for communicate protocal
ipc = None


# call this method to init gpio port that we need to use
def init_gpio(robot_ipc):
    
    global ipc
    global pwm
    global motor_pwm
    global servo
    global current_ms
    GPIO.setmode(GPIO.BCM)

    
    #send protocal ipc.write()
    ipc = robot_ipc


    # set up servo
    servo = PWM.Servo()
    
    # assume we set servo at the middle which is 1500 ms
    current_ms = 1500
    servo.set_servo(servo_port, current_ms)


    # set up enable for motor
    GPIO.setup(motor, GPIO.OUT)
    motor_pwm = GPIO.PWM(motor, 100)
    motor_pwm.start(0)

    # set up control for motor
    GPIO.setup(motor_control_a, GPIO.OUT)
    GPIO.setup(motor_control_b, GPIO.OUT)


# command set for robot to move forward
# note that parameter value here is distance that robot will move forward
def move_forward(value):
    interupt_cali.running = True
    # robot move forward with servo at center and speed of 75% duty cycle
    servo_direction(2)
    motor_direction(1)
    motor_pwm.ChangeDutyCycle(75)

    # call thread send distance and stop function for calculation
    dist = value
    thread = threading.Thread(target=interupt.dist_thread, args=(dist, stop))
  
    # implement thread to handle robot stuck here don't forget to move first thread to below here
    thread_cali = threading.Thread(target = interupt_cali.balance, args=())
    thread_obs = threading.Thread(target = interupt_cali.detect_obstacle, args=())

    # start all threads
    thread.start()
    thread_cali.start()
    thread_obs.start()
    
    # end all threads
    thread.join()
    thread_cali.join()
    thread_obs.join()

    # report that the task is sucessfully finished
    ipc.write("DONE")


# command sets for robot to move backward
# note that parameter value here is distance that robot will move forward
def move_backward(value):
    interupt_cali.running = True
    # robot move backward with servo at center and speed of 75% duty cycle
    servo_direction(2)
    motor_direction(2)
    motor_pwm.ChangeDutyCycle(75)

    # call thread send distance and stop function for calculation
    dist = value
    thread = threading.Thread(target=interupt.dist_thread, args=(dist, stop))
    
    # implement thread to handle robot stuck here don't forget to move first thread to below here
    thread_cali = threading.Thread(target = interupt_cali.balance, args=())
    thread_obs = threading.Thread(target = interupt_cali.detect_obstacle, args=())

    # start all threads
    thread.start()
    thread_cali.start()
    thread_obs.start()
    
    # end all threads
    thread.join()
    thread_cali.join()
    thread_obs.join()

    # report that the task is sucessfully finished
    ipc.write("DONE")


# note value here is the current degree that the robot is heading
def turn_right(value):
    myCompass = compass_work.compass_work()
    myCompass.set_value()

    #this is the angle that the robot is heading
    current_angle = myCompass.get_value()
    
    #this is the new angle(direction) that we need 
    new_angle = (current_angle + 90)%360

    # set motor and servo behaviour
    servo_direction(3)
    motor_direction(1)
    motor_pwm.ChangeDutyCycle(75)

    # call thread to check degree here
    # thread will keep checking angle till it meets new_angle
    thread_right = threading.Thread(target=interupt_turn.turn_thread, args=(new_angle,stop))
    thread_obs = threading.Thread(target = interupt_cali.detect_obstacle, args=())

    # start the turn right thread and obstacle detection thread
    thread_right.start()
    thread_obs.start()

    # waiting till they're done
    thread_right.join()
    thread_obs.join()

    # report that the task is sucessfully finished
    ipc.write("DONE")


# note value here is the current degree that the robot is heading
def turn_left(value):
    myCompass = compass_work.compass_work()
    myCompass.set_value()

    #this is the angle that the robot is heading
    current_angle = myCompass.get_value()
    
    #this is the new angle(direction) that we need 
    new_angle = (current_angle - 90)%360

    # set motor and servo behaviour
    servo_direction(1)
    motor_direction(1)
    motor_pwm.ChangeDutyCycle(75)

    # call thread to check degree here
    # thread will keep checking angle till it meets new_angle
    thread_left = threading.Thread(target=interupt_turn.turn_thread, args=(new_angle,stop))
    thread_obs = threading.Thread(target = interupt_cali.detect_obstacle, args=())

    # start turning and obstacle detection thread
    thread_left.start()
    thread_obs.start()

    # wait till they're finished
    thread_left.join()
    thread_obs.join()

    # report that the task is sucessfully finished
    ipc.write("DONE")


def turn_servo_middle(value):
    servo_direction(2)


# stop
def stop(value):
    motor_pwm.ChangeDutyCycle(0)
    servo_direction(2)


# below here will not be top level method
# set degree of servo
def servo_direction(direction):
    global servo
    # 1 is left, 2 is middle, 3 is right
    if direction == 3:
        # servo.set_servo(servo_port, 1100)
        servo.set_servo(servo_port, 1200)

    elif direction == 2:
        servo.set_servo(servo_port, 1500)

    elif direction == 1:
        # servo.set_servo(servo_port, 1900)
        servo.set_servo(servo_port, 1800)

# method to switch the direction of motor
def motor_direction(direction):
    if direction == 1:
        GPIO.output(motor_control_a, GPIO.HIGH)
        GPIO.output(motor_control_b, GPIO.LOW)
    elif direction == 2:
        GPIO.output(motor_control_b, GPIO.HIGH)
        GPIO.output(motor_control_a, GPIO.LOW)

print("I'm on the ass of Automate.py")
