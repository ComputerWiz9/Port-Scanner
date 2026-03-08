import socket
import threading
from queue import Queue
import argparse
import sys

services = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP"
}

print("""
======================================================
    PYTHON MULTITHREADED SCANNER PORT SCANNER
            Built by Sami
======================================================
""")

parser = argparse.ArgumentParser(description="Multithreaded Python Port Scanner")
parser.add_argument("-t", "--target", help="Target IP or domain")
parser.add_argument("-p", "--port", help="Port range, e.g., 1-1024", default="1-1024")
args = parser.parse_args()

if args.target:
    target = args.target
else:
    target = input("Enter target IP or domain: ")

if target.lower() == "coffee":
    print("\n☕ ACCESSING CAFFEINE PROTOCOL...")
    print("Granting developer energy boost...\n")
    sys.exit(0)

port_range =args.port.split("-")
start_port = int(port_range[0])
end_port = int(port_range[1])

print(f"\nScanning {target} from port {start_port} to {end_port}")
print("-" * 50)

queue = Queue()
open_ports = []
lock = threading.Lock()
total_ports = end_port - start_port + 1
counter = 0

def scan_port():
    global counter
    while not queue.empty():
        port = queue.get()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)

        try:
         result = s.connect_ex((target, port))
         if result == 0:
            service = services.get(port, "Unknown")
            with lock:
                open_ports.append((port, service))
                print(f"[+] OPEN PORT {port} ({service})")
        except (socket.error, OSError):
            pass

        s.close()
        queue.task_done()

        with lock:
             counter += 1
             print(f"\rScanning... {counter}/{total_ports} ports", end="", flush=True)


for port in range(start_port, end_port + 1):
        queue.put(port)

num_threads = 100
for _ in range(num_threads):
        t = threading.Thread(target=scan_port)
        t.daemon = True
        t.start()

queue.join()

with lock:
    with open("scan_results.txt", "w") as f:
        for port, service in open_ports:
            f.write(f"{port} {service}\n")

print("\n\nScan Complete.")

if open_ports:
    print("\nOpen Ports Found:")
    for port, service in open_ports:
        print(f"[+] {port} ({service}")
else:
     print("No open ports found.")

print("\nResults saved to scan_results.txt")