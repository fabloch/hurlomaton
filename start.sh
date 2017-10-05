#!/bin/sh
lpstat -p
sleep 2
python /home/pi/dev/hurlomaton/1_watch.py &
python /home/pi/dev/hurlomaton/2_hurlomaton.py &
