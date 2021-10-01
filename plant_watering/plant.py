#!/bin/env python3
"""implements Plant class for watering systems"""

import os
import datetime
import json
import git_log
from pump import Pump

class Plant:
  @staticmethod
  def init_plants(plants_folder):
    """create plant objects based on configuration files from plants_folder"""
    plant_files_paths = [os.path.join(plants_folder, file_name) for file_name in os.listdir(plants_folder)]
    plant_configs = []
    for plant_file_path in plant_files_paths:
      with open(plant_file_path, "r") as plant_file:
        plant_configs += [json.load(plant_file)]

    print(f"Loaded plant configs:\n{plant_configs}")
    plants = [ \
      Plant(plantConfig["name"], Pump(plantConfig["pumpPin"]), plantConfig["minHumidity"], plantConfig["timePlan"]) \
      for plantConfig in plant_configs]
    return plants

  def __init__(self, name, pump, min_humidity, time_plan):
    self.name = name
    self.pump = pump
    self.min_humidity = min_humidity
    self.interval = datetime.timedelta(days=1)
    self.last_res = None
    self.last_measure_datetime = None
    self.time_plan = [datetime.datetime.strptime(time_unit, "%H:%M").time() for time_unit in time_plan]

  def measure(self):
    res = -1
    raise Exception("Not implemented")
    curr_datetime = datetime.datetime.now()
    git_log.log_to_repo(f"{curr_datetime} - {res} %")
    print(f"Measurement: {res}")
    self.last_measure_datetime = curr_datetime
    self.last_res = res
    return res

  def water(self):
    print(f"Watering plant {self.name}")
    self.pump.pump(2)
