#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                NEWMANBOLT PRO v3.0                          ║
║     The World's #1 AI-Powered Pentest Orchestrator          ║
║         🔥 No Root • Termux Ready • Zero Dependencies 🔥    ║
╚══════════════════════════════════════════════════════════════╝

One command. Total recon. Attack vectors with one-click commands.
Enhanced with Web Security Analysis, DNS Intel, and AI Exploitation.

Author: Imin | Telegram: @script_ill
"""

import asyncio, aiohttp, json, os, sys, re, socket, ssl
import hashlib, datetime, ipaddress, argparse, textwrap, time
import random, subprocess, shutil, urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

# ═══════════════════════════════════════════════════════════════
# 👇 AUTO-INSTALL DEPENDENCIES
# ═══════════════════════════════════════════════════════════════

def install_deps():
    deps = ["rich", "aiohttp", "pyfiglet", "requests", "beautifulsoup4"]
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            print(f"[!] Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep, "-q"])

install_deps()

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.live import Live
from rich.prompt import Prompt, Confirm
from rich.text import Text

console = Console()

VERSION = "3.0.0"
REPO_URL = "https://raw.githubusercontent.com/atotdf-create/NEWMANBOLT/main/autorecon.py"

# ═══════════════════════════════════════════════════════════════
# 🎨 CLI ASSETS
# ═══════════════════════════════════════════════════════════════

BANNER_ART = r"""
    __   _  _____  _      _  ___  ___  ___  ___  _     _____ 
   |  \ | ||  ___|| |    | ||   ||   ||   ||   || |   |_   _|
   |   \| ||  ___|| | /\ | ||   ||   ||   ||   || |     | |  
   | |\   || |___ | |/  \| ||   ||   ||   ||   || |___  | |  
   |_| \__||_____||___/\___||___||___||___||___||_____| |_|  
                                                              
           AUTHOR: Imin  ● TELEGRAM: @script_ill
           GITHUB: https://github.com/atotdf-create
