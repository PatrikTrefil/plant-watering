#!/usr/bin/env python3

import socket
import logging
import json
from config import get_config
from scheduler import Scheduler


def window(host='127.0.0.1', port=65432):
  """
  open socket for client to look inside the running program
  @host Standard loopback interface address (localhost)
  @port Port to listen on (non-privileged ports are > 1023)
  """
  logging.info("Window thread: started")
  while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((host, port))
      s.listen()
      conn, addr = s.accept()
      with conn:
        logging.info("Connected by %s", addr)
        while True:
          data = conn.recv(1024)
          if not data:
            break
          if data.decode('utf-8') == "scheduler":
            conn.sendall(json.dumps(Scheduler.get_instance().__dict__).encode('utf-8'))
          else:
            break
