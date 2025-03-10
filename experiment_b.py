#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.log import setLogLevel, info, error
import time
import os
from topo import AssignmentTopo

CLIENT_CONFIG = [
    {'host': 'h1', 'delay': 0, 'duration': 150},
    {'host': 'h3', 'delay': 15, 'duration': 120},
    {'host': 'h4', 'delay': 30, 'duration': 90}
]

def run_experiment_b():
    net = Mininet(topo=AssignmentTopo(), link=TCLink, controller=Controller)
    net.start()
    
    for cong in ['cubic', 'westwood', 'scalable']:
        info(f'\n{"#"*40}\nTesting {cong} congestion control\n{"#"*40}\n')
        
        h7 = net.get('h7')
        h7.cmd('pkill -f "python3 server.py"; killall tcpdump')
        time.sleep(1)
        
        # Start server with explicit IP binding
        server_cmd = f'python3 server.py --option=b --cong={cong} &> server_{cong}.log &'
        h7.cmd(server_cmd)
        time.sleep(5)  # Increased server start time
        
        # Start capture with absolute path
        pcap_dir = os.path.abspath('.')
        pcap_file = f"{pcap_dir}/h7_{cong}.pcap"
        h7.cmd(f'tcpdump -i h7-eth0 -w {pcap_file} &')
        info(f"Capture started: {pcap_file}\n")
        
        # Start staggered clients with validation
        for client in CLIENT_CONFIG:
            host = net.get(client['host'])
            cmd = (
                f'sleep {client["delay"]}; '
                f'python3 client.py --option=b --cong={cong} '
                f'--duration={client["duration"]} &> client_{cong}_{client["host"]}.log &'
            )
            host.cmd(cmd)
            info(f"Started {client['host']} after {client['delay']}s\n")
        
        # Wait for longest duration + buffer
        total_wait = 150 + 30
        info(f"Waiting {total_wait}s for tests...\n")
        time.sleep(total_wait)
        
        # Verify capture file
        if not os.path.exists(pcap_file):
            error(f"ERROR: {pcap_file} not created!\n")
        else:
            info(f"Capture size: {os.path.getsize(pcap_file)} bytes\n")
        
        h7.cmd('killall tcpdump; pkill -f "python3 server.py"')

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_experiment_b()