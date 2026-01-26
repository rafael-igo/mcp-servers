# MCP Quick Reference Card

## 🚨 Comandos de Emergência

```python
# Auto-healing completo
docker-admin.auto_heal()

# Health check
docker-admin.health_check()

# Reiniciar tudo
docker-admin.manage_mcps("restart")
```

## 📋 Workflow Padrão

### Início
```python
docker-admin.check_docker_status()
memory-manager.load_context()
agente-resumo.get_next_steps()
```

### Durante
```python
memory-manager.update_progress(task, status, notes)
agente-orchestrator.invoke_agent(agent_name, task)
agente-insights.capture_insight(idea)
```

### Fim
```python
memory-manager.save_context(module, status, details)
checklist-validator.mark_completed(checklist_path, task)
agente-resumo.add_next_step(task, priority, estimate)
```

## 🎯 MCPs por Categoria

### 📊 Dados
```python
excel-server.read_excel_tabs(file_path)
excel-server.read_excel_with_formulas(file_path)
```

### 🤖 Agentes
```python
agente-orchestrator.list_agents()
agente-orchestrator.invoke_agent(name, task)
igo-openai-gateway.run_agent(name, task)
```

### 🧠 Memória
```python
memory-manager.load_context()
memory-manager.save_context(module, status, details)
memory-manager.add_decision(decision, ...)
```

### 📈 Status
```python
agente-resumo.get_project_status()
agente-resumo.get_module_status(module)
agente-resumo.generate_report(type, audience)
```

### ✅ Tarefas
```python
checklist-validator.get_pending_tasks()
checklist-validator.mark_completed(path, task)
checklist-validator.validate_checklist(path)
```

### 💡 Insights
```python
agente-insights.capture_insight(idea, type, complexity)
agente-insights.get_insights(status, type, limit)
agente-insights.make_decision(id, status, rationale)
```

### 🐳 Docker
```python
docker-admin.health_check()
docker-admin.auto_heal()
docker-admin.manage_mcp(name, action)
docker-admin.get_logs(service, lines)
```

## 🎓 Agentes Especializados

### Negócio
| Agente | Uso |
|--------|-----|
| agente-comercial-igo | Regras comerciais, vendas |
| agente-diretoria-igo | Visão estratégica |
| agente-marketing-igo | Marketing, comunicação |
| agente-operacao-igo | Processos operacionais |

### Técnicos
| Agente | Uso |
|--------|-----|
| agente-arquiteto-igo | Arquitetura, design patterns |
| agente-backend | Backend, APIs, banco de dados |
| agente-frontend-igo | Frontend, UX/UI, componentes |
| agente-qa-testes | QA, testes, qualidade |

### Módulos
| Agente | Uso |
|--------|-----|
| agente-transfer | Módulo Transfer |
| agente-rooming-list | Rooming List |
| agente-checkin | Check-in |
| agente-rsvp | RSVP |
| agente-credenciamento | Credenciamento |
| agente-tracking | Tracking |
| agente-analytics-kpi | Analytics e KPIs |

## 🔥 Comandos Mais Usados

### Top 10
```python
# 1. Health check
docker-admin.health_check()

# 2. Carregar contexto
memory-manager.load_context()

# 3. Próximos passos
agente-resumo.get_next_steps()

# 4. Invocar agente
agente-orchestrator.invoke_agent("agente-arquiteto-igo", task)

# 5. Análise profunda
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

## 💻 Comandos Docker

**Nota:** Apenas 2 MCPs rodam em Docker (docker-admin e api-database-tester).
Os outros 8 rodam via Python local automaticamente.

```bash
# Iniciar containers Docker
docker-compose up -d

# Parar containers
docker-compose down

# Status (deve mostrar apenas 2 containers)
docker-compose ps

# Logs
docker-compose logs -f docker-admin
docker-compose logs -f api-database-tester

# Reiniciar
docker-compose restart [docker-admin|api-database-tester]

