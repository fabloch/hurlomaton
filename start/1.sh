#!/bin/sh
# Execute python script script_1_crop_watch

pause() {
    read -n1 -rsp $'Press any key to close the terminal...\n'
}
cd /home/pi/dev/hurlomaton/
python script_1_crop_watch.py

pause