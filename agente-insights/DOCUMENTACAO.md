# 📚 Documentação do Agente de Insights

## Onde Encontrar Informações

### Memória do Projeto

Sempre consulte antes de processar insights:

```bash
projeto-claude/06-MEMORIA-AGENTE/
├── contexto-atual.md         # Estado atual do projeto
├── proximos-passos.md         # Roadmap e prioridades
├── decisoes-tecnicas.md       # ADRs e decisões importantes
└── ultimas-acoes.md          # Histórico de ações
```

### Prompts de Agentes

Para consultar especialistas:

```bash
projeto-claude/01-AGENTES/
├── agente-arquiteto/PROMPT.md
├── agente-backend/PROMPT.md
├── agente-design-ux/PROMPT.md
├── agente-transfer/PROMPT.md
├── agente-rooming-list/PROMPT.md
├── agente-checkin/PROMPT.md
├── agente-seguranca/PROMPT.md
├── agente-admin/PROMPT.md
├── agente-rsvp/PROMPT.md
├── agente-credenciamento/PROMPT.md
└── agente-resumo/PROMPT.md
```

### Arquitetura e Stack

```bash
projeto-claude/00-OVERVIEW/
├── ARQUITETURA_GERAL.md      # Arquitetura do sistema
├── STACK_TECNICA.md          # Tecnologias usadas
└── ROADMAP.md                # Roadmap macro
```

### Checklists

```bash
projeto-claude/05-CHECKLISTS/
├── mvp.md                     # Checklist MVP geral
├── transfer.md               # Checklist Transfer
├── rooming-list.md           # Checklist Rooming
├── checkin.md                # Checklist Check-in
└── backend.md                # Checklist Backend
```

### Documentação de Módulos

```bash
projeto-claude/02-MODULOS/
├── transfer/
├── rooming-list/
├── checkin-in-loco/
├── admin/
├── rsvp/
└── credenciamento/
```

### API

```bash
projeto-claude/03-API/
├── endpoints/                 # Documentação de endpoints
├── payloads/                 # Exemplos de payloads
└── documentacao/             # Manuais da API
```

### Infraestrutura

```bash
projeto-claude/04-INFRAESTRUTURA/
├── FERRAMENTAS_NECESSARIAS.md
├── mcps/                      # MCPs customizados
├── docker/                   # Docker configs
└── ci-cd/                    # CI/CD pipelines
```

---

## Arquivos Que Você Mantém

### Insights Capturados

```bash
projeto-claude/01-AGENTES/agente-insights/INSIGHTS_CAPTURADOS.md
```

**Conteúdo:**
- Todos os insights registrados
- Status de cada insight
- Decisões tomadas
- Histórico completo

**Atualização:**
- Sempre que capturar novo insight
- Quando status de insight mudar
- Ao implementar insight aprovado

### Decisões Técnicas

```bash
projeto-claude/06-MEMORIA-AGENTE/decisoes-tecnicas.md
```

**Conteúdo:**
- ADRs (Architecture Decision Records)
- Decisões importantes
- Justificativas técnicas
- Impacto das decisões

**Atualização:**
- Quando decisão arquitetural for tomada
- Quando tecnologia for escolhida
- Quando padrão for definido

### Próximos Passos

```bash
projeto-claude/06-MEMORIA-AGENTE/proximos-passos.md
```

**Conteúdo:**
- Tarefas priorizadas
- Roadmap atualizado
- Dependências
- Agentes responsáveis

**Atualização:**
- Quando insights afetarem prioridades
- Quando tarefas forem completadas
- Quando roadmap mudar

### Contexto Atual

```bash
projeto-claude/06-MEMORIA-AGENTE/contexto-atual.md
```

**Conteúdo:**
- Fase do projeto
- Progresso por módulo
- Status geral
- Bloqueadores

**Atualização:**
- Quando módulo atingir novo marco
- Quando bloqueador for identificado/resolvido
- Quando fase do projeto mudar

---

## Referências Rápidas

### Comandos Git

```bash
# Ver status
git status

# Ver últimos commits
git log --oneline -10

# Ver arquivos modificados
git diff --name-only
```

### MCPs Disponíveis

```bash
# Excel Server (ativo)
cat .mcp.json

# Futuro: Agente Orchestrator
# Futuro: Memory Manager
# Futuro: Checklist Validator
```

### Estrutura do Código Fonte

```bash
src/
├── views/              # Telas principais
│   ├── TransferView.vue
│   ├── HospedagemView.vue
│   └── CheckInView.vue (planejado)
├── components/         # Componentes reutilizáveis
├── stores/            # Pinia stores
└── utils/             # Helpers
```

---

## Templates de Documentos

### Template de Insight

```markdown
## [YYYY-MM-DD HH:mm] - [Título]

**ID:** INS-NNNN
**Tipo:** [Feature/Bug/Improvement/Decision/Exploration]
**Complexidade:** [Baixa/Média/Alta]
**Status:** [📝/🔍/✅/❌/🚀]

**Descrição:**
[O que foi sugerido]

**Módulos Impactados:**
- [Lista]

**Agentes Consultados:**
- [Lista com feedback]

**Análise de Impacto:**
- Esforço: [estimativa]
- Risco: [nível]
- Valor: [nível]
- Prioridade: [nível]

**Decisão:**
[Status e justificativa]

**Próximos Passos:**
1. [ ] [Ação - Agente]

**Referências:**
- [Links]
```

### Template de ADR

```markdown
## ADR-NNN: [Título da Decisão]

**Data:** YYYY-MM-DD
**Status:** [Proposto/Aceito/Rejeitado/Depreciado]
**Decisores:** [Agentes consultados]

### Contexto
[Por que precisamos dessa decisão?]

### Decisão
[O que foi decidido?]

### Alternativas Consideradas
1. [Opção A] - [Prós/Contras]
2. [Opção B] - [Prós/Contras]

### Consequências
**Positivas:**
- [Lista]

**Negativas:**
- [Lista]

**Riscos:**
- [Lista]

### Implementação
[Como será implementado]

### Referências
- [Links]
```

---

## Integração com Agente de Resumo

O Agente de Resumo lê os mesmos arquivos para gerar relatórios:

```
Agente Insights (Escrita)  →  Memória  ←  Agente Resumo (Leitura)
```

**Fluxo:**
1. Insights captura e documenta decisão
2. Insights atualiza memória do projeto
3. Resumo lê memória atualizada
4. Resumo gera relatórios atualizados

---

## Links Externos

### Documentação Original

```bash
docs/
├── ESCOPO_COMPLETO_IGO_EXPERIENCE.md
├── ESPECIFICACAO_COMPLETA_IGO_EXPERIENCE.md
├── modulo_rooming_list_regras.md
└── anexos-email-igo-experience/
    └── [mockups e PDFs]
```

### Repositórios

- **Principal:** `/Users/rafamacpro/Projetos/GIT/Transfer-logistica`
- **Projeto Claude:** `/Users/rafamacpro/Projetos/GIT/Transfer-logistica/projeto-claude`

---

**Mantenha a documentação sempre atualizada e facilmente acessível!**
