# Índice Completo de Agentes - I Go Journey

## Agentes de Desenvolvimento (6)

| Agente | Especialidade | Quando Usar |
|--------|--------------|-------------|
| **agente-arquiteto-igo** | Arquitetura, decisões técnicas, escalabilidade | Decisões de design, novos módulos, trade-offs |
| **agente-frontend-igo** | Vue 3, Vuetify 3, Composition API, UX | Telas, componentes, fluxos de usuário |
| **agente-backend** | .NET 9, C#, EF9, APIs REST, SQL Server/PostgreSQL | Endpoints, queries, services, performance |
| **agente-qa-testes** | Testes, qualidade, cenários críticos | Planos de teste, edge cases, validações |
| **agente-integracoes-igo** | APIs externas, webhooks, sync | Integrações com terceiros |
| **agente-solucoes** | Problemas complexos, debugging | Bugs difíceis, análise de causa raiz |
| **agente-guardiao** | LP Guardian | Fluxos LP, componentes, stores, validação de configs |

## Agentes de Módulo (6)

| Agente | Módulo | Responsabilidade |
|--------|--------|-----------------|
| **agente-rooming-list** | Hospedagem | Alocação de quartos, hotéis, reservas |
| **agente-transfer** | Logística | Transporte, rotas, veículos |
| **agente-checkin** | Credenciamento | Check-in, NFC, presença |
| **agente-rsvp** | Confirmações | Convites, confirmações, respostas |
| **agente-tracking** | Rastreamento | Localização, histórico de participantes |
| **agente-credenciamento** | Credenciamento | Crachás, acesso, identificação |

## Agentes de Negócio (5)

| Agente | Área | Responsabilidade |
|--------|------|-----------------|
| **agente-analytics-kpi** | Dados | Métricas, dashboards, KPIs |
| **agente-comercial-igo** | Vendas | Propostas, clientes, contratos |
| **agente-diretoria-igo** | Estratégia | Decisões executivas, prioridades |
| **agente-marketing-igo** | Marketing | Comunicação, campanhas |
| **agente-operacao-igo** | Operação | Eventos ao vivo, execução |

---

## MCPs de Suporte (10)

| MCP | Função | Principal Uso |
|-----|--------|--------------|
| **igo-openai-gateway** | LLM auxiliar (GPT-5.2) | Análise de código, decisões, testes |
| **vuetify-uiux** | Design Vuetify 3 | Componentes, layouts, cores |
| **api-database-tester** | Testes de API/SQL | HTTP requests, queries |
| **memory-manager** | Memória do projeto | Contexto, decisões (ADR) |
| **agente-insights** | Ideias e decisões | Captura insights, feedback |
| **agente-resumo** | Status e relatórios | Progresso, métricas |
| **checklist-validator** | Checklists | Validação pré-evento |
| **excel-server** | Leitura Excel | Planilhas, importação |
| **docker-admin** | Infraestrutura | Containers Docker |
| **lp-guardian** | Guardião LP | Fluxos, componentes, validação de configs |

---

## Parâmetros Válidos dos MCPs

### vuetify-uiux
```
color_scheme: professional_blue | modern_purple | dark_mode
accessibility_guide: color_contrast | keyboard_navigation | screen_readers
layout_pattern: dashboard | form_page
design_tips: mobile | formulario | dashboard | tabela | cor
suggest_component: formulario | tabela | lista | card | modal | dashboard
component_info: v-text-field | v-select | v-data-table | v-btn | v-card | v-dialog
```

### api-database-tester
```
database_type: sqlserver | postgresql
method: GET | POST | PUT | DELETE | PATCH
```

### memory-manager
```
status: completed | in_progress | pending | blocked
```

### agente-insights
```
insight_type: feature | bug | improvement | decision | exploration
complexity: low | medium | high
decision_status: approved | rejected | deferred
priority: critical | high | medium | low
```

### igo-openai-gateway
```
reasoning_effort: none | low | medium | high | xhigh
verbosity: low | medium | high
analysis_type: review | refactor | debug | optimize | security
test_type: unit | integration | e2e
```

---

## Stack Técnica

### Backend
- .NET 9 + C# 13
- Entity Framework 9
- SQL Server (prod) / PostgreSQL (alt)
- SignalR, JWT, Swagger

### Frontend
- Vue 3 + Composition API + `<script setup lang="ts">`
- Vuetify 3
- TypeScript strict
- Pinia + Vite

---

## Fluxo de Decisão

```
Requisição → Orquestrador → igo-openai-gateway (decide_agent)
                                    ↓
                            Agente recomendado
                                    ↓
                            Execução da tarefa
                                    ↓
                            memory-manager (salva contexto)
```
