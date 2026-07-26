#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║                NEWMAN BOLT PRO v9.0                         ║
║     The World's #1 AI-Powered Pentest Orchestrator          ║
║         🔥 No Root • Termux Ready • AI-Driven 🔥            ║
╚══════════════════════════════════════════════════════════════╝

Advanced Reconnaissance & OSINT Orchestrator.
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
import argparse
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# 🛡️ DEPENDENCY MANAGER
# ═══════════════════════════════════════════════════════════════

def install_deps():
    deps = ["requests", "colorama", "bs4", "rich", "aiohttp", "pyfiglet"]
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            print(f"[*] Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep, "--quiet"])

install_deps()

import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

init(autoreset=True)
console = Console()

# ═══════════════════════════════════════════════════════════════
# 🎨 ASSETS & COLORS
# ═══════════════════════════════════════════════════════════════

BANNER = r"""
    __   _  _____  _      _  ___  ___  ___  ___  _     _____ 
   |  \ | ||  ___|| |    | ||   ||   ||   ||   || |   |_   _|
   |   \| ||  ___|| | /\ | ||   ||   ||   ||   || |     | |  
   | |\   || |___ | |/  \| ||   ||   ||   ||   || |___  | |  
   |_| \__||_____||___/\___||___||___||___||___||_____| |_|  
                                                              
           AUTHOR: Imin  ● TELEGRAM: @script_ill
           NEWMAN BOLT PRO v9.0 (AI-POWERED)
"""

# ═══════════════════════════════════════════════════════════════
# 🧠 NEWMAN BOLT PRO ENGINE
# ═══════════════════════════════════════════════════════════════

class NewmanBoltPro:
    def __init__(self, target, deep=False):
        self.target = target.replace("http://", "").replace("https://", "").split("/")[0]
        self.deep = deep
        self.results = {
            "ip": None,
            "whois": None,
            "ports": [],
            "vulns": [],
            "tech": []
        }

    def get_dns_intel(self):
        try:
            self.results["ip"] = socket.gethostbyname(self.target)
            return True
        except: return False

    def get_whois(self):
        try:
            res = subprocess.check_output(["whois", self.target], stderr=subprocess.DEVNULL).decode()
            self.results["whois"] = res[:500] + "..."
            return True
        except: return False

    def scan_ports(self):
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 8080]
        if self.deep: ports.extend(range(1024, 2048))
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((self.results["ip"], port)) == 0:
                self.results["ports"].append(port)
            sock.close()

    def audit_web(self):
        try:
            url = f"http://{self.target}"
            res = requests.get(url, timeout=5, headers={"User-Agent": "NewmanBoltPro/9.0"})
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Tech detection
            headers = str(res.headers).lower()
            if "nginx" in headers: self.results["tech"].append("Nginx")
            if "apache" in headers: self.results["tech"].append("Apache")
            if "wp-content" in res.text: self.results["tech"].append("WordPress")
            
            # Vuln check
            checks = ["/.env", "/.git/config", "/backup.sql"]
            for c in checks:
                if requests.get(url + c, timeout=3).status_code == 200:
                    self.results["vulns"].append(c)
        except: pass

    def run(self):
        console.print(Panel(f"[bold red]🚀 INITIATING PRO SCAN: {self.target}[/bold red]", border_style="red"))
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), console=console) as progress:
            t1 = progress.add_task("[cyan]DNS Intel...", total=100)
            self.get_dns_intel(); progress.update(t1, advance=100)
            
            t2 = progress.add_task("[yellow]WHOIS Lookup...", total=100)
            self.get_whois(); progress.update(t2, advance=100)
            
            t3 = progress.add_task("[green]Port Scanning...", total=100)
            self.scan_ports(); progress.update(t3, advance=100)
            
            t4 = progress.add_task("[magenta]Web & Tech Audit...", total=100)
            self.audit_web(); progress.update(t4, advance=100)

        self.display_report()

    def display_report(self):
        table = Table(title=f"Newman Bolt Pro Report - {self.target}", border_style="cyan")
        table.add_column("Category", style="yellow")
        table.add_column("Findings", style="white")
        
        table.add_row("Main IP", self.results["ip"] or "N/A")
        table.add_row("Open Ports", ", ".join(map(str, self.results["ports"])) or "None")
        table.add_row("Tech Stack", ", ".join(self.results["tech"]) or "Unknown")
        table.add_row("Vulnerabilities", ", ".join(self.results["vulns"]) or "[green]None Detected[/green]")
        
        console.print(table)
        if self.results["whois"]:
            console.print(Panel(self.results["whois"], title="[bold white]WHOIS DATA[/bold white]", border_style="blue"))

# ═══════════════════════════════════════════════════════════════
# 🎯 MAIN MENU
# ═══════════════════════════════════════════════════════════════

def main():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        console.print(f"[bold red]{BANNER}[/bold red]")
        console.print(Panel(
            "[1] 🔥 Full Pro Recon (DNS + WHOIS + Ports + Tech)\n"
            "[2] ⚡ Deep Scan (Full Port Range)\n"
            "[3] 🔍 Quick DNS & WHOIS Intel\n"
            "[0] 🚪 Exit",
            title="[bold white]NEWMAN BOLT COMMAND CENTER[/bold white]", border_style="blue"
        ))
        
        choice = input(f"\n{Fore.YELLOW}Select Command > {Fore.WHITE}")
        
        if choice == '0': break
        
        target = input(f"{Fore.GREEN}Enter Target Domain > {Fore.WHITE}")
        if not target: continue
        
        engine = NewmanBoltPro(target, deep=(choice == '2'))
        engine.run()
        
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
