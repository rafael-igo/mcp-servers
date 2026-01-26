# Arquitetura Visual dos MCPs

## 🎨 Diagrama da Arquitetura Atual

```
┌─────────────────────────────────────────────────────────────┐
│                      EDITORES                                │
│  VSCode + Claude Code │ Cursor │ Codex │ Claude CLI         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ .mcp.json (configuração)
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐            ┌────────────────┐
│  🐍 PYTHON    │            │  🐳 DOCKER     │
│   LOCAL       │            │   CONTAINERS   │
│   (8 MCPs)    │            │   (2 MCPs)     │
├───────────────┤            ├────────────────┤
│               │            │                │
│ excel-server  │            │ docker-admin   │
│ orchestrator  │            │ api-db-tester  │
│ memory-mgr    │            │                │
│ checklist     │            └────────────────┘
│ insights      │                    │
│ resumo        │                    │
│ openai-gw     │            ┌───────┴────────┐
│ vuetify       │            │                │
│               │            ▼                ▼
└───────────────┘     Docker Socket      ODBC Driver 18
        │                   │               (SQL Server)
        │                   │
        ▼                   ▼
┌─────────────────────────────────┐
│    SISTEMA DE ARQUIVOS          │
│  - Excel files                  │
│  - Memória persistente          │
│  - Checklists                   │
│  - Insights                     │
│  - Agentes docs                 │
└─────────────────────────────────┘
```

## 📊 Comparação: Antes vs Depois

### ANTES (Tudo em Docker)

```
┌──────────────────────────────────────────┐
│              EDITORES                    │
└─────────────┬────────────────────────────┘
              │
              ▼
    ┌─────────────────────┐
    │   docker-compose    │
    │   (8 containers)    │
    │                     │
    │ ┌─────────────────┐ │
    │ │ excel-server    │ │  ~200MB
    │ ├─────────────────┤ │
    │ │ orchestrator    │ │  ~200MB
    │ ├─────────────────┤ │
    │ │ memory-mgr      │ │  ~200MB
    │ ├─────────────────┤ │
    │ │ checklist       │ │  ~200MB
    │ ├─────────────────┤ │
    │ │ insights        │ │  ~200MB
    │ ├─────────────────┤ │
    │ │ resumo          │ │  ~200MB
    │ ├─────────────────┤ │
    │ │ docker-admin    │ │  ~200MB
    │ ├─────────────────┤ │
    │ │ openai-gw       │ │  ~200MB
    │ └─────────────────┘ │
    │                     │
    │ Total: ~1.6GB       │
    │ Startup: 20-30s     │
    └─────────────────────┘
```

### DEPOIS (Arquitetura Híbrida)

```
┌──────────────────────────────────────────┐
│              EDITORES                    │
└──────────┬───────────────────┬───────────┘
           │                   │
           ▼                   ▼
    ┌─────────────┐    ┌──────────────┐
    │  Python     │    │    Docker    │
    │  Local      │    │  (2 only)    │
    │             │    │              │
    │ excel       │    │ docker-admin │ ~200MB
    │ orch        │    │ api-db-test  │ ~200MB
    │ memory      │    │              │
    │ checklist   │    │ Total: ~400MB│
    │ insights    │    │ Start: ~5s   │
    │ resumo      │    └──────────────┘
    │ openai      │
    │ vuetify     │
    │             │
    │ Total: ~400MB│
    │ Start: ~0s  │
    └─────────────┘

    TOTAL SISTEMA:
    - Memória: ~800MB (antes: 1.6GB) ✅ -50%
    - Startup: ~5s (antes: 30s)      ✅ -83%
    - Containers: 2 (antes: 8)       ✅ -75%
```

## 🔄 Fluxo de Requisição

### Python Local (Maioria dos MCPs)

```
Editor
  │
  │ 1. Comando MCP via stdio
  ▼
Python Process (local)
  │
  │ 2. Executa função
  │
  ├─→ Lê arquivo local (Excel, MD, etc)
  ├─→ Chama API (OpenAI, etc)
  ├─→ Processa dados
  │
  │ 3. Retorna resultado
  ▼
Editor
  │
  └─→ ~1ms latência total ⚡
```

