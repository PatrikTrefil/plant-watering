#!/bin/env python3
"""signal and log errors"""

from config import get_config
from led import Led

class ErrorLog:
  led = Led(20)

  @staticmethod
  def signal_error():
    ErrorLog.led.flash(10)
