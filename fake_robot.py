from RPIO import PWM

def init():
	servo_port = 18
	servo = PWM.Servo()

def servo_direction_degree(degree):
	global servo
	servo.set_servo(servo_port,degree)