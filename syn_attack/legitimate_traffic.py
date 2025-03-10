import socket
import time

SERVER_IP = "192.168.64.2"
SERVER_PORT = 12345

def generate_legitimate_traffic():
    print("Starting legitimate traffic...")
    start_time = time.time()

    while time.time() - start_time < 140:  # Run for 140 seconds
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, SERVER_PORT))
            data = client_socket.recv(1024)
            print(f"Received: {data.decode()}")
            client_socket.close()
        except Exception as e:
            print(f"Connection failed: {e}")
        time.sleep(1)  # New connection every 1 second

    print("Legitimate traffic stopped.")

if __name__ == "__main__":
    generate_legitimate_traffic()
