#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.log import setLogLevel, info, error
import time
import os
from topo import AssignmentTopo

def run_experiment(option, cong_algs=['cubic', 'westwood', 'scalable']):
    net = Mininet(topo=AssignmentTopo(), link=TCLink, controller=Controller)
    net.start()

    h1 = net.get('h1')
    h7 = net.get('h7')

    for cong in cong_algs:
        info(f'\n{"#"*40}\nTesting {cong} (15 seconds)\n{"#"*40}\n')
        
        # Clean previous processes
        h7.cmd('pkill -f "python3 server.py"')
        h7.cmd('killall tcpdump')
        time.sleep(1)  # Cleanup time

        # Start server with congestion control
        server_log = f'server_{cong}.log'
        h7.cmd(f'python3 server.py --option={option} --cong={cong} &> {server_log} &')
        info("Server started. Waiting 5 seconds...\n")
        time.sleep(5)  # Ensure server is ready

        # Start packet capture
        pcap_file = f"h7_{cong}.pcap"
        h7.cmd(f'tcpdump -i h7-eth0 -w {pcap_file} -v &')
        info(f"Started capture: {pcap_file}\n")
        time.sleep(2)  # Capture initialization

        # Run client test
        client_log = f'client_{cong}.log'
        h1.cmd(f'python3 client.py --option={option} --cong={cong} --duration=15 &> {client_log}')
        info("Client test completed.\n")

        # Stop capture and verify
        h7.cmd('killall tcpdump')
        time.sleep(2)  # Ensure capture file is written
        
        # Verify PCAP contents
        info(f"Verifying {pcap_file}...\n")
        pcap_info = h7.cmd(f'capinfos {pcap_file}')
        info(pcap_info + '\n')
        
        packet_count = h7.cmd(f'tshark -r {pcap_file} -Y "tcp.port==5201" | wc -l').strip()
        info(f"Packets in capture: {packet_count}\n")

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_experiment('a')
