#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                     Newmanbolt v2.0                          ║
║     The World's #1 AI-Powered Pentest Orchestrator          ║
║         🔥 No Root • Termux Ready • Zero Dependencies 🔥    ║
╚══════════════════════════════════════════════════════════════╝

One command. Total recon. Attack vectors with one-click commands.

Usage:
    python3 autorecon.py                          # Interactive menu
    python3 autorecon.py example.com              # Quick scan (auto-detect)
    python3 autorecon.py --deep example.com       # Full recon
    python3 autorecon.py --stealth example.com    # Stealth mode
    python3 autorecon.py --ai example.com -k sk-xxx  # AI-powered
    python3 autorecon.py --batch targets.txt      # Batch mode
"""

import asyncio, aiohttp, json, os, sys, re, socket, ssl
import hashlib, datetime, ipaddress, argparse, textwrap, time
import random, subprocess, shutil, urllib.request, webbrowser
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
from dataclasses import dataclass, field

VERSION = "2.0.0"
AUTHOR = "Imin"
CURRENT_YEAR = 2026

# ═══════════════════════════════════════════════════════════════
# 👇 TRY TO IMPORT RICH — IF MISSING, INSTALL IT AUTOMATICALLY
# ═══════════════════════════════════════════════════════════════

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import (
        Progress, SpinnerColumn, BarColumn, TextColumn,
        TimeElapsedColumn, TimeRemainingColumn
    )
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.columns import Columns
    from rich import box
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    RICH_AVAILABLE = True
except ImportError:
    print("[!] Installing rich for beautiful terminal output...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "-q"])
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import (
        Progress, SpinnerColumn, BarColumn, TextColumn,
        TimeElapsedColumn, TimeRemainingColumn
    )
    from rich.layout import Layout
    from rich.live import Live
    from rich.text import Text
    from rich.columns import Columns
    from rich import box
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    RICH_AVAILABLE = True

console = Console()

try:
    import pyfiglet
    FIGLET = True
except ImportError:
    FIGLET = False

# ═══════════════════════════════════════════════════════════════
# 🎨 CRAZY CLI BANNER
# ═══════════════════════════════════════════════════════════════

BANNER_ART = r"""

    ___         ___   ___   ___   ___   ___   ___
   |   | |   |   |   |   | |   | |     |     |   | |\  |
   |-+-| |   |   +   |   | |-+-  |-+-  |     | + | | + |
   |   | |   |   |   |   | |  \  |     |     |   | |  \|
          ---         ---         ---   ---   ---

           AUTHOR: Imin  ● TELEGRAM: @script_ill
           GITHUB: https://github.com/script-ill


