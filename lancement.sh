#!/bin/bash
source /home/pi/dev/venv/bin/activate
cd /home/pi/dev/hurlomaton
echo "tempo pour la caméra 5..." &&
sleep 1s &&
echo "4..." &&
sleep 1s &&
echo "3..." &&
sleep 1s &&
echo "2..." &&
sleep 1s &&
echo "1..." &&
sleep 1s &&
echo "lancement du hurlomaton" &&
python3 0_hardware_check.py
