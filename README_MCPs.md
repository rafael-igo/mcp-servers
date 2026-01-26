# MCPs - Guia Completo de Configuração

Este projeto possui 8 MCPs (Model Context Protocol Servers) que funcionam como ferramentas especializadas para assistentes de IA.

## 🚀 Quick Start

### 1. Iniciar MCPs que precisam de Docker
```bash
docker-compose up -d
```

**Nota:** Apenas 2 MCPs rodam via Docker:
- `docker-admin` - Gerenciamento de containers
- `api-database-tester` - Testes de API/DB (precisa ODBC Driver 18)

Os outros 8 MCPs rodam via **Python local** automaticamente quando você usa os editores.

### 2. Verificar Status
```bash
# Ver containers Docker
docker-compose ps

# Deve mostrar apenas 2 containers:
# - igo-docker-admin
# - igo-api-database-tester
```

### 3. Testar MCPs
Abra seu editor e use:
```python
docker-admin.health_check()
```

## 🏗️ Arquitetura Híbrida

Este projeto usa **arquitetura híbrida** para otimizar performance:

- **2 MCPs em Docker** - Apenas os que realmente precisam
- **8 MCPs via Python** - Performance máxima, desenvolvimento ágil

**Por quê?**
- ⚡ Startup 4-6x mais rápido
- 🚀 Latência 10-50x menor
- 💾 75% menos memória
- 💻 Hot reload automático

📖 Leia mais: [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) | [MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md)

## 📚 Documentação por Editor

Escolha seu editor e siga o guia específico:

### [VSCode](VSCODE_GUIDELINES.md)
- Configuração do VSCode
- Extensões recomendadas
- Atalhos e workflows
- Integração com Claude Code

### [Cursor](CURSOR_SETUP.md)
- Setup completo do Cursor
- Features exclusivas (Cmd+K, Composer)
- Workflows otimizados
- @-mentions e context

### [GitHub Codex](CODEX_GUIDELINES.md)
- Templates para code review
- Workflows de PR
- Análises profundas
- Gestão de insights

### [Claude Code CLI](GUIDELINES.md)
- Documentação completa de todos os MCPs
- Boas práticas
- Fluxos de trabalho
- Troubleshooting

## 🛠️ MCPs Disponíveis

### MCPs via Docker (2)
| MCP | Container | Descrição |
|-----|-----------|-----------|
| **docker-admin** | igo-docker-admin | Administração de Docker e MCPs |
| **api-database-tester** | igo-api-database-tester | Testes de API e Database (ODBC) |

### MCPs via Python Local (8)
| MCP | Execução | Descrição |
|-----|----------|-----------|
| **excel-server** | Python local | Leitura e processamento de Excel |
| **agente-orchestrator** | Python local | Orquestração de agentes especializados |
| **memory-manager** | Python local | Gerenciamento de contexto do projeto |
| **checklist-validator** | Python local | Validação de checklists |
| **agente-insights** | Python local | Captura e análise de insights |
| **agente-resumo** | Python local | Resumos e status do projeto |
| **igo-openai-gateway** | Python local | Gateway OpenAI/GPT-5.2 com reasoning |
| **vuetify-uiux** | Python local | Componentes Vuetify e UI/UX |

## 🎯 Qual Arquivo Ler?

**Escolha baseado no seu caso de uso:**

| Quero... | Leia... |
|----------|---------|
| Configurar VSCode | [VSCODE_GUIDELINES.md](VSCODE_GUIDELINES.md) |
| Configurar Cursor | [CURSOR_SETUP.md](CURSOR_SETUP.md) |
| Usar no GitHub Codex | [CODEX_GUIDELINES.md](CODEX_GUIDELINES.md) |
| **Acesso remoto (SSH)** | [SETUP_REMOTO.md](SETUP_REMOTO.md) 🌐 |
| Entender todos os MCPs | [GUIDELINES.md](GUIDELINES.md) |
| **Entender Docker vs Python** | [DOCKER_vs_PYTHON.md](DOCKER_vs_PYTHON.md) ⭐ |
| Ver migração Docker→Python | [MIGRACAO_DOCKER_PYTHON.md](MIGRACAO_DOCKER_PYTHON.md) |
| Saber o que mudou | Este arquivo (README_MCPs.md) |
| Configurar .cursorrules | [.cursorrules](.cursorrules) |
| Configurar Claude Code | [.claude/README.md](.claude/README.md) |

## 🔧 Configuração Rápida por Editor

### 🌐 Local vs Remoto

Este projeto suporta **2 modos**:

- **🏠 Local:** `.mcp.json` - MCPs no PC (<1ms latência)
- **🌐 Remoto:** `.mcp.remote.json` - MCPs via SSH no servidor 15.15.255.9 (~20-100ms)

📖 **Setup remoto:** [SETUP_REMOTO.md](SETUP_REMOTO.md)

---

### VSCode
1. Instale extensão "Claude Code"
2. **Local:** `.mcp.json` já configurado
3. **Remoto:** Renomeie `.mcp.remote.json` → `.mcp.json`
4. Permissões em `.claude/settings.local.json`
5. Leia: [VSCODE_GUIDELINES.md](VSCODE_GUIDELINES.md)

### Cursor
1. Instale Cursor de https://cursor.sh
2. Arquivo `.cursorrules` já configurado
3. **Local:** Config aponta para `.mcp.json`
4. **Remoto:** Aponte para `.mcp.remote.json`
5. Leia: [CURSOR_SETUP.md](CURSOR_SETUP.md)

