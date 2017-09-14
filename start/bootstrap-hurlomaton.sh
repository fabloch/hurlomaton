#!/bin/sh
python /home/pi/Desktop/huuurlomaton/camera/hurlomaton.py &>/dev/null &
node /home/pi/dev/huuurlomaton/interface/server.js &>/dev/null &
chromium-browser http://localhost:3000/ --kiosk

