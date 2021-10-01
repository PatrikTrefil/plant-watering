#!/bin/env python3
"""library to handle event scheduling"""

import datetime
from sorted_linked_list import SortedLinkedList
import events

class Scheduler:
  """Simple scheduler. No guarantee of execution in time."""
  def __init__(self):
    self.event_calendar = SortedLinkedList(None)

  def add_event(self, event):
    self.log("event added", event)
    self.event_calendar.add_item(event)

  def log(self, descr, event):
    print("|{:<10}|{:<10}|{:<10}|{:<10}|".format(descr, event, event.due_datetime, datetime.datetime.now()))

  def remove_next_event(self):
    removed_event = self.get_next_event()
    self.event_calendar.remove_start_node()
    if removed_event is not None:
      return removed_event
    return None

  def get_next_event(self):
    if self.event_calendar.start_node is not None:
      return self.event_calendar.start_node.value
    return None

  def is_empty(self):
    return self.event_calendar.start_node is None

  def resolve_event(self):
    curr_event = self.remove_next_event()
    self.log("resolving event", curr_event)
    for event_listener in events.Event.get_event_listener(type(curr_event)):
      event_listener(curr_event.sender)
    self.log("event resolved", curr_event)
