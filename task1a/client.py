#!/usr/bin/env python3
import socket
import sys
import time
import argparse
from datetime import datetime

def run_client(server_ip, port, cong_alg, duration=15, loss_rate=0):
    print(f"[CLIENT] Connecting to {server_ip}:{port} | Congestion: {cong_alg} | Start: {datetime.now().isoformat()}")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_TCP, socket.TCP_CONGESTION, cong_alg.encode())
    
    try:
        sock.connect((server_ip, port))
    except ConnectionRefusedError:
        print(f"[CLIENT] Connection refused! Check server status.", file=sys.stderr)
        sys.exit(1)
    
    start_time = time.time()
    total_sent = 0
    
    try:
        while time.time() - start_time < duration:
            data = b'X' * 1024  # 1KB payload
            sent = sock.send(data)
            total_sent += sent
            time.sleep(0.001)  # Prevent buffer overrun
            
    finally:
        duration_actual = time.time() - start_time
        sock.close()
        print(f"\n[CLIENT] Statistics for {cong_alg}:")
        print(f" - Total sent: {total_sent} bytes")
        print(f" - Duration: {duration_actual:.2f} seconds")
        print(f" - Throughput: {(total_sent * 8) / (duration_actual * 1e6):.2f} Mbps")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--option', required=True)
    parser.add_argument('--cong', default='cubic')
    parser.add_argument('--loss', type=float, default=0)
    parser.add_argument('--duration', type=int, default=15)
    args = parser.parse_args()

    run_client('10.0.0.7', 5201, args.cong, args.duration, args.loss)
