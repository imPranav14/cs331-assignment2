#!/usr/bin/env python3
import socket
import sys
import time
import argparse
from threading import Thread
from datetime import datetime

def run_server(host, port, cong_alg, loss_rate=0):
    # Create TCP socket with congestion control
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_TCP, socket.TCP_CONGESTION, cong_alg.encode())
    
    try:
        sock.bind((host, port))
    except OSError as e:
        print(f"[SERVER] Bind failed: {str(e)}", file=sys.stderr)
        sys.exit(1)

    sock.listen(5)
    print(f"[SERVER] Listening on {host}:{port} | Congestion: {cong_alg} | Started at {datetime.now().isoformat()}")
    
    # Metrics tracking
    total_bytes = 0
    start_time = time.time()
    active = True
    
    def handle_client(conn):
        nonlocal total_bytes
        while active:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                total_bytes += len(data)
            except ConnectionResetError:
                break
        conn.close()

    try:
        conn, addr = sock.accept()
        print(f"[SERVER] Connection from {addr[0]}:{addr[1]}")
        Thread(target=handle_client, args=(conn,)).start()
        
        # Run for 15 seconds (matches client duration)
        time.sleep(15)
        active = False
        
    finally:
        duration = time.time() - start_time
        sock.close()
        print(f"\n[SERVER] Statistics for {cong_alg}:")
        print(f" - Total data: {total_bytes} bytes")
        print(f" - Duration: {duration:.2f} seconds")
        print(f" - Goodput: {(total_bytes * 8) / (duration * 1e6):.2f} Mbps")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--option', required=True)
    parser.add_argument('--cong', default='cubic')
    parser.add_argument('--loss', type=float, default=0)
    args = parser.parse_args()

    run_server('0.0.0.0', 5201, args.cong, args.loss)