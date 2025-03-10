#!/usr/bin/env python3
"""
Mininet Experiment Script for Assignment 2:
Manually runs iperf3 tests on H1 → H7 using three TCP congestion control protocols:
cubic, westwood, and scalable.
Before each test, the script pauses and prompts you to press Enter.
This script uses the topology defined in assignment_topo.py.
"""

from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.util import dumpNodeConnections
import time

# Import your provided topology from assignment_topo.py
from topo import AssignmentTopo

def runExperiment():
    # Create the network using the provided topology
    net = Mininet(topo=AssignmentTopo(), link=TCLink, controller=Controller)
    net.start()

    info('*** Dumping host connections\n')
    dumpNodeConnections(net.hosts)
    
    info('*** Running ping test\n')
    net.pingAll()

    # Get the client and server hosts
    h1 = net.get('h1')
    h7 = net.get('h7')
    
    # Start iperf3 server on h7 in the background
    info('*** Starting iperf3 server on h7\n')
    h7.cmd('iperf3 -s &')
    time.sleep(2)  # Allow server to start

    # Get H7's IP address
    h7_ip = h7.IP()
    info('*** H7 IP: %s\n' % h7_ip)

    # List of congestion control protocols to test
    protocols = ['cubic', 'westwood', 'scalable']

    # Run tests manually for each protocol
    for proto in protocols:
        input("Press Enter to run iperf3 test on h1 with protocol: %s ..." % proto)
        info('*** Running iperf3 test on h1 with protocol: %s\n' % proto)
        # Run the iperf3 test from H1 to H7
        output = h1.cmd('iperf3 -c %s -p 5201 -b 10M -P 10 -t 10 -C %s' % (h7_ip, proto))
        info('*** Test output for %s:\n%s\n' % (proto, output))
        time.sleep(5)  # Optional pause before next test

    # Stop the iperf3 server on h7
    info('*** Stopping iperf3 server on h7\n')
    h7.cmd('killall iperf3')

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    runExperiment()