### GitHub Codex
1. Codex detecta `.mcp.json` automaticamente
2. **Remoto:** Renomeie `.mcp.remote.json` → `.mcp.json`
3. Use templates em [CODEX_GUIDELINES.md](CODEX_GUIDELINES.md)
4. Sempre comece com `memory-manager.load_context()`

### Claude Code CLI
1. **Local:** `.mcp.json` já configurado
2. **Remoto:** Renomeie `.mcp.remote.json` → `.mcp.json`
3. Execute: `claude chat`
4. Use: `docker-admin.health_check()`

## 📋 Arquivos Importantes

```
mcp-servers/
├── .mcp.json                      # Config MCPs (todos os editores)
├── .cursorrules                   # Regras do Cursor
├── .claude/
│   ├── settings.local.json        # Permissões Claude Code
│   └── README.md                  # Docs configuração Claude
├── GUIDELINES.md                  # 📘 Documentação completa MCPs
├── VSCODE_GUIDELINES.md           # 📗 Guia VSCode
├── CURSOR_SETUP.md                # 📙 Guia Cursor
├── CODEX_GUIDELINES.md            # 📕 Guia Codex
├── README_MCPs.md                 # 📄 Este arquivo
└── docker-compose.yml             # Orquestração containers
```

## 🎬 Workflows Essenciais

### Início do Dia
```python
# 1. Verificar infraestrutura
docker-admin.health_check()

# 2. Carregar contexto
memory-manager.load_context()

# 3. Ver próximos passos
agente-resumo.get_next_steps()
```

### Durante Desenvolvimento
```python
# Consultar especialista
agente-orchestrator.invoke_agent("agente-arquiteto-igo", "sua tarefa")

# Análise profunda
igo-openai-gateway.run_architectural_review(description, reasoning_effort="xhigh")

# Atualizar progresso
memory-manager.update_progress(task, status, notes)
```

### Fim do Dia
```python
# Salvar contexto
memory-manager.save_context(module, status, details)

# Marcar tarefas completadas
checklist-validator.mark_completed(checklist_path, task_pattern)

# Adicionar próximos passos
agente-resumo.add_next_step(task, priority, estimate)
```

## 🆘 Troubleshooting

### MCPs não respondem
```python
docker-admin.auto_heal()
```

### Docker não está rodando
```bash
# Verificar
docker ps

# Iniciar MCPs
docker-compose up -d
```

### Ver logs de um MCP
```python
docker-admin.get_logs("igo-memory-manager", lines=50)
```

### Reiniciar tudo
```bash
docker-compose restart
```

## 🌟 Features Destacadas

### 1. Auto-Healing
MCPs se auto-corrigem:
```python
docker-admin.auto_heal()  # Detecta e corrige problemas automaticamente
```

### 2. Agentes Especializados
Delegue para especialistas:
- `agente-arquiteto-igo` - Arquitetura
- `agente-frontend-igo` - Frontend
- `agente-backend` - Backend
- `agente-qa-testes` - QA e testes

### 3. Reasoning com GPT-5.2
Análises profundas:
```python
igo-openai-gateway.run_architectural_review(
    description="Problema complexo",
    reasoning_effort="xhigh"  # Máximo reasoning
)
```

### 4. Memória Persistente
Contexto entre sessões:
```python
memory-manager.load_context()  # Carrega tudo da última sessão
```

### 5. Insights Automáticos
Captura sugestões:
```python
agente-insights.capture_insight(idea, insight_type, complexity)
```

## 🎓 Ordem de Leitura Recomendada

**Para iniciantes:**
1. 📄 Este arquivo (README_MCPs.md)
2. 📘 [GUIDELINES.md](GUIDELINES.md) - Entender todos os MCPs
3. 📗 Guia do seu editor (VSCode/Cursor/Codex)
4. 🚀 Começar a usar!

**Para desenvolvedores experientes:**
1. 📄 Este arquivo
2. 📗 Guia do editor que usa
3. 📕 [.cursorrules](.cursorrules) - Ver regras
4. 🚀 Direto ao código!

**Para code reviews:**
1. 📕 [CODEX_GUIDELINES.md](CODEX_GUIDELINES.md)
2. Templates de workflow
3. Usar `igo-openai-gateway` para análises

## 💡 Dicas de Ouro

### 1. Sempre Comece com Contexto
```python
memory-manager.load_context()
```

### 2. Use Auto-Healing Primeiro
Antes de debugar manualmente:
```python
docker-admin.auto_heal()
```

### 3. Delegue para Especialistas
Não faça tudo sozinho:
```python
agente-orchestrator.invoke_agent("agente-apropriado", task)
```

### 4. Capture Insights
Toda sugestão/ideia:
```python
agente-insights.capture_insight(idea)
```

### 5. Documente Decisões
Decisões técnicas importantes:
```python
memory-manager.add_decision(decision, context, alternatives, chosen, reason)
```

## 🔗 Links Úteis

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Claude Code](https://docs.anthropic.com/claude/docs)
- [Cursor](https://docs.cursor.sh)

## 📞 Suporte

- Problemas com MCPs: `docker-admin.auto_heal()`
- Ver logs: `docker-admin.get_logs(service)`
- Status geral: `docker-admin.health_check()`

## 🎉 Próximos Passos

1. ✅ Iniciar Docker: `docker-compose up -d`
2. ✅ Escolher seu editor
3. ✅ Ler o guia específico
4. ✅ Testar com `docker-admin.health_check()`
5. ✅ Começar a desenvolver!

---

**Pronto para começar?** Escolha seu editor e leia o guia correspondente! 🚀
