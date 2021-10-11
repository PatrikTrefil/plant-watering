#!/bin/env python3
"""module for working with a log git repository"""

import os
import datetime
import sys
import tempfile
from config import get_config
from git import Repo
from git import Git
import error
import logging

def log_to_repo(text:str):
  try:
    with tempfile.TemporaryDirectory() as tmpdir:
      config = get_config()
      git_ssh_identity_file = os.path.expanduser(config["ssh_key_path"])
      git_ssh_cmd = 'ssh -i %s' % git_ssh_identity_file
      with Git().custom_environment(GIT_SSH_COMMAND=git_ssh_cmd):
        repo = Repo.clone_from(config["log_repo_url"], tmpdir)
        curr_datetime = datetime.datetime.now()
        new_file_name = f"{curr_datetime.date()}--{curr_datetime.hour}-{curr_datetime.minute}.txt"
        new_file_path = os.path.join(tmpdir, new_file_name)
        text_to_append = text
        if (os.path.isfile(new_file_path)):
          text_to_append = "\n" + text_to_append
        with open(new_file_path, "a") as new_file:
          new_file.write(text_to_append)
        repo.index.add([new_file_path])
        repo.git.commit("-m", "automatic update")
        remote = repo.remote("origin")
        remote.push()
  except Exception as excep:
    logging.exception("Could not log to git repo")
    # HACK: should raise Error event, signalling should be an event handler
    # error.ErrorLog.signal_error()