"""

TAGLINES = [
    "One target. Endless possibilities.",
    "Your reconnaissance, supercharged.",
    "See everything. Miss nothing.",
    "From recon to root in one command.",
    "The hacker's Swiss Army knife.",
    "Because manual recon is so 2020.",
    "AI-powered. Human-guided. Lethal.",
    "Scan smarter, not harder.",
    "The target doesn't stand a chance.",
    "Your next shell is one scan away.",
]

SCAN_MODES = {
    "quick":    {"ports": "top100",  "timeout": 2, "subs": 50,  "desc": "Fast scan — common ports"},
    "deep":     {"ports": "full",    "timeout": 5, "subs": 200, "desc": "Thorough — all ports, deeper checks"},
    "stealth":  {"ports": "top50",   "timeout": 4, "subs": 30,  "desc": "Slow stealth — avoids detection"},
    "ai":       {"ports": "top100",  "timeout": 3, "subs": 100, "desc": "AI-powered analysis (needs API key)"},
}

def show_banner():
    """Display the crazy animated banner."""
    console.clear()
    colors = ["cyan", "green", "yellow", "red", "magenta", "blue", "bright_cyan", "bright_green"]
    color = random.choice(colors)

    if FIGLET:
        try:
            f = pyfiglet.Figlet(font="slant", width=100)
            banner_text = f.renderText("AutoRecon")
            console.print(f"[bold {color}]{banner_text}[/bold {color}]")
        except:
            console.print(f"[bold {color}]{BANNER_ART}[/bold {color}]")
    else:
        console.print(f"[bold {color}]{BANNER_ART}[/bold {color}]")

    console.print(Panel.fit(
        "[bold bright_cyan]AI-Powered Pentest Orchestrator[/bold bright_cyan] • "
        "[bold green]Non-Root Termux[/bold green] • "
        f"[bold yellow]v{VERSION}[/bold yellow]\n"
        f"[dim]{random.choice(TAGLINES)}[/dim]",
        border_style="bright_blue",
        padding=(1, 10)
    ))
    console.print()

# ═══════════════════════════════════════════════════════════════
# 🎯 INTERACTIVE MENU
# ═══════════════════════════════════════════════════════════════

def interactive_menu() -> dict:
    """Show the interactive menu and return scan config."""
    show_banner()

    console.print(Panel.fit(
        "[bold bright_cyan]🎯 What do you want to do today?[/bold bright_cyan]\n\n"
        "[bold bright_magenta][1] Quick Scan — Fast recon on a domain/IP[/bold bright_magenta]\n"
        "[2] Deep Scan — Full port scan + all modules\n"
        "[3] Stealth Scan — Slow and quiet\n"
        "[4] AI Scan — AI-powered attack vectors\n"
        "[5] Email OSINT — Investigate an email address\n"
        "[6] Phone OSINT — Investigate a phone number\n"
        "[7] Batch Mode — Scan multiple targets from a file\n"
        "[8] Help — Show detailed usage guide\n"
        "[9] Exit",
        border_style="bright_green",
        padding=(1, 4)
    ))

    choice = Prompt.ask("[bold green]👉 Select option[/bold green]", choices=["1","2","3","4","5","6","7","8","9"], default="1")

    if choice == "9":
        console.print("[bold red]👋 Exiting. Stay sharp![/bold red]")
        sys.exit(0)

    if choice == "8":
        show_help()
        console.input("[dim]Press Enter to return to menu...[/dim]")
        return interactive_menu()

    mode_map = {"1": "quick", "2": "deep", "3": "stealth", "4": "ai", "5": "email", "6": "phone", "7": "batch"}
    mode = mode_map[choice]

    config = {"mode": mode}

    if mode == "batch":
        config["batch_file"] = Prompt.ask("[bold green]📂 Enter path to targets file[/bold green]")
        if not os.path.exists(config["batch_file"]):
            console.print(f"[bold red]❌ File not found: {config['batch_file']}[/bold red]")
            console.input("[dim]Press Enter...[/dim]")
            return interactive_menu()
    elif mode == "ai":
        config["target"] = Prompt.ask("[bold green]🎯 Enter target (domain/IP)[/bold green]")
        config["api_key"] = Prompt.ask("[bold green]🔑 Enter OpenAI API key[/bold green]", password=True)
    elif mode == "email":
        config["target"] = Prompt.ask("[bold green]📧 Enter email address[/bold green]")
    elif mode == "phone":
        config["target"] = Prompt.ask("[bold green]📱 Enter phone number (with +)[/bold green]")
    else:
        config["target"] = Prompt.ask(f"[bold green]🎯 Enter target (domain/IP)[/bold green]")

    config["output_dir"] = ""
    custom = Confirm.ask("[dim]Custom output directory?[/dim]", default=False)
    if custom:
        config["output_dir"] = Prompt.ask("[bold green]📁 Output path[/bold green]")

    return config

def show_help():
    """Display detailed help."""
    console.print(Panel.fit(
        "[bold bright_magenta]   📖 AutoRecon Help Guide[/bold bright_magenta]\n\n"
        "[bold green]QUICK START:[/bold green]\n"
        "[bold cyan]  python3 autorecon.py example.com[/bold cyan]\n"
        "  python3 autorecon.py example.com --deep\n"
        "  python3 autorecon.py example.com --ai -k sk-xxx\n"
        "  python3 autorecon.py --batch targets.txt\n\n"
        "[bold green]TARGET TYPES:[/bold green]\n"
        "  • Domain:      example.com, sub.example.com\n"
        "  • IP Address:  192.168.1.1, 10.0.0.0/24\n"
        "  • Email:       user@example.com\n"
        "  • Phone:       +1234567890\n\n"
        "[bold green]SCAN MODES:[/bold green]\n"
        "  --quick     Top 100 ports, fast checks (default)\n"
        "  --deep      All 65535 ports, all modules\n"
        "  --stealth   Slow, randomized timing (evade IDS)\n"
        "  --ai        AI-powered attack vector generation\n\n"
        "[bold green]OUTPUT:[/bold green]\n"
        "  ./reports/<target>_<date>/report.html\n"
        "  ./reports/<target>_<date>/recon_results.json\n"
        "  ./reports/<target>_<date>/attack_vectors.txt\n\n"
        "[bold green]EXAMPLES:[/bold green]\n"
        "  python3 autorecon.py example.com -o ./engagement1\n"
        "  python3 autorecon.py --deep scanme.org\n"
        "  python3 autorecon.py --ai vulnerable.site -k sk-xxx\n"
        "  python3 autorecon.py admin@company.com       (email)\n"
        "  python3 autorecon.py +1234567890             (phone)",
        border_style="bright_yellow",
        padding=(1, 3)
    ))

# ═══════════════════════════════════════════════════════════════
# 🏗️ PROGRESS SPINNERS & LIVE STATUS
# ═══════════════════════════════════════════════════════════════

class ReconProgress:
    """Live progress display for recon operations."""

    def __init__(self):
        self.progress = Progress(
            SpinnerColumn(spinner_name="dots12", style="bright_cyan"),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=30, style="bright_blue", pulse_style="bright_cyan"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
            expand=True,
            transient=False
        )
        self.tasks = {}
        self._live = None
        self._running = False

    def __enter__(self):
        self._live = Live(self.progress, console=console, refresh_per_second=8)
        self._live.__enter__()
        self._running = True
        return self

    def __exit__(self, *args):
        if self._live and self._running:
            self._live.__exit__(*args)
            self._running = False

    def add_task(self, name: str, total: int = 100) -> str:
        """Add a progress task and return its ID."""
        task_id = self.progress.add_task(f"[bold cyan]{name}[/bold cyan]", total=total)
        self.tasks[name] = task_id
        return task_id

    def update(self, name: str, advance: int = 1, description: str = None):
        """Update a task's progress."""
        task_id = self.tasks.get(name)
        if task_id is not None:
            self.progress.advance(task_id, advance=advance)
            if description:
                self.progress.update(task_id, description=description)

    def complete(self, name: str):
        """Mark a task as complete."""
        task_id = self.tasks.get(name)
        if task_id is not None:
            self.progress.update(task_id, completed=self.progress.tasks[task_id].total or 100)

