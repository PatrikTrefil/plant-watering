#!/bin/env python3
"""plant watering system"""

import datetime
import signal
import time
import logging
import sys
from scheduler import Scheduler
import RPi.GPIO as GPIO
import plant
import events
import git_log
from config import get_config
from systemd.journal import JournaldLogHandler

DELAY_OF_BUSY_WAITING = 0.3

def main():
  logging.info("Starting plant watering")
  # cleanup
  signal.signal(signal.SIGTERM, lambda _ : GPIO.cleanup() )
  signal.signal(signal.SIGINT, lambda _ : GPIO.cleanup() )
  # init
  GPIO.setmode(GPIO.BOARD)


  config = get_config()
  scheduler = Scheduler()
  plant_list = plant.Plant.init_plants(config["plants_folder"])
  # setup events
  # HACK: don't have hardware for measuring
  # @events.Event.register_as_listener(evenets.Measurement)
  def measure(sender):
    sender.measure()
    scheduler.add_event(events.MeasurementDone(datetime.datetime.now(), sender))
  @events.Event.register_as_listener(events.MeasurementDone)
  def water_if_needed(sender):
    if sender.last_res < sender.min_humidity:
      scheduler.add_event(events.LackOfWater(datetime.datetime.now(), sender))

  @events.Event.register_as_listener(events.MeasurementDone)
  def log_measurement_res_to_git(sender):
    git_log.log_to_repo(sender.last_res)

  # water when needed
  @events.Event.register_as_listener(events.LackOfWater)
  def water_sender(sender):
    sender.water()
  @events.Event.register_as_listener(events.LackOfWater)
  def log_watering(sender):
    git_log.log_to_repo(f"Watered {sender.name}")

  @events.Event.register_as_listener(events.ScheduleDay)
  def schedule_day(sender):
    for plant_item in plant_list:
      # don't schedule for the past
      curr_datetime = datetime.datetime.now()
      for measurement_time in plant_item.time_plan:
        if measurement_time >= curr_datetime.time():
            desired_datetime = datetime.datetime.combine(
              datetime.date.today(),
              datetime.time(hour=measurement_time.hour, minute=measurement_time.minute))
            # HACK: should be Measurement, but measuring not yet implemented
            scheduler.add_event(events.LackOfWater(desired_datetime, plant_item))

  # schedule every night at 00:01
  @events.Event.register_as_listener(events.ScheduleDay)
  def schedule_scheduling(sender):
    next_day_midnight = datetime.datetime.combine( \
      datetime.date.today(), \
      datetime.time(hour=0, minute=1)) + datetime.timedelta(days=1)
    scheduler.add_event(events.ScheduleDay(next_day_midnight, scheduler))

  scheduler.add_event(events.ScheduleDay(datetime.datetime.now(), None))

  # main loop
  while True:
    while scheduler.is_empty() or not scheduler.get_next_event().is_ready():
      time.sleep(DELAY_OF_BUSY_WAITING)
    scheduler.resolve_event()


if __name__=="__main__":
  # logging config
  r = logging.root
  r.setLevel(logging.DEBUG)
  r.addHandler(JournaldLogHandler())
  try:
    main()
  except Exception as e:
    logging.exception("App crashed")
    GPIO.cleanup()
