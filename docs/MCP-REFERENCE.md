# Referência Completa dos MCPs - I Go Journey

Este documento contém a documentação detalhada de todos os MCPs disponíveis.
Usado pelo igo-openai-gateway para auxiliar nas decisões e respostas.

---

## 1. agente-orchestrator

**Função:** Orquestração de agentes especializados

### Tools

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `list_agents` | Lista todos os agentes | `compact`: bool (default: False) |
| `ask_ai_to_decide` | Pede ajuda à IA para decidir agente | `user_request`: str, `project`: str, `branch`: str |
| `invoke_agent` | Invoca um agente específico | `agent_name`: str, `task`: str |
| `get_agent_docs` | Retorna docs de um agente | `agent_name`: str |
| `update_agent_memory` | Atualiza memória do sistema | `action`: str, `details`: str |

---

## 2. igo-openai-gateway

**Função:** Gateway GPT-5.2 para análise de código, arquitetura e decisões

### Tools

| Tool | Descrição | Parâmetros |
|------|-----------|------------|
| `run_prompt` | Executa prompt direto | `prompt`: str, `input_text`: str, `model`: str, `reasoning_effort`: str, `verbosity`: str |
| `run_agent` | Executa agente com GPT-5.2 | `agent_name`: str, `task`: str, `reasoning_effort`: str |
| `decide_agent` | Decide qual agente usar | `user_request`: str, `available_agents`: str, `project_context`: str |
| `run_code_analysis` | Analisa código | `code`: str, `analysis_type`: review\|refactor\|debug\|optimize\|security |
| `run_architectural_review` | Revisão arquitetural | `description`: str, `context`: str |
| `generate_tests` | Gera testes | `code`: str, `test_type`: unit\|integration\|e2e, `framework`: str |
| `run_development_agent` | Executa agente de dev | `agent_name`: str, `task`: str |

### Parâmetros Globais
- `reasoning_effort`: none, low, medium, high, xhigh
- `verbosity`: low, medium, high
- `model`: gpt-5.2-2025-12-11 (default)

---

## 3. vuetify-uiux

**Função:** Consultor de design Vuetify 3

### Tools e Parâmetros Válidos

| Tool | Parâmetro | Valores |
|------|-----------|---------|
| `suggest_component` | use_case | formulario, tabela, lista, card, navegacao, modal, alerta, loading, upload, dashboard |
| `component_info` | component | v-text-field, v-select, v-data-table, v-btn, v-card, v-dialog |
| `layout_pattern` | pattern | dashboard, form_page |
| `color_scheme` | scheme | professional_blue, modern_purple, dark_mode (ou vazio para todos) |
| `accessibility_guide` | topic | color_contrast, keyboard_navigation, screen_readers (ou vazio) |
| `design_tips` | context | mobile, formulario, dashboard, tabela, cor |
| `spacing_guide` | - | Sem parâmetros |
| `typography_guide` | - | Sem parâmetros |
| `breakpoints_guide` | - | Sem parâmetros |
| `review_code` | code | Código Vue/Vuetify para analisar |

---

## 4. api-database-tester

**Função:** Testes de API HTTP e queries SQL

### Tools

| Tool | Parâmetros |
|------|------------|
| `execute_http_request` | `url`: str, `method`: GET\|POST\|PUT\|DELETE\|PATCH, `headers`: JSON str, `body`: JSON str, `timeout`: int |
| `execute_sql_query` | `query`: str, `connection_string`: str, `database_type`: sqlserver\|postgresql, `fetch_limit`: int |
| `quick_api_test` | `endpoint`: str, `bearer_token`: str, `method`: str |
| `get_table_schema` | `table_name`: str, `connection_string`: str, `database_type`: str |

### Exemplos de Connection String
```
SQL Server: DRIVER={ODBC Driver 18 for SQL Server};SERVER=server;DATABASE=db;UID=user;PWD=pass
PostgreSQL: postgresql://user:pass@host:5432/dbname
```

---

## 5. lp-guardian

**Função:** Guardião do LP (fluxos, componentes, stores e validação de configs)

### Tools

| Tool | Parâmetros |
|------|------------|
| `explain_flow` | `nome_fluxo`: link_cripto\|rsvp\|chave\|optin\|cadastro_igo\|upload |
| `explain_component` | `nome_componente`: ModuloFormulario\|FormularioSistemaPadrao |
| `get_store_structure` | `nome_store`: mainStore\|formularioStore\|colaboradorStore\|eventoStore\|adminStore |
| `search_docs` | `query`: str, `limite`: int |
| `suggest_fix` | `descricao_erro`: str |
| `trace_data_flow` | `campo`: str |
| `validate_config` | `config_json`: str, `tipo_config`: lp_flow\|lp_formulario\|lp_conteudo |
| `check_compatibility` | `versao_flow`: str |

