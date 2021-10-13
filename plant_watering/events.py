#!/bin/env python3
"""implements event class"""

import datetime

class Event:
  """
  Class for events that trigger exactly one routine.
  Multiple event handlers not supported.
  """
  def __init__(self, due_datetime, sender):
    self.due_datetime = due_datetime
    self.sender = sender

  def is_ready(self):
    """returns true if the event's scheduled time is now or in the past"""
    curr_datetime = datetime.datetime.now()
    return curr_datetime >= self.due_datetime

  def __str__(self):
    fmted_time = self.due_datetime.strftime('%y-%m-%d %H:%M')
    return f"{type(self)} sent by {self.sender}, planned for {fmted_time}"

  __event_listeners__ = dict() # expects functions that have one parameter sender

  @staticmethod
  def add_event_listener(event_class, func):
    if event_class not in Event.__event_listeners__:
      Event.__event_listeners__[event_class] = set()
    Event.__event_listeners__[event_class].add(func)

  @staticmethod
  def get_event_listener(event_class):
    return Event.__event_listeners__[event_class]

  @staticmethod
  def register_as_listener(event_class):
    """to be used as decorator"""
    def decorator(func):
      Event.add_event_listener(event_class, func)
      return func
    return decorator


class Measurement(Event):
  """scheduler plans these on daily basis according to the configuration"""

class MeasurementDone(Event):
  """
  This event should fire right after finishing humidity measuerments.
  The sender object is expected to have the result saved in sender.last_res
  """

class LackOfWater(Event):
  """
  if we measure soil humidity under configured threshold, this event
  fires and we water the plant
  """

class ScheduleDay(Event):
  """
  this triggers daily planning and plans itself for the next day
  """
