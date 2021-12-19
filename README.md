# Plant Watering for Raspberry Pi

This is a Raspberry Pi project that waters plants
based on soil humidity. Devices and circuits used
are described in a separate file.

## Goals

1. Water the plants
2. Have status of the plants available online ([log](https://github.com/PatrikTrefil/plant-watering-log))
3. Ability to get status via ssh

## Setup

### Warning

Provided that I decided to implement many things myself for practice,
there are probably bugs in this software. If you run into any issues,
please let me know via Github Issues, or make a PR with a fix.
### Prerequisites

- Python 3.7
  - pipenv
- Raspberry Pi
- empty Git repository for the log

Configuration can be found in `/config.json`.

- `log_repo_url` expects a repository address (for SSH connection)
- `ssh_key_path` expects a path to a SSH key, that can be used to connect to the specified repository
- `plants_folder` expects a path to folder that contains configuration files for individual plants
- `pins` expects an object describing the wiring

Plant configuration (JSON format):

- `name` expects a string with a name of the plant
- `pumpPin` expects the number of the pin used for the pump (GPIO.BOARD numbering)
- `minHumidity` expects a number defining the minimum soil humidity of the plant
- `timePlan` expect an array of (string) times, when to perform watering if needed

Install the `plant_watering.service` on your Raspberry Pi and start the service.
Make sure to set the correct WorkingDir and ExecStart.
