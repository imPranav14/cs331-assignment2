from mininet.net import Mininet
from mininet.node import Controller
from task3_topo import Task3Topo
import time

def run_experiment():
    net = Mininet(topo=Task3Topo(), controller=Controller)
    net.start()

    h1 = net.get('h1')
    h7 = net.get('h7')

    configs = [
        (1, 1),  # Nagle ON, Delayed-ACK ON
        (1, 0),  # Nagle ON, Delayed-ACK OFF
        (0, 1),  # Nagle OFF, Delayed-ACK ON
        (0, 0)   # Nagle OFF, Delayed-ACK OFF
    ]

    for idx, (nagle, delay_ack) in enumerate(configs, 1):
        print(f"\n{'#'*40}\nTEST {idx}: Nagle={'ON' if nagle else 'OFF'}, Delayed-ACK={'ON' if delay_ack else 'OFF'}\n{'#'*40}")

        # Start server
        h7.cmd(f'python3 task3_server.py --nagle={nagle} --delay_ack={delay_ack} > server_{idx}.log 2>&1 &')
        time.sleep(5)  # Wait for server to start

        # Start packet capture
        pcap = f"test3_{idx}.pcap"
        h7.cmd(f'tcpdump -i h7-eth0 -w {pcap} &')
        time.sleep(2)  # Capture initialization

        # Run client
        h1.cmd(f'python3 task3_client.py --nagle={nagle} --delay_ack={delay_ack} > client_{idx}.log 2>&1')

        # Cleanup
        time.sleep(5)  # Allow final packets to be captured
        h7.cmd('killall tcpdump; pkill -f task3_server.py')
        time.sleep(2)  # Ensure process cleanup

    net.stop()

if __name__ == '__main__':
    run_experiment()