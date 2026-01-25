# 🚀 Guia de Uso Rápido - Sistema de Agentes Inteligentes

**Versão:** 1.0.0
**Data:** 2026-01-25

---

## ⚡ Início Instantâneo

### Passo 1: Escolha Seu Objetivo

```
💭 Quero saber status → "📊 Status"
💡 Tenho uma ideia → "💡 [sua ideia]"
🔧 Preciso implementar → "⚡ Implementar [feature]"
❓ Tenho dúvida → "Como funciona [X]?"
```

### Passo 2: Fale Naturalmente

Não precisa de comandos especiais! Exemplos:

```
✅ "Como tá o projeto?"
✅ "Adicionar busca no Transfer"
✅ "Corrige o bug do Excel"
✅ "Me explica como funciona o Rooming"
✅ "Quais os próximos passos?"
✅ "Vale a pena usar GraphQL?"
```

---

## 🎯 3 Agentes Principais

### 1. 📊 Agente de Resumo

**Quando usar:** Quer saber "como está"

**Atalhos:**
```
📊 Status              → Status geral
📊 Status Transfer     → Status de módulo
📋 Próximos           → Roadmap
📜 Histórico          → Últimas ações
📈 Métricas           → Estatísticas
```

**Exemplo:**
```
Você: "📊 Status"

Resumo:
┌──────────────────────────────────┐
│ I GO Experience - Status Geral   │
├──────────────────────────────────┤
│ Fase: MVP Desenvolvimento (65%)  │
│ Transfer: 90% ✅                 │
│ Rooming: 100% ✅                 │
│ Backend: 0% 🔴 (próximo)         │
│ Check-in: 0% 🔴                  │
└──────────────────────────────────┘
```

### 2. 💡 Agente de Insights

**Quando usar:** Tem ideia ou precisa decidir

**Atalhos:**
```
💡 [ideia]                → Captura simples
🔍 Analisar: [ideia]     → Análise profunda
🎯 Implementar: [grande] → Orquestração
❓ Feedback sobre [X]    → Consultar especialistas
```

**Exemplo:**
```
Você: "💡 Adicionar filtro de busca no Transfer"

Insights:
✅ Insight capturado!
📁 Tipo: Feature
🎯 Módulo: Transfer
⚡ Complexidade: Baixa

Consultando agentes...
✓ Transfer: Implementação fácil
✓ Design/UX: Sugeriu posição

✅ Aprovado - Prioridade Média
Estimativa: 30min

Próximos passos:
1. [ ] Design mockup do filtro
2. [ ] Implementar lógica de busca
```

### 3. 🔧 Agentes Especializados

**Quando usar:** Implementar algo específico

**Agentes disponíveis:**
- 🏗️ Arquiteto (decisões técnicas)
- 🔧 Backend (API, endpoints)
- 🎨 Design/UX (interface)
- 📱 Transfer (módulo Transfer)
- 🏨 Rooming (módulo Rooming)
- ✅ Check-in (módulo Check-in)

**Exemplo:**
```
Você: "⚡ Implementar filtro de busca"

→ Agente Transfer ativa automaticamente
→ Implementa código
→ Atualiza memória
→ Testa funcionalidade
```

---

## 🔄 Fluxo Completo de Trabalho

### Manhã: Planejamento

```bash
1. "📊 Status"
   → Ver estado geral

2. "📋 Próximos passos"
   → Ver tarefas prioritárias

3. "📊 Status [módulo que vou trabalhar]"
   → Detalhes do módulo
```

### Durante o Dia: Desenvolvimento

```bash
4. "⚡ Implementar [tarefa escolhida]"
   → Agente específico executa

5. "💡 [ideias que surgirem]"
   → Insights captura para depois

6. "❓ Como funciona [X]?"
   → Agente especialista explica
```

### Fim do Dia: Retrospectiva

```bash
7. "📜 O que fiz hoje?"
   → Histórico de ações

8. "📊 Progresso geral"
   → Ver impacto do dia

9. "📋 Próximos passos"
   → Planejar amanhã
```

---

## 💬 Comandos por Emoji

### Status e Informações 📊

| Emoji | Comando | O Que Faz |
|-------|---------|-----------|
| 📊 | Status | Status geral do projeto |
| 📊 | Status [módulo] | Status de módulo específico |
| 📋 | Próximos | Lista próximos passos |
| 📜 | Histórico | Últimas 10 ações |
| 📈 | Métricas | Estatísticas do projeto |
| 👋 | Onboarding | Explicação completa |

### Ideias e Decisões 💡

| Emoji | Comando | O Que Faz |
|-------|---------|-----------|
| 💡 | [ideia] | Captura insight rápido |
| 🔍 | Analisar: [X] | Análise profunda |
| 🎯 | Implementar: [X] | Orquestração multi-agente |
| ❓ | Feedback sobre [X] | Consulta especialistas |

### Ações Diretas ⚡

| Emoji | Comando | O Que Faz |
|-------|---------|-----------|
| ⚡ | Implementar [X] | Executa implementação |
| 🔧 | Corrigir [bug] | Corrige problema |
| 🎨 | Design de [tela] | Cria interface |
| 🏗️ | Arquitetura de [X] | Decisão arquitetural |

---

## 🧪 Exemplos Práticos

### Exemplo 1: Primeira Vez no Projeto

