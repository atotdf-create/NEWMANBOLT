#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                NEWMANBOLT FINAL v8.0                        ║
║     The Ultimate Error-Free Pentest Orchestrator            ║
║         🔥 No Root • Termux Ready • Self-Healing 🔥         ║
╚══════════════════════════════════════════════════════════════╝

The most stable, powerful, and error-free version ever created.
Author: Imin | Telegram: @script_ill
"""

import sys
import os
import socket
import threading
import time
import json
import subprocess
import re
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# 🛡️ SELF-HEALING DEPENDENCY MANAGER
# ═══════════════════════════════════════════════════════════════

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"[*] Installing {package} for you...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])

# Core dependencies
deps = ["requests", "colorama", "bs4"]
for dep in deps:
    install_and_import(dep)

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)

# ═══════════════════════════════════════════════════════════════
# 🎨 ASSETS & COLORS
# ═══════════════════════════════════════════════════════════════

C = Fore.CYAN
G = Fore.GREEN
Y = Fore.YELLOW
R = Fore.RED
W = Fore.WHITE
B = Style.BRIGHT

BANNER = f"""{R}{B}
    __   _  _____  _      _  ___  ___  ___  ___  _     _____ 
   |  \\ | ||  ___|| |    | ||   ||   ||   ||   || |   |_   _|
   |   \\| ||  ___|| | /\\ | ||   ||   ||   ||   || |     | |  
   | |\\   || |___ | |/  \\| ||   ||   ||   ||   || |___  | |  
   |_| \\__||_____||___/\\___||___||___||___||___||_____| |_|  
                                                              
           {W}AUTHOR: Imin  ● {G}FINAL v8.0 {Y}(ERROR-FREE)
"""

# ═══════════════════════════════════════════════════════════════
# 🧠 CORE ENGINE (ERROR-FREE)
# ═══════════════════════════════════════════════════════════════

class NewmanboltEngine:
    def __init__(self, target):
        self.target = target.replace("http://", "").replace("https://", "").split("/")[0]
        self.results = []

    def log(self, msg, type="info"):
        prefix = f"{G}[+]" if type == "ok" else f"{Y}[*]" if type == "info" else f"{R}[!]"
        print(f"{prefix} {msg}")

    def get_ip(self):
        try:
            ip = socket.gethostbyname(self.target)
            self.log(f"Resolved IP: {W}{ip}", "ok")
            return ip
        except Exception as e:
            self.log(f"DNS Resolution Failed: {str(e)}", "err")
            return None

    def scan_ports(self, ip):
        self.log(f"Scanning common ports on {ip}...")
        ports = [21, 22, 80, 443, 3306, 8080]
        open_ports = []
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        
        if open_ports:
            self.log(f"Open Ports: {G}{', '.join(map(str, open_ports))}", "ok")
        else:
            self.log("No common ports found open.", "info")

    def check_vulns(self):
        self.log(f"Auditing {self.target} for vulnerabilities...")
        paths = ["/.env", "/.git/config", "/phpinfo.php", "/backup.sql"]
        for path in paths:
            try:
                url = f"http://{self.target}{path}"
                res = requests.get(url, timeout=5, headers={"User-Agent": "Newmanbolt/8.0"})
                if res.status_code == 200:
                    self.log(f"CRITICAL EXPOSURE: {R}{path}", "err")
            except:
                pass

    def run_full(self):
        print(f"\n{C}{'='*50}\n{B}{W}TARGET: {self.target}\n{C}{'='*50}")
        ip = self.get_ip()
        if ip:
            self.scan_ports(ip)
            self.check_vulns()
        print(f"{C}{'='*50}")
        input(f"\n{Y}Press Enter to return to menu...")

# ═══════════════════════════════════════════════════════════════
# 🎯 MAIN INTERFACE
# ═══════════════════════════════════════════════════════════════

def main_menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print(BANNER)
        print(f"{C}[1] {W}Full Auto-Recon (Guaranteed Working)")
        print(f"{C}[2] {W}DNS & IP Discovery")
        print(f"{C}[3] {W}Vulnerability Audit")
        print(f"{C}[0] {R}Exit")
        
        choice = input(f"\n{Y}Select Option > {W}")
        
        if choice == '0':
            print(f"{G}Stay Sharp. Goodbye!")
            break
            
        if choice in ['1', '2', '3']:
            target = input(f"{G}Enter Target Domain (e.g. google.com) > {W}")
            if not target: continue
            
            engine = NewmanboltEngine(target)
            if choice == '1': engine.run_full()
            elif choice == '2': 
                engine.get_ip()
                input(f"\n{Y}Press Enter...")
            elif choice == '3':
                engine.check_vulns()
                input(f"\n{Y}Press Enter...")
        else:
            print(f"{R}Invalid Choice!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n{R}[!] Fatal Error: {str(e)}")
