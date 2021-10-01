#!/bin/env python3
"""Module for controlling water pumps"""

import time
from relay import Relay

class Pump:
  def __init__(self, pin_number):
    """pinNumber in GPIO.BOARD"""
    self.relay = Relay(pin_number)

  def pump(self, on_time):
    """time in seconds"""
    self.relay.switch(True)
    time.sleep(on_time)
    self.relay.switch(False)
