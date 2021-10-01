#!/bin/env python3
"""Module for controlling LED"""

import sleep

class Led:
  def __init__(self, pin_num):
    self.pin_num = pin_num

  def turn_on_off(self, is_on):
    raise Exception("Not Implemented")

  def flash(self, count, interval=2):
    """flash $count number of times with $interval second intervals"""
    # TODO: reimplement as non-blocking using events
    for _ in range(count):
      self.turn_on_off(True)
      time.sleep(interval)
      self.turn_on_off(False)
