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
# Create a wrapper script in Termux $PREFIX/bin for global access
if [ -n "$PREFIX" ]; then
    WRAPPER="$PREFIX/bin/newmanbolt"
    echo "#!/bin/bash" > $WRAPPER
    echo "python3 $HOME/Newmanbolt/autorecon.py \"\$@\"" >> $WRAPPER
    chmod +x $WRAPPER
    echo -e "${GREEN}[+] Global command 'newmanbolt' created in $PREFIX/bin!${NC}"
else
    # Fallback for other Linux environments
    mkdir -p $HOME/.local/bin
    WRAPPER="$HOME/.local/bin/newmanbolt"
    echo "#!/bin/bash" > $WRAPPER
    echo "python3 $HOME/Newmanbolt/autorecon.py \"\$@\"" >> $WRAPPER
    chmod +x $WRAPPER
    echo "export PATH=\$PATH:\$HOME/.local/bin" >> $HOME/.bashrc
    echo -e "${YELLOW}[!] Added command to $HOME/.local/bin and updated PATH in .bashrc.${NC}"
fi

echo -e "${GREEN}[+] Installation complete!${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"
echo -e "${YELLOW}Launching Newmanbolt automatically...${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"

# Launch the tool immediately
python3 $HOME/Newmanbolt/autorecon.py
