#! /usr/bin/python
import time, urllib

class ConnectionStatusChecker:

  # CONSTANTS
  __INTERNET_CHECK_URL = 'http://google.com/robots.txt'
  __SECONDS_BETWEEN_CHECKS = 30

  # VARIABLES
  __connectedState = True
  __observer = None

  def __init__(self, observer):
    self.__observer = observer

  def __checkConnection(self):
    try:
      # Check the connection by opening a socket to a URL
      connection = urllib.urlopen(self.__INTERNET_CHECK_URL)
      # Connected successfully so close the socket
      connection.close()
      self.__connected()
    except Exception:
      # We are not connected
      self.__notConnected()

  def __connected(self):
    if (self.__connectedState == False):
      self.__connectedState = True
      self.__notifyObservers()

  def __notConnected(self):
    if (self.__connectedState == True):
      self.__connectedState = False
      self.__notifyObservers()

  def __notifyObservers(self):
    try:
      self.__observer.statusChanged(self.__connectedState)
    except Exception:
      # Ignore all errors from observers
      pass

  def run(self):
    while (True):
      self.__checkConnection()
      time.sleep(self.__SECONDS_BETWEEN_CHECKS)


class ConnectionStatusObserver:

  def statusChanged(self, connected):
    pass
