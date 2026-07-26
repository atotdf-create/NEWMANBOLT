#!/bin/bash

# Newmanbolt v7.0 Hybrid - Automated Installer for Termux
# Created by Manus for Imin (Integrating SIRMA-SCAN-TOOL Features)

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}          NEWMANBOLT v7.0 HYBRID ULTRA             ${NC}"
echo -e "${CYAN}====================================================${NC}"

echo -e "${YELLOW}[*] Updating system packages...${NC}"
pkg update -y && pkg upgrade -y

echo -e "${YELLOW}[*] Installing Core Dependencies (Node.js, Git, Wget)...${NC}"
pkg install nodejs git wget -y

echo -e "${YELLOW}[*] Installing Termux-specific tools (API & Wake-Lock)...${NC}"
pkg install termux-api -y
termux-wake-lock

echo -e "${YELLOW}[*] Cloning Newmanbolt Hybrid repository...${NC}"
cd $HOME
if [ -d "Newmanbolt" ]; then
    rm -rf Newmanbolt
fi
git clone https://github.com/atotdf-create/NEWMANBOLT.git

echo -e "${YELLOW}[*] Installing Node dependencies...${NC}"
cd $HOME/Newmanbolt
npm install axios

echo -e "${YELLOW}[*] Setting up global command 'newmanbolt'...${NC}"
if [ -n "$PREFIX" ]; then
    ln -sf $HOME/Newmanbolt/index.js $PREFIX/bin/newmanbolt
    chmod +x $HOME/Newmanbolt/index.js
    echo -e "${GREEN}[+] Global command created!${NC}"
fi

echo -e "${GREEN}[+] Hybrid Ultra Installation complete!${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"
echo -e "${YELLOW}Launching Newmanbolt Hybrid Ultra...${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"

node index.js
