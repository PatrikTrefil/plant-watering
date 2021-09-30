#!/bin/env python3
"""Module for controlling water pumps"""

import time
import RPi.GPIO as GPIO
from relay import Relay

class Pump:
  def __init__(self, pin_number):
    """pinNumber in GPIO.BOARD"""
    self.relay = Relay(pin_number)

  def pump(self, on_time):
    """time in seconds"""
    relay.switch(True)
    time.sleep(on_time)
    relay.switch(False)
