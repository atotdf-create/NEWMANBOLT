#!/bin/bash

# Newmanbolt v2.0 - Automated Installer for Termux
# Created by Manus for Imin

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}          NEWMANBOLT v2.0 INSTALLER                ${NC}"
echo -e "${CYAN}====================================================${NC}"

echo -e "${YELLOW}[*] Updating system packages...${NC}"
pkg update -y && pkg upgrade -y

echo -e "${YELLOW}[*] Installing dependencies (Python, Git, etc.)...${NC}"
pkg install python git -y

echo -e "${YELLOW}[*] Installing Python libraries...${NC}"
pip install rich aiohttp pyfiglet

echo -e "${YELLOW}[*] Cloning Newmanbolt repository...${NC}"
cd $HOME
if [ -d "Newmanbolt" ]; then
    rm -rf Newmanbolt
fi
git clone https://github.com/atotdf-create/NEWMANBOLT.git

echo -e "${YELLOW}[*] Setting up command shortcut...${NC}"
echo "alias newmanbolt='python $HOME/Newmanbolt/autorecon.py'" >> $HOME/.bashrc
echo "alias autorecon='python $HOME/Newmanbolt/autorecon.py'" >> $HOME/.bashrc

echo -e "${GREEN}[+] Installation complete!${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"
echo -e "${YELLOW}To start the tool, restart Termux or run:${NC}"
echo -e "${GREEN}source ~/.bashrc${NC}"
echo -e "${YELLOW}Then just type:${NC} ${GREEN}newmanbolt${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"
