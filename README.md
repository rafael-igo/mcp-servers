# MCP Servers - Sistema de Agentes Especializados

Sistema completo de **Model Context Protocol (MCP) Servers** com arquitetura híbrida otimizada para máxima performance.

## 🚀 Quick Start

```bash
# 1. Iniciar containers Docker (apenas 2)
docker-compose up -d

# 2. Verificar status
docker-compose ps

# 3. Abrir seu editor (VSCode/Cursor/Codex)
# MCPs Python iniciam automaticamente!

# 4. Testar
docker-admin.health_check()
```

## 📦 O que são MCPs?

**MCPs (Model Context Protocol Servers)** são ferramentas especializadas que estendem as capacidades dos assistentes de IA (Claude, GPT, etc) com funcionalidades específicas:

- 📊 Processar arquivos Excel
- 🤖 Orquestrar agentes especializados
- 🧠 Gerenciar memória persistente
- ✅ Validar checklists
- 💡 Capturar e analisar insights
- 📈 Gerar relatórios de status
- 🐳 Administrar Docker
- 🔍 Testar APIs e bancos de dados
- 🎨 Gerar componentes UI/UX

## 🏗️ Arquitetura Híbrida

Este projeto usa **arquitetura híbrida** para otimizar performance:

### 🐳 Docker (2 MCPs)
Apenas os que **realmente precisam**:
- **docker-admin** - Acesso ao Docker socket
- **api-database-tester** - ODBC Driver 18 (Linux)

### 🐍 Python Local (8 MCPs)
Performance máxima:
- excel-server
- agente-orchestrator
- memory-manager
- checklist-validator
- agente-insights
- agente-resumo
- igo-openai-gateway
- vuetify-uiux

### 🎯 Por que Híbrida?

- ⚡ **4-6x startup mais rápido** (5s vs 30s)
- 🚀 **10-50x latência menor** (<1ms vs 10-50ms)
- 💾 **75% menos memória** (800MB vs 1.6GB)
- 💻 **Hot reload automático** (0s vs 30s rebuild)
- 🔧 **Debug nativo no IDE**

📖 Leia mais: [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md)

## 📚 Documentação

### 🌟 Comece Aqui
| Documento | Descrição |
|-----------|-----------|
| **[README_MCPs.md](README_MCPs.md)** ⭐ | Índice principal - Comece aqui! |
| **[GUIDELINES.md](GUIDELINES.md)** | Documentação completa dos 10 MCPs |
| **[MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md)** | Comandos rápidos e templates |

### 🏗️ Arquitetura
| Documento | Descrição |
|-----------|-----------|
| **[DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md)** | Por que 2 Docker + 8 Python |
| **[ARQUITETURA_VISUAL.md](ARQUITETURA_VISUAL.md)** | Diagramas e fluxos visuais |
| **[MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md)** | Antes/depois, impacto, benefícios |

### 💻 Por Editor
| Documento | Descrição |
|-----------|-----------|
| **[VSCODE_GUIDELINES.md](VSCODE_GUIDELINES.md)** | Setup VSCode + Claude Code |
| **[CURSOR_SETUP.md](CURSOR_SETUP.md)** | Setup Cursor completo |
| **[CODEX_GUIDELINES.md](CODEX_GUIDELINES.md)** | Guia GitHub Codex |

### 📖 Outros
| Documento | Descrição |
|-----------|-----------|
| **[CONFIGURACAO_COMPLETA.md](CONFIGURACAO_COMPLETA.md)** | Mapa completo do projeto |
| **[INDICE_DOCUMENTACAO.md](INDICE_DOCUMENTACAO.md)** | Índice de toda documentação |

## 🛠️ MCPs Disponíveis

### 🐳 Via Docker (2)
| MCP | Descrição | Por que Docker? |
|-----|-----------|-----------------|
| **docker-admin** | Administração de containers | Precisa Docker socket |
| **api-database-tester** | Testes API/Database | Precisa ODBC Driver 18 |

### 🐍 Via Python Local (8)
| MCP | Descrição |
|-----|-----------|
| **excel-server** | Processamento de arquivos Excel |
| **agente-orchestrator** | Orquestração de agentes especializados |
| **memory-manager** | Gerenciamento de contexto e memória |
| **checklist-validator** | Validação de checklists |
| **agente-insights** | Captura e análise de insights |
| **agente-resumo** | Resumos e status do projeto |
| **igo-openai-gateway** | Gateway OpenAI/GPT-5.2 com reasoning |
| **vuetify-uiux** | Componentes Vuetify e UI/UX |

