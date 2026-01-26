# Guidelines para Desenvolvimento com MCPs

## Visão Geral

Este projeto utiliza um sistema de **Model Context Protocol (MCP) Servers** para prover funcionalidades especializadas aos assistentes de IA. Todos os MCPs rodam via Docker e estão disponíveis para VSCode, Cursor, Claude Code e Codex.

## MCPs Disponíveis

### 1. 📊 excel-server
**Container:** `igo-excel-server`

Leitura e processamento de arquivos Excel.

**Ferramentas:**
- `read_excel_tabs` - Lê todas as abas de um arquivo Excel
- `read_excel_with_formulas` - Lê Excel preservando fórmulas
- `get_excel_metadata` - Retorna metadados do arquivo

**Quando usar:**
- Processar arquivos Excel (rooming lists, relatórios)
- Extrair dados de planilhas
- Validar estrutura de Excel

---

### 2. 🎯 agente-orchestrator
**Container:** `igo-agente-orchestrator`

Orquestra e invoca agentes especializados do projeto.

**Ferramentas:**
- `list_agents` - Lista todos os agentes disponíveis
- `invoke_agent` - Invoca um agente específico com uma tarefa
- `get_agent_docs` - Retorna documentação de um agente
- `update_agent_memory` - Atualiza memória do sistema

**Quando usar:**
- Precisar de expertise específica (frontend, backend, negócio)
- Delegar tarefas a agentes especializados
- Consultar documentação de agentes

**Agentes Disponíveis:**
- **Negócio:** agente-comercial-igo, agente-diretoria-igo, agente-marketing-igo, agente-operacao-igo
- **Técnicos:** agente-arquiteto-igo, agente-backend, agente-frontend-igo, agente-qa-testes
- **Módulos:** agente-transfer, agente-rooming-list, agente-checkin, agente-rsvp, agente-credenciamento, agente-tracking, agente-analytics-kpi

---

### 3. 🧠 memory-manager
**Container:** `igo-memory-manager`

Gerencia contexto e memória do projeto através de sessões de trabalho.

**Ferramentas:**
- `save_context` - Salva contexto de um módulo
- `load_context` - Carrega contexto completo do projeto
- `update_progress` - Atualiza progresso de tarefas
- `get_next_steps` - Retorna próximos passos planejados
- `add_decision` - Registra decisões técnicas (ADR)
- `get_memory_summary` - Resumo de toda memória

**Quando usar:**
- Início de uma nova sessão de trabalho
- Registrar progresso e decisões
- Consultar histórico e próximos passos

---

### 4. ✅ checklist-validator
**Container:** `igo-checklist-validator`

Valida e gerencia checklists de desenvolvimento.

**Ferramentas:**
- `validate_checklist` - Valida um checklist
- `mark_completed` - Marca tarefa como completa
- `get_pending_tasks` - Lista tarefas pendentes
- `list_checklists` - Lista todos os checklists
- `create_checklist` - Cria novo checklist

**Quando usar:**
- Validar progresso de implementação
- Criar checklists para novas features
- Marcar tarefas completadas

---

### 5. 💡 agente-insights
**Container:** `igo-agente-insights`

Captura, analisa e gerencia insights e sugestões do usuário.

**Ferramentas:**
- `capture_insight` - Captura nova ideia/sugestão
- `get_insights` - Lista insights com filtros
- `update_insight_status` - Atualiza status de insight
- `add_agent_feedback` - Adiciona feedback de agente especialista
- `make_decision` - Registra decisão sobre insight
- `get_statistics` - Estatísticas dos insights

**Quando usar:**
- Usuário sugere melhorias ou features
- Capturar ideias durante desenvolvimento
- Analisar viabilidade de sugestões

---

### 6. 📈 agente-resumo
**Container:** `igo-agente-resumo`

Fornece resumos e status do projeto.

**Ferramentas:**
- `get_project_status` - Status geral do projeto
- `get_module_status` - Status de módulo específico
- `update_module_progress` - Atualiza progresso de módulo
- `get_next_steps` - Próximos passos priorizados
- `add_next_step` - Adiciona próximo passo
- `generate_report` - Gera relatórios formatados
- `get_metrics` - Métricas do projeto

**Quando usar:**
- Onboarding de novos membros
- Gerar relatórios para stakeholders
- Consultar status de módulos

---

### 7. 🐳 docker-admin
**Container:** `igo-docker-admin`

Administração completa de containers Docker e MCPs.

