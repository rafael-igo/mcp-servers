#!/bin/bash

echo "🧪 Testando MCPs do I GO Experience..."
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_mcp() {
    local name=$1
    local container=$2

    echo -n "Testing $name... "

    result=$(docker exec -i "$container" python server.py <<< '{"method":"tools/list"}' 2>&1)

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ OK${NC}"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}"
        echo "  Error: $result"
        return 1
    fi
}

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker não está rodando${NC}"
    exit 1
fi

# Verificar se containers estão rodando
echo "📦 Verificando containers..."
docker-compose ps

echo ""
echo "🔍 Testando MCPs individuais..."
echo ""

# Testar cada MCP
test_mcp "excel-server" "igo-excel-server"
test_mcp "agente-orchestrator" "igo-agente-orchestrator"
test_mcp "memory-manager" "igo-memory-manager"
test_mcp "checklist-validator" "igo-checklist-validator"
test_mcp "agente-insights" "igo-agente-insights"
test_mcp "agente-resumo" "igo-agente-resumo"
test_mcp "docker-admin" "igo-docker-admin"

echo ""
echo "✅ Testes completos!"
