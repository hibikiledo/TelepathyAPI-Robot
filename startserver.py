__author__ = 'hibiki'

import dispatcher
import server
import packet

# Create a dispatcher
d = dispatcher.Dispatcher()

# Perform registration here


# Create a server
s = server.CommandServer('0.0.0.0', 5000, dispatcher=d)
s.start_server()