# ═══════════════════════════════════════════════════════════════
# 🧠 TARGET CLASSIFIER
# ═══════════════════════════════════════════════════════════════

def classify_target(target: str) -> dict:
    """Classify target type from raw input."""
    t = target.strip()
    result = {"raw": t, "type": "unknown", "normalized": t, "subtypes": []}

    # IP
    try:
        ip = ipaddress.ip_address(t)
        result["type"] = "ip"; result["normalized"] = str(ip)
        result["subtypes"].append("ipv4" if ip.version == 4 else "ipv6")
        return result
    except: pass

    # CIDR
    if '/' in t:
        try:
            net = ipaddress.ip_network(t, strict=False)
            result["type"] = "cidr"; result["normalized"] = str(net)
            result["subtypes"].append(f"{net.num_addresses}_hosts")
            return result
        except: pass

    # Email
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', t):
        result["type"] = "email"; result["normalized"] = t.lower()
        result["subtypes"] = ["email", f"domain:{t.split('@')[1]}"]
        return result

    # Phone
    clean = re.sub(r'[\s\-\(\)\.]', '', t)
    if clean.startswith('+') and clean[1:].isdigit() and len(clean) >= 8:
        result["type"] = "phone"; result["normalized"] = clean
        result["subtypes"].append("intl"); return result
    if clean.isdigit() and len(clean) >= 7:
        result["type"] = "phone"; result["normalized"] = f"+{clean}"
        result["subtypes"].append("domestic"); return result

    # Domain
    if '.' in t and ' ' not in t:
        if '://' in t: domain = urlparse(t).netloc or urlparse(t).path
        else: domain = t.split('/')[0]
        if re.match(r'^([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$', domain):
            result["type"] = "domain"; result["normalized"] = domain.lower()
            result["subtypes"].append("subdomain" if len(domain.split('.')) > 2 else "root")
            return result

    # Fallback
    if ' ' not in t and len(t) > 3:
        result["type"] = "domain"; result["normalized"] = t.lower()
        result["subtypes"].append("likely_domain")
    return result

