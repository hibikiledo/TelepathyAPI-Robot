
class IncompletePacketError(Exception):
  def __init__(self, size):
    self.value = "Cannot get complete packet of size: " + str(size)
  def __str__(self):
    return repr(self.value)


class UnknowPacketTypeError(Exception):
  def __init__(self):
    self.value = "Unknown packet type"
  def __str__(self):
    return repr(self.value)

class UnknowIdError(Exception):
  def __init__(self):
    self.value = "Unknown id"
  def __str__(self):
    return repr(self.value)

class UnknowCommandError(Exception):
  def __init__(self):
    self.value = "Unknown command"
  def __str__(self):
    return repr(self.value)