### Docker (Apenas 2 MCPs)

```
Editor
  │
  │ 1. Comando via docker exec
  ▼
Docker Container
  │
  │ 2. Executa Python no container
  │
  ├─→ Acessa Docker socket (docker-admin)
  ├─→ Usa ODBC Driver (api-db-tester)
  │
  │ 3. Retorna resultado
  ▼
Docker → Editor
  │
  └─→ ~10-50ms latência total 🐢
```

## 💡 Decisão de Arquitetura

### Árvore de Decisão

```
┌─────────────────────────────┐
│  Novo MCP a ser criado      │
└─────────────┬───────────────┘
              │
              ▼
    ┌─────────────────────┐
    │ Precisa de Docker   │
    │ socket?             │
    └──┬────────────┬─────┘
       │            │
      SIM          NÃO
       │            │
       ▼            ▼
    ┌──────┐   ┌─────────────────┐
    │DOCKER│   │ Precisa drivers │
    └──────┘   │ Linux?          │
               └──┬──────────┬───┘
                  │          │
                 SIM        NÃO
                  │          │
                  ▼          ▼
               ┌──────┐  ┌────────┐
               │DOCKER│  │ PYTHON │ ⭐
               └──────┘  └────────┘
```

## 📈 Performance: Cenários Reais

### Cenário 1: Carregar Contexto (memory-manager)

```
ANTES (Docker):
─────────────────────────────────────────
Editor → Docker exec → Container Python → Ler arquivo → Retorna
│         5ms         │      10ms      │    20ms    │   5ms
└────────────────────────────────────────────────────────────┘
Total: ~40ms

DEPOIS (Python):
─────────────────────────
Editor → Python → Ler arquivo → Retorna
│         0ms   │    1ms     │   0ms
└─────────────────────────────────────┘
Total: ~1ms

MELHORIA: 40x mais rápido! ⚡
```

### Cenário 2: Análise de Excel (excel-server)

```
ANTES (Docker):
────────────────────────────────────────────────
Editor → Docker → Container → Pandas → Retorna
│        5ms   │    10ms   │  100ms  │   5ms
└──────────────────────────────────────────────┘
Total: ~120ms

DEPOIS (Python):
───────────────────────────────
Editor → Python → Pandas → Retorna
│         0ms  │  100ms  │   0ms
└─────────────────────────────────┘
Total: ~100ms

MELHORIA: 20% mais rápido ⚡
```

### Cenário 3: Gerenciar Docker (docker-admin)

```
SEMPRE Docker (necessário):
─────────────────────────────────────────────────
Editor → Docker exec → Container → Docker API → Retorna
│         5ms        │   10ms    │    50ms    │   5ms
└───────────────────────────────────────────────────────┘
Total: ~70ms

NÃO PODE migrar para Python local:
❌ Python local não tem acesso ao Docker socket
✅ Deve permanecer em Docker
```

## 🎯 Casos de Uso por MCP

### 🐍 Python Local (Performance Crítica)

```
┌─────────────────────┐
│ excel-server        │ → Lê Excel frequentemente
├─────────────────────┤    Precisa de I/O rápido
│ memory-manager      │ → Carregado em TODA sessão
├─────────────────────┤    Latência crítica
│ agente-orchestrator │ → Invocado múltiplas vezes
├─────────────────────┤    Comunicação rápida
│ checklist-validator │ → Lê/escreve MD
├─────────────────────┤    I/O frequente
│ agente-insights     │ → Captura em tempo real
├─────────────────────┤    Escrita rápida
│ agente-resumo       │ → Gera relatórios
├─────────────────────┤    Processamento local
│ igo-openai-gateway  │ → Chamadas API externas
├─────────────────────┤    Sem necessidade de container
│ vuetify-uiux        │ → Componentes UI
└─────────────────────┘    Processamento local
```

### 🐳 Docker (Necessidade Específica)

```
┌─────────────────────┐
│ docker-admin        │ → PRECISA: Docker socket
│                     │   Gerencia containers
│                     │   Privileged access
├─────────────────────┤
│ api-database-tester │ → PRECISA: ODBC Driver 18
│                     │   SQL Server (Linux)
│                     │   Driver não disponível no Windows
└─────────────────────┘
```

## 📦 Distribuição de Tamanho

### Antes (Tudo Docker)

```
Total: ~4GB em disco

┌──────────────────────────────────────┐
│         Imagens Docker (4GB)         │
├──────────────────────────────────────┤
│ excel-server:        500MB █████     │
│ orchestrator:        500MB █████     │
│ memory-mgr:          500MB █████     │
│ checklist:           500MB █████     │
│ insights:            500MB █████     │
│ resumo:              500MB █████     │
│ docker-admin:        500MB █████     │
│ openai-gw:           500MB █████     │
└──────────────────────────────────────┘
```

### Depois (Híbrido)

```
Total: ~1.2GB em disco

┌──────────────────────────────────────┐
│      Imagens Docker (800MB)          │
├──────────────────────────────────────┤
│ docker-admin:        400MB ████      │
│ api-db-tester:       400MB ████      │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│      Python Local (~400MB)           │
├──────────────────────────────────────┤
│ 8 MCPs × ~50MB cada = 400MB ████     │
│ (venv + deps compartilhadas)         │
└──────────────────────────────────────┘

ECONOMIA: ~70% de disco ✅
```

## 🚀 Startup Sequence

### Antes

```
$ docker-compose up -d

[0s]   Building images...
[10s]  Creating network...
[12s]  Creating containers...
[15s]  Starting excel-server...
[17s]  Starting orchestrator...
[19s]  Starting memory-mgr...
[21s]  Starting checklist...
[23s]  Starting insights...
[25s]  Starting resumo...
[27s]  Starting docker-admin...
[29s]  Starting openai-gw...
[30s]  ✅ All containers up

Total: ~30 segundos
```

### Depois

```
$ docker-compose up -d

[0s]  Creating network...
[1s]  Starting docker-admin...
[3s]  Starting api-db-tester...
[5s]  ✅ All containers up

Total: ~5 segundos (-83%)

Python MCPs: Iniciam automaticamente quando usados (0s)
```

## 💻 Uso de Recursos

### CPU

```
Antes (8 containers):
────────────────────────────────────
Idle: 5-10% CPU
  - 8 processos Python
  - 8 processos Docker
  - Overhead de virtualização

Depois (2 containers + 8 Python):
────────────────────────────────────
Idle: 1-2% CPU
  - 2 processos Docker
  - 8 processos Python (quando em uso)
  - Menos overhead

ECONOMIA: ~80% CPU em idle
```

### Memória

```
Antes (8 containers):
════════════════════════════════════
│████████████████│ 1.6GB (containers)
│████            │ 400MB (overhead Docker)
└─────────────────────────────────────
Total: ~2GB

Depois (2 containers + 8 Python):
════════════════════════════════════
│████│ 400MB (2 containers)
│████│ 400MB (8 Python MCPs)
│██  │ 200MB (overhead reduzido)
└─────────────────────────────────────
Total: ~1GB

ECONOMIA: ~50% memória
```

## 🎓 Lições Aprendidas

### ✅ Use Python Local quando:
1. Performance é crítica
2. I/O frequente a arquivos
3. Desenvolvimento ativo
4. Não há dependências de sistema específicas
5. Debug frequente

### ✅ Use Docker quando:
1. Precisa de drivers de sistema (ODBC, etc)
2. Precisa de acesso ao Docker socket
3. Isolamento de rede necessário
4. Deploy em produção/CI
5. Conflitos de dependências

### ❌ Não use Docker apenas por:
- "Organização"
- "Todos em containers"
- Conveniência
- Moda/tendência

---

**Princípio:** "Use a ferramenta certa para o trabalho certo" 🎯

**Resultado:** Arquitetura híbrida otimizada! 🚀