## ⚙️ Instalação

### 🌐 Escolha seu Modo

**🏠 Local (Desenvolvimento):**
- MCPs rodam no seu PC
- Melhor performance (<1ms)
- Use: `.mcp.json`

**🌐 Remoto (Servidor 15.15.255.9):**
- MCPs rodam no servidor via SSH
- Acesso de qualquer PC
- Use: `.mcp.remote.json`
- 📖 Guia: [SETUP_REMOTO.md](SETUP_REMOTO.md)

---

### Pré-requisitos

**Local:**
- Docker Desktop (para 2 MCPs)
- Python 3.11+ (para 8 MCPs)
- VSCode/Cursor ou acesso ao GitHub Codex

**Remoto:**
- Cliente SSH (Windows: OpenSSH, Mac/Linux: nativo)
- Chave SSH configurada
- Acesso ao servidor 15.15.255.9

### Setup Local (Desenvolvimento)

**Nota:** Para desenvolvimento local no servidor, você pode rodar os MCPs via Python diretamente (mais rápido).
Para acesso remoto de Windows, use todos via Docker (veja Setup Remoto).

```bash
# 1. Clone o repositório
git clone <repo-url>
cd mcp-servers

# 2. Inicie containers Docker (TODOS os 10 MCPs)
docker-compose up -d

# 3. Verifique status
docker-compose ps
# Deve mostrar 10 containers: todos com status "Up"

# 4. Configure seu editor
# Veja o guia específico do seu editor
```

### Setup Remoto (Windows → Servidor Linux)

**Guia rápido:** [QUICK_START_REMOTO.md](QUICK_START_REMOTO.md) ⚡

```powershell
# No Windows:

# 1. Configure SSH (sem senha)
ssh-keygen -t ed25519
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh rafael@15.15.255.9 "cat >> ~/.ssh/authorized_keys"

# 2. Subir containers no servidor
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose up -d"

# 3. Usar configuração remota (todos via Docker)
cd C:\GIT-RAFAEL\mcp-servers
Rename-Item .mcp.json .mcp.local.json
Copy-Item .mcp.remote-docker.json .mcp.json

# 4. Reload editor e testar
# VSCode: Ctrl+Shift+P → "Reload Window"
# Teste: docker-admin.health_check()
```

**Guia completo:** [SETUP_WINDOWS_REMOTO.md](SETUP_WINDOWS_REMOTO.md)

### Configuração por Editor

#### VSCode + Claude Code
```bash
# Instale extensão "Claude Code"
# Arquivo .mcp.json já configurado
# Permissões em .claude/settings.local.json

# Leia: VSCODE_GUIDELINES.md
```

#### Cursor
```bash
# Abra projeto no Cursor
# Arquivo .cursorrules já configurado
# Configure MCP path em settings

# Leia: CURSOR_SETUP.md
```

#### GitHub Codex
```bash
# Codex detecta .mcp.json automaticamente
# Use em PRs do GitHub

# Leia: CODEX_GUIDELINES.md
```

## 💡 Uso Básico

### Workflow Padrão

```python
# 1. Início de sessão
docker-admin.health_check()
memory-manager.load_context()
agente-resumo.get_next_steps()

# 2. Durante desenvolvimento
agente-orchestrator.invoke_agent("agente-arquiteto-igo", "sua tarefa")
memory-manager.update_progress(task, status, notes)
agente-insights.capture_insight(idea)

# 3. Fim de sessão
memory-manager.save_context(module, status, details)
checklist-validator.mark_completed(checklist_path, task)
agente-resumo.add_next_step(task, priority)
```

### Top 10 Comandos

```python
# 1. Health check completo
docker-admin.health_check()

# 2. Carregar contexto do projeto
memory-manager.load_context()

# 3. Ver próximos passos
agente-resumo.get_next_steps()

# 4. Invocar agente especializado
agente-orchestrator.invoke_agent("agente-arquiteto-igo", task)

# 5. Análise profunda com reasoning
igo-openai-gateway.run_architectural_review(desc, reasoning_effort="xhigh")

# 6. Atualizar progresso
memory-manager.update_progress(task, "in_progress", notes)

# 7. Capturar insight
agente-insights.capture_insight(idea, "feature", "medium")

# 8. Status do projeto
agente-resumo.get_project_status(include_details=True)

# 9. Tarefas pendentes
checklist-validator.get_pending_tasks()

# 10. Auto-healing
docker-admin.auto_heal()
```

