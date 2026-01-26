# Lista Completa de MCPs - I GO Experience

**Última Atualização:** 2026-01-26
**Total de MCPs:** 11

## 📋 Visão Geral

Este projeto possui **11 MCPs** (Model Context Protocol servers) que fornecem ferramentas especializadas para o desenvolvimento do sistema I GO Experience.

### 🔄 Mudança Importante - Janeiro 2026

**8 MCPs migrados para execução nativa Windows (sem Docker):**
- ✅ Inicialização mais rápida (~0.5s vs ~2-5s)
- ✅ Menos overhead de recursos
- ✅ Debugging mais fácil
- ✅ Não depende de Docker Desktop

**Apenas 2 MCPs mantêm Docker (necessário):**
- docker-admin (gerencia containers)
- api-database-tester (precisa ODBC Driver 18 Linux)

---

## 🔧 MCPs Disponíveis

### 1. excel-server 🟢 LOCAL
**Modo:** Python local (Windows)
**Diretório:** `mcp-servers/excel-server/`
**Comando:** `python c:/GIT-RAFAEL/mcp-servers/excel-server/server.py`

**Descrição:** Servidor especializado em leitura e processamento de arquivos Excel.

**Ferramentas:**
- `read_excel_tabs()` - Lê todas as abas de um arquivo Excel
- `read_excel_with_formulas()` - Lê Excel preservando fórmulas
- `get_excel_metadata()` - Retorna metadados do arquivo

**Casos de Uso:**
- Processar planilhas de rooming list
- Validar dados de transfer
- Extrair informações de check-in

---

### 2. agente-orchestrator 🟢 LOCAL
**Modo:** Python local (Windows)
**Diretório:** `mcp-servers/agente-orchestrator/`
**Comando:** `python c:/GIT-RAFAEL/mcp-servers/agente-orchestrator/server.py`

**Descrição:** Orquestrador de agentes especializados do projeto.

**Ferramentas:**
- `list_agents()` - Lista todos os agentes e MCPs disponíveis
- `invoke_agent()` - Invoca um agente específico com uma tarefa
- `get_agent_docs()` - Retorna documentação completa de um agente
- `update_agent_memory()` - Atualiza memória do sistema de agentes

**MCPs Gerenciados:**
- agente-insights
- agente-resumo
- igo-openai-gateway
- api-database-tester
- excel-server
- memory-manager
- checklist-validator
- docker-admin
- vuetify-uiux

**Agentes Especializados (17):**
- agente-rooming-list, agente-transfer, agente-checkin
- agente-backend, agente-tracking, agente-credenciamento
- agente-rsvp, agente-arquiteto-igo, agente-frontend-igo
- agente-integracoes-igo, agente-qa-testes
- agente-comercial-igo, agente-marketing-igo
- agente-diretoria-igo, agente-operacao-igo
- agente-solucoes, agente-analytics-kpi

---

### 3. memory-manager 🟢 LOCAL ⭐ MULTI-PROJETO
**Modo:** Python local (Windows)
**Diretório:** `mcp-servers/memory-manager/`
**Comando:** `python c:/GIT-RAFAEL/mcp-servers/memory-manager/server.py`

**Descrição:** Gerenciador de contexto e memória do projeto com suporte multi-projeto/branch.

**Novidade:** Sistema híbrido de contexto - configure uma vez, use em todas as chamadas.

**Ferramentas (10):**

**Contexto (2 novas):**
- `set_project_context(project, branch)` - Define contexto global
- `get_project_context()` - Retorna contexto atual

**Memória (6 atualizadas):**
- `save_context(module, status, details, project?, branch?)` - Salva contexto
- `load_context(project?, branch?)` - Carrega contexto completo
- `update_progress(task, status, notes?, project?, branch?)` - Atualiza progresso
- `get_next_steps(project?, branch?)` - Retorna próximos passos
- `add_decision(decision, context, alternatives, chosen, reason, project?, branch?)` - Registra ADR
- `get_memory_summary(project?, branch?, include_all_branches?)` - Resumo da memória

