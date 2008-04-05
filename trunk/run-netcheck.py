#! /usr/bin/python

import time
from netcheck import ConnectionStatusChecker, ConnectionStatusObserver

class MyConnectionStatusObserver(ConnectionStatusObserver):

  def statusChanged(self, connected):
    if (connected == True):
      print "Connected!"
    else:
      print "Disconnected!"


try:
  observer = MyConnectionStatusObserver()
  checker = ConnectionStatusChecker(observer)
  checker.run()
except KeyboardInterrupt:
  # User has killed program with keyboard interrupt (Ctrl+C)
  print "Exiting\n"