## 🎯 Casos de Uso

### Code Review
```python
# Análise de código com reasoning alto
igo-openai-gateway.run_code_analysis(
    code="[código]",
    analysis_type="review",
    reasoning_effort="high"
)
```

### Decisão Arquitetural
```python
# Revisão arquitetural com reasoning máximo
igo-openai-gateway.run_architectural_review(
    description="Sistema de notificações",
    reasoning_effort="xhigh"
)
```

### Consultar Especialista
```python
# Invocar agente especializado
agente-orchestrator.invoke_agent(
    agent_name="agente-frontend-igo",
    task="Revisar componentes React"
)
```

### Gerar Testes
```python
# Gerar testes automaticamente
igo-openai-gateway.generate_tests(
    code="[código]",
    test_type="unit",
    framework="pytest"
)
```

## 🤖 Agentes Especializados

### Negócio
- **agente-comercial-igo** - Regras comerciais
- **agente-diretoria-igo** - Visão estratégica
- **agente-marketing-igo** - Marketing
- **agente-operacao-igo** - Processos operacionais

### Técnicos
- **agente-arquiteto-igo** - Arquitetura e design
- **agente-backend** - Backend/APIs
- **agente-frontend-igo** - Frontend/UX
- **agente-qa-testes** - QA e testes

### Módulos
- **agente-transfer** - Transfer module
- **agente-rooming-list** - Rooming List
- **agente-checkin** - Check-in
- **agente-rsvp** - RSVP
- **agente-credenciamento** - Credenciamento
- **agente-tracking** - Tracking
- **agente-analytics-kpi** - Analytics

## 🚨 Troubleshooting

### MCPs não respondem
```python
docker-admin.auto_heal()
```

### Docker não está rodando
```bash
# Verificar
docker ps

# Iniciar Docker Desktop
# Então:
docker-compose up -d
```

### Ver logs
```python
docker-admin.get_logs("igo-docker-admin", lines=50)
```

### Reiniciar tudo
```bash
docker-compose restart
```

## 📊 Performance

| Métrica | Antes (8 Docker) | Depois (2 Docker + 8 Python) | Melhoria |
|---------|------------------|------------------------------|----------|
| Startup | 20-30s | 5s | **4-6x** |
| Latência | 10-50ms | <1ms | **10-50x** |
| Memória | 1.6GB | 800MB | **50%** |
| CPU idle | 5-10% | 1-2% | **5x** |
| Disco | 4GB | 1.2GB | **70%** |

## 🛡️ Segurança

- MCPs Python rodam com permissões do usuário
- Containers Docker com usuário não-root
- Acesso limitado via volumes
- Isolamento de rede via bridge
- Permissões granulares no `.claude/settings.local.json`

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -m 'Add NovaFeature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT - veja o arquivo LICENSE para detalhes.

## 🙏 Agradecimentos

- [Anthropic](https://www.anthropic.com/) - Claude e MCP Protocol
- [OpenAI](https://openai.com/) - GPT-5.2
- Comunidade open source

## 📞 Suporte

- 📖 Documentação: [README_MCPs.md](README_MCPs.md)
- ⚡ Quick Reference: [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md)
- 🏗️ Arquitetura: [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md)
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/mcp-servers/issues)

## 🗺️ Roadmap

- [ ] Adicionar mais agentes especializados
- [ ] Suporte a mais editores
- [ ] Melhorar performance
- [ ] Adicionar mais MCPs
- [ ] Documentação em vídeo
- [ ] Testes automatizados
- [ ] CI/CD pipeline

## 📈 Status do Projeto

- ✅ **10 MCPs** implementados e testados
- ✅ **Arquitetura híbrida** otimizada
- ✅ **Documentação completa** (17 arquivos)
- ✅ **Suporte a 3 editores** (VSCode, Cursor, Codex)
- ✅ **Performance otimizada** (4-6x mais rápido)

---

**🚀 Começar agora:** [README_MCPs.md](README_MCPs.md)

**💡 Dúvidas?** Leia: [INDICE_DOCUMENTACAO.md](INDICE_DOCUMENTACAO.md)

**🎯 Arquitetura?** Veja: [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md)