```
Você: "👋 Onboarding"
→ Resumo: Explicação completa do projeto

Você: "📊 Status"
→ Resumo: Onde estamos

Você: "📋 Próximos passos"
→ Resumo: O que fazer

Você: "Vou trabalhar no Transfer"
→ Resumo: Detalhes do Transfer + tarefas disponíveis

Você: "⚡ Implementar otimização de performance"
→ Transfer: Guia de implementação
```

### Exemplo 2: Dia Normal de Dev

```
# Manhã
Você: "📊 Status Transfer"
→ Transfer está 90% completo

Você: "📋 O que falta no Transfer?"
→ Otimizações de performance

Você: "⚡ Implementar otimizações"
→ Transfer: Implementa

# Tarde
Você: "💡 Seria legal adicionar cache dos resultados"
→ Insights: Analisa e aprova

Você: "⚡ Implementar cache"
→ Transfer: Implementa

# Fim do dia
Você: "📊 Status Transfer"
→ Transfer: 95% completo (subiu 5%)

Você: "📜 O que fiz hoje?"
→ Resumo: Otimizações + cache implementados
```

### Exemplo 3: Brainstorming Técnico

```
Você: "🔍 Analisar: Devemos usar Redis ou memcache?"

→ Insights: Consultando agentes...
  → Arquiteto: Perspectiva arquitetural
  → Backend: Perspectiva de implementação
  → Segurança: Perspectiva de segurança

→ Insights: Consolidação
  ✅ Recomendação: Redis
  📝 Justificativa: [detalhes]
  📋 Próximos passos: [ações]

Você: "📊 Decisões técnicas"
→ Resumo: ADR criado para Redis
```

### Exemplo 4: Resolução de Bug

```
Você: "🔧 Corrigir bug de exportação Excel no Transfer"

→ Transfer: Diagnosticando...
→ Transfer: Bug identificado (SheetJS config)
→ Transfer: Correção implementada
→ Transfer: Testado ✅

Você: "📊 Status Transfer"
→ Transfer: Bug corrigido, 90% completo

Você: "📜 Histórico"
→ Resumo: Mostra correção registrada
```

---

## 🔌 MCPs Disponíveis

### Automáticos (Usados pelos Agentes)

Os agentes usam automaticamente quando necessário:

- **excel-server**: Leitura de Excel
- **agente-orchestrator**: Orquestração de agentes
- **memory-manager**: Gerenciamento de memória
- **checklist-validator**: Validação de checklists

### Manuais (Você Pode Usar Diretamente)

```
# Ler Excel com fórmulas
"Use excel-server para ler [arquivo]"

# Listar agentes
"Use agente-orchestrator para listar agentes"

# Ver contexto do projeto
"Use memory-manager para carregar contexto"

# Validar checklist
"Use checklist-validator para validar mvp.md"
```

---

## 🎓 Dicas Pro

### 1. Seja Específico

```
❌ "Fazer aquilo"
✅ "Implementar filtro de busca por nome no Transfer"

❌ "Como tá?"
✅ "📊 Status Transfer"

❌ "Tive uma ideia"
✅ "💡 Adicionar exportação PDF no Rooming"
```

### 2. Use Emojis para Velocidade

```
⚡ Mais rápido que "Implementar"
📊 Mais rápido que "Status"
💡 Mais rápido que "Tenho uma ideia"
```

### 3. Consulte Antes de Implementar

```
1. "📊 Status [módulo]"  → Ver contexto
2. "💡 [ideia]"          → Validar com agentes
3. "⚡ Implementar"      → Executar
```

### 4. Registre Ideias Mesmo Que Não Vá Fazer Agora

```
"💡 Futuramente adicionar modo escuro"
→ Insights: Registrado para backlog
```

### 5. Use Linguagem Natural

```
✅ "E aí, como tá o projeto?"
✅ "Preciso fazer aquele filtro"
✅ "Cadê o roadmap?"
✅ "Tá pronto?"
```

---

## 📞 Ajuda Rápida

### Esqueceu Como Usar?

```
"❓ Como usar o sistema de agentes?"
"❓ Quais os atalhos disponíveis?"
"❓ Como funciona o orquestrador?"
```

### Dúvida Sobre Agente Específico?

```
"❓ O que o agente de insights faz?"
"❓ Quando usar o agente de resumo?"
"❓ Qual agente para backend?"
```

### Feedback ou Sugestão?

```
"💡 Sugestão: [sua sugestão]"
```

---

## 🎯 Resumo dos Resumos

**Para status e informações:**
→ Fale com 📊 Agente de Resumo

**Para ideias e decisões:**
→ Fale com 💡 Agente de Insights

**Para implementações:**
→ Fale com 🔧 Agentes Especializados

**Não sabe qual usar?**
→ Fale naturalmente, o orquestrador decide!

---

## ✅ Checklist de Primeiro Uso

- [ ] Leu este guia
- [ ] Testou `📊 Status`
- [ ] Testou `💡 [alguma ideia]`
- [ ] Testou `📋 Próximos passos`
- [ ] Entendeu os 3 tipos de agentes
- [ ] Sabe usar emojis para atalhos
- [ ] Pronto para trabalhar! 🚀

---

**Sistema de Agentes I GO Experience** - Tornando desenvolvimento intuitivo e eficiente.

💡 **Lembre-se:** Você não precisa pensar em agentes. Apenas expresse o que quer!
