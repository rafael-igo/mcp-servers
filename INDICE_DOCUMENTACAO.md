# 📚 Índice Completo da Documentação

## 🎯 Por Onde Começar?

### Novo no Projeto?
1. ⭐ **[README_MCPs.md](README_MCPs.md)** - COMECE AQUI
2. 📘 **[GUIDELINES.md](GUIDELINES.md)** - Entenda os MCPs
3. 🏗️ **[DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md)** - Arquitetura
4. **Guia do seu editor** (VSCode/Cursor/Codex)

### Desenvolvedor Experiente?
1. **[README_MCPs.md](README_MCPs.md)** - Overview
2. **Guia do seu editor**
3. **[MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md)** - Consulta rápida

### Curioso sobre Arquitetura?
1. **[DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md)** - Por que híbrida?
2. **[ARQUITETURA_VISUAL.md](ARQUITETURA_VISUAL.md)** - Diagramas visuais
3. **[MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md)** - O que mudou

---

## 📖 Documentação Principal

### 🌟 Essenciais

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| **[README_MCPs.md](README_MCPs.md)** ⭐ | Índice principal com links para tudo | Primeiro arquivo a ler |
| **[GUIDELINES.md](GUIDELINES.md)** 📘 | Documentação completa dos 10 MCPs | Referência detalhada |
| **[MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md)** ⚡ | Comandos rápidos, top 10, templates | Consulta diária |
| **[SETUP_REMOTO.md](SETUP_REMOTO.md)** 🌐 | Acesso remoto via SSH ao servidor | Usar MCPs remotamente |
| **[CONFIGURACAO_COMPLETA.md](CONFIGURACAO_COMPLETA.md)** 📋 | Mapa completo de arquivos e configs | Visão geral do projeto |

### 🏗️ Arquitetura

| Arquivo | Descrição | Quando Usar |
|---------|-----------|-------------|
| **[DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md)** 🔀 | Por que 2 Docker + 8 Python | Entender decisões arquiteturais |
| **[ARQUITETURA_VISUAL.md](ARQUITETURA_VISUAL.md)** 🎨 | Diagramas visuais da arquitetura | Ver estrutura visualmente |
| **[MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md)** 🔄 | Antes/depois, impacto, benefícios | Entender mudanças recentes |

---

## 💻 Por Editor

### VSCode

| Arquivo | Descrição |
|---------|-----------|
| **[VSCODE_GUIDELINES.md](VSCODE_GUIDELINES.md)** | Setup completo VSCode + Claude Code |
| **[.claude/settings.local.json](.claude/settings.local.json)** | Permissões pre-aprovadas |
| **[.claude/README.md](.claude/README.md)** | Como configurar permissões |

**Conteúdo:**
- ✅ Extensões recomendadas
- ✅ settings.json
- ✅ tasks.json
- ✅ launch.json
- ✅ Atalhos de teclado
- ✅ Snippets
- ✅ Multi-root workspace
- ✅ Workflows específicos

### Cursor

| Arquivo | Descrição |
|---------|-----------|
| **[CURSOR_SETUP.md](CURSOR_SETUP.md)** | Setup completo Cursor |
| **[.cursorrules](.cursorrules)** | Regras auto-carregadas |

**Conteúdo:**
- ✅ Setup passo-a-passo
- ✅ Features exclusivas (Cmd+K, Composer)
- ✅ @-mentions
- ✅ Settings recomendadas
- ✅ Atalhos essenciais
- ✅ Workflows otimizados
- ✅ Diferenças vs VSCode/Codex

### GitHub Codex

| Arquivo | Descrição |
|---------|-----------|
| **[CODEX_GUIDELINES.md](CODEX_GUIDELINES.md)** | Guia completo Codex |

**Conteúdo:**
- ✅ Templates de code review
- ✅ Workflows de PR
- ✅ Análises profundas
- ✅ Gestão de insights
- ✅ Templates úteis

---

## 🔧 Configuração

### Arquivos de Config

