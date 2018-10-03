#!/bin/bash
source /home/pi/dev/virtualenv/hurlo/bin/activate
cd /home/pi/dev/hurlomaton
python3 1_crop_watch.py &
python3 2_upload_watch.py &
python3 3_hurlomaton.py