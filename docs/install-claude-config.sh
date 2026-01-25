#!/bin/bash

# Script para instalar/atualizar configuração do Claude Desktop com os MCPs

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Instalador de Configuração Claude Desktop${NC}"
echo ""

# Detectar sistema operacional
OS="unknown"
CONFIG_PATH=""

if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    CONFIG_PATH="$HOME/.config/claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    OS="Windows"
    CONFIG_PATH="$APPDATA/Claude/claude_desktop_config.json"
else
    echo -e "${RED}✗ Sistema operacional não suportado: $OSTYPE${NC}"
    exit 1
fi

echo -e "Sistema detectado: ${GREEN}$OS${NC}"
echo -e "Caminho de configuração: ${BLUE}$CONFIG_PATH${NC}"
echo ""

# Verificar se o diretório existe
CONFIG_DIR=$(dirname "$CONFIG_PATH")
if [ ! -d "$CONFIG_DIR" ]; then
    echo -e "${YELLOW}⚠ Diretório de configuração não existe. Criando...${NC}"
    mkdir -p "$CONFIG_DIR"
fi

# Fazer backup se o arquivo existir
if [ -f "$CONFIG_PATH" ]; then
    BACKUP_PATH="${CONFIG_PATH}.backup-$(date +%Y%m%d-%H%M%S)"
    echo -e "${YELLOW}📦 Fazendo backup da configuração atual...${NC}"
    cp "$CONFIG_PATH" "$BACKUP_PATH"
    echo -e "${GREEN}✓ Backup salvo em: $BACKUP_PATH${NC}"
    echo ""
fi

# Copiar nova configuração
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EXAMPLE_CONFIG="$SCRIPT_DIR/claude_desktop_config.example.json"

if [ ! -f "$EXAMPLE_CONFIG" ]; then
    echo -e "${RED}✗ Arquivo de exemplo não encontrado: $EXAMPLE_CONFIG${NC}"
    exit 1
fi

echo -e "${BLUE}📝 Instalando nova configuração...${NC}"
cp "$EXAMPLE_CONFIG" "$CONFIG_PATH"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Configuração instalada com sucesso!${NC}"
    echo ""
    echo -e "${YELLOW}⚠ IMPORTANTE: Você precisa reiniciar o Claude Desktop para aplicar as mudanças${NC}"
    echo ""

    if [[ "$OS" == "macOS" ]]; then
        echo -e "${BLUE}Para reiniciar no macOS:${NC}"
        echo "  killall Claude && sleep 2 && open -a Claude"
    elif [[ "$OS" == "Linux" ]]; then
        echo -e "${BLUE}Para reiniciar no Linux:${NC}"
        echo "  pkill -f claude && sleep 2 && claude &"
    else
        echo -e "${BLUE}Para reiniciar no Windows:${NC}"
        echo "  - Feche o Claude pela bandeja do sistema"
        echo "  - Reabra o Claude"
    fi

    echo ""
    echo -e "${GREEN}🎉 MCPs configurados:${NC}"
    echo "  1. igo-memory (original)"
    echo "  2. excel-server"
    echo "  3. agente-orchestrator"
    echo "  4. memory-manager"
    echo "  5. checklist-validator"
    echo "  6. agente-insights"
    echo "  7. agente-resumo"
    echo "  8. docker-admin"
else
    echo -e "${RED}✗ Erro ao instalar configuração${NC}"
    exit 1
fi