# Rebuild
docker-compose up -d --build [docker-admin|api-database-tester]
```

## 🎨 Reasoning Levels

| Level | Uso |
|-------|-----|
| `none` | Tarefas triviais |
| `low` | Tarefas simples |
| `medium` | Code review, análises |
| `high` | Debugging, decisões |
| `xhigh` | Arquitetura, crítico |

Exemplo:
```python
igo-openai-gateway.run_architectural_review(
    description="Sistema de notificações",
    reasoning_effort="xhigh"
)
```

## 📝 Templates Rápidos

### Code Review
```python
context = memory-manager.load_context()
analysis = igo-openai-gateway.run_code_analysis(
    code="[código]",
    analysis_type="review",
    reasoning_effort="high"
)
```

### Nova Feature
```python
context = memory-manager.load_context()
plan = agente-orchestrator.invoke_agent(
    "agente-arquiteto-igo",
    "Planejar feature X"
)
decision = memory-manager.add_decision(...)
```

### Debugging
```python
context = memory-manager.load_context()
analysis = igo-openai-gateway.run_code_analysis(
    code="[código com bug]",
    analysis_type="debug",
    reasoning_effort="high"
)
```

### Gerar Testes
```python
tests = igo-openai-gateway.generate_tests(
    code="[código]",
    test_type="unit",
    framework="pytest",
    reasoning_effort="medium"
)
```

## 🛠️ Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| MCPs não respondem | `docker-admin.auto_heal()` |
| Docker não roda | `docker ps` → Iniciar Docker Desktop |
| Container parado | `docker-admin.manage_mcp(name, "restart")` |
| Ver erro | `docker-admin.get_logs(service, 100)` |
| Config dessinc | `docker-admin.sync_mcp_config()` |

## 📚 Documentação Completa

| Arquivo | Conteúdo |
|---------|----------|
| [README_MCPs.md](README_MCPs.md) | Índice principal |
| [GUIDELINES.md](GUIDELINES.md) | Docs completa MCPs |
| [VSCODE_GUIDELINES.md](VSCODE_GUIDELINES.md) | Setup VSCode |
| [CURSOR_SETUP.md](CURSOR_SETUP.md) | Setup Cursor |
| [CODEX_GUIDELINES.md](CODEX_GUIDELINES.md) | Guia Codex |
| [.cursorrules](.cursorrules) | Regras Cursor |
| [.claude/README.md](.claude/README.md) | Config Claude |

## 🎯 Casos de Uso

### "Quero revisar código"
```python
igo-openai-gateway.run_code_analysis(code, "review", "python", "high")
```

### "Preciso de um plano arquitetural"
```python
igo-openai-gateway.run_architectural_review(description, reasoning_effort="xhigh")
```

### "Quero consultar um especialista"
```python
agente-orchestrator.invoke_agent("agente-[tipo]", task)
```

### "Preciso gerar testes"
```python
igo-openai-gateway.generate_tests(code, "unit", "pytest")
```

### "Quero ver status do projeto"
```python
agente-resumo.get_project_status(include_details=True)
```

### "Capturar uma sugestão"
```python
agente-insights.capture_insight(idea, "feature", "medium", ["Module"])
```

### "Ver o que falta fazer"
```python
checklist-validator.get_pending_tasks()
agente-resumo.get_next_steps()
```

## 🔑 Atalhos por Editor

### VSCode
- `Cmd/Ctrl + Shift + P` → Command Palette
- `Cmd/Ctrl + K` → Claude quick command
- `Cmd/Ctrl + L` → Claude panel

### Cursor
- `Cmd/Ctrl + K` → Edit inline
- `Cmd/Ctrl + L` → Chat
- `Cmd/Ctrl + I` → Composer

### Codex
- Abre automaticamente no PR
- Use templates do CODEX_GUIDELINES.md

## 💾 Salvar para Depois

```python
# Sempre no fim:
memory-manager.save_context(module, status, details)
memory-manager.add_decision(decision, context, alternatives, chosen, reason)
agente-resumo.add_next_step(task, priority, estimate)
```

## ⚡ Performance Tips

1. Use `reasoning_effort="low"` para tarefas simples
2. Use `limit` em queries que retornam listas
3. Carregue contexto apenas uma vez por sessão
4. Use auto-heal em vez de reiniciar manualmente
5. Delegue para agentes especializados

---

**💡 Tip:** Mantenha este arquivo aberto em uma aba para consulta rápida!

**📌 Print e cole na parede:**
```
Início: health_check → load_context → get_next_steps
Durante: invoke_agent → update_progress → capture_insight
Fim: save_context → mark_completed → add_next_step
```
