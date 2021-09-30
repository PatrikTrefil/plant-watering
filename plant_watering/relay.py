#!/bin/env python3

class Relay:
  def __init__(self, pin_num):
    self.pin_num = pin_num
    GPIO.setup(pin_num, GPIO.OUT, initial=GPIO.LOW) # default to 0 V

  def switch(self, on):
    GPIO.output(self.pin_num, GPIO.LOW if on is True else GPIO.HIGH)
