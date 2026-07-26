#!/usr/bin/env node

const axios = require('axios');
const readline = require('readline');
const dns = require('dns').promises;
const net = require('net');
const { execSync } = require('child_process');

const VERSION = "5.0.0 (JS Edition)";
const AUTHOR = "Imin";

const BANNER = `
    __   _  _____  _      _  ___  ___  ___  ___  _     _____ 
   |  \\ | ||  ___|| |    | ||   ||   ||   ||   || |   |_   _|
   |   \\| ||  ___|| | /\\ | ||   ||   ||   ||   || |     | |  
   | |\\   || |___ | |/  \\| ||   ||   ||   ||   || |___  | |  
   |_| \\__||_____||___/\\___||___||___||___||___||_____| |_|  
                                                              
           AUTHOR: ${AUTHOR}  ● JS EDITION v${VERSION}
`;

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

const question = (query) => new Promise((resolve) => rl.question(query, resolve));

async function scanPort(host, port) {
    return new Promise((resolve) => {
        const socket = new net.Socket();
        socket.setTimeout(2000);
        socket.on('connect', () => {
            socket.destroy();
            resolve(port);
        });
        socket.on('timeout', () => {
            socket.destroy();
            resolve(null);
        });
        socket.on('error', () => {
            socket.destroy();
            resolve(null);
        });
        socket.connect(port, host);
    });
}

async function runRecon(target) {
    console.log(`\n[\x1b[33m*\x1b[0m] Starting JS Recon on: \x1b[36m${target}\x1b[0m`);
    
    try {
        const addr = await dns.lookup(target);
        console.log(`[\x1b[32m+\x1b[0m] IP Address: \x1b[32m${addr.address}\x1b[0m`);
        
        console.log(`[\x1b[33m*\x1b[0m] Scanning common ports...`);
        const ports = [21, 22, 23, 25, 53, 80, 443, 3306, 8080];
        const openPorts = [];
        
        for (const port of ports) {
            const p = await scanPort(addr.address, port);
            if (p) openPorts.push(p);
        }
        console.log(`[\x1b[32m+\x1b[0m] Open Ports: \x1b[32m${openPorts.join(', ') || 'None'}\x1b[0m`);

        console.log(`[\x1b[33m*\x1b[0m] Checking for vulnerabilities...`);
        const vulns = ['/.env', '/.git/config', '/phpinfo.php'];
        for (const v of vulns) {
            try {
                const res = await axios.get(`http://${target}${v}`, { timeout: 3000 });
                if (res.status === 200) console.log(`[\x1b[31m!\x1b[0m] Potential Leak: \x1b[31m${v}\x1b[0m`);
            } catch (e) {}
        }
        
    } catch (err) {
        console.log(`[\x1b[31m!\x1b[0m] Error: ${err.message}`);
    }
    
    await question("\nPress Enter to return to menu...");
    mainMenu();
}

function mainMenu() {
    console.clear();
    console.log(`\x1b[31m${BANNER}\x1b[0m`);
    console.log(`\x1b[36m[1] Full JS Recon\x1b[0m`);
    console.log(`\x1b[36m[2] Port Scanner\x1b[0m`);
    console.log(`\x1b[36m[3] Vulnerability Audit\x1b[0m`);
    console.log(`\x1b[31m[0] Exit\x1b[0m`);
    
    rl.question("\nSelect an option: ", async (choice) => {
        if (choice === '0') {
            rl.close();
            process.exit(0);
        }
        const target = await question("Enter Target Domain: ");
        if (choice === '1') await runRecon(target);
        else mainMenu();
    });
}

mainMenu();
