import subprocess
import time
from datetime import datetime
import re
import threading

domain = input("Enter the domain name: ")
dns_server = input("Enter the DNS server to use (e.g. 8.8.8.8): ")

raw_file = "ips_raw.txt"
unique_file = "ips_unique.txt"
interval = 2

tools = {
    "1": "dig",
    "2": "host",
    "3": "nslookup",
    "4": "drill"
}

print("Choose the tools you want to use (enter numbers separated by commas):")
print("1. dig")
print("2. host")
print("3. nslookup")
print("4. drill")

tool_choices = input("Enter your choices (e.g. 1,3,4): ").split(',')

selected_tools = [tools[choice.strip()] for choice in tool_choices if choice.strip() in tools]

if not selected_tools:
    print("[!] No valid tools selected. Exiting...")
    exit()

print(f"[*] Starting IP collection for domain: {domain}")
print(f"[*] Using DNS server: {dns_server}")
print(f"[*] Using tools: {', '.join(selected_tools)}")
print(f"[*] Raw output will be saved to: {raw_file}")
print(f"[*] Unique IP list will be saved to: {unique_file}")
print("[*] Press Ctrl+C to stop.")

seen_ips = set()

def extract_ips(output):
    ips = []
    for line in output.splitlines():
        ip = re.match(r'(\d{1,3}\.){3}\d{1,3}', line.strip())
        if ip:
            ips.append(ip.group(0))
    return ips

def handle_drill_output(output):
    ips = []
    lines = output.splitlines()
    for line in lines:
        if dns_server in line:
            continue
        match = re.search(r'(\d{1,3}\.){3}\d{1,3}', line.strip())
        if match:
            ips.append(match.group(0))
    return ips

def handle_host_nslookup_output(output):
    ips = []
    lines = output.splitlines()
    for line in lines:
        if dns_server in line:
            continue
        match = re.search(r'(\d{1,3}\.){3}\d{1,3}', line.strip())
        if match:
            ips.append(match.group(0))
    return ips

def run_tool(tool):
    global seen_ips
    while True:
        print(f"[+] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Running {tool} for {domain}")

        if tool == "dig":
            result = subprocess.run(
                ["dig", f"@{dns_server}", "+short", domain],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        elif tool == "host":
            result = subprocess.run(
                ["host", domain, dns_server],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        elif tool == "nslookup":
            result = subprocess.run(
                ["nslookup", domain, dns_server],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        elif tool == "drill":
            result = subprocess.run(
                ["drill", f"@{dns_server}", domain],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            ips = handle_drill_output(result.stdout)
        
        if tool != "drill":
            ips = handle_host_nslookup_output(result.stdout)

        with open(raw_file, "a") as rf:
            for ip in ips:
                rf.write(ip + "\n")
                seen_ips.add(ip)

        with open(unique_file, "w") as uf:
            for ip in sorted(seen_ips):
                uf.write(ip + "\n")

        print(f"[*] Unique IPs collected so far: {len(seen_ips)}")
        time.sleep(interval)

try:
    threads = []
    for tool in selected_tools:
        thread = threading.Thread(target=run_tool, args=(tool,))
        thread.daemon = True
        thread.start()
        threads.append(thread)

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[!] Interrupted by user. Exiting...")
    print(f"[✓] Final unique IPs saved to {unique_file}")
