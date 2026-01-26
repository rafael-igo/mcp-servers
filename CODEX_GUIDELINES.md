# Codex Guidelines - MCPs Project

## Visão Geral

Este projeto possui 8 MCPs (Model Context Protocol Servers) que fornecem funcionalidades especializadas via Docker. Use estas guidelines no GitHub Codex para aproveitar ao máximo essas ferramentas.

## Quick Start no Codex

Ao abrir uma nova conversa no Codex:

```markdown
1. Verificar Docker: docker-admin.check_docker_status()
2. Carregar contexto: memory-manager.load_context()
3. Ver próximos passos: agente-resumo.get_next_steps()
```

## MCPs Essenciais

### 🧠 memory-manager
**Sua primeira parada em qualquer sessão**

```python
# Carregar contexto do projeto
memory-manager.load_context()

# Salvar progresso
memory-manager.save_context(
    module="Transfer",
    status="in_progress",
    details="Implementado validação de passageiros"
)

# Registrar decisão técnica
memory-manager.add_decision(
    decision="Usar Redis para cache",
    context="Performance estava ruim nas buscas",
    alternatives="In-memory, Memcached, Redis",
    chosen="Redis",
    reason="Melhor persistência e suporte a TTL"
)
```

### 🎯 agente-orchestrator
**Delegue para especialistas**

```python
# Listar agentes disponíveis
agente-orchestrator.list_agents()

# Invocar agente de arquitetura
agente-orchestrator.invoke_agent(
    agent_name="agente-arquiteto-igo",
    task="Revisar arquitetura do módulo de Transfer"
)

# Invocar agente de frontend
agente-orchestrator.invoke_agent(
    agent_name="agente-frontend-igo",
    task="Sugerir melhorias na UX do formulário de rooming list"
)

# Obter documentação de um agente
agente-orchestrator.get_agent_docs("agente-qa-testes")
```

### 🤖 igo-openai-gateway
**Análises profundas com GPT-5.2**

```python
# Revisão arquitetural com reasoning máximo
igo-openai-gateway.run_architectural_review(
    description="Implementação de sistema de notificações real-time",
    reasoning_effort="xhigh"
)

# Análise de código com reasoning alto
igo-openai-gateway.run_code_analysis(
    code="[seu código aqui]",
    analysis_type="security",
    language="python",
    reasoning_effort="high"
)

# Gerar testes automaticamente
igo-openai-gateway.generate_tests(
    code="[seu código aqui]",
    test_type="unit",
    framework="pytest",
    reasoning_effort="medium"
)

# Executar agente de desenvolvimento
igo-openai-gateway.run_development_agent(
    agent_name="agente-qa-testes",
    task="Revisar cobertura de testes do módulo X",
    reasoning_effort="medium",
    verbosity="high"
)
```

### 💡 agente-insights
**Capture e analise sugestões**

```python
# Capturar insight do PR
agente-insights.capture_insight(
    idea="Adicionar autocomplete no campo de hotel",
    insight_type="feature",
    complexity="medium",
    modules=["Rooming List", "Frontend"]
)

# Listar insights pendentes
agente-insights.get_insights(
    status="captured",
    limit=10
)

# Decidir sobre insight
agente-insights.make_decision(
    insight_id="INS-0001",
    decision_status="approved",
    rationale="Melhora UX significativamente",
    priority="high",
    effort_estimate="2-3 dias"
)
```

### 📈 agente-resumo
**Status e relatórios**

```python
# Status do projeto
agente-resumo.get_project_status(include_details=True)

# Status de módulo específico
agente-resumo.get_module_status("Transfer")

# Gerar relatório executivo
agente-resumo.generate_report(
    report_type="executive",
    audience="management"
)

# Gerar relatório técnico
agente-resumo.generate_report(
    report_type="technical",
    audience="team"
)

# Métricas
agente-resumo.get_metrics()
```

### 🐳 docker-admin
**Gestão de infraestrutura**

```python
# Auto-healing completo
docker-admin.auto_heal()

# Health check
docker-admin.health_check()

# Reiniciar todos MCPs
docker-admin.manage_mcps("restart")

# Reiniciar MCP específico
docker-admin.manage_mcp("excel-server", "restart")

# Ver logs
docker-admin.get_logs("igo-memory-manager", lines=50)

# Sincronizar config
docker-admin.sync_mcp_config()
```

