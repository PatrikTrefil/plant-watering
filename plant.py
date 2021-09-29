#!/bin/env python3

from events import Event
import datetime
import git_log
import os
import pump

class Plant:
  @staticmethod
  def init_plants(plants_folder):
    """create plant objects based on configuration files from plants_folder"""
    plant_files_paths = os.listdir(plants_folder)
    plantConfigs = []
    for plant_file_path in plant_files_paths:
      with open(plant_file_path, "r") as plant_file:
        plantConfigs += [json.load(plant_file)]

    plants = [Plant(plantConfig.name, pump.Pump(plantConfig.pumpPin, plantConfig.minHumidity)) for plantConfig in plantConfigs]
    return plants

  def __init__(self, name, pump, min_humidity):
    self.name = name
    self.pump = pump
    self.min_humidity = min_humidity
    self.interval = datetime.timedelta(days=1)

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
    pump.pump(2)

  def care(self, scheduler):
    """This method takes care of everything the plant needs, i.e.:
      measure (log result) soil humidity,
      water if needed
      plan next care"""
    # measure
    res = self.measure()
    # watering
    if res <= self.min_humidity:
      self.water()
    # plan
    self.plan(
      scheduler,
      curr_datetime + interval,
      self.measure_and_plan
    )
