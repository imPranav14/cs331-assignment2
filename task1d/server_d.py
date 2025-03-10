import socket
import time

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_TCP, socket.TCP_CONGESTION, b'cubic')
    sock.bind(('0.0.0.0', 5201))
    sock.listen(5)
    
    start = time.time()
    total = 0
    
    while time.time() - start < 300:
        conn, _ = sock.accept()
        while True:
            data = conn.recv(1024)
            if not data: break
            total += len(data)
        conn.close()

if __name__ == '__main__':
    run_server()
