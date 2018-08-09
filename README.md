
# Fishbowl CS Club 2018

## Setting up:

The programs are built for Python3.6.

Install dependencies for programs `python3.6 -m pip3.6 install -Ur requirements.txt`
or alternatively do pip3.6 install click matplotlib

## Running.

Conways game of life: python3.6 game_of_life.py
Spirographs: python3.6 spirographs.py

Each program has a CLI interface for arguments which can be seen via --help.
ie: 
``python3.6 game_of_life.py --help
Usage: game_of_life.py [OPTIONS]

Options:
  --gridsize INTEGER      Size of grid, must be greater than 8
  --movfile TEXT          File to save animation to
  --interval INTEGER      Interval for each frame in miliseconds, ie: 1000 = 1
                          second
  --glider / --no-glider  Have a glider on the screen or not.
  --density INTEGER       Density of screen, ie: 70 = 70% full
  --help                  Show this message and exit.
``
