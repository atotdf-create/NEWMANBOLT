#!/bin/bash

# Newmanbolt v8.0 - Final Error-Free Installer
# Created by Manus for Imin

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}====================================================${NC}"
echo -e "${GREEN}          NEWMANBOLT v8.0 FINAL INSTALLER          ${NC}"
echo -e "${CYAN}====================================================${NC}"

echo -e "${YELLOW}[*] Updating system packages...${NC}"
pkg update -y && pkg upgrade -y

echo -e "${YELLOW}[*] Installing Core Dependencies (Python, Git, Wget)...${NC}"
pkg install python git wget -y

echo -e "${YELLOW}[*] Cloning Newmanbolt Final repository...${NC}"
cd $HOME
if [ -d "Newmanbolt" ]; then
    rm -rf Newmanbolt
fi
git clone https://github.com/atotdf-create/NEWMANBOLT.git

echo -e "${YELLOW}[*] Setting up global command 'newmanbolt'...${NC}"
if [ -n "$PREFIX" ]; then
    # Termux specific
    WRAPPER="$PREFIX/bin/newmanbolt"
    echo "#!/bin/bash" > $WRAPPER
    echo "python3 $HOME/Newmanbolt/autorecon.py \"\$@\"" >> $WRAPPER
    chmod +x $WRAPPER
    echo -e "${GREEN}[+] Global command created in $PREFIX/bin!${NC}"
else
    # Fallback for other Linux
    mkdir -p $HOME/.local/bin
    WRAPPER="$HOME/.local/bin/newmanbolt"
    echo "#!/bin/bash" > $WRAPPER
    echo "python3 $HOME/Newmanbolt/autorecon.py \"\$@\"" >> $WRAPPER
    chmod +x $WRAPPER
    echo "export PATH=\$PATH:\$HOME/.local/bin" >> $HOME/.bashrc
    echo -e "${GREEN}[+] Command added to .local/bin and .bashrc updated.${NC}"
fi

echo -e "${GREEN}[+] Final Installation complete!${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"
echo -e "${YELLOW}Launching Newmanbolt Final v8.0...${NC}"
echo -e "${CYAN}----------------------------------------------------${NC}"

python3 $HOME/Newmanbolt/autorecon.py
