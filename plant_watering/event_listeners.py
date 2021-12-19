#!/bin/env python3
# pylint: disable=unused-variable, unused-argument

import datetime
import events
import git_log
from scheduler import Scheduler

def init_event_listeners(config, plant_list):
  @events.Measurement.register_as_listener
  def measure(sender):
    sender.measure()
    Scheduler.get_instance().add_event(events.MeasurementDone(datetime.datetime.now(), sender))

  @events.MeasurementDone.register_as_listener
  def water_if_needed(sender):
    if sender.last_res < sender.min_humidity:
      Scheduler.get_instance().add_event(events.LackOfWater(datetime.datetime.now(), sender))

  @events.MeasurementDone.register_as_listener
  def log_measurement_res_to_git(sender):
    git_log.log_to_repo(f"Measured {sender.name}: {sender.last_res}")

  @events.LackOfWater.register_as_listener
  def water_sender(sender):
    sender.water()

  @events.LackOfWater.register_as_listener
  def log_watering(sender):
    git_log.log_to_repo(f"Watered {sender.name}")

  @events.ScheduleDay.register_as_listener
  def schedule_day(sender):
    for plant_item in plant_list:
      # don't schedule for the past
      curr_datetime = datetime.datetime.now()
      for measurement_time in plant_item.time_plan:
        if measurement_time >= curr_datetime.time():
          desired_datetime = datetime.datetime.combine(
            datetime.date.today(),
            datetime.time(hour=measurement_time.hour, minute=measurement_time.minute))
          Scheduler.get_instance().add_event(events.Measurement(desired_datetime, plant_item))

  # schedule every night at 00:01
  @events.ScheduleDay.register_as_listener
  def schedule_scheduling(sender):
    next_day_midnight = datetime.datetime.combine( \
      datetime.date.today(), \
      datetime.time(hour=0, minute=1)) + datetime.timedelta(days=1)
    Scheduler.get_instance().add_event(events.ScheduleDay(next_day_midnight, scheduler))
