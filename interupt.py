import RPi.GPIO as GPIO

def dist_thread(dist,stop):
    # keep signal at 0 and wait for signal 1 to arrive
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    count = 0
    distance = 0
    
    while True:
        print ("Waiting for high signal")
        try:
            GPIO.wait_for_edge(4, GPIO.RISING)
            count +=1
            distance += 6.283
            dist -= 6.283

            print ("total number of times sensors pass hole", count)
            print ("total distance", distance)
            print ("this is DIST", dist)
            if int(dist) <= 0:
                stop(0)  
        except KeyboardInterrupt:
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit
       # GPIO.cleanup()           # clean up GPIO on normal exit




 

