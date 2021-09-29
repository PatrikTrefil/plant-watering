#!/bin/env python3
"""Module for controlling water pumps"""

import time
import RPi.GPIO as GPIO

class Pump:
  def __init__(self, pin_number):
    """pinNumber in GPIO.BOARD"""
    self.pin_number = pin_number
    GPIO.setup(self.pin_number, GPIO.OUT)

  def pump(self, on_time):
    """time in seconds"""
    GPIO.output(self.pin_number, GPIO.HIGH)
    time.sleep(on_time)
    GPIO.output(self.pin_number, GPIO.LOW)
    raise Exception("Not implemented")
