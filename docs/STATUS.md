# Status dos MCPs

**Última atualização:** 2026-01-25 (18:30)
**Status Geral:** ✅ 8 MCPs ATIVOS

## MCPs Ativos

### 1. igo-memory (Original)
- Container: `igo-memory-server-mcp-server-1`
- Status: ✅ Rodando

### 2. excel-server
- Container: `igo-excel-server`
- Status: ✅ Rodando
- Ferramentas: 3

### 3. agente-orchestrator
- Container: `igo-agente-orchestrator`
- Status: ✅ Rodando
- Ferramentas: 4

### 4. memory-manager
- Container: `igo-memory-manager`
- Status: ✅ Rodando
- Ferramentas: 6

### 5. checklist-validator
- Container: `igo-checklist-validator`
- Status: ✅ Rodando
- Ferramentas: 5

### 6. agente-insights
- Container: `igo-agente-insights`
- Status: ✅ Rodando

### 7. agente-resumo
- Container: `igo-agente-resumo`
- Status: ✅ Rodando

### 8. docker-admin (NOVO)
- Container: `igo-docker-admin`
- Status: ✅ Rodando
- Ferramentas: 7
- Funcionalidades:
  - Auto-start do Docker
  - Gestão automática de MCPs
  - Gestão da API
  - Auto-healing
  - Logs centralizados

## Configuração Claude Desktop

**Arquivo:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Configurado com todos os 8 MCPs.

## Documentação

Toda documentação movida para `/api/mcp-servers/docs/`:
- ✅ README.md - Guia completo
- ✅ SETUP.md - Setup passo a passo
- ✅ DOCKER-ADMIN.md - Documentação do docker-admin
- ✅ GUIA_USO_RAPIDO.md
- ✅ ORQUESTRADOR.md
- ✅ claude_desktop_config.example.json
- ✅ test-mcps.sh
- ✅ memoria/ - Diretório de memória

## Comandos Úteis

### Verificar Status
```bash
cd /Users/rafamacpro/Projetos/GIT/Transfer-logistica/api/mcp-servers
docker-compose ps
```

### Iniciar Todos
```bash
docker-compose up -d
```

### Rebuild
```bash
docker-compose up -d --build
```

### Logs
```bash
docker-compose logs -f
```

### Parar Todos
```bash
docker-compose down
```

## Próximos Passos

1. Reiniciar Claude Desktop para ativar todos os MCPs:
```bash
killall Claude && sleep 2 && open -a Claude
```

2. Testar docker-admin:
```python
# Verificar saúde
health_check()

# Auto-healing
auto_heal()

# Gerenciar MCPs
manage_mcps("status")
```

## Estrutura Final

```
api/mcp-servers/
├── docs/                          # ← Toda documentação
│   ├── README.md
│   ├── SETUP.md
│   ├── DOCKER-ADMIN.md
│   ├── STATUS.md
│   ├── GUIA_USO_RAPIDO.md
│   ├── ORQUESTRADOR.md
│   ├── claude_desktop_config.example.json
│   ├── test-mcps.sh
│   └── memoria/
├── excel-server/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── agente-orchestrator/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── memory-manager/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── checklist-validator/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── agente-insights/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── agente-resumo/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-admin/                  # ← NOVO
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
└── docker-compose.yml
```
