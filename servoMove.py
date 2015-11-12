import ComplementaryFilter
import time
import RobotCali
from RPIO import PWM


def self_balancing(current_angle):
	# assume we get current_angle = -6
	print("current_angle = ", current_angle)

	# compute the uS_servo that servo need to supply to PWM in order to balance itself
	# assume we got uS_servo = 53.3333334 degree
	uS_servo = float( current_angle )* 8.88888889

	# use 1500 + because we need to assume the direction of the servo first
	robot.servo_direction_degree(1500 + round(uS_servo))

	print("uS_servo = ", round(uS_servo))
