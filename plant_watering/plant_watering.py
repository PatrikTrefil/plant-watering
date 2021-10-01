#!/bin/env python3
"""plant watering system"""

import datetime
import signal
import time
from scheduler import Scheduler
import RPi.GPIO as GPIO
import plant
import events
import git_log
from config import get_config


def test_routine():
  print("provedeno")

def main():
  # cleanup
  signal.signal(signal.SIGTERM, lambda _ : GPIO.cleanup() )
  signal.signal(signal.SIGINT, lambda _ : GPIO.cleanup() )
  # init
  GPIO.setmode(GPIO.BOARD)
  config = get_config()
  scheduler = Scheduler()
  plant_list = plant.Plant.init_plants(config["plants_folder"])
  # setup events
  def measure(sender):
    sender.measure()
    scheduler.add_event(events.MeasurementDone(datetime.datetime.now(), sender))
  events.Measurement.add_event_listener(events.Measurement, measure)
  def water_if_needed(sender):
    if sender.last_res < sender.min_humidity:
      scheduler.add_event(events.LackOfWater(datetime.datetime.now(), sender))
  events.MeasurementDone.add_event_listener(events.MeasurementDone, water_if_needed)
  events.MeasurementDone.add_event_listener(events.MeasurementDone, lambda sender: git_log.log_to_repo(sender.last_res))

  # water when needed
  events.LackOfWater.add_event_listener(events.LackOfWater, lambda sender: sender.water())
  events.LackOfWater.add_event_listener(events.LackOfWater, lambda sender: git_log.log_to_repo(f"Watered {sender.name} at {datetime.datetime.now()}"))
  # day scheduling
  def schedule_day(sender):
    for plant_item in plant_list:
      # don't schedule for the past
      curr_datetime = datetime.datetime.now()
      for measurement_time in plant_item.time_plan:
        if measurement_time >= curr_datetime.time():
            desired_datetime = datetime.datetime.today()
            desired_datetime.hour = measurement_time.hour
            desired_datetime.minute = mesurement_time.minute
            scheduler.add_event(events.Measurement(desired_datetime, plant_item))

  events.ScheduleDay.add_event_listener(events.ScheduleDay, schedule_day)
  # schedule every night at 00:00
  events.ScheduleDay.add_event_listener(events.ScheduleDay, lambda sender:
    scheduler.add_event(events.ScheduleDay(datetime.datetime.today() + datetime.timedelta(days=1), scheduler))
  )
  scheduler.add_event(events.ScheduleDay(datetime.datetime.now(), None))

  # main loop
  while True:
    while scheduler.is_empty() or not scheduler.get_next_event().is_ready():
      time.sleep(20)
    scheduler.resolve_event()


if __name__=="__main__":
  main()
