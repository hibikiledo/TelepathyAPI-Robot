import compass_work
def turn_thread(new_angle, stop):
    myCompass = compass_work.compass_work()
    myCompass.set_value()

    #this is the angle that the robot is heading
    while True:
        current_angle = myCompass.get_value()
        
        print ("this is needed angle = ", int(new_angle))
        print ("this is the angle u heading = ", int(current_angle))

        if (int(current_angle) < int(new_angle+2)) and (int(current_angle) > int(new_angle-2)):            
            stop(0)
            break
