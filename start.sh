#!/usr/bin/env bash

tmux new-session -d -s hector 'python3 src/HardwareRunner.py'
tmux new-window -t  hector:1 'python3 src/NeoPixel.py'
python3 src/main.py