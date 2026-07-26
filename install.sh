#!/bin/bash

# Newmanbolt v3.0 - Automated Installer for Termux
# Created by Manus for Imin

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}          NEWMANBOLT v3.0 INSTALLER                ${NC}"
echo -e "${CYAN}====================================================${NC}"

echo -e "${YELLOW}[*] Updating system packages...${NC}"
pkg update -y && pkg upgrade -y

echo -e "${YELLOW}[*] Installing dependencies (Python, Git, etc.)...${NC}"
pkg install python git -y

echo -e "${YELLOW}[*] Installing Python libraries...${NC}"
pip install rich aiohttp pyfiglet requests beautifulsoup4

echo -e "${YELLOW}[*] Cloning Newmanbolt repository...${NC}"
cd $HOME
if [ -d "Newmanbolt" ]; then
    rm -rf Newmanbolt
fi
git clone https://github.com/atotdf-create/NEWMANBOLT.git

echo -e "${YELLOW}[*] Setting up global command...${NC}"
# Create a wrapper script in /data/data/com.termux/files/usr/bin/ for global access
WRAPPER="/data/data/com.termux/files/usr/bin/newmanbolt"
if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    echo "#!/bin/bash" > $WRAPPER
    echo "python3 $HOME/Newmanbolt/autorecon.py \"\$@\"" >> $WRAPPER
    chmod +x $WRAPPER
    echo -e "${GREEN}[+] Global command 'newmanbolt' created!${NC}"
else
    # Fallback to alias if not in Termux
    echo "alias newmanbolt='python3 $HOME/Newmanbolt/autorecon.py'" >> $HOME/.bashrc
    echo -e "${YELLOW}[!] Not in Termux environment, added alias to .bashrc instead.${NC}"
fi

echo -e "${GREEN}[+] Installation complete!${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"
echo -e "${YELLOW}Launching Newmanbolt automatically...${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"

# Launch the tool immediately
python3 $HOME/Newmanbolt/autorecon.py