---

## 6. memory-manager

**Função:** Gerenciamento de contexto e memória do projeto

### Tools

| Tool | Parâmetros |
|------|------------|
| `set_project_context` | `project`: str, `branch`: str |
| `get_project_context` | - |
| `save_context` | `module`: str, `status`: completed\|in_progress\|pending, `details`: str |
| `load_context` | `project`: str, `branch`: str |
| `update_progress` | `task`: str, `status`: completed\|in_progress\|pending\|blocked, `notes`: str |
| `get_next_steps` | `project`: str, `branch`: str |
| `add_decision` | `decision`: str, `context`: str, `alternatives`: str, `chosen`: str, `reason`: str |
| `get_memory_summary` | `project`: str, `branch`: str, `include_all_branches`: bool |
| `compare_branches` | `project`: str, `branch_a`: str, `branch_b`: str |
| `list_all_projects` | - |

---

## 7. agente-insights

**Função:** Captura ideias, decisões e feedback de especialistas

### Tools e Parâmetros

| Tool | Parâmetros Principais |
|------|----------------------|
| `capture_insight` | `idea`: str, `insight_type`: feature\|bug\|improvement\|decision\|exploration, `complexity`: low\|medium\|high, `modules`: list |
| `get_insights` | `status`: captured\|analyzing\|approved\|rejected\|implemented, `insight_type`: str, `limit`: int |
| `update_insight_status` | `insight_id`: str, `new_status`: str, `notes`: str |
| `add_agent_feedback` | `insight_id`: str, `agent_name`: str, `feedback`: str, `recommendation`: str |
| `make_decision` | `insight_id`: str, `decision_status`: approved\|rejected\|deferred, `rationale`: str, `priority`: critical\|high\|medium\|low |
| `get_statistics` | `cross_project`: bool |

---

## 8. agente-resumo

**Função:** Status do projeto, métricas e relatórios

### Tools

| Tool | Parâmetros |
|------|------------|
| `get_project_status` | `project`: str, `branch`: str, `include_details`: bool |
| `get_module_status` | `module_name`: str |
| `update_module_progress` | `module_name`: str, `progress_pct`: int, `status`: str, `notes`: str |
| `get_next_steps` | `limit`: int |
| `add_next_step` | `task`: str, `priority`: high\|medium\|low, `module`: str, `estimate`: str |
| `generate_report` | `report_type`: executive\|detailed, `audience`: team\|management |
| `get_metrics` | - |

---

## 9. checklist-validator

**Função:** Validação e gerenciamento de checklists

### Tools

| Tool | Parâmetros |
|------|------------|
| `validate_checklist` | `checklist_path`: str |
| `mark_completed` | `checklist_path`: str, `task_pattern`: str |
| `get_pending_tasks` | `checklist_path`: str (ou None para todos) |
| `list_checklists` | - |
| `create_checklist` | `name`: str, `title`: str, `sections`: JSON str |

---

## 10. excel-server

**Função:** Leitura e manipulação de arquivos Excel

### Tools

| Tool | Parâmetros |
|------|------------|
| `read_excel_tabs` | `file_path`: str (caminho completo) |
| `read_excel_with_formulas` | `file_path`: str, `sheet_name`: str |
| `get_excel_metadata` | `file_path`: str |

**IMPORTANTE:** Este MCP precisa rodar LOCAL se for ler arquivos locais.

---

## Mapa de Uso Rápido

| Necessidade | MCP | Tool |
|-------------|-----|------|
| Criar tela Vue | vuetify-uiux | suggest_component, layout_pattern |
| Testar API | api-database-tester | quick_api_test, execute_http_request |
| Query SQL | api-database-tester | execute_sql_query |
| Salvar decisão | memory-manager | add_decision |
| Capturar ideia | agente-insights | capture_insight |
| Status do projeto | agente-resumo | get_project_status |
| Analisar código | igo-openai-gateway | run_code_analysis |
| Decidir agente | agente-orchestrator | ask_ai_to_decide |
| Ler Excel | excel-server | read_excel_tabs |
| Validar checklist | checklist-validator | validate_checklist |
