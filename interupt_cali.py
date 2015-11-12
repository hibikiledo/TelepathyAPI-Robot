import ComplementaryFilter
import RobotCali

running = True


def balance():

    # init object from complementaryfilter class
    myFilter = ComplementaryFilter.ComplementaryFilter()
    myFilter.initual_filter_compute()

    counter = 0
    RobotCali.setup()

    # stop this while loop when we finish moving forward or backward task
    # by setting running to False ---> interupt.py knows when the task is done
    while running:
        # note in the case we are not using y_value
        x_value, y_value = myFilter.filter_compute()
        #print ("x val", x_value)

        if counter == 0:

            print("here is my x", x_value)

            if x_value > 1 or x_value < -1:
             # we have to calibrate the robot
                RobotCali.calibrate(x_value)

        counter += 1

        if counter == 5:
            counter = 0
    print("balance is done")

def detect_obstacle():

    # init object from complementaryfilter class
    myFilter = ComplementaryFilter.ComplementaryFilter()
    myFilter.initual_filter_compute()

    counter = 0
    RobotCali.setup()

    # stop this while loop when we finish moving forward or backward task
    # by setting running to False ---> interupt.py knows when the task is done
    while running:
        # note in the case we are not using y_value
        x_value, y_value = myFilter.filter_compute()

        if counter == 0:

            print("here is my x", x_value)

            if y_value > 40 or y_value < -15:
                # obstacle found!! report to ratthanan
                ipc.write("ERROR")

        counter += 1

        if counter == 5:
            counter = 0
    print("obstacle is found")