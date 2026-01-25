# Lista Completa de MCPs - I GO Experience

## 📋 Visão Geral

Este projeto possui **8 MCPs** (Model Context Protocol servers) ativos que fornecem ferramentas especializadas para o desenvolvimento do sistema I GO Experience.

## 🔧 MCPs Disponíveis

### 1. igo-memory (Original)
**Container:** `igo-memory-server-mcp-server-1`
**Status:** Legado - já existia antes da implementação atual

**Descrição:** MCP original do projeto para gerenciamento de memória.

---

### 2. excel-server
**Container:** `igo-excel-server`
**Diretório:** `api/mcp-servers/excel-server/`

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

### 3. agente-orchestrator
**Container:** `igo-agente-orchestrator`
**Diretório:** `api/mcp-servers/agente-orchestrator/`

**Descrição:** Orquestrador de agentes especializados do projeto.

**Ferramentas:**
- `list_agents()` - Lista todos os agentes disponíveis
- `invoke_agent()` - Invoca um agente específico com uma tarefa
- `get_agent_docs()` - Retorna documentação completa de um agente
- `update_agent_memory()` - Atualiza memória do sistema de agentes

**Agentes Disponíveis:**
- agente-rooming-list
- agente-transfer
- agente-checkin
- agente-backend
- agente-tracking
- agente-credenciamento
- agente-rsvp
- agente-arquiteto-igo
- agente-frontend-igo
- agente-integracoes-igo
- agente-qa-testes
- agente-comercial-igo
- agente-marketing-igo
- agente-diretoria-igo
- agente-operacao-igo
- agente-solucoes
- agente-analytics-kpi

---

### 4. memory-manager
**Container:** `igo-memory-manager`
**Diretório:** `api/mcp-servers/memory-manager/`

**Descrição:** Gerenciador de contexto e memória do projeto.

**Ferramentas:**
- `save_context()` - Salva contexto de um módulo
- `load_context()` - Carrega contexto completo do projeto
- `update_progress()` - Atualiza progresso de tarefas
- `get_next_steps()` - Retorna próximos passos planejados
- `add_decision()` - Registra decisões técnicas (ADR)
- `get_memory_summary()` - Resumo completo da memória

**Casos de Uso:**
- Manter continuidade entre sessões
- Registrar decisões arquiteturais
- Planejar próximos passos

---

### 5. checklist-validator
**Container:** `igo-checklist-validator`
**Diretório:** `api/mcp-servers/checklist-validator/`

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

### 6. agente-insights
**Container:** `igo-agente-insights`
**Diretório:** `api/mcp-servers/agente-insights/`

**Descrição:** Captura e gerencia insights e sugestões do usuário.

**Ferramentas:**
- `capture_insight()` - Captura nova ideia/sugestão
- `get_insights()` - Lista insights com filtros
- `update_insight_status()` - Atualiza status de um insight
- `add_agent_feedback()` - Adiciona feedback de agente especialista
- `make_decision()` - Registra decisão sobre insight
- `get_statistics()` - Estatísticas dos insights

**Tipos de Insight:**
- feature - Nova funcionalidade
- bug - Correção de bug
- improvement - Melhoria
- decision - Decisão técnica
- exploration - Exploração/investigação

**Casos de Uso:**
- Capturar ideias durante desenvolvimento
- Consultar agentes especializados sobre sugestões
- Priorizar e decidir sobre implementações

---

### 7. agente-resumo
**Container:** `igo-agente-resumo`
**Diretório:** `api/mcp-servers/agente-resumo/`

**Descrição:** Gera resumos e relatórios do projeto.

**Ferramentas:**
- `get_project_status()` - Status geral do projeto
- `get_module_status()` - Status de módulo específico
- `update_module_progress()` - Atualiza progresso de módulo
- `get_next_steps()` - Lista próximos passos priorizados
- `add_next_step()` - Adiciona novo passo
- `generate_report()` - Gera relatório formatado
- `get_metrics()` - Métricas do projeto

**Tipos de Relatório:**
- executive - Resumo executivo
- technical - Detalhes técnicos
- onboarding - Para novos membros
- stakeholder - Para stakeholders

**Casos de Uso:**
- Gerar status reports
- Onboarding de novos desenvolvedores
- Apresentações para stakeholders

---

### 8. docker-admin
**Container:** `igo-docker-admin`
**Diretório:** `api/mcp-servers/docker-admin/`

