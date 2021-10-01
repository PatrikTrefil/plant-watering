#!/bin/env python3
"""Simple implementation of sorted linked list"""

class SortedLinkedList:
  class Node:
    def __init__(self, value, next_item=None):
      self.value = value
      self.next_item = next_item

  def __init__(self, start_node=None):
    self.start_node = start_node

  def __add_node__(self, new_node):
    if self.start_node is None:
      self.start_node = new_node
    else:
      prev_node = None
      curr_node = self.start_node
      while new_node.value > curr_node.value:
        prev_node = curr_node
        curr_node = curr_node.next
      # add new node between prev and curr
      if prev_node is None:
        self.start_node = new_node
        new_node.next = curr_node
      else:
        prev_node.next = new_node
        new_node.next = curr_node

  def add_item(self, item):
    self.__add_node__(Node(item))

  def remove_start_node(self):
    if self.start_node is not None:
      self.start_node = self.start_node.next
