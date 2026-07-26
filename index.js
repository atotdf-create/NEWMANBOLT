#!/usr/bin/env node

const axios = require('axios');
const readline = require('readline');
const dns = require('dns').promises;
const net = require('net');
const { execSync } = require('child_process');

const VERSION = "6.0.0 (JS Pro)";
const AUTHOR = "Imin";

const BANNER = `
    __   _  _____  _      _  ___  ___  ___  ___  _     _____ 
   |  \\ | ||  ___|| |    | ||   ||   ||   ||   || |   |_   _|
   |   \\| ||  ___|| | /\\ | ||   ||   ||   ||   || |     | |  
   | |\\   || |___ | |/  \\| ||   ||   ||   ||   || |___  | |  
   |_| \\__||_____||___/\\___||___||___||___||___||_____| |_|  
                                                              
           AUTHOR: ${AUTHOR}  ● JS PRO v${VERSION}
`;

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

// --- Modules ---

async function scanPort(host, port) {
    return new Promise((resolve) => {
        const socket = new net.Socket();
        socket.setTimeout(1500);
        socket.on('connect', () => { socket.destroy(); resolve(port); });
        socket.on('timeout', () => { socket.destroy(); resolve(null); });
        socket.on('error', () => { socket.destroy(); resolve(null); });
        socket.connect(port, host);
    });
}

async function getTech(target) {
    try {
        const res = await axios.get(`http://${target}`, { timeout: 5000 });
        const headers = JSON.stringify(res.headers).toLowerCase();
        const body = res.data.toLowerCase();
        const techs = [];
        if (headers.includes('nginx')) techs.push('Nginx');
        if (headers.includes('apache')) techs.push('Apache');
        if (body.includes('wp-content')) techs.push('WordPress');
        if (body.includes('jquery')) techs.push('jQuery');
        return techs;
    } catch (e) { return []; }
}

async function discoverSubdomains(target) {
    const subs = ['www', 'mail', 'ftp', 'dev', 'api', 'admin', 'test'];
    const found = [];
    for (const s of subs) {
        try {
            await dns.lookup(`${s}.${target}`);
            found.push(`${s}.${target}`);
        } catch (e) {}
    }
    return found;
}

// --- Core ---

async function runFullRecon(target) {
    console.log(`\n\x1b[31m[!] INITIATING PRO RECON: ${target}\x1b[0m`);
    
    try {
        const addr = await dns.lookup(target);
        console.log(`\x1b[36m[DNS]\x1b[0m IP: ${addr.address}`);
        
        const subs = await discoverSubdomains(target);
        console.log(`\x1b[36m[SUBS]\x1b[0m Found: ${subs.join(', ') || 'None'}`);
        
        const ports = [21, 22, 80, 443, 3306, 8080];
        const open = [];
        for (const p of ports) {
            if (await scanPort(addr.address, p)) open.push(p);
        }
        console.log(`\x1b[36m[PORTS]\x1b[0m Open: ${open.join(', ') || 'None'}`);
        
        const tech = await getTech(target);
        console.log(`\x1b[36m[TECH]\x1b[0m Detected: ${tech.join(', ') || 'Unknown'}`);

    } catch (err) {
        console.log(`\x1b[31m[ERROR]\x1b[0m ${err.message}`);
    }
    
    await question("\nPress Enter to return...");
    mainMenu();
}

function mainMenu() {
    console.clear();
    console.log(`\x1b[31m${BANNER}\x1b[0m`);
    console.log(`\x1b[33m[1] Full Pro Recon\x1b[0m`);
    console.log(`\x1b[33m[2] Subdomain Discovery\x1b[0m`);
    console.log(`\x1b[33m[3] Technology Detection\x1b[0m`);
    console.log(`\x1b[31m[0] Exit\x1b[0m`);
    
    rl.question("\nSelect: ", async (choice) => {
        if (choice === '0') process.exit(0);
        const target = await question("Target Domain: ");
        if (choice === '1') await runFullRecon(target);
        else mainMenu();
    });
}

mainMenu();
