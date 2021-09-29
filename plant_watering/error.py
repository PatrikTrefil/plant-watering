#!/bin/env python3
"""signal and log errors"""

from config import get_config
from led import Led

class ErrorLog:
  led = Led()

  @staticmethod
  def log_error(text):
    config = get_config()
    with open(config["error_log"], "w") as error_file:
      error_file.write(text)

  @staticmethod
  def signal_error():
    ErrorLog.led.flash(10)
