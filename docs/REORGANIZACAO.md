# Reorganização Completa - MCPs

**Data:** 2026-01-25

## Mudanças Realizadas

### 1. Estrutura de Diretórios

**ANTES:**
```
projeto-claude/
├── 01-AGENTES/
├── 05-CHECKLISTS/
└── 06-MEMORIA-AGENTE/
```

**DEPOIS:**
```
api/mcp-servers/
├── docs/
│   ├── agentes/          ← Movido de projeto-claude/01-AGENTES
│   ├── checklists/       ← Movido de projeto-claude/05-CHECKLISTS
│   ├── memoria/          ← Movido de projeto-claude/06-MEMORIA-AGENTE
│   ├── README.md
│   ├── SETUP.md
│   ├── DOCKER-ADMIN.md
│   ├── COMO-USAR-DOCKER-ADMIN.md
│   ├── STATUS.md
│   └── ...
├── excel-server/
├── agente-orchestrator/
├── memory-manager/
├── checklist-validator/
├── agente-insights/
├── agente-resumo/
├── docker-admin/
└── docker-compose.yml
```

### 2. Atualização dos MCPs

Todos os server.py foram atualizados para apontar para `/api/mcp-servers/docs/`:

#### agente-orchestrator
```python
# ANTES
LEGACY_agentes_dir = PROJECT_ROOT / "projeto-claude" / "01-AGENTES"
LEGACY_MEMORIA_DIR = PROJECT_ROOT / "projeto-claude" / "06-MEMORIA-AGENTE"

# DEPOIS
DOCS_DIR = Path(__file__).parent.parent / "docs"
AGENTES_DIR = DOCS_DIR / "agentes"
MEMORIA_DIR = DOCS_DIR / "memoria"
```

#### memory-manager
```python
# ANTES
MEMORIA_DIR = PROJECT_ROOT / "projeto-claude" / "06-MEMORIA-AGENTE"

# DEPOIS
DOCS_DIR = Path(__file__).parent.parent / "docs"
MEMORIA_DIR = DOCS_DIR / "memoria"
```

#### checklist-validator
```python
# ANTES
CHECKLISTS_DIR = PROJECT_ROOT / "projeto-claude" / "05-CHECKLISTS"

# DEPOIS
DOCS_DIR = Path(__file__).parent.parent / "docs"
CHECKLISTS_DIR = DOCS_DIR / "checklists"
```

#### agente-insights (Já estava correto)
```python
DOCS_DIR = Path(__file__).parent.parent / "docs"
INSIGHTS_FILE = DOCS_DIR / "insights_capturados.json"
MEMORIA_DIR = DOCS_DIR / "memoria"
```

#### agente-resumo (Já estava correto)
```python
DOCS_DIR = Path(__file__).parent.parent / "docs"
MEMORIA_DIR = DOCS_DIR / "memoria"
CONTEXT_FILE = MEMORIA_DIR / "contexto-atual.json"
```

#### docker-admin (Novo - já criado corretamente)
```python
DOCS_DIR = Path("/app/docs")
```

### 3. Criação de Diretórios Automática

Todos os MCPs agora garantem que os diretórios existem:

```python
def _ensure_memoria_dir():
    """Garante que diretório de memória existe."""
    MEMORIA_DIR.mkdir(parents=True, exist_ok=True)

def _ensure_checklists_dir():
    """Garante que diretório de checklists existe."""
    CHECKLISTS_DIR.mkdir(parents=True, exist_ok=True)
```

### 4. Arquivo Inicial Automático

MCPs criam arquivos iniciais se não existirem:

**memory-manager:**
- `contexto-atual.md`
- `ultimas-acoes.md`
- `proximos-passos.md`
- `decisoes-tecnicas.md`

**agente-orchestrator:**
- `ultimas-acoes.md`

**checklist-validator:**
- Cria arquivos sob demanda

**agente-insights:**
- `insights_capturados.json`

**agente-resumo:**
- `contexto-atual.json`
- `progresso.json`

## MCPs Ativos

### 1. excel-server
- Container: `igo-excel-server`
- Ferramentas: 3
- Status: ✅ Atualizado e rodando

### 2. agente-orchestrator
- Container: `igo-agente-orchestrator`
- Ferramentas: 4
- Status: ✅ Atualizado e rodando
- Mudanças: Removido legacy paths

### 3. memory-manager
- Container: `igo-memory-manager`
- Ferramentas: 6
- Status: ✅ Atualizado e rodando
- Mudanças: Novo path + auto-criação de arquivos

### 4. checklist-validator
- Container: `igo-checklist-validator`
- Ferramentas: 5
- Status: ✅ Atualizado e rodando
- Mudanças: Novo path + auto-criação de diretório

### 5. agente-insights
- Container: `igo-agente-insights`
- Ferramentas: 6
- Status: ✅ Rodando (já estava correto)

### 6. agente-resumo
- Container: `igo-agente-resumo`
- Ferramentas: 7
- Status: ✅ Rodando (já estava correto)

### 7. docker-admin
- Container: `igo-docker-admin`
- Ferramentas: 7
- Status: ✅ Novo e rodando

### 8. igo-memory (Original)
- Container: `igo-memory-server-mcp-server-1`
- Status: ✅ Rodando

## Documentação Reorganizada

Toda documentação movida para `/api/mcp-servers/docs/`:

- ✅ README.md - Guia completo
- ✅ SETUP.md - Setup passo a passo
- ✅ STATUS.md - Status atual
- ✅ DOCKER-ADMIN.md - Documentação técnica
- ✅ COMO-USAR-DOCKER-ADMIN.md - Guia de uso
- ✅ GUIA_USO_RAPIDO.md
- ✅ ORQUESTRADOR.md
- ✅ claude_desktop_config.example.json
- ✅ test-mcps.sh
- ✅ memoria/ - Diretório de memória
- ✅ agentes/ - Diretório de agentes
- ✅ checklists/ - Diretório de checklists

## Comandos de Teste

### Rebuild Completo
```bash
cd /Users/rafamacpro/Projetos/GIT/Transfer-logistica/api/mcp-servers
docker-compose up -d --build
```

### Verificar Status
```bash
docker-compose ps
```

### Ver Logs
```bash
docker-compose logs -f
```

### Testar MCPs
```bash
cd docs
./test-mcps.sh
```

## Compatibilidade

- ✅ Todos os MCPs apontam para `/api/mcp-servers/docs/`
- ✅ Nenhum path legado (projeto-claude) restante
- ✅ Auto-criação de diretórios e arquivos
- ✅ Docker-compose atualizado
- ✅ Claude Desktop config atualizado (9 MCPs)

## Próximos Passos

1. Reiniciar Claude Desktop:
```bash
killall Claude && sleep 2 && open -a Claude
```

2. Testar docker-admin:
```python
health_check()
auto_heal()
```

3. Verificar todos os MCPs funcionando:
```python
list_agents()
get_project_status(True)
validate_checklist("mvp.md")  # Se existir
```

## Notas Importantes

- ✅ Pasta `projeto-claude/` foi removida
- ✅ Tudo centralizado em `api/mcp-servers/docs/`
- ✅ MCPs criam estrutura automaticamente se não existir
- ✅ docker-admin gerencia toda infraestrutura
- ✅ 9 MCPs ativos e funcionais

**Reorganização completa em:** 2026-01-25 (18:45)
