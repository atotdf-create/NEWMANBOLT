#!/usr/bin/env node

const axios = require('axios');
const readline = require('readline');
const dns = require('dns').promises;
const net = require('net');
const { execSync } = require('child_process');
const os = require('os');

const VERSION = "7.0.0 (Hybrid Ultra)";
const AUTHOR = "Imin & Eden lite & TDF";

const BANNER = `
    __   _  _____  _      _  ___  ___  ___  ___  _     _____ 
   |  \\ | ||  ___|| |    | ||   ||   ||   ||   || |   |_   _|
   |   \\| ||  ___|| | /\\ | ||   ||   ||   ||   || |     | |  
   | |\\   || |___ | |/  \\| ||   ||   ||   ||   || |___  | |  
   |_| \\__||_____||___/\\___||___||___||___||___||_____| |_|  
                                                              
           AUTHOR: ${AUTHOR}  ● HYBRID ULTRA v${VERSION}
           🔥 Powered by VPN-KING Engine 🔥
`;

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

// --- Colors ---
const colors = {
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    cyan: '\x1b[36m',
    reset: '\x1b[0m',
    bold: '\x1b[1m'
};

// --- Modules ---

async function scanPort(host, port) {
    return new Promise((resolve) => {
        const socket = new net.Socket();
        socket.setTimeout(1000);
        socket.on('connect', () => { socket.destroy(); resolve(port); });
        socket.on('timeout', () => { socket.destroy(); resolve(null); });
        socket.on('error', () => { socket.destroy(); resolve(null); });
        socket.connect(port, host);
    });
}

async function getNetworkInfo() {
    console.log(`\n${colors.cyan}[*] Gathering Network Intelligence...${colors.reset}`);
    const interfaces = os.networkInterfaces();
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                console.log(`${colors.green}[+] Interface: ${name} | IP: ${iface.address}${colors.reset}`);
            }
        }
    }
}

async function discoverSubdomains(target) {
    console.log(`\n${colors.yellow}[*] Bruteforcing Subdomains (VPN-KING Style)...${colors.reset}`);
    const subs = ['www', 'mail', 'ftp', 'dev', 'api', 'admin', 'test', 'vpn', 'proxy', 'secure', 'portal'];
    const found = [];
    for (const s of subs) {
        try {
            const addr = await dns.lookup(`${s}.${target}`);
            console.log(`${colors.green}[+] Found: ${s}.${target} (${addr.address})${colors.reset}`);
            found.push(`${s}.${target}`);
        } catch (e) {}
    }
    return found;
}

async function scanVulns(target) {
    console.log(`\n${colors.red}[*] Auditing Vulnerabilities...${colors.reset}`);
    const paths = ['/.env', '/.git/config', '/phpinfo.php', '/wp-json/wp/v2/users', '/backup.sql', '/.htaccess'];
    for (const p of paths) {
        try {
            const res = await axios.get(`http://${target}${p}`, { timeout: 3000 });
            if (res.status === 200) {
                console.log(`${colors.red}[!] CRITICAL: Exposed ${p} found on ${target}${colors.reset}`);
            }
        } catch (e) {}
    }
}

// --- Termux Specific ---
function termuxVibrate() {
    try { execSync('termux-vibrate -d 200'); } catch (e) {}
}

function termuxNotify(msg) {
    try { execSync(`termux-notification -t "Newmanbolt Alert" -c "${msg}"`); } catch (e) {}
}

// --- Core ---

async function runHybridScan(target) {
    termuxVibrate();
    console.log(`\n${colors.bold}${colors.red}🔥 INITIATING HYBRID ULTRA SCAN: ${target}${colors.reset}`);
    
    await getNetworkInfo();
    
    try {
        const addr = await dns.lookup(target);
        console.log(`\n${colors.cyan}[DNS] Main IP: ${addr.address}${colors.reset}`);
        
        await discoverSubdomains(target);
        
        console.log(`\n${colors.yellow}[PORTS] Scanning...${colors.reset}`);
        const common = [21, 22, 80, 443, 3306, 8080, 10000];
        for (const p of common) {
            if (await scanPort(addr.address, p)) {
                console.log(`${colors.green}[+] Port ${p} is OPEN${colors.reset}`);
            }
        }
        
        await scanVulns(target);

        termuxNotify(`Scan complete for ${target}`);
    } catch (err) {
        console.log(`${colors.red}[ERROR] ${err.message}${colors.reset}`);
    }
    
    await question(`\n${colors.cyan}Press Enter to return to Command Center...${colors.reset}`);
    mainMenu();
}

function mainMenu() {
    console.clear();
    console.log(`${colors.red}${BANNER}${colors.reset}`);
    console.log(`${colors.bold}${colors.cyan}[1] 🔥 Hybrid Ultra Scan (All-in-One)${colors.reset}`);
    console.log(`${colors.cyan}[2] 📡 Network Intelligence Gathering${colors.reset}`);
    console.log(`${colors.cyan}[3] 🔍 VPN-KING Subdomain Recon${colors.reset}`);
    console.log(`${colors.cyan}[4] 🛡️ Vulnerability Audit${colors.reset}`);
    console.log(`${colors.red}[0] 🚪 Exit${colors.reset}`);
    
    rl.question(`\n${colors.yellow}Select Command: ${colors.reset}`, async (choice) => {
        if (choice === '0') process.exit(0);
        const target = await question(`${colors.green}Enter Target (e.g., google.com): ${colors.reset}`);
        if (choice === '1') await runHybridScan(target);
        else if (choice === '2') { await getNetworkInfo(); await question("\nDone. Press Enter..."); mainMenu(); }
        else if (choice === '3') { await discoverSubdomains(target); await question("\nDone. Press Enter..."); mainMenu(); }
        else if (choice === '4') { await scanVulns(target); await question("\nDone. Press Enter..."); mainMenu(); }
        else mainMenu();
    });
}

mainMenu();
