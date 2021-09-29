#!/bin/env python3

import datetime

class Event:
  """Class for events that trigger exactly one routine. Multiple event handlers not supported."""
  def __init__(self, datetime, routine):
    self.datetime = datetime
    # routine is a function to be performed at scheduled time
    self.routine = routine

  def is_ready(self):
    """returns true if the event's scheduled time is now or in the past"""
    curr_datetime = datetime.datetime.now()
    return curr_datetime >= self.datetime

  def __str__(self):
    return f"{self.datetime} + {self.routine}"