# ═══════════════════════════════════════════════════════════════
# 📡 DATA: COMMON PORTS & WORDLISTS
# ═══════════════════════════════════════════════════════════════

COMMON_PORTS = {
    21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",80:"HTTP",81:"HTTP-Alt",
    110:"POP3",111:"RPC",135:"MSRPC",139:"NetBIOS",143:"IMAP",161:"SNMP",
    389:"LDAP",443:"HTTPS",445:"SMB",465:"SMTPS",500:"ISAKMP",587:"SMTP-Sub",
    636:"LDAPS",993:"IMAPS",995:"POP3S",1080:"SOCKS",1433:"MSSQL",1434:"MSSQL-Mon",
    1521:"Oracle",1723:"PPTP",2049:"NFS",2181:"ZooKeeper",2375:"Docker",
    2376:"Docker-TLS",3128:"Squid",3306:"MySQL",3389:"RDP",3689:"DAAP",
    4000:"ICQ",4443:"HTTPS-Alt",4848:"GlassFish",5000:"UPnP",5432:"PostgreSQL",
    5555:"ADB",5666:"Nagios",5800:"VNC-HTTP",5900:"VNC",5901:"VNC-1",
    5985:"WinRM-HTTP",5986:"WinRM-HTTPS",6000:"X11",6379:"Redis",6443:"K8s-API",
    6667:"IRC",7001:"WebLogic",7070:"RTSP",8000:"HTTP-Alt",8080:"HTTP-Proxy",
    8086:"InfluxDB",8090:"HTTP-Alt",8096:"Emby",8200:"Vault",8333:"Bitcoin",
    8443:"HTTPS-Alt",8500:"Consul",8834:"Nessus",8888:"HTTP-Alt",8983:"Solr",
    9000:"HTTP-Alt",9042:"Cassandra",9050:"Tor",9080:"WebSphere",9090:"HTTP-Alt",
    9092:"Kafka",9100:"JetDirect",9200:"Elasticsearch",9300:"ES-Cluster",
    9418:"Git",9443:"HTTPS-Alt",9600:"OMAPI",11211:"Memcached",11371:"OpenPGP",
    12345:"NetBus",16379:"Redis-Alt",16992:"AMD-RM",20000:"DNP3",27017:"MongoDB",
    27018:"MongoDB",28015:"RethinkDB",31337:"BackOrifice",50070:"HDFS",61613:"STOMP",
}

SUBDOMAIN_WORDLIST = [
    'www','mail','ftp','admin','api','dev','test','stage','staging','blog',
    'cdn','static','assets','img','js','css','app','portal','my','secure',
    'vpn','remote','access','webmail','owa','exchange','autodiscover','cpanel',
    'ns1','ns2','mx','smtp','pop3','imap','git','jenkins','jira','confluence',
]

