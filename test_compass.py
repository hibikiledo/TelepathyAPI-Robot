import compass_work
import time

myCompass = compass_work.compass_work()
myCompass.set_value()

#add loop here if needed 
# now while loop got taken out bcus of experiment
compass_val = myCompass.get_value()
print "here is compass value", compass_val
time.sleep(.5)   
