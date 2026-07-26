#!/bin/bash

# Newmanbolt v5.0 JS - Automated Installer for Termux
# Created by Manus for Imin

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}          NEWMANBOLT v5.0 JS INSTALLER             ${NC}"
echo -e "${CYAN}====================================================${NC}"

echo -e "${YELLOW}[*] Updating system packages...${NC}"
pkg update -y && pkg upgrade -y

echo -e "${YELLOW}[*] Installing Node.js and Git...${NC}"
pkg install nodejs git wget -y

echo -e "${YELLOW}[*] Cloning Newmanbolt repository...${NC}"
cd $HOME
if [ -d "Newmanbolt" ]; then
    rm -rf Newmanbolt
fi
git clone https://github.com/atotdf-create/NEWMANBOLT.git

echo -e "${YELLOW}[*] Installing dependencies...${NC}"
cd $HOME/Newmanbolt
npm install

echo -e "${YELLOW}[*] Setting up global command...${NC}"
if [ -n "$PREFIX" ]; then
    ln -sf $HOME/Newmanbolt/index.js $PREFIX/bin/newmanbolt
    chmod +x $HOME/Newmanbolt/index.js
    echo -e "${GREEN}[+] Global command 'newmanbolt' created!${NC}"
fi

echo -e "${GREEN}[+] Installation complete!${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"
echo -e "${YELLOW}Launching Newmanbolt JS Edition...${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"

node index.js