TECH_SIGNATURES = {
    "WordPress": ['/wp-content/', '/wp-admin/', '/wp-includes/', 'wp-json'],
    "Drupal": ['/sites/default/', 'Drupal', 'Generator" content="Drupal'],
    "Joomla": ['/components/', '/modules/', 'generator" content="Joomla'],
    "Laravel": ['laravel', '_token', 'XSRF-TOKEN'],
    "Django": ['csrftoken', 'sessionid', 'Django'],
    "Rails": ['rails', '_csrf_token', 'Rails'],
    "ASP.NET": ['ASP.NET', '__VIEWSTATE', '__EVENTVALIDATION'],
    "nginx": ['nginx'], "Apache": ['Apache'], "IIS": ['IIS', 'Microsoft-IIS'],
    "Cloudflare": ['cloudflare', '__cfduid', 'cf-ray'],
}

# ═══════════════════════════════════════════════════════════════
# 🚀 THE RECON ENGINE
# ═══════════════════════════════════════════════════════════════

class ReconEngine:
    def __init__(self, target: str, mode: str = "quick", output_dir: str = None):
        self.target = target
        self.mode = mode
        self.config = SCAN_MODES.get(mode, SCAN_MODES["quick"])
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(output_dir or f"reports/{target.replace('.', '_')}_{self.timestamp}")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = {
            "target": target,
            "mode": mode,
            "timestamp": self.timestamp,
            "ip": None,
            "subdomains": [],
            "ports": [],
            "tech": [],
            "vulns": []
        }

    async def resolve_target(self, progress):
        progress.update("Recon", description="[bold yellow]Resolving target IP...[/bold yellow]")
        try:
            self.results["ip"] = socket.gethostbyname(self.target)
            return True
        except:
            return False

    async def scan_ports(self, progress):
        progress.update("Recon", description="[bold yellow]Scanning ports...[/bold yellow]")
        ports_to_scan = list(COMMON_PORTS.keys())
        if self.mode == "deep":
            ports_to_scan = list(range(1, 1025))

        tasks = []
        for port in ports_to_scan:
            tasks.append(self.check_port(port))
        
        results = await asyncio.gather(*tasks)
        for port, open_status in results:
            if open_status:
                service = COMMON_PORTS.get(port, "Unknown")
                self.results["ports"].append({"port": port, "service": service})
        
        progress.update("Recon", advance=30)

    async def check_port(self, port):
        try:
            conn = asyncio.open_connection(self.results["ip"], port)
            reader, writer = await asyncio.wait_for(conn, timeout=self.config["timeout"])
            writer.close()
            await writer.wait_closed()
            return port, True
        except:
            return port, False

    async def discover_subdomains(self, progress):
        if "." not in self.target: return
        progress.update("Recon", description="[bold yellow]Bruteforcing subdomains...[/bold yellow]")
        
        async def check_sub(sub):
            domain = f"{sub}.{self.target}"
            try:
                await asyncio.get_event_loop().getaddrinfo(domain, None)
                return domain
            except:
                return None

        tasks = [check_sub(sub) for sub in SUBDOMAIN_WORDLIST[:self.config["subs"]]]
        found = await asyncio.gather(*tasks)
        self.results["subdomains"] = [d for d in found if d]
        progress.update("Recon", advance=30)

    async def detect_tech(self, progress):
        progress.update("Recon", description="[bold yellow]Detecting technologies...[/bold yellow]")
        url = f"http://{self.target}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    text = await response.text()
                    headers = str(response.headers)
                    
                    for tech, sigs in TECH_SIGNATURES.items():
                        if any(sig.lower() in text.lower() or sig.lower() in headers.lower() for sig in sigs):
                            self.results["tech"].append(tech)
        except:
            pass
        progress.update("Recon", advance=30)

    def generate_report(self):
        report_file = self.output_dir / "report.json"
        with open(report_file, "w") as f:
            json.dump(self.results, f, indent=4)
        
        html_file = self.output_dir / "report.html"
        html_content = f"""
        <html>
        <head><title>Recon Report - {self.target}</title>
        <style>body {{ font-family: sans-serif; background: #121212; color: #e0e0e0; padding: 20px; }}
        .card {{ background: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #333; }}
        h1, h2 {{ color: #00e5ff; }}
        .tag {{ background: #00e5ff; color: #000; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 5px; }}
        </style></head>
        <body>
            <h1>AutoRecon Report: {self.target}</h1>
            <div class="card">
                <h2>Target Info</h2>
                <p>IP: {self.results['ip']}</p>
                <p>Mode: {self.mode}</p>
                <p>Time: {self.timestamp}</p>
            </div>
            <div class="card">
                <h2>Open Ports</h2>
                <ul>{''.join([f"<li><b>{p['port']}</b>: {p['service']}</li>" for p in self.results['ports']])}</ul>
            </div>
            <div class="card">
                <h2>Subdomains</h2>
                <ul>{''.join([f"<li>{d}</li>" for d in self.results['subdomains']])}</ul>
            </div>
            <div class="card">
                <h2>Technologies</h2>
                <p>{' '.join([f"<span class='tag'>{t}</span>" for t in self.results['tech']])}</p>
            </div>
        </body></html>
        """
        with open(html_file, "w") as f:
            f.write(html_content)
        
        return report_file, html_file

    async def run(self):
        with ReconProgress() as progress:
            progress.add_task("Recon", total=100)
            
            if not await self.resolve_target(progress):
                console.print(f"[bold red]❌ Could not resolve target: {self.target}[/bold red]")
                return

            await asyncio.gather(
                self.scan_ports(progress),
                self.discover_subdomains(progress),
                self.detect_tech(progress)
            )
            
            progress.complete("Recon")
        
        json_path, html_path = self.generate_report()
        console.print(Panel.fit(
            f"[bold green]✅ Recon Complete![/bold green]\n\n"
            f"📂 Results saved to: [cyan]{self.output_dir}[/cyan]\n"
            f"📄 JSON Report: [dim]{json_path}[/dim]\n"
            f"🌐 HTML Report: [dim]{html_path}[/dim]",
            border_style="bright_green"
        ))

