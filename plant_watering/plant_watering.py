#!/bin/env python3
"""plant watering system"""

from scheduler import Scheduler
import RPi.GPIO as GPIO
import plants
import datetime
import signal
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
  plant_list = plants.init_plants(config["plants_folder"])
  # schedule for next 10:00 AM
  if (datetime.datetime.now() > datetime.datetime.today() + datetime.timedelta(hours=config.time_of_watering)):
    planned_time = datetime.datetime.today() + datetime.timedelta(days=1, hours=config.time_of_watering)
  else:
    planned_time = datetime.datetime.today() + datetime.timedelta(hours=config.time_of_watering)

  for plant in plant_list:
    scheduler.add_event(Event(planned_time, plant.care))

  # main loop
  while True:
    while scheduler.is_empty() or not scheduler.get_next_event().is_ready():
      time.sleep(20)
    scheduler.resolve_event()


if __name__=="__main__":
  main()
