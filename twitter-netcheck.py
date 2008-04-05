#! /usr/bin/python

import sys, time, twitter
from netcheck import ConnectionStatusChecker, ConnectionStatusObserver

class ConnectionStatusTwitject(ConnectionStatusObserver):

  __twitter = None
  __dmUsername = None
  __disconnectedTime = None

  def __init__(self, username, password, dmUsername=None):
    self.__twitter = twitter.Api(username, password)
    self.__dmUsername = dmUsername

  def statusChanged(self, connected):
    try:
      if (connected == True):
        connectedTime = time.time()
        message = self.__getMessage(connectedTime)
        print message
        self.__postToTwitter(message)
      else:
        self.__disconnectedTime = time.time()
    except Exception, exception:
      print str(exception)

  def __getMessage(self, connectedTime):
    disconnectedTimeString = time.strftime("%c", time.localtime(self.__disconnectedTime))
    duration = time.localtime(connectedTime - self.__disconnectedTime)
    durationYears = duration.tm_year - 1970
    durationMonths = duration.tm_mon - 1
    durationDays = duration.tm_mday - 1
    durationHours = duration.tm_hour - 1
    durationMinutes = duration.tm_min
    durationSeconds = duration.tm_sec
    durationString = ""
    if (durationYears > 0):
      durationString += str(durationYears) + " years, "
    if (durationMonths > 0):
      durationString += str(durationMonths) + " months, "
    if (durationDays > 0):
      durationString += str(durationDays) + " days, "
    if (durationHours > 0):
      durationString += str(durationHours) + " hours, "
    if (durationMinutes > 0):
      durationString += str(durationMinutes) + " minutes, "
    durationString += str(durationSeconds) + " seconds"
    return "Back online! Been disconnected for " + durationString + " (since " + disconnectedTimeString + ")"

  def __postToTwitter(self, message):
    try:
      print "Posting to twitter"
      self.__twitter.PostUpdate(message)
    except Exception, exception:
      # Failed to post to twitter
      print str(exception)
    try:
      if (self.__dmUsername != None):
        print "Sending direct message to '" + self.__dmUsername + "'"
        self.__twitter.PostDirectMessage(self.__dmUsername, message)
    except Exception, exception:
      # Failed to post to twitter
      print str(exception)

try:
  if (len(sys.argv) > 2):
    username = sys.argv[1]
    password = sys.argv[2]
    if (len(sys.argv) > 3):
      dmUsername = sys.argv[3]
      observer = ConnectionStatusTwitject(username, password, dmUsername)
    else:
      observer = ConnectionStatusTwitject(username, password)
    checker = ConnectionStatusChecker(observer)
    checker.run()
  else:
    print "Usage: " + sys.argv[0] + " twitter-username twitter-password [twitter-username-to-send-direct-message]"
except KeyboardInterrupt:
  # User has killed program with keyboard interrupt (Ctrl+C)
  print "Exiting\n"
