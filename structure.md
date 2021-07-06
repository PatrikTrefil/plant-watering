# Project Structure

This file describes how the project is layed out.

## Online availability

Script `update_repo.sh` is for uploading current
status to the repository *plant-watering-log*,
which can then be displayed using a web browser
or a mobile app. I think is's possible to get notifications
for new commits to the repo.

## Ssh status

There is a status file in `~/.local/plant_watering_status.txt`
which can be read using `cat`. If you don't want to open an interactive
shell, use this command: `ssh plants "cat ~/.local/plant_watering_status.txt"`
for plants alias.

## Plant watering system

I am (probably) using Python with this [library](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/).
