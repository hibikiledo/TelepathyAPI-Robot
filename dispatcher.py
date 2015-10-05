__author__ = 'hibiki'


class Dispatcher:

    def __init__(self):
        self.handler_map = {}

    def handle(self, action, value):
        self.handler_map['action'](value)

    def register(self, action, handler):
        self.handler_map[action] = handler
