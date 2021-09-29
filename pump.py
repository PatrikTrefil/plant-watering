#!/bin/env python3

import RPi.GPIO as GPIO
import time

class Pump:
  def __init__(self, pinNumber):
    """pinNumber in GPIO.BOARD"""
    self.pinNumber = pinNumber
    GPIO.setup(self.pinNumber, GPIO.OUT)

  def pump(self, time):
    """time in seconds"""
    raise Exception("Not implemented")
    GPIO.output(self.pinNumber, GPIO.HIGH)
    time.sleep(time)
    GPIO.output(self.pinNumber, GPIO.LOW)