**Analytics (2 novas):**
- `compare_branches(project, branch_a, branch_b)` - Compara duas branches
- `list_all_projects()` - Lista todos os projetos e branches

**Estrutura:**
```
docs/memoria/
├── igo-journey/
│   ├── main/
│   │   ├── contexto-atual.md
│   │   ├── ultimas-acoes.md
│   │   └── decisoes-tecnicas.md
│   ├── feature-rooming/
│   └── core/
└── sigaevento/
    ├── main/
    └── develop/
```

**Casos de Uso:**
- Manter continuidade entre sessões por projeto/branch
- Registrar decisões arquiteturais específicas de branch
- Comparar progresso entre branches
- Analytics cross-project da empresa

---

### 4. checklist-validator 🟢 LOCAL
**Modo:** Python local (Windows)
**Diretório:** `mcp-servers/checklist-validator/`
**Comando:** `python c:/GIT-RAFAEL/mcp-servers/checklist-validator/server.py`

**Descrição:** Validador e gerenciador de checklists do projeto.

**Ferramentas:**
- `validate_checklist()` - Valida e retorna estatísticas
- `mark_completed()` - Marca tarefa como completa
- `get_pending_tasks()` - Lista tarefas pendentes
- `list_checklists()` - Lista todos os checklists
- `create_checklist()` - Cria novo checklist

**Casos de Uso:**
- Acompanhar progresso do MVP
- Validar conclusão de módulos
- Gerenciar tarefas do projeto

---

### 5. agente-insights 🟢 LOCAL ⭐ MULTI-PROJETO
**Modo:** Python local (Windows)
**Diretório:** `mcp-servers/agente-insights/`
**Comando:** `python c:/GIT-RAFAEL/mcp-servers/agente-insights/server.py`

**Descrição:** Captura e gerencia insights e sugestões com suporte multi-projeto/branch.

**Ferramentas (12):**

**Contexto (2 novas):**
- `set_project_context(project, branch)` - Define contexto global
- `get_project_context()` - Retorna contexto atual

**Insights (6 atualizadas):**
- `capture_insight(idea, type, complexity, modules?, project?, branch?)` - Captura insight
- `get_insights(status?, type?, limit, project?, branch?)` - Lista insights
- `update_insight_status(id, status, notes?, project?, branch?)` - Atualiza status
- `add_agent_feedback(id, agent, feedback, recommendation?, project?, branch?)` - Adiciona feedback
- `make_decision(id, decision, rationale, priority?, estimate?, project?, branch?)` - Decide sobre insight
- `get_statistics(project?, branch?, cross_project?)` - Estatísticas

**Analytics (4 novas):**
- `compare_branch_insights(project, branch_a, branch_b)` - Compara insights entre branches
- `list_all_project_insights()` - Lista todos os projetos e insights

**Estrutura:**
```
docs/insights/
├── igo-journey/
│   ├── main/
│   │   └── insights.json
│   └── feature-rooming/
│       └── insights.json
└── sigaevento/
    └── main/
        └── insights.json
```

**Tipos de Insight:**
- feature - Nova funcionalidade
- bug - Correção de bug
- improvement - Melhoria
- decision - Decisão técnica
- exploration - Exploração/investigação

**Casos de Uso:**
- Capturar ideias por projeto/branch
- Consultar agentes sobre sugestões
- Comparar insights entre branches (feature vs main)
- Analytics cross-project da empresa

---

### 6. agente-resumo 🟢 LOCAL ⭐ MULTI-PROJETO
**Modo:** Python local (Windows)
**Diretório:** `mcp-servers/agente-resumo/`
**Comando:** `python c:/GIT-RAFAEL/mcp-servers/agente-resumo/server.py`

**Descrição:** Gera resumos e relatórios do projeto com suporte multi-projeto/branch.

**Ferramentas (9):**

**Contexto (2 novas):**
- `set_project_context(project, branch)` - Define contexto global
- `get_project_context()` - Retorna contexto atual

