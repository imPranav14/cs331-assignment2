import socket
import time
import argparse

def run_client(duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_TCP, socket.TCP_CONGESTION, b'cubic')
    sock.connect(('10.0.0.7', 5201))
    
    start = time.time()
    while time.time() - start < duration:
        sock.send(b'X' * 1024)
        time.sleep(0.001)
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=int, required=True)
    args = parser.parse_args()
    run_client(args.duration)