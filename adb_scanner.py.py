#!/usr/bin/env python3
# ---------------------------------------------------
# 🔒 ADB Vulnerability Framework
# ✨ Developed by: Mohanad Sayed
# 📅 Version: 4.0
# ---------------------------------------------------

import socket
import ipaddress
import threading
import random
from queue import Queue
from datetime import datetime

# إعدادات عامة
TIMEOUT = 2
DEFAULT_PORT = 5555
MAX_THREADS = 50

q = Queue()
results = []

# --- Multiple Banners ---
BANNERS = [
r"""
   _  _      _          _  _                 
   |  \/  | _ _| | __  | |/ ()_  __  _ __  
   | |\/| |/ ` | |/ / _ \ | ' /| / _|/ _ \| '_ \ 
   | |  | | (| |   <  _/ | . \| \_ \ () | | | |
   ||  ||\_,||\\_| ||\\|_/\_/|| |_|
----------------------------------------------------
   🚀 ADB Framework - Developed by: Mohanad Sayed
----------------------------------------------------
""",
r"""
      _       _       _             
     / \   _| |   | | __   __ _ 
    / _ \ / _` | | | | |/ _ \ / _` |
   / _ | (| | || | | () | (| |
  //   \\_,|\_,||\_/ \_, |
                              |_/ 
---------------------------------------
   🔥 Mohanad Sayed - ADB Framework
---------------------------------------
"""
]

def print_banner():
    print(random.choice(BANNERS))

# --- Scanner ---
def check_adb(ip, port=DEFAULT_PORT):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((ip, port))
        sock.send(b"host:version")
        data = sock.recv(1024)
        sock.close()

        if data:
            msg = f"[!] {ip}:{port} Vulnerable - ADB is OPEN"
            print(msg)
            results.append(msg)
        else:
            msg = f"[-] {ip}:{port} Open but no ADB response"
            print(msg)
            results.append(msg)

    except (socket.timeout, ConnectionRefusedError):
        pass
    except Exception as e:
        print(f"[!] Error on {ip}:{port} -> {e}")

def worker():
    while not q.empty():
        ip = q.get()
        check_adb(str(ip))
        q.task_done()

def scan_range(network, port=DEFAULT_PORT):
    print(f"\n[+] Scanning network: {network}")
    net = ipaddress.ip_network(network, strict=False)

    for ip in net.hosts():
        q.put(ip)

    for _ in range(min(MAX_THREADS, q.qsize())):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    q.join()

def save_report():
    if not results:
        print("\n[+] No vulnerable devices found 🎉")
        return

    filename = f"adb_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write("\n".join(results))
    print(f"\n[+] Report saved to: {filename}")

# --- CLI Framework ---
def cli():
    print_banner()
    print("Type 'help' for commands.\n")

    # Default options
    RHOST = None
    RPORT = DEFAULT_PORT

    while True:
        cmd = input("msfadb > ").strip()

        if cmd in ["exit", "quit"]:
            print("[+] Exiting framework. Goodbye Mohanad 🚀")
            break

        elif cmd == "help":
            print("""
Available commands:
  show options           Show current settings
  set RHOST <IP/CIDR>    Set target IP or Subnet
  set RPORT <PORT>       Set target port (default 5555)
  run                    Start scanning
  save                   Save results to report file
  clear                  Clear results
  exit                   Exit framework
""")

        elif cmd == "show options":
            print(f"""
Current Settings:
  RHOST => {RHOST if RHOST else 'Not set'}
  RPORT => {RPORT}
""")

        elif cmd.startswith("set "):
            parts = cmd.split()
            if len(parts) < 3:
                print("[!] Usage: set <OPTION> <VALUE>")
                continue

            option, value = parts[1], parts[2]

            if option.upper() == "RHOST":
                RHOST = value
                print(f"[+] RHOST set to {RHOST}")
            elif option.upper() == "RPORT":
                try:
                    RPORT = int(value)
                    print(f"[+] RPORT set to {RPORT}")
                except:
                    print("[!] Invalid port number")
            else:
                print(f"[!] Unknown option {option}")

        elif cmd == "run":
            if not RHOST:
                print("[!] Please set RHOST first (e.g., set RHOST 192.168.1.0/24)")
                continue

            results.clear()
            start_time = datetime.now()

            if "/" in RHOST:
                scan_range(RHOST, RPORT)
            else:
                check_adb(RHOST, RPORT)

            print(f"\n[+] Scan finished in {datetime.now() - start_time}")

        elif cmd == "save":
            save_report()

        elif cmd == "clear":
            results.clear()
            print("[+] Results cleared")

        else:
            print(f"[!] Unknown command: {cmd} (type 'help' for options)")

# --- Main ---
if _name_ == "_main_":
    cli()