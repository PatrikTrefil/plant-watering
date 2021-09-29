#!/bin/env python3
"""signal and log errors"""

from config import get_config
import led

def log_error(text):
  config = get_config()
  with open(config["error_log"], "w") as error_file:
    error_file.write(text)

def signal_error():
  led.flash(10)