**Descrição:** Gerenciador de infraestrutura Docker e MCPs.

**Ferramentas:**
- `check_docker_status()` - Verifica e inicia Docker se necessário
- `manage_mcps()` - Gerencia todos os MCPs (start/stop/restart/rebuild/status)
- `manage_mcp()` - Gerencia MCP específico
- `manage_api()` - Gerencia API do projeto
- `health_check()` - Verifica saúde e auto-corrige problemas
- `get_logs()` - Obtém logs de serviço
- `auto_heal()` - Auto-healing completo
- `get_mcp_status()` - Status de containers e configuração
- `sync_mcp_config()` - Sincroniza .mcp.json com containers
- `verify_mcp_config()` - Verifica sincronização
- `update_and_restart_mcps()` - Atualiza e reinicia todos os MCPs

**Casos de Uso:**
- Auto-healing de containers
- Gerenciamento de infraestrutura
- Monitoramento de saúde
- Atualização de MCPs

---

## 🚀 Como Usar

### Testar Todos os MCPs

```bash
cd /Users/rafamacpro/Projetos/GIT/Transfer-logistica/api/mcp-servers/docs
./test-mcps.sh
```

### Testar MCP Específico

```bash
docker exec -i igo-excel-server python server.py <<< '{"method":"tools/list"}'
```

### No Claude Desktop

Após configurar, você pode usar os MCPs naturalmente:

```
Use excel-server para ler o arquivo exemplo.xlsx
Use agente-orchestrator para listar agentes disponíveis
Use memory-manager para carregar o contexto atual
Use checklist-validator para validar o checklist mvp.md
Use agente-insights para capturar esta ideia: [sua ideia]
Use agente-resumo para gerar um relatório executivo
Use docker-admin para verificar o status dos containers
```

## 📊 Status dos Containers

Verificar se todos estão rodando:

```bash
cd /Users/rafamacpro/Projetos/GIT/Transfer-logistica/api/mcp-servers
docker-compose ps
```

Deve mostrar 7 containers UP:
- ✅ igo-excel-server
- ✅ igo-agente-orchestrator
- ✅ igo-memory-manager
- ✅ igo-checklist-validator
- ✅ igo-agente-insights
- ✅ igo-agente-resumo
- ✅ igo-docker-admin

## 🔄 Gerenciamento

### Iniciar Todos

```bash
cd /Users/rafamacpro/Projetos/GIT/Transfer-logistica/api/mcp-servers
docker-compose up -d
```

### Parar Todos

```bash
docker-compose down
```

### Rebuild Completo

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Ver Logs

```bash
# Todos os logs
docker-compose logs -f

# MCP específico
docker logs -f igo-excel-server
```

## 📚 Documentação Adicional

- [SETUP.md](SETUP.md) - Guia completo de instalação
- [REORGANIZACAO.md](REORGANIZACAO.md) - Estrutura e arquitetura
- [test-mcps.sh](test-mcps.sh) - Script de testes
- [install-claude-config.sh](install-claude-config.sh) - Instalador de configuração

## 🎯 Roadmap

### Implementados ✅
- [x] Excel Server
- [x] Agente Orchestrator
- [x] Memory Manager
- [x] Checklist Validator
- [x] Agente Insights
- [x] Agente Resumo
- [x] Docker Admin

### Planejados 📋
- [ ] API Gateway (consolidação de MCPs)
- [ ] Dashboard Web
- [ ] Notificações e Alertas
- [ ] Backup Automático
- [ ] Métricas e Analytics

## 💡 Dicas de Uso

1. **Use docker-admin** para gerenciar a infraestrutura sem sair do Claude
2. **Use agente-insights** para capturar ideias durante o desenvolvimento
3. **Use agente-resumo** para gerar relatórios periódicos
4. **Use memory-manager** para manter contexto entre sessões
5. **Use checklist-validator** para acompanhar progresso do MVP

## 🆘 Troubleshooting

Se algum MCP não estiver funcionando:

```bash
# 1. Verificar status
docker-compose ps

# 2. Ver logs
docker logs igo-[nome-do-mcp]

# 3. Reiniciar
docker-compose restart [nome-do-servico]

# 4. Rebuild
docker-compose build --no-cache [nome-do-servico]
docker-compose up -d [nome-do-servico]
```

Ou use o **docker-admin**:

```
Use docker-admin para executar auto-healing completo
```
