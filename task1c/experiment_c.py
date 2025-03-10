from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from assignment_topo_c import AssignmentTopoC  # Critical import fix
import time

def run_test(test_name, clients, duration):
    net = Mininet(topo=AssignmentTopoC(), link=TCLink, controller=Controller)
    net.start()
    
    h7 = net.get('h7')
    h7.cmd('pkill -f "python3 server_c.py"; python3 server_c.py &')
    time.sleep(2)
    
    # Start capture
    pcap = f'{test_name}_c.pcap'
    h7.cmd(f'tcpdump -i h7-eth0 -w {pcap} &')
    
    # Start clients
    for client in clients:
        host = net.get(client['name'])
        cmd = f'python3 client_c.py --duration={duration} &'
        host.cmd(cmd)
        time.sleep(client['delay'])
    
    time.sleep(duration + 5)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    
    # Condition 1: H3->H7
    run_test('condition1', [{'name': 'h3', 'delay': 0}], 150)
    
    # Condition 2a: H1+H2->H7
    run_test('condition2a', [
        {'name': 'h1', 'delay': 0},
        {'name': 'h2', 'delay': 15}
    ], 120)
    
    # Condition 2b: H1+H3->H7 
    run_test('condition2b', [
        {'name': 'h1', 'delay': 0},
        {'name': 'h3', 'delay': 30}
    ], 90)
    
    # Condition 2c: H1+H3+H4->H7
    run_test('condition2c', [
        {'name': 'h1', 'delay': 0},
        {'name': 'h3', 'delay': 15},
        {'name': 'h4', 'delay': 30}
    ], 90)
