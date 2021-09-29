#!/bin/env python3

class Node:
  def __init__(self, value, next=None):
    self.value = value
    self.next = next

class SortedLinkedList:
  def __init__(self, start_node=None):
    self.start_node = start_node

  def add_node(self, new_node):
    if self.start_node == None:
      self.start_node = new_node
    else:
      prev_node = None
      curr_node = self.start_node
      while (new_node.value > curr_node.value):
        prev_node = curr_node
        curr_node = curr_node.next
      # add new node between prev and curr
      if prev_node is None:
        self.start_node = new_node
        new_node.next = curr_node
      else:
        prev_node.next = new_node
        new_node.next = curr_node

  def remove_start_node(self):
    if self.start_node is not None:
      self.start_node = self.start_node.next
