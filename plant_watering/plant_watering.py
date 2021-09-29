#!/bin/env python3
"""plant watering system"""

import datetime
import signal
import time
from scheduler import Scheduler
import RPi.GPIO as GPIO
import plant
from events import Event
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
  # schedule for next 10:00 AM
  todays_watering_time = \
    datetime.datetime.today() + datetime.timedelta(hours=config.time_of_watering)

  if datetime.datetime.now() > todays_watering_time:
    planned_time = \
      datetime.datetime.today() + datetime.timedelta(days=1, hours=config.time_of_watering)
  else:
    planned_time = todays_watering_time

  for plant_item in plant_list:
    scheduler.add_event(Event(planned_time, plant_item.care))

  # main loop
  while True:
    while scheduler.is_empty() or not scheduler.get_next_event().is_ready():
      time.sleep(20)
    scheduler.resolve_event()


if __name__=="__main__":
  main()
