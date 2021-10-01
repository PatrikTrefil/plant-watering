#!/bin/env python3
"""plant watering system"""

import datetime
import signal
import time
from scheduler import Scheduler
import RPi.GPIO as GPIO
import plant
import events
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
<<<<<<< HEAD
  # setup events
  def measure(sender):
    sender.measure()
    scheduler.add_event(events.MeasurementDone(datetime.datetime.now(), sender))
  events.Measurement.add_event_listener(measure)
  def water_if_needed(sender):
    if sender.last_res < sender.min_humidity:
      scheduler.add_event(events.LackOfWater(datetime.datetime.now(), sender))
  events.MeasurementDone.add_event_listener(water_if_needed)

  # water when needed
  events.LackOfWater.add_event_listener(lambda sender: sender.water())
  # day scheduling
  def schedule_day(sender):
    for plant_item in plant_list:
      # don't schedule for the past
      curr_datetime = datetime.datetime.now()
      for measurement_time in config.time_plan:
        if measurement_time >= curr_datetime:
            scheduler.add_event(events.Measurement(measurement_time, None))

  events.ScheduleDay.add_event_listener(schedule_day)
  # schedule every night at 00:00
  events.ScheduleDay.add_event_listener(lambda sender:
    scheduler.add_event(events.ScheduleDay(datetime.datetime.today() + datetime.timedelta(days=1)))
  )
  scheduler.add_event(events.ScheduleDay(datetime.datetime.now()))
=======
  # schedule for next 10:00 AM
  todays_watering_time = \
    datetime.datetime.today() + datetime.timedelta(hours=config["time_of_watering"])

  if datetime.datetime.now() > todays_watering_time:
    planned_time = \
      datetime.datetime.today() + datetime.timedelta(days=1, hours=config.time_of_watering)
  else:
    planned_time = todays_watering_time

  for plant_item in plant_list:
    scheduler.add_event(Event(planned_time, plant_item.care))
>>>>>>> main

  # main loop
  while True:
    while scheduler.is_empty() or not scheduler.get_next_event().is_ready():
      time.sleep(20)
    scheduler.resolve_event()


if __name__=="__main__":
  main()
