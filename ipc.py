import os
import pipes

class RobotIPC:

  def __init__(self, shm_name):
    self.shm_name = shm_name
    self.shm_partial_name = shm_name + ".partial"

  def write(self, value):
    # write into partial file
    partial_output = open(self.shm_partial_name, "w+")
    partial_output.write(value)
    partial_output.close()
    # rename partial file to full file
    os.rename(self.shm_partial_name, self.shm_name)

  def read(self):
    output_file = open(self.shm_name, "r")
    return output_file.read()
