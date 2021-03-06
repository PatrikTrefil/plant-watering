#!/bin/env python3
"""plant watering system"""

import datetime
import signal
import threading
import time
import logging
from scheduler import Scheduler
from window import window
from RPi import GPIO
import plant
import events
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

  windowThread = threading.Thread(
    target=window,
    args=(config.socket.host, config.socket.port),
    daemon=True)
  windowThread.start()

  plant_list = plant.Plant.init_plants(config["plants_folder"])
  scheduler = Scheduler.get_instance()

  event_listeners.init_event_listeners(config, plant_list)
  scheduler.add_event(events.ScheduleDay(datetime.datetime.now(), None))

  # main loop
  while True:
    while scheduler.is_empty() or not scheduler.get_next_event().is_ready():
      time.sleep(DELAY_OF_BUSY_WAITING)
    scheduler.resolve_next_event()


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
