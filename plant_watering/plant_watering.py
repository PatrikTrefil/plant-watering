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
import event_listeners
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

  event_listeners.init_event_listeners(config, scheduler, plant_list)
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
