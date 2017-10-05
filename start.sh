#!/bin/sh
lpstat -p
sleep 2
python /home/pi/dev/hurlomaton/script_1_upload_watch.py &
python /home/pi/dev/hurlomaton/script_2_print_watch.py &
python /home/pi/dev/hurlomaton/script_3_hurlomaton.py &