| Arquivo | Propósito | Editor |
|---------|-----------|--------|
| **[.mcp.json](.mcp.json)** | Configuração de todos os 10 MCPs | Todos |
| **[.cursorrules](.cursorrules)** | Regras automáticas do Cursor | Cursor |
| **[.claude/settings.local.json](.claude/settings.local.json)** | Permissões Claude Code | VSCode/CLI |
| **[docker-compose.yml](docker-compose.yml)** | Apenas 2 containers Docker | Todos |

### Estrutura de .mcp.json

```json
{
  "mcpServers": {
    "nome-mcp": {
      "command": "python | docker",
      "args": ["caminho ou docker args"],
      "env": {}
    }
  }
}
```

**10 MCPs configurados:**
- 8 via `python` (local)
- 2 via `docker` (containers)

---

## 🎓 Guias Temáticos

### Performance

| Tópico | Onde Ler |
|--------|----------|
| Por que Python é mais rápido | [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) |
| Comparações de latência | [ARQUITETURA_VISUAL.md](ARQUITETURA_VISUAL.md) |
| Impacto da migração | [MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md) |
| Otimizações | [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) |

### Desenvolvimento

| Tópico | Onde Ler |
|--------|----------|
| Workflows diários | [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md) |
| Debugging | Guia do seu editor |
| Hot reload | [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) |
| Testes | Guia do seu editor |

### Docker

| Tópico | Onde Ler |
|--------|----------|
| Quais MCPs em Docker | [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) |
| Por que apenas 2? | [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) |
| Como migrar de volta | [MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md) |
| Comandos Docker | [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md) |

### MCPs Específicos

| MCP | Documentação |
|-----|--------------|
| Todos os MCPs | [GUIDELINES.md](GUIDELINES.md) |
| docker-admin | [GUIDELINES.md](GUIDELINES.md) + [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) |
| api-database-tester | [GUIDELINES.md](GUIDELINES.md) |
| Agentes especializados | [GUIDELINES.md](GUIDELINES.md) |

---

## 📊 Estrutura dos Documentos

### Documentos Conceituais (Leitura)

```
README_MCPs.md
├── Overview dos MCPs
├── Links para guias
├── Quick start
└── Troubleshooting básico

GUIDELINES.md
├── Cada MCP em detalhe
├── Todas as ferramentas
├── Quando usar
├── Boas práticas
└── Workflows

DOCKER_vs_PYTHON.md
├── Por que híbrida?
├── Comparações
├── Casos de uso
└── Recomendações

ARQUITETURA_VISUAL.md
├── Diagramas
├── Fluxos
├── Comparações visuais
└── Performance

MIGRACAO_DOCKER_PYTHON.md
├── Antes/depois
├── Impacto
├── Benefícios
└── Como reverter
```

### Documentos Práticos (Referência)

```
MCP_QUICK_REFERENCE.md
├── Top 10 comandos
├── Templates
├── Troubleshooting rápido
└── Casos de uso

VSCODE_GUIDELINES.md
├── Setup
├── Configs
├── Workflows
└── Dicas

CURSOR_SETUP.md
├── Setup
├── Features
├── Workflows
└── Dicas

CODEX_GUIDELINES.md
├── Templates
├── Workflows
└── Dicas
```

### Documentos de Config (Setup)

```
.mcp.json
└── Configuração de todos MCPs

.cursorrules
└── Regras do Cursor

.claude/settings.local.json
└── Permissões Claude Code

docker-compose.yml
└── 2 containers Docker
```

---

## 🎯 Casos de Uso

### "Quero começar a usar os MCPs"
1. [README_MCPs.md](README_MCPs.md)
2. [GUIDELINES.md](GUIDELINES.md)
3. Guia do seu editor
4. [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md)

### "Quero entender a arquitetura"
1. [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md)
2. [ARQUITETURA_VISUAL.md](ARQUITETURA_VISUAL.md)
3. [MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md)

### "Preciso de comandos rápidos"
1. [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md)

### "Quero configurar meu editor"
1. **VSCode:** [VSCODE_GUIDELINES.md](VSCODE_GUIDELINES.md)
2. **Cursor:** [CURSOR_SETUP.md](CURSOR_SETUP.md)
3. **Codex:** [CODEX_GUIDELINES.md](CODEX_GUIDELINES.md)

### "Tenho um problema"
1. [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md) → Troubleshooting
2. Guia do seu editor → Troubleshooting
3. [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) → Quando usar cada um

