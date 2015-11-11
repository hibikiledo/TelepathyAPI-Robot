import time

class Dispatcher:

    def __init__(self):
        self.handler_map = {}

    def handle(self, action, value):
        print("Handle @", time.strftime("%H:%M"))
        self.handler_map[action](value)

    def register(self, action, handler):
        self.handler_map[action] = handler
