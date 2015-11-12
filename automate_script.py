import Automate
import time
Automate.init_gpio()

Automate.move_forward(100)
time.sleep(1)
Automate.move_backward(100)
