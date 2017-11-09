#!/bin/sh
lpstat -p

python /home/pi/dev/hurlomaton/script_1_crop_watch.py | sed -e 's/^/[CROP] /' &
P1=$!
python /home/pi/dev/hurlomaton/script_2_upload_watch.py | sed -e 's/^/[UPLOAD] /' &
P2=$!
python /home/pi/dev/hurlomaton/script_3_print_watch.py | sed -e 's/^/[PRINT] /' &
P3=$!
python /home/pi/dev/hurlomaton/script_4_hurlomaton.py | sed -e 's/^/[HURLOMATON] /' &
P4=$!
wait $P1 $P2 $P3 $P4
