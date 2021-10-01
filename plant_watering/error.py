#!/bin/env python3
"""signal and log errors"""

from config import get_config
from led import Led

class ErrorLog:
  led = Led(get_config()["pins"]["led"])

  @staticmethod
  def signal_error():
    ErrorLog.led.flash(10)