**Ferramentas:**
- `check_docker_status` - Verifica se Docker está rodando
- `manage_mcps` - Gerencia todos MCPs (start/stop/restart)
- `manage_mcp` - Gerencia MCP específico
- `manage_api` - Gerencia API do projeto
- `health_check` - Verifica saúde completa
- `auto_heal` - Auto-correção de problemas
- `get_mcp_status` - Status de containers e config
- `sync_mcp_config` - Sincroniza .mcp.json com containers

**Quando usar:**
- Problemas com containers
- Iniciar/parar MCPs
- Verificar saúde do sistema
- Auto-healing de infraestrutura

---

### 8. 🤖 igo-openai-gateway
**Container:** `igo-openai-gateway`

Gateway para execução de prompts e agentes usando GPT-5.2 com reasoning.

**Ferramentas:**
- `run_prompt` - Executa prompt direto via OpenAI
- `run_agent` - Executa agente com contexto do projeto
- `list_available_agents` - Lista agentes por categoria
- `run_development_agent` - Executa agente de desenvolvimento
- `run_code_analysis` - Análise de código com reasoning alto
- `run_architectural_review` - Revisão arquitetural (reasoning xhigh)
- `generate_tests` - Gera testes automaticamente

**Quando usar:**
- Análises complexas que requerem reasoning profundo
- Revisões arquiteturais
- Geração de testes
- Consultar agentes sem context completo do Claude

---

## Fluxo de Trabalho Recomendado

### Início de Sessão
1. **Carregar contexto:** `memory-manager.load_context`
2. **Verificar saúde:** `docker-admin.health_check`
3. **Consultar próximos passos:** `agente-resumo.get_next_steps`

### Durante Desenvolvimento
1. **Usar agentes especializados** quando precisar de expertise
2. **Registrar decisões** importantes via `memory-manager.add_decision`
3. **Atualizar progresso** via `memory-manager.update_progress`

### Fim de Sessão
1. **Salvar contexto** de módulos trabalhados
2. **Marcar tarefas** completadas nos checklists
3. **Registrar próximos passos** via `agente-resumo.add_next_step`

---

## Boas Práticas

### 1. Sempre Verifique Docker
Antes de usar qualquer MCP, verifique se o Docker está rodando:
```
docker-admin.check_docker_status
```

### 2. Use Auto-Healing
Se encontrar problemas, use primeiro:
```
docker-admin.auto_heal
```

### 3. Contexto é Rei
- Sempre carregue contexto no início: `memory-manager.load_context`
- Sempre salve contexto no final: `memory-manager.save_context`

### 4. Delegue para Especialistas
Não tente fazer tudo sozinho. Use `agente-orchestrator.invoke_agent` para:
- Decisões arquiteturais → agente-arquiteto-igo
- Código frontend → agente-frontend-igo
- Código backend → agente-backend
- Testes → agente-qa-testes
- Regras de negócio → agente-comercial-igo, agente-operacao-igo

### 5. Capture Insights
Sempre que o usuário sugerir algo:
```
agente-insights.capture_insight
```

### 6. Documente Decisões
Use ADRs para decisões técnicas importantes:
```
memory-manager.add_decision
```

---

## Resolução de Problemas

### MCPs não respondem
```
docker-admin.auto_heal
```

### Container específico com problema
```
docker-admin.manage_mcp("nome-do-mcp", "restart")
```

### Verificar logs
```
docker-admin.get_logs("nome-do-container")
```

### Sincronizar configuração
```
docker-admin.sync_mcp_config
```

---

## Estrutura do Projeto

```
mcp-servers/
├── .mcp.json                    # Configuração MCP para Claude Code
├── .claude/settings.local.json  # Permissões Claude Code
├── docker-compose.yml           # Orquestração dos containers
├── docs/                        # Documentação
│   ├── agentes/                 # Prompts dos agentes especializados
│   └── memoria/                 # Memória do projeto
├── excel-server/                # MCP de Excel
├── agente-orchestrator/         # MCP Orquestrador
├── memory-manager/              # MCP de Memória
├── checklist-validator/         # MCP de Checklists
├── agente-insights/             # MCP de Insights
├── agente-resumo/               # MCP de Resumos
├── docker-admin/                # MCP de Docker
└── igo-openai-gateway/          # MCP Gateway OpenAI
```

---

## Referências

- [LISTA_MCPS.md](docs/LISTA_MCPS.md) - Lista completa de MCPs
- [DOCKER-ADMIN.md](docs/DOCKER-ADMIN.md) - Documentação Docker Admin
- [ORQUESTRADOR.md](docs/ORQUESTRADOR.md) - Documentação Orquestrador
- [RESUMO_EXECUTIVO.md](docs/RESUMO_EXECUTIVO.md) - Visão executiva do projeto