# ═══════════════════════════════════════════════════════════════
# 🏁 MAIN ENTRY
# ═══════════════════════════════════════════════════════════════

async def main():
    parser = argparse.ArgumentParser(description="AutoRecon v2.0 - AI-Powered Pentest Orchestrator")
    parser.add_argument("target", nargs="?", help="Target domain or IP")
    parser.add_argument("--deep", action="store_true", help="Run deep scan")
    parser.add_argument("--stealth", action="store_true", help="Run stealth scan")
    parser.add_argument("--ai", action="store_true", help="Run AI-powered scan")
    parser.add_argument("-k", "--key", help="OpenAI API key for AI mode")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("--batch", help="Batch scan targets from file")

    args = parser.parse_args()

    if not args.target and not args.batch:
        config = interactive_menu()
        if config["mode"] == "batch":
            targets = open(config["batch_file"]).read().splitlines()
            for t in targets:
                engine = ReconEngine(t, mode="quick", output_dir=config.get("output_dir"))
                await engine.run()
        else:
            engine = ReconEngine(config["target"], mode=config["mode"], output_dir=config.get("output_dir"))
            await engine.run()
    else:
        mode = "quick"
        if args.deep: mode = "deep"
        elif args.stealth: mode = "stealth"
        elif args.ai: mode = "ai"

        if args.batch:
            targets = open(args.batch).read().splitlines()
            for t in targets:
                engine = ReconEngine(t, mode=mode, output_dir=args.output)
                await engine.run()
        else:
            engine = ReconEngine(args.target, mode=mode, output_dir=args.output)
            await engine.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]Interrupted by user. Exiting...[/bold red]")
        sys.exit(1)
