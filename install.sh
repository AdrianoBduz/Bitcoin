#!/bin/bash

# Cores para o bash
RED='\033[0;91m'
GREEN='\033[0;92m'
YELLOW='\033[0;93m'
BLUE='\033[0;94m'
PURPLE='\033[0;95m'
CYAN='\033[0;96m'
WHITE='\033[0;97m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${PURPLE}${BOLD}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                TERMUX BITCOIN FINDER SETUP                  ║"
echo "║                 Professional Edition v2.0                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}${BOLD}🔧 Atualizando pacotes...${NC}"
pkg update && pkg upgrade -y

echo -e "${CYAN}${BOLD}🐍 Instalando Python...${NC}"
pkg install python -y

echo -e "${CYAN}${BOLD}📦 Instalando dependências Python...${NC}"
pip install --upgrade pip

echo -e "${GREEN}${BOLD}✅ Instalação concluída com sucesso!${NC}"
echo -e "${YELLOW}📝 Para executar: ${BOLD}python bitcoin_finder.py${NC}"
echo -e "${YELLOW}🎨 Script profissional com interface colorida!${NC}"
