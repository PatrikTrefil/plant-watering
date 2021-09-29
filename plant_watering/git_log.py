#!/bin/env python3
"""module for working with a log git repository"""

import subprocess
from config import get_config
from git import Repo
import tempfile
import os
import datetime


def log_to_repo(text:str):
  try:
    with tempfile.TemporaryDirectory() as tmpdir:
      config = get_config()
      repo = Repo.clone_from(config["log_repo_url"], tmpdir)
      curr_datetime = datetime.datetime.today()
      new_file_name = f"{curr_datetime.date()}--{curr_datetime.hour}-{curr_datetime.minute}.txt"
      new_file_path = os.path.join(tmpdir, new_file_name)
      with open(new_file_path, "w") as new_file:
        new_file.write(text)
      repo.index.add([new_file_path])
      repo.git.commit("-m", "automatic update")
      remote = repo.remote("origin")
      remote.push()
  except Exception as e:
    led.flash(10)
