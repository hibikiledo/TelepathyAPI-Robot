import robot
import ComplementaryFilter

robot.init_gpio()

# simulate main
myFilter = ComplementaryFilter.ComplementaryFilter()
myFilter.initual_filter_compute()

def self_balancing():
	while True:
		current_angle, i_dont_use_this = myFilter.filter_compute()
		# assume we get current_angle = -6
		print("current_angle = ", current_angle)
		# compute the uS_servo that servo need to supply to PWM in order to balance itself
		# assume we got uS_servo = 53.3333334 degree
		uS_servo = float( current_angle )* 8.88888889

		# use 1500 + because we need to assume the direction of the servo first
		robot.servo_direction_degree(1500 + round(uS_servo))

		print("uS_servo = ", round(uS_servo))

self_balancing()









