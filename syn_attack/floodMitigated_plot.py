#!/usr/bin/env python3
from scapy.all import rdpcap, IP, TCP
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def normalize_connection(pkt):
    """
    Return a normalized tuple (src_ip, dst_ip, src_port, dst_port)
    so that connections are uniquely identified regardless of direction.
    """
    src_ip = pkt[IP].src
    dst_ip = pkt[IP].dst
    src_port = pkt[TCP].sport
    dst_port = pkt[TCP].dport
    if src_ip < dst_ip or (src_ip == dst_ip and src_port <= dst_port):
        return (src_ip, dst_ip, src_port, dst_port)
    else:
        return (dst_ip, src_ip, dst_port, src_port)

# Use the mitigated flood PCAP file
pcap_path = '/Users/pranav/Desktop/sem6/CN/assignment2/SYN/floodMitigated.pcap'
packets = rdpcap(pcap_path)

connections = {}

for pkt in packets:
    # Process only packets that have both IP and TCP layers
    if not (IP in pkt and TCP in pkt):
        continue
    conn = normalize_connection(pkt)
    tcp = pkt[TCP]
    
    # Identify connection start: packet with SYN flag only (no ACK)
    if 'S' in tcp.flags and 'A' not in tcp.flags:
        if conn not in connections:
            connections[conn] = {
                'start': float(pkt.time),
                'end': None,
                'fin_ack_seen': False,
                'status': 'open'
            }
    
    # If connection exists and no end time recorded, check for termination events
    if conn in connections and connections[conn]['end'] is None:
        # Case 1: RESET event
        if 'R' in tcp.flags:
            connections[conn]['end'] = float(pkt.time)
            connections[conn]['status'] = 'reset'
        # Case 2: FIN-ACK observed
        elif 'F' in tcp.flags and 'A' in tcp.flags:
            connections[conn]['fin_ack_seen'] = True
        # Case 3: ACK-only packet after FIN-ACK indicates termination
        elif connections[conn]['fin_ack_seen'] and tcp.flags == 'A':
            connections[conn]['end'] = float(pkt.time)
            connections[conn]['status'] = 'closed'

# Compute connection durations and start times for plotting
durations = []
start_times = []
for conn, data in connections.items():
    # If no termination, assign a default duration of 100 seconds
    duration = data['end'] - data['start'] if data['end'] is not None else 100.0
    durations.append(duration)
    start_times.append(datetime.fromtimestamp(data['start']))

# Determine baseline time from the earliest connection start time
baseline = min(data['start'] for data in connections.values())
attack_start_time = datetime.fromtimestamp(baseline + 20)  # Attack starts 20 seconds after baseline
attack_end_time   = datetime.fromtimestamp(baseline + 120) # Attack ends 120 seconds after baseline

# Plot connection duration vs. connection start time
plt.figure(figsize=(14, 7))
plt.scatter(start_times, durations, alpha=0.7, edgecolors='k')
plt.xlabel('Connection Start Time')
plt.ylabel('Connection Duration (seconds)')
plt.title('TCP Connection Durations (Mitigated SYN Flood)')
plt.grid(True)

# Format x-axis as HH:MM:SS
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gcf().autofmt_xdate()

# Mark the attack period using vertical dashed lines (blue for mitigated case)
plt.axvline(attack_start_time, color='blue', linestyle='--', label='Attack Start (Mitigated)')
plt.axvline(attack_end_time, color='blue', linestyle='--', label='Attack End (Mitigated)')
plt.legend()

plt.tight_layout()
plt.show()
