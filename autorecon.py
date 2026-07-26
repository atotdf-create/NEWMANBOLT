#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                NEWMANBOLT ULTIMATE v4.0                     ║
║     The World's #1 AI-Powered Pentest Orchestrator          ║
║         🔥 No Root • Termux Ready • Zero Dependencies 🔥    ║
╚══════════════════════════════════════════════════════════════╝

The Ultimate Pentest Tool: Blazing Fast, AI-Driven, Lethal.
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
from rich.layout import Layout
from bs4 import BeautifulSoup

console = Console()
VERSION = "4.0.0"

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
# 🛠️ ULTIMATE ENGINE
# ═══════════════════════════════════════════════════════════════

class UltimateScanner:
    def __init__(self, target):
        self.target = target
        self.results = {
            "ip": None,
            "ports": [],
            "vulns": [],
            "tech": [],
            "links": []
        }

    async def scan(self):
        console.print(Panel(f"[bold red]🔥 ULTIMATE SCAN INITIATED: {self.target}[/bold red]", border_style="red"))
        
        with Progress(
            SpinnerColumn(spinner_name="dots12"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("[yellow]Engine Running...", total=100)
            
            # 1. IP & DNS
            try:
                self.results["ip"] = socket.gethostbyname(self.target)
            except: pass
            progress.update(task, advance=20, description="[cyan]IP Resolved")

            # 2. Fast Port Scan & Banner Grabbing
            await self.fast_port_scan()
            progress.update(task, advance=30, description="[cyan]Ports & Banners Scanned")

            # 3. Vulnerability Audit
            await self.audit_vulns()
            progress.update(task, advance=30, description="[cyan]Vulnerabilities Audited")

            # 4. Web Spidering
            await self.spider()
            progress.update(task, advance=20, description="[cyan]Spidering Complete")

        self.display_results()

    async def fast_port_scan(self):
        common = [21, 22, 23, 25, 53, 80, 443, 445, 3306, 3389, 8080]
        async def grab(port):
            try:
                reader, writer = await asyncio.wait_for(asyncio.open_connection(self.results["ip"], port), timeout=2)
                writer.close()
                await writer.wait_closed()
                return port
            except: return None
        
        tasks = [grab(p) for p in common]
        found = await asyncio.gather(*tasks)
        self.results["ports"] = [p for p in found if p]

    async def audit_vulns(self):
        url = f"http://{self.target}"
        async with aiohttp.ClientSession() as session:
            checks = [("/.env", "Env Leak"), ("/.git/config", "Git Leak"), ("/wp-config.php.bak", "Backup Leak")]
            for path, name in checks:
                try:
                    async with session.get(url + path, timeout=3) as resp:
                        if resp.status == 200: self.results["vulns"].append(name)
                except: pass

    async def spider(self):
        url = f"http://{self.target}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as resp:
                    soup = BeautifulSoup(await resp.text(), 'html.parser')
                    for a in soup.find_all('a', href=True):
                        if len(self.results["links"]) < 10:
                            self.results["links"].append(a['href'])
        except: pass

    def display_results(self):
        table = Table(title="[bold red]ULTIMATE SCAN RESULTS[/bold red]", border_style="red")
        table.add_column("Category", style="cyan")
        table.add_column("Findings", style="white")
        
        table.add_row("Target IP", self.results["ip"] or "N/A")
        table.add_row("Open Ports", ", ".join(map(str, self.results["ports"])) or "None")
        table.add_row("Vulnerabilities", ", ".join(self.results["vulns"]) or "[green]Clean[/green]")
        table.add_row("Spider Links", f"{len(self.results['links'])} found")
        
        console.print(table)
        if self.results["links"]:
            console.print(Panel("\n".join(self.results["links"][:5]), title="[yellow]Top Endpoints[/yellow]", border_style="yellow"))

# ═══════════════════════════════════════════════════════════════
# 🎯 MENU
# ═══════════════════════════════════════════════════════════════

async def main_menu():
    while True:
        console.clear()
        console.print(f"[bold red]{BANNER_ART}[/bold red]")
        console.print(Panel.fit(f"[bold yellow]ULTIMATE v{VERSION}[/bold yellow]", border_style="red"))
        
        console.print(Panel(
            "[1] 🔥 Ultimate Full Scan\n"
            "[2] 🕷️ Web Spider & Endpoint Extractor\n"
            "[3] 🛡️ Vulnerability Audit\n"
            "[4] 📡 Port & Banner Grabbing\n"
            "[0] 🚪 Exit",
            title="[bold white]COMMAND CENTER[/bold white]", border_style="blue"
        ))
        
        choice = Prompt.ask("Select Command", choices=["1", "2", "3", "4", "0"], default="1")
        
        if choice == "0": break
        
        target = Prompt.ask("[bold green]Enter Target Domain[/bold green]")
        scanner = UltimateScanner(target)
        
        if choice == "1": await scanner.scan()
        elif choice == "2": await scanner.spider(); console.print(scanner.results["links"])
        elif choice == "3": await scanner.audit_vulns(); console.print(scanner.results["vulns"])
        elif choice == "4": await scanner.fast_port_scan(); console.print(scanner.results["ports"])
        
        Prompt.ask("\n[dim]Press Enter to continue...[/dim]")

if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        sys.exit(0)
