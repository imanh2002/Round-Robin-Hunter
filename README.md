# 🏹 Round Robin Hunter

**Round Robin Hunter** is a Python-based DNS reconnaissance tool that continuously
hunts for IP addresses returned by DNS round-robin configurations using multiple
DNS utilities — all running in parallel 🧵⚡

---

## 🚀 Features

✅ Supports multiple DNS tools  
✅ Parallel execution with threading  
✅ Continuous DNS querying  
✅ Real-time IP extraction  
✅ Automatic deduplication  
✅ Clean CLI interface  
✅ Graceful shutdown with `Ctrl + C`

---

## 🧠 How It Works

1. Provide:
   - A **target domain**
   - A **DNS server** (e.g. `8.8.8.8`)
2. Choose one or more DNS tools:
   - `dig`
   - `host`
   - `nslookup`
   - `drill`
3. Round Robin Hunter will:
   - Repeatedly query DNS records
   - Extract IPv4 addresses
   - Save results into two files:
     - `ips_raw.txt` (all results)
     - `ips_unique.txt` (deduplicated list)

Each selected tool runs in its **own thread**, maximizing IP discovery coverage 🎯

---

## 🛠️ Requirements

### 🐍 Software
- Python **3.7+**
- Linux / macOS  
  (Windows supported if DNS tools are installed and available in PATH)

### 🔧 DNS Tools
At least **one** of the following must be installed:

- `dig`
- `host`
- `nslookup`
- `drill`

#### Debian / Ubuntu
```bash
sudo apt install dnsutils ldnsutils
