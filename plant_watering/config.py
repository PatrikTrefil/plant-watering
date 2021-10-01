#!/bin/env python3
"""Provides access to program configuration"""

import json
import datetime

def get_config():
  """returns config object"""
  CONFIG_FILE_PATH = "./config.json"
  with open(CONFIG_FILE_PATH, "r") as config_file:
    config_obj = json.load(config_file)
    return config_obj
