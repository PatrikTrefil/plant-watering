#!/bin/env python3
"""Module for controlling LED"""

import time
import RPi.GPIO as GPIO

class Led:
  is_on = False
  def __init__(self, pin_num):
    self.pin_num = pin_num

  def turn_on_off(self, is_on):
    self.is_on = is_on
    GPIO.output(
      self.pin_num,
      GPIO.HIGH if is_on is True else GPIO.LOW
    )

  def flash(self, count, interval=2):
    """flash $count number of times with $interval second intervals"""
    # TODO: reimplement as non-blocking using events
    for _ in range(count):
      self.turn_on_off(True)
      time.sleep(interval)
      self.turn_on_off(False)
