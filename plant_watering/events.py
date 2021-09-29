#!/bin/env python3
"""implements event class"""

import datetime

class Event:
  """Class for events that trigger exactly one routine. Multiple event handlers not supported."""
  def __init__(self, due_datetime, routine):
    self.due_datetime = due_datetime
    # routine is a function to be performed at scheduled time
    self.routine = routine

  def is_ready(self):
    """returns true if the event's scheduled time is now or in the past"""
    curr_datetime = datetime.datetime.now()
    return curr_datetime >= self.due_datetime

  def __str__(self):
    return f"{self.due_datetime} + {self.routine}"