**Status (7 atualizadas):**
- `get_project_status(include_details?, project?, branch?)` - Status geral
- `get_module_status(module, project?, branch?)` - Status de módulo
- `update_module_progress(module, progress, status?, notes?, project?, branch?)` - Atualiza progresso
- `get_next_steps(limit?, project?, branch?)` - Próximos passos
- `add_next_step(task, priority, estimate?, module?, project?, branch?)` - Adiciona passo
- `generate_report(type, audience, project?, branch?)` - Gera relatório
- `get_metrics(project?, branch?)` - Métricas do projeto

**Analytics (1 nova):**
- `list_all_projects()` - Lista todos os projetos e branches

**Estrutura:**
```
docs/resumo/
├── igo-journey/
│   ├── main/
│   │   └── progresso.json
│   └── feature-rooming/
│       └── progresso.json
└── sigaevento/
    └── main/
        └── progresso.json
```

**Tipos de Relatório:**
- executive - Resumo executivo
- technical - Detalhes técnicos
- onboarding - Para novos membros
- stakeholder - Para stakeholders

**Casos de Uso:**
- Gerar status reports por projeto/branch
- Comparar progresso entre branches
- Onboarding em projetos específicos
- Apresentações para stakeholders

---

### 7. docker-admin 🔴 DOCKER (necessário)
**Modo:** Docker container
**Container:** `igo-docker-admin`
**Diretório:** `mcp-servers/docker-admin/`

**Descrição:** Gerenciador de infraestrutura Docker e MCPs.

**Por que Docker:** Precisa acessar Docker daemon para gerenciar containers.

**Ferramentas:**
- `check_docker_status()` - Verifica e inicia Docker
- `manage_mcps(action)` - Gerencia todos os MCPs
- `manage_mcp(name, action)` - Gerencia MCP específico
- `manage_api(action)` - Gerencia API do projeto
- `health_check()` - Verifica saúde e auto-corrige
- `get_logs(service, lines?)` - Obtém logs
- `auto_heal()` - Auto-healing completo
- `get_mcp_status()` - Status de containers
- `sync_mcp_config()` - Sincroniza .mcp.json
- `verify_mcp_config()` - Verifica sincronização
- `update_and_restart_mcps()` - Atualiza e reinicia

**Casos de Uso:**
- Auto-healing de containers
- Gerenciamento de infraestrutura
- Monitoramento de saúde

---

### 8. igo-openai-gateway 🟢 LOCAL
**Modo:** Python local (Windows)
**Diretório:** `mcp-servers/igo-openai-gateway/`
**Comando:** `python c:/GIT-RAFAEL/mcp-servers/igo-openai-gateway/server.py`

**Descrição:** Gateway para executar tarefas via OpenAI GPT-5.2 Responses API.

**Modelo:** gpt-5.2-2025-12-11

**Ferramentas (7):**

**Básicas:**
- `run_prompt(prompt, input, model?, reasoning?, verbosity?, max_tokens?)` - Executa prompt direto
- `run_agent(agent_name, task, model?, reasoning?, verbosity?, max_tokens?, include_context?)` - Executa agente

**Especializadas:**
- `list_available_agents(category?)` - Lista agentes por categoria
- `run_development_agent(agent, task, reasoning?, verbosity?, use_preambles?)` - Agente de dev
- `run_code_analysis(code, analysis_type, language?, reasoning?)` - Análise de código
- `run_architectural_review(description, context?, reasoning?)` - Revisão arquitetural
- `generate_tests(code, test_type, framework?, reasoning?)` - Geração de testes

**Parâmetros Avançados:**
- `reasoning_effort`: none, low, medium, high, xhigh
- `verbosity`: low, medium, high

**Configuração:**
- Requer `OPENAI_API_KEY` como variável de ambiente

**Casos de Uso:**
- Análises profundas com reasoning
- Revisões arquiteturais complexas
- Geração de testes automatizada
- Decisões técnicas com GPT-5.2

---

### 9. api-database-tester 🔴 DOCKER (necessário)
**Modo:** Docker container
**Container:** `igo-api-database-tester`
**Diretório:** `mcp-servers/api-database-tester/`

