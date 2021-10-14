#!/bin/env python3
"""implements Plant class for watering systems"""

import os
import datetime
import logging
import board
import json
import git_log
from pump import Pump
import adafruit_pcf8591.pcf8591 as PCF
from adafruit_pcf8591.analog_in import AnalogIn
from adafruit_pcf8591.analog_out import AnalogOut

class Plant:
  @staticmethod
  def init_plants(plants_folder):
    """create plant objects based on configuration files from plants_folder"""
    plant_files_paths = [
      os.path.join(plants_folder, file_name)
      for file_name in os.listdir(plants_folder)]
    plant_configs = []
    for plant_file_path in plant_files_paths:
      with open(plant_file_path, "r") as plant_file:
        plant_configs += [json.load(plant_file)]

    logging.info("Loaded plant configs:\n%s", plant_configs)
    plants = [ \
      Plant(
        plantConfig["name"],
        Pump(plantConfig["pumpPin"]),
        plantConfig["minHumidity"],
        plantConfig["timePlan"]) \
      for plantConfig in plant_configs]
    return plants

  def __init__(self, name, pump, min_humidity, time_plan):
    self.name = name
    self.pump = pump
    self.min_humidity = min_humidity
    self.interval = datetime.timedelta(days=1)
    self.last_res = None
    self.last_measure_datetime = None
    i2c = board.I2C()
    pcf = PCF.PCF8591(i2c)
    self.soil_humidity_sensor = AnalogIn(pcf, PCF.A0)
    self.time_plan = [ \
      datetime.datetime.strptime(time_unit, "%H:%M").time() \
      for time_unit in time_plan]

  def __str__(self):
    return f"plant {self.name}"

  def measure(self):
    """returns voltage measured on pin"""
    raw_res = self.soil_humidity_sensor.value
    res = (raw_res / 65535) * self.soil_humidity_sensor.reference_voltage
    curr_datetime = datetime.datetime.now()
    logging.info("Measurement: %s", res)
    self.last_measure_datetime = curr_datetime
    self.last_res = res
    return res

  def water(self):
    logging.info("Watering plant %s", self.name)
    self.pump.pump(2)