## Workflow para Code Review

### 1. Preparação
```python
# Carregar contexto
memory-manager.load_context()

# Ver status do módulo relacionado
agente-resumo.get_module_status("Transfer")
```

### 2. Análise do Código
```python
# Análise de segurança
igo-openai-gateway.run_code_analysis(
    code="[código do PR]",
    analysis_type="security",
    reasoning_effort="high"
)

# Invocar QA
agente-orchestrator.invoke_agent(
    agent_name="agente-qa-testes",
    task="Revisar testes do PR #123"
)
```

### 3. Verificar Testes
```python
# Validar checklist
checklist-validator.validate_checklist("transfer-checklist.md")

# Ver tarefas pendentes
checklist-validator.get_pending_tasks()
```

### 4. Registrar Review
```python
# Salvar contexto
memory-manager.save_context(
    module="Transfer",
    status="completed",
    details="Code review PR #123 aprovado com sugestões"
)

# Capturar insights encontrados
agente-insights.capture_insight(
    idea="Adicionar validação de data no backend",
    insight_type="improvement",
    complexity="low"
)
```

## Workflow para Nova Feature

### 1. Planejamento
```python
# Carregar contexto
memory-manager.load_context()

# Consultar arquiteto
agente-orchestrator.invoke_agent(
    agent_name="agente-arquiteto-igo",
    task="Planejar implementação de feature X"
)

# Análise arquitetural profunda
igo-openai-gateway.run_architectural_review(
    description="Feature de notificações push",
    reasoning_effort="xhigh"
)
```

### 2. Desenvolvimento
```python
# Atualizar progresso
memory-manager.update_progress(
    task="Implementar notificações push",
    status="in_progress",
    notes="API criada, falta integração com frontend"
)

# Consultar frontend
agente-orchestrator.invoke_agent(
    agent_name="agente-frontend-igo",
    task="Sugerir componentes para notificações"
)
```

### 3. Testes
```python
# Gerar testes
igo-openai-gateway.generate_tests(
    code="[código da feature]",
    test_type="integration",
    framework="pytest"
)

# Validar checklist
checklist-validator.validate_checklist("feature-checklist.md")
```

### 4. Finalização
```python
# Marcar como completo
memory-manager.update_progress(
    task="Implementar notificações push",
    status="completed"
)

# Salvar contexto
memory-manager.save_context(
    module="Notifications",
    status="completed",
    details="Feature de notificações push implementada e testada"
)

# Adicionar próximo passo
agente-resumo.add_next_step(
    task="Documentar API de notificações",
    priority="medium",
    estimate="2h"
)
```

## Workflow para Debugging

### 1. Investigação
```python
# Carregar contexto do módulo
memory-manager.load_context()

# Análise do código
igo-openai-gateway.run_code_analysis(
    code="[código com bug]",
    analysis_type="debug",
    reasoning_effort="high"
)
```

### 2. Consultar Especialista
```python
# Backend bug
agente-orchestrator.invoke_agent(
    agent_name="agente-backend",
    task="Analisar bug no endpoint /api/transfers"
)
```

### 3. Registrar Solução
```python
# Registrar decisão
memory-manager.add_decision(
    decision="Fix race condition usando locks",
    context="Bug em transferências simultâneas",
    alternatives="Locks, Transactions, Queue",
    chosen="Locks com timeout",
    reason="Mais simples e resolve o problema específico"
)
```

## Templates Úteis

### Template: Início de Trabalho
```python
# 1. Verificar infraestrutura
docker-admin.health_check()

# 2. Carregar contexto
context = memory-manager.load_context()

# 3. Ver próximos passos
steps = agente-resumo.get_next_steps(limit=5)

# 4. Ver tarefas pendentes
tasks = checklist-validator.get_pending_tasks()
```

### Template: Consultar Especialista
```python
# Listar agentes disponíveis
agents = agente-orchestrator.list_agents()

# Invocar agente apropriado
result = agente-orchestrator.invoke_agent(
    agent_name="[nome-do-agente]",
    task="[descrição da tarefa]"
)
```