**Descrição:** Testa APIs remotas/locais e executa queries SQL.

**Por que Docker:** Precisa de ODBC Driver 18 for SQL Server (Linux-specific).

**Ferramentas:**
- `execute_http_request(url, method?, headers?, body?, timeout?)` - Requisição HTTP
- `execute_sql_query(query, connection_string, database_type, fetch_limit?)` - Query SQL
- `quick_api_test(endpoint, bearer_token?, method?)` - Teste rápido de API
- `get_table_schema(table, connection_string, database_type)` - Schema de tabela

**Bancos Suportados:**
- SQL Server (via ODBC Driver 18)
- PostgreSQL

**Casos de Uso:**
- Testar APIs em produção
- Executar queries SQL Server
- Consultar schemas de banco
- Validar endpoints

---

### 10. vuetify-uiux 🟢 LOCAL
**Modo:** Python local (Windows)
**Diretório:** `mcp-servers/vuetify-uiux/`
**Comando:** `python c:/GIT-RAFAEL/mcp-servers/vuetify-uiux/server.py`

**Descrição:** Consultor de design Vuetify 3 - componentes, layouts, cores e acessibilidade.

**Ferramentas (10):**
- `suggest_component(use_case)` - Sugere componentes
- `component_info(component)` - Informações detalhadas
- `layout_pattern(pattern)` - Padrões de layout
- `color_scheme(scheme?)` - Esquemas de cores
- `accessibility_guide(topic?)` - Guia WCAG
- `spacing_guide()` - Guia de espaçamento
- `typography_guide()` - Guia de tipografia
- `breakpoints_guide()` - Breakpoints responsivos
- `review_code(code)` - Análise de código Vue/Vuetify
- `design_tips(context)` - Dicas de design

**Componentes Documentados:** 38 (v-container, v-row, v-col, v-btn, v-data-table, etc)

**Casos de Uso:**
- Desenvolver interfaces Vuetify
- Verificar acessibilidade
- Escolher esquemas de cores
- Code review de componentes Vue

---

### 11. igo-memory (Original) - LEGADO
**Container:** `igo-memory-server-mcp-server-1`
**Status:** Legado - existia antes, mantido por compatibilidade

**Descrição:** MCP original do projeto para gerenciamento de memória.

**Nota:** Substituído pelo `memory-manager` com suporte multi-projeto.

---

## 🚀 Como Usar

### Configuração Local (Windows)

Os MCPs locais já estão configurados em `.mcp.json`:

```json
{
  "mcpServers": {
    "excel-server": {
      "command": "python",
      "args": ["c:/GIT-RAFAEL/mcp-servers/excel-server/server.py"]
    },
    "memory-manager": {
      "command": "python",
      "args": ["c:/GIT-RAFAEL/mcp-servers/memory-manager/server.py"]
    }
    // ... outros MCPs
  }
}
```

### Configuração Remota (SSH)

Para uso remoto via SSH, usar `docs/mcp.json`:

```json
{
  "mcpServers": {
    "memory-manager": {
      "command": "ssh",
      "args": ["rafael@15.15.255.9", "python", "/root/mcp-servers/memory-manager/server.py"]
    }
  }
}
```

### Uso no Claude Code

```
# MCPs Locais (rápidos)
Use memory-manager para configurar contexto igo-journey/main
Use agente-insights para capturar insight sobre nova feature
Use agente-resumo para gerar relatório executivo
Use vuetify-uiux para sugerir componentes de formulário

# MCPs Docker (quando necessário)
Use docker-admin para verificar saúde dos containers
Use api-database-tester para testar API de produção
```

### Sistema Multi-Projeto

```python
# Configurar contexto uma vez
memory-manager.set_project_context("igo-journey", "main")

# Usar em todas as chamadas seguintes (implícito)
memory-manager.save_context("Transfer", "completed", "...")
agente-insights.capture_insight("Nova ideia", "feature")
agente-resumo.update_module_progress("Transfer", 100)

# Override quando necessário
memory-manager.save_context(
    "Rooming", "active", "...",
    project="sigaevento",
    branch="develop"
)
```

