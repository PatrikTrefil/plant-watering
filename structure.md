# Project Structure

This file describes how the project is layed out.

## Scheduler

`scheduler.py` is a simple module for scheduling events.
(Cron could be used instead)

## Plant configuration

`config.json` contains all configuration for plants (pins, watering
times, etc.)

## Online availability

`git_log.py` takes care of logging to git.

## Ssh status

The plan is to utilize sockets to receive requests for commands.
