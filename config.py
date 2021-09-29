#!/bin/env python3

import json

def get_config():
  CONFIG_FILE_PATH = "./config.json"
  with open(CONFIG_FILE_PATH, "r") as config_file:
    return json.load(config_file)