## 📊 Comparação: Docker vs Local

| Aspecto | Docker | Local (Windows) |
|---------|--------|-----------------|
| Inicialização | ~2-5s | ~0.5s |
| RAM | ~100MB/container | ~30MB |
| Debugging | docker logs | print direto |
| Dependências | Isoladas | Compartilhadas (pip --user) |
| Portabilidade | Alta | Média |
| Depende de Docker Desktop | ✅ Sim | ❌ Não |

**Escolha Local para:**
- MCPs de dados (memory, insights, resumo)
- MCPs de utilitários (orchestrator, checklist, vuetify)
- Desenvolvimento local rápido

**Escolha Docker para:**
- Drivers específicos de SO (ODBC 18)
- Gerenciamento de containers (docker-admin)
- Produção/deploy

## 📚 Documentação Adicional

- [FASE-1-MULTI-PROJETO-STATUS.md](FASE-1-MULTI-PROJETO-STATUS.md) - Sistema multi-projeto/branch
- [GPT-5.2-FEATURES-IMPLEMENTADAS.md](GPT-5.2-FEATURES-IMPLEMENTADAS.md) - Recursos GPT-5.2
- [VUETIFY-UIUX-IMPLEMENTACAO.md](VUETIFY-UIUX-IMPLEMENTACAO.md) - Implementação Vuetify
- [SETUP.md](SETUP.md) - Guia de instalação
- [REORGANIZACAO.md](REORGANIZACAO.md) - Estrutura do projeto

## 🎯 Roadmap

### Fase 1 - Sistema Multi-Projeto ✅ COMPLETO
- [x] memory-manager com suporte multi-projeto/branch
- [x] agente-insights com suporte multi-projeto/branch
- [x] agente-resumo com suporte multi-projeto/branch
- [x] Migração para Python local (8 MCPs)
- [x] Contexto híbrido (global + override)
- [x] Ferramentas de comparação de branches

### Fase 2 - Orchestrator + Gateway Integration ⚠️ EM PROGRESSO
- [ ] Integração Orchestrator com igo-openai-gateway
- [ ] Gateway como "cérebro" para decisões inteligentes
- [ ] `ask_ai_to_decide` no orchestrator
- [ ] `decide_agent` no gateway
- [ ] GPT-5.2 reasoning para escolher agentes

### Fase 3 - Analytics & Cross-Project 📋 PLANEJADO
- [ ] Comparação cross-project
- [ ] Métricas agregadas da empresa
- [ ] Dashboards de progresso
- [ ] Padrões e insights automáticos

### Futuro 🔮
- [ ] API Gateway REST
- [ ] Dashboard Web
- [ ] Notificações e Alertas
- [ ] Backup Automático

## 💡 Dicas de Uso

1. **Configure contexto uma vez** - Use `set_project_context` e todas as chamadas seguintes usarão automaticamente
2. **Compare branches antes de merge** - Use `compare_branches` para ver diferenças
3. **Analytics cross-project** - Use `get_statistics(cross_project=true)` para visão da empresa
4. **Use GPT-5.2 para decisões complexas** - `run_architectural_review` com reasoning xhigh
5. **MCPs locais são mais rápidos** - Priorize uso local quando possível

## 🆘 Troubleshooting

### MCPs Locais (Python)

```bash
# Testar diretamente
cd memory-manager
python server.py

# Ver erros
python -c "from server import *; print(set_project_context('test', 'main'))"
```

### MCPs Docker

```bash
# Ver logs
docker logs igo-api-database-tester -f

# Reiniciar
docker-compose restart api-database-tester

# Rebuild
docker-compose build --no-cache api-database-tester
docker-compose up -d api-database-tester
```

### Auto-Healing

```
Use docker-admin para executar auto-healing completo
```

---

**Mantido por:** Claude Sonnet 4.5
**Última atualização:** 2026-01-26