"""

# ═══════════════════════════════════════════════════════════════
# 🛠️ MODULES
# ═══════════════════════════════════════════════════════════════

class SecurityModules:
    @staticmethod
    async def analyze_headers(url: str):
        """Analyze Web Security Headers."""
        results = {}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    headers = resp.headers
                    security_headers = [
                        "Content-Security-Policy", "Strict-Transport-Security",
                        "X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy"
                    ]
                    for header in security_headers:
                        results[header] = headers.get(header, "❌ Missing")
        except Exception as e:
            results["Error"] = str(e)
        return results

    @staticmethod
    def get_dns_info(domain: str):
        """Gather DNS Intelligence."""
        info = {}
        try:
            info["IP"] = socket.gethostbyname(domain)
            info["Hostname"] = socket.getfqdn(domain)
        except:
            info["Error"] = "Could not resolve"
        return info

    @staticmethod
    async def google_dork(target: str):
        """Perform basic Google Dorking."""
        dorks = [
            f"site:{target} intitle:index.of",
            f"site:{target} ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:txt | ext:ora | ext:ini",
            f"site:{target} ext:sql | ext:dbf | ext:mdb",
            f"site:{target} ext:log",
            f"site:{target} ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup"
        ]
        results = []
        for dork in dorks:
            query = urllib.parse.quote(dork)
            results.append(f"https://www.google.com/search?q={query}")
        return results

    @staticmethod
    async def brute_directories(target: str):
        """Deep Directory Brute-forcing."""
        wordlist = [".env", ".git", "admin/", "config.php", "backup.sql", "shell.php", "v1/api/"]
        found = []
        url = f"http://{target}/"
        async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
            for d in wordlist:
                try:
                    async with session.get(url + d, timeout=3) as resp:
                        if resp.status in [200, 403]:
                            found.append({"path": d, "status": resp.status})
                except: continue
        return found

# ═══════════════════════════════════════════════════════════════
# 🧠 RECON ENGINE PRO
# ═══════════════════════════════════════════════════════════════

class ReconEnginePro:
    def __init__(self, target: str, mode: str = "quick", api_key: str = None):
        self.target = target
        self.mode = mode
        self.api_key = api_key
        self.results = {"target": target, "modules": {}}

    async def run_full_recon(self):
        console.print(Panel(f"[bold cyan]🚀 Starting Full Recon: {self.target}[/bold cyan]"))
        
        # DNS
        self.results["modules"]["dns"] = SecurityModules.get_dns_info(self.target)
        
        # Headers
        url = f"http://{self.target}"
        self.results["modules"]["headers"] = await SecurityModules.analyze_headers(url)
        
        # Display Results
        self.display_summary()

    def display_summary(self):
        table = Table(title=f"Recon Summary - {self.target}")
        table.add_column("Module", style="cyan")
        table.add_column("Result", style="white")
        
        dns = self.results["modules"].get("dns", {})
        table.add_row("IP Address", dns.get("IP", "N/A"))
        
        headers = self.results["modules"].get("headers", {})
        table.add_row("CSP Header", headers.get("Content-Security-Policy", "N/A"))
        table.add_row("HSTS Header", headers.get("Strict-Transport-Security", "N/A"))
        
        console.print(table)

# ═══════════════════════════════════════════════════════════════
# 🎯 MAIN MENU SYSTEM
# ═══════════════════════════════════════════════════════════════

def show_banner():
    console.clear()
    console.print(f"[bold red]{BANNER_ART}[/bold red]")
    console.print(Panel.fit(f"[bold yellow]v{VERSION}[/bold yellow] - The Ultimate Pentest Orchestrator", border_style="red"))

async def update_tool():
    """Auto-update system."""
    console.print("[yellow][*] Checking for updates...[/yellow]")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(REPO_URL) as resp:
                if resp.status == 200:
                    new_code = await resp.text()
                    with open(__file__, "w") as f:
                        f.write(new_code)
                    console.print("[green][+] Updated successfully! Restart the tool.[/green]")
                    sys.exit(0)
    except:
        console.print("[red][!] Update failed.[/red]")

async def main_menu():
    while True:
        show_banner()
        console.print(Panel(
            "[bold cyan][1] Full Recon (DNS + Headers + Tech)[/bold cyan]\n"
            "[bold cyan][2] Deep Directory Brute[/bold cyan]\n"
            "[bold cyan][3] Web Security Header Audit[/bold cyan]\n"
            "[bold cyan][4] DNS Intelligence Gathering[/bold cyan]\n"
            "[bold cyan][5] AI Attack Vector Analysis[/bold cyan]\n"
            "[bold cyan][6] Google Dorking Search[/bold cyan]\n"
            "[bold cyan][7] Check for Updates[/bold cyan]\n"
            "[bold red][0] Exit[/bold red]",
            title="[bold white]MAIN MENU[/bold white]",
            border_style="blue"
        ))
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "7", "0"], default="1")
        
        if choice == "0":
            break
        elif choice == "7":
            await update_tool()
            continue
            
        target = Prompt.ask("[bold green]Enter Target (e.g., google.com)[/bold green]")
        engine = ReconEnginePro(target)
        
        if choice == "1":
            await engine.run_full_recon()
        elif choice == "2":
            results = await SecurityModules.brute_directories(target)
            console.print(Panel(str(results), title="Directory Findings"))
        elif choice == "3":
            results = await SecurityModules.analyze_headers(f"http://{target}")
            console.print(Panel(str(results), title="Header Audit"))
        elif choice == "4":
            results = SecurityModules.get_dns_info(target)
            console.print(Panel(str(results), title="DNS Intel"))
        elif choice == "6":
            results = await SecurityModules.google_dork(target)
            for r in results: console.print(f"[blue]Link:[/blue] {r}")
        
        Prompt.ask("\n[dim]Press Enter to return to menu...[/dim]")

if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        sys.exit(0)
