#!/bin/bash

# Newman Bolt Pro v9.0 - Automated Installer
# Integrating AutoRecon Features
# Author: Imin

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}          NEWMAN BOLT PRO v9.0 INSTALLER           ${NC}"
echo -e "${CYAN}====================================================${NC}"

echo -e "${YELLOW}[*] Updating system packages...${NC}"
pkg update -y && pkg upgrade -y

echo -e "${YELLOW}[*] Installing Dependencies (Python, Git, Whois, DNSUtils)...${NC}"
pkg install python git whois dnsutils wget -y

echo -e "${YELLOW}[*] Installing Python Libraries (Rich, Aiohttp, Pyfiglet)...${NC}"
pip install rich aiohttp pyfiglet requests beautifulsoup4 colorama

echo -e "${YELLOW}[*] Cloning Newman Bolt repository...${NC}"
cd $HOME
if [ -d "Newmanbolt" ]; then
    rm -rf Newmanbolt
fi
git clone https://github.com/atotdf-create/NEWMANBOLT.git

echo -e "${YELLOW}[*] Setting up global command 'newmanbolt'...${NC}"
if [ -n "$PREFIX" ]; then
    WRAPPER="$PREFIX/bin/newmanbolt"
    echo "#!/bin/bash" > $WRAPPER
    echo "python3 $HOME/Newmanbolt/autorecon.py \"\$@\"" >> $WRAPPER
    chmod +x $WRAPPER
    echo -e "${GREEN}[+] Global command 'newmanbolt' created!${NC}"
fi

echo -e "${GREEN}[+] Installation complete!${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"
echo -e "${YELLOW}Launching Newman Bolt Pro v9.0...${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"

python3 $HOME/Newmanbolt/autorecon.py
