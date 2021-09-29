#!/bin/env python3
"""library to handle event scheduling"""

import datetime
from sorted_linked_list import SortedLinkedList

class Scheduler:
  """Simple scheduler. No guarantee of execution in time."""
  def __init__(self):
    self.event_calendar = SortedLinkedList(None)

  def add_event(self, event):
    assert event.due_datetime >= datetime.datetime.now()
    print(f"Event added: {event}")
    self.event_calendar.add_item(event)

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
    print(f"Event resolved: {curr_event}")
    curr_event.routine()
