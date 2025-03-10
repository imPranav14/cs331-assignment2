#!/bin/bash
PPID=$!
echo "Starting packet capture..."

python3 legitimate_traffic.py &

# Wait 20 seconds before starting the SYN flood
sleep 20

# Start SYN flood attack for 100 seconds
sudo ./syn_flood.sh &

# Store hping3 PID to kill it later
SYN_PID=$!

# Wait 100 seconds for the attack to complete
sleep 100

# Stop the SYN flood attack
kill $SYN_PID
echo "SYN flood attack terminated."

# Wait 20 more seconds for legitimate traffic to finish (total 140s)
sleep 20
kill $PPID
