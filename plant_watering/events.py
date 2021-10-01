#!/bin/env python3
"""implements event class"""

import datetime

class Event:
  """Class for events that trigger exactly one routine. Multiple event handlers not supported."""
  def __init__(self, due_datetime, sender):
    self.due_datetime = due_datetime
    self.sender = sender

  def is_ready(self):
    """returns true if the event's scheduled time is now or in the past"""
    curr_datetime = datetime.datetime.now()
    return curr_datetime >= self.due_datetime

  def __str__(self):
    return f"{self.due_datetime} + {self.sender}"

  event_listeners = set() # expects functions that have one parameter sender

# scheduler plans these on daily basis according to configuration
class Measurement(Event):
  pass

class MeasurementDone(Event):
  """
  This event should fire right after finishing humidity measuerments.
  The sender object is expected to have the result saved in sender.last_res
  """
  pass

class LackOfWater(Event):
  pass

class ScheduleDay(Event):
  pass
