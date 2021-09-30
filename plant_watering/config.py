#!/bin/env python3
"""Provides access to program configuration"""

import json
import datetime

def get_config():
  CONFIG_FILE_PATH = "./config.json"
  with open(CONFIG_FILE_PATH, "r") as config_file:
    config_obj = json.load(config_file)
    config_obj.time_plan = [datetime.datetime.strptime(time_unit, '%H:%M') for time_unit in config_obj.time_plan]
    return config_obj
