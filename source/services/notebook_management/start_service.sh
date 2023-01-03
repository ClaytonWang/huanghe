#!/bin/bash
nohup python3 scheduler_task.py > scheduler.log 2>&1 &
python3 main.py