### "Quero criar um novo MCP"
1. [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) → Decisão Python vs Docker
2. [MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md) → Como migrar
3. [GUIDELINES.md](GUIDELINES.md) → Ver exemplos

---

## 📏 Tamanho dos Documentos

| Arquivo | Linhas | Complexidade |
|---------|--------|--------------|
| **README_MCPs.md** | ~300 | ⭐⭐ Médio |
| **GUIDELINES.md** | ~400 | ⭐⭐⭐ Alto |
| **MCP_QUICK_REFERENCE.md** | ~250 | ⭐ Fácil |
| **DOCKER_vs_PYTHON.md** | ~350 | ⭐⭐ Médio |
| **ARQUITETURA_VISUAL.md** | ~500 | ⭐⭐⭐ Alto |
| **MIGRACAO_DOCKER_PYTHON.md** | ~300 | ⭐⭐ Médio |
| **VSCODE_GUIDELINES.md** | ~400 | ⭐⭐ Médio |
| **CURSOR_SETUP.md** | ~350 | ⭐⭐ Médio |
| **CODEX_GUIDELINES.md** | ~400 | ⭐⭐ Médio |
| **CONFIGURACAO_COMPLETA.md** | ~250 | ⭐ Fácil |

---

## 🔍 Busca Rápida

### Por Palavra-chave

| Procurando | Veja |
|------------|------|
| **Performance** | [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md), [ARQUITETURA_VISUAL.md](ARQUITETURA_VISUAL.md) |
| **Comandos** | [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md) |
| **Setup** | Guia do editor |
| **Arquitetura** | [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md), [ARQUITETURA_VISUAL.md](ARQUITETURA_VISUAL.md) |
| **Docker** | [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md), [MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md) |
| **Python** | [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) |
| **MCPs** | [GUIDELINES.md](GUIDELINES.md) |
| **Workflows** | [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md), Guias dos editores |
| **Troubleshooting** | [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md) |
| **Migração** | [MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md) |

---

## 📦 Arquivos por Categoria

### 📚 Documentação Geral (5)
- README_MCPs.md
- GUIDELINES.md
- MCP_QUICK_REFERENCE.md
- CONFIGURACAO_COMPLETA.md
- INDICE_DOCUMENTACAO.md (este arquivo)

### 🏗️ Arquitetura (3)
- DOCKER_vs_PYTHON.md
- ARQUITETURA_VISUAL.md
- MIGRACAO_DOCKER_PYTHON.md

### 💻 Por Editor (3)
- VSCODE_GUIDELINES.md
- CURSOR_SETUP.md
- CODEX_GUIDELINES.md

### ⚙️ Configuração (4)
- .mcp.json
- .cursorrules
- .claude/settings.local.json
- docker-compose.yml

### 📖 Meta (2)
- .claude/README.md
- INDICE_DOCUMENTACAO.md

**Total:** 17 arquivos de documentação

---

## 🎨 Convenções de Ícones

| Ícone | Significado |
|-------|-------------|
| ⭐ | Essencial, comece aqui |
| 📘 | Documentação detalhada |
| ⚡ | Quick reference |
| 🔀 | Comparação/decisão |
| 🎨 | Visual/diagramas |
| 🔄 | Mudanças/migração |
| 💻 | Específico de editor |
| ⚙️ | Configuração |
| 🐳 | Docker |
| 🐍 | Python |
| 📊 | Estatísticas/métricas |
| 🎯 | Objetivo/caso de uso |
| ✅ | Checklist/passo-a-passo |

---

## 🗺️ Mapa de Navegação

```
COMECE AQUI
    │
    ├─→ Novo? → README_MCPs.md → GUIDELINES.md → Guia Editor
    │
    ├─→ Experiente? → README_MCPs.md → Guia Editor → Quick Reference
    │
    ├─→ Arquitetura? → DOCKER_vs_PYTHON.md → ARQUITETURA_VISUAL.md
    │
    ├─→ Consulta rápida? → MCP_QUICK_REFERENCE.md
    │
    └─→ Visão geral? → CONFIGURACAO_COMPLETA.md
```

---

**Navegação:** Use este índice para encontrar rapidamente a documentação que precisa! 🚀