### Template: Análise Profunda
```python
# Para decisões arquiteturais importantes
review = igo-openai-gateway.run_architectural_review(
    description="[descrição do problema/feature]",
    context="[contexto adicional opcional]",
    reasoning_effort="xhigh"  # Máximo reasoning
)
```

### Template: Fim de Trabalho
```python
# 1. Salvar contexto
memory-manager.save_context(
    module="[nome do módulo]",
    status="[completed/in_progress/blocked]",
    details="[descrição do que foi feito]"
)

# 2. Marcar tarefas completadas
checklist-validator.mark_completed(
    checklist_path="[caminho do checklist]",
    task_pattern="[padrão da tarefa]"
)

# 3. Adicionar próximos passos
agente-resumo.add_next_step(
    task="[próxima tarefa]",
    priority="[critical/high/medium/low]",
    estimate="[estimativa]"
)
```

## Dicas para Codex

### 1. Use Contexto Sempre
O Codex não tem estado entre conversas. Sempre comece com:
```python
memory-manager.load_context()
```

### 2. Seja Específico com Agentes
Ao invés de fazer tudo sozinho, delegue:
```python
# ❌ Ruim: tentar analisar arquitetura sozinho
# ✅ Bom: invocar especialista
agente-orchestrator.invoke_agent("agente-arquiteto-igo", task)
```

### 3. Use Reasoning Apropriado
- `none/low`: Tarefas simples, diretas
- `medium`: Análises moderadas, code review
- `high`: Decisões importantes, debugging complexo
- `xhigh`: Arquitetura, decisões críticas

### 4. Capture Insights
Toda sugestão no PR ou discussão:
```python
agente-insights.capture_insight(idea, insight_type="feature")
```

### 5. Documente Decisões
Toda decisão técnica importante:
```python
memory-manager.add_decision(...)
```

## Agentes Disponíveis

### Negócio
- `agente-comercial-igo` - Regras comerciais
- `agente-diretoria-igo` - Visão estratégica
- `agente-marketing-igo` - Marketing e comunicação
- `agente-operacao-igo` - Processos operacionais

### Técnicos
- `agente-arquiteto-igo` - Arquitetura e design
- `agente-backend` - Backend/API
- `agente-frontend-igo` - Frontend/UX
- `agente-qa-testes` - QA e testes

### Módulos
- `agente-transfer` - Transfer module
- `agente-rooming-list` - Rooming List module
- `agente-checkin` - Check-in module
- `agente-rsvp` - RSVP module
- `agente-credenciamento` - Credenciamento
- `agente-tracking` - Tracking
- `agente-analytics-kpi` - Analytics e KPIs

## Troubleshooting no Codex

### MCP não responde
```python
docker-admin.auto_heal()
```

### Erro de conexão
```python
docker-admin.check_docker_status()
docker-admin.manage_mcps("restart")
```

### Container específico com problema
```python
# Ver logs
docker-admin.get_logs("igo-[nome-mcp]", lines=100)

# Reiniciar
docker-admin.manage_mcp("[nome-mcp]", "restart")
```

### Configuração dessincronizada
```python
docker-admin.sync_mcp_config()
```

## Referências Rápidas

- [GUIDELINES.md](GUIDELINES.md) - Guidelines completas
- [.cursorrules](.cursorrules) - Regras do Cursor
- [docs/LISTA_MCPS.md](docs/LISTA_MCPS.md) - Lista detalhada de MCPs
- [docs/DOCKER-ADMIN.md](docs/DOCKER-ADMIN.md) - Docker Admin docs
- [docs/ORQUESTRADOR.md](docs/ORQUESTRADOR.md) - Orquestrador docs

## Comandos Essenciais

```python
# Status completo
docker-admin.health_check()
agente-resumo.get_project_status(include_details=True)

# Tudo pendente
checklist-validator.get_pending_tasks()
agente-resumo.get_next_steps()

# Relatório executivo
agente-resumo.generate_report(report_type="executive")

# Auto-healing
docker-admin.auto_heal()
```

---

**Lembre-se:** No Codex, sempre comece carregando o contexto e termine salvando. Os MCPs são sua equipe de especialistas - use-os!
