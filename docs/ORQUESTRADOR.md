# 🎯 Orquestrador de Agentes - Guia de Uso Intuitivo

**Versão:** 1.0.0
**Data:** 2026-01-25

---

## 🚀 Como Usar os Agentes de Forma Natural

Este sistema foi projetado para ser **intuitivo**. Você não precisa pensar em qual agente usar - o orquestrador detecta automaticamente baseado no que você pede.

---

## 🧠 Detecção Automática de Intençã

### Quando Você Quer Saber "Como Está" → Agente de Resumo 📊

**Palavras-chave:**
- "Como está...", "Status...", "Progresso..."
- "O que foi feito...", "Histórico..."
- "Próximos passos...", "Roadmap..."
- "Estatísticas...", "Métricas..."
- "Explicar projeto...", "Onboarding..."

**Exemplos:**

```
Você: "Como está o projeto?"
→ Agente Resumo responde com status geral

Você: "Status do Transfer?"
→ Agente Resumo com detalhes do módulo

Você: "O que foi feito essa semana?"
→ Agente Resumo com histórico

Você: "Quais os próximos passos?"
→ Agente Resumo com roadmap
```

### Quando Você Tem Uma Ideia → Agente de Insights 💡

**Palavras-chave:**
- "Acho que...", "E se...", "Poderíamos..."
- "Adicionar...", "Implementar...", "Criar..."
- "Melhorar...", "Otimizar...", "Refatorar..."
- "Analisar...", "Avaliar...", "Considerar..."

**Exemplos:**

```
Você: "Acho que devíamos adicionar busca no Transfer"
→ Agente Insights captura e analisa

Você: "E se usássemos GraphQL ao invés de REST?"
→ Agente Insights consulta especialistas

Você: "Implementar notificações por email"
→ Agente Insights orquestra planejamento
```

### Quando Você Quer Fazer Algo → Agente Específico 🔧

**Palavras-chave:**
- "Implementar...", "Corrigir...", "Desenvolver..."
- "Fazer...", "Criar...", "Editar..."
- Referência direta a módulo

**Exemplos:**

```
Você: "Implementar coluna de observações no Rooming"
→ Agente Rooming List

Você: "Corrigir bug no agrupamento do Transfer"
→ Agente Transfer

Você: "Criar endpoint de check-in"
→ Agente Backend
```

---

## 🎨 Comandos Rápidos com Emojis

Use emojis para invocar rapidamente:

### Resumos e Status 📊

```
📊 Status                    → Status geral
📊 Status [módulo]          → Status de módulo específico
📋 Próximos                  → Próximos passos
📜 Histórico                 → Últimas ações
📈 Métricas                  → Estatísticas do projeto
👋 Onboarding                → Explicação completa para novo dev
```

### Insights e Ideias 💡

```
💡 [ideia]                   → Captura simples
🔍 Analisar: [ideia]        → Análise profunda
🎯 Implementar: [feature]   → Orquestração completa
❓ Feedback sobre [ideia]   → Consultar especialistas
```

### Ações Diretas ⚡

```
⚡ Implementar [feature]    → Agente específico executa
🔧 Corrigir [bug]           → Agente específico corrige
🎨 Design de [tela]         → Agente Design/UX
🏗️ Arquitetura de [sistema] → Agente Arquiteto
```

---

## 🔄 Fluxos de Trabalho Completos

### Fluxo 1: Nova Ideia → Implementação

```
1️⃣ Você: "💡 Adicionar filtro de busca no Transfer"
   → Agente Insights captura

2️⃣ Insights: Consulta agentes (Transfer + Design/UX)
   → Retorna análise e decisão

3️⃣ Você: "📊 Status" (para ver atualização)
   → Agente Resumo mostra novo item em próximos passos

4️⃣ Você: "⚡ Implementar filtro de busca"
   → Agente Transfer implementa

5️⃣ Você: "📊 Status Transfer" (para confirmar)
   → Agente Resumo mostra filtro implementado
```

### Fluxo 2: Dúvida Técnica → Decisão

```
1️⃣ Você: "🔍 Analisar: Usar Redis ou memcache para cache?"
   → Agente Insights processa

2️⃣ Insights: Consulta Arquiteto + Backend + Segurança
   → Consolida feedback técnico

3️⃣ Insights: Apresenta recomendação com justificativa
   → Registra decisão em ADR

4️⃣ Você: "📊 Decisões técnicas"
   → Agente Resumo mostra ADR criado
```

### Fluxo 3: Acompanhamento de Progresso

```
1️⃣ Segunda-feira você: "📊 Status"
   → Resumo: Transfer 90%, Rooming 70%, Backend 0%

2️⃣ Durante a semana: Implementações acontecem

3️⃣ Sexta-feira você: "📊 Status"
   → Resumo: Transfer 90%, Rooming 100%, Backend 20%

4️⃣ Você: "📜 O que mudou essa semana?"
   → Resumo: Lista de implementações e decisões
```

---

## 🤖 Matriz de Roteamento Automático

| Sua Mensagem | Agente Ativado | O Que Acontece |
|--------------|----------------|----------------|
| "Como está o projeto?" | 📊 Resumo | Gera status geral |
| "Adicionar feature X" | 💡 Insights | Captura, analisa, decide |
| "Implementar X" | 🔧 Específico | Executa implementação |
| "Status do Transfer" | 📊 Resumo | Status do módulo |
| "Analisar viabilidade de Y" | 💡 Insights | Análise profunda |
| "Próximos passos" | 📊 Resumo | Lista roadmap |
| "O que os agentes pensam sobre Z?" | 💡 Insights | Consulta especialistas |
| "Corrigir bug no..." | 🔧 Específico | Correção direta |
| "Design de tela X" | 🎨 Design/UX | Criação de UI |
| "Arquitetura de Y" | 🏗️ Arquiteto | Decisão arquitetural |

---

## 💬 Linguagem Natural - Exemplos Reais

Você pode falar naturalmente, sem comandos especiais:

### Consultas de Status

```
✅ "Como tá indo?"
✅ "Me dá um resumão"
✅ "Cadê o roadmap?"
✅ "Tá pronto?"
✅ "Quanto falta?"
✅ "O que tá bloqueado?"
```

### Ideias e Sugestões

```
✅ "Tive uma ideia"
✅ "E se a gente..."
✅ "Seria legal adicionar..."
✅ "Precisamos pensar em..."
✅ "Alguém sugeriu que..."
✅ "Vi em outro projeto que..."
```

### Solicitações de Implementação

```
✅ "Vamos fazer X"
✅ "Preciso implementar Y"
✅ "Pode criar Z?"
✅ "Faz um componente de..."
✅ "Corrige o bug do..."
✅ "Adiciona validação em..."
```

### Dúvidas Técnicas

```
✅ "Como funciona o..."
✅ "Por que escolheram..."
✅ "Qual a diferença entre..."
✅ "Vale a pena usar..."
✅ "É melhor X ou Y?"
✅ "Qual o impacto de..."
```

---

## 🎯 Cenários Comuns

### Cenário 1: Primeira Vez Usando o Sistema

```
Você (novo): "Não entendi nada, explica o projeto"
→ Resumo: Onboarding completo com links

Você: "Posso começar pelo Transfer?"
→ Resumo: Status do Transfer + links para docs

Você: "Qual tarefa posso pegar?"
→ Resumo: Lista de próximos passos com prioridades

Você: "Vou fazer a otimização de performance então"
→ Transfer: Guia de implementação específica
```

### Cenário 2: Standupaily/Reunião

```
Gestor: "Status geral do projeto?"
→ Resumo: Executivo (alto nível, % completo)

Dev: "O que eu fiz ontem?"
→ Resumo: Suas últimas ações (via git)

PO: "Quando vai ficar pronto?"
→ Resumo: Estimativas baseadas em roadmap

Arquiteto: "Quais decisões técnicas foram tomadas?"
→ Resumo: Lista de ADRs
```

### Cenário 3: Brainstorming

```
Time: "E se adicionarmos gamificação?"
→ Insights: Captura ideia

Insights: "Analisando impacto... consultando agentes..."
→ Arquiteto: Avalia arquitetura
→ Design/UX: Avalia UX
→ Backend: Avalia implementação

Insights: "Decisão: Adicionar ao backlog (prioridade baixa)"
→ Justificativa técnica documentada

Time: "Ok, e notificações push?"
→ Insights: Novo ciclo de análise
```

### Cenário 4: Resolução de Problema

```
Você: "O Excel não tá exportando direito no Transfer"
→ Transfer: Diagnóstico do problema

Transfer: "Identificado: SheetJS precisa configuração"
→ Implementa correção

Você: "Funcionou! Mas agora quero adicionar PDF também"
→ Insights: Captura nova feature
→ Análise de esforço
→ Adiciona ao roadmap

Você: "📊 Status Transfer"
→ Resumo: Bug corrigido ✅, PDF planejado 📋
```

---

## 🔧 Configuração Personalizada

### Ajustar Verbosidade

Você pode pedir resumos mais ou menos detalhados:

```
"Status resumido"           → Executivo (5 linhas)
"Status"                    → Padrão (15 linhas)
"Status detalhado"          → Técnico (50 linhas)
"Status completo com ADRs"  → Exaustivo (100+ linhas)
```

### Ajustar Foco

```
"Status apenas backend"     → Filtra por módulo
"Status de bugs"            → Filtra por tipo
"Status crítico"            → Filtra por prioridade
"Status desta semana"       → Filtra por data
```

### Ajustar Formato

```
"Status em lista"           → Bullet points
"Status em tabela"          → Tabela markdown
"Status em JSON"            → Estruturado (para APIs)
"Status visual"             → Com gráficos emoji
```

---

## 📊 Dashboard Mental dos Agentes

Os agentes mantêm um modelo mental compartilhado:

```
┌─────────────────────────────────────────────┐
│          PROJETO I GO EXPERIENCE            │
│                                             │
│  Fase: MVP Desenvolvimento (65%)            │
│  Última Atualização: 2026-01-25 16:00       │
├─────────────────────────────────────────────┤
│  MÓDULOS:                                   │
│  ✅ Transfer: 90%    ✅ Rooming: 100%       │
│  🔴 Check-in: 0%     🔴 Backend: 0%         │
├─────────────────────────────────────────────┤
│  PRÓXIMO:                                   │
│  1. Setup Backend API                       │
│  2. JWT Auth                                │
│  3. Check-in Frontend                       │
├─────────────────────────────────────────────┤
│  AGENTES ATIVOS:                            │
│  🧠 Insights  📊 Resumo  🏗️ Arquiteto       │
│  🔧 Backend   🎨 Design/UX                  │
├─────────────────────────────────────────────┤
│  INSIGHTS CAPTURADOS: 1                     │
│  DECISÕES TÉCNICAS: 3                       │
│  TAREFAS PENDENTES: 12                      │
└─────────────────────────────────────────────┘
```

---

## 🎓 Dicas de Uso

### ✅ Boas Práticas

1. **Seja natural** - Fale como falaria com um colega
2. **Seja específico** - Quanto mais contexto, melhor
3. **Use emojis** - Facilitam roteamento rápido
4. **Consulte status** - Antes de decidir próximos passos
5. **Registre ideias** - Mesmo que não vá implementar agora

### ❌ Evite

1. **Ambiguidade** - "Fazer aquilo" não é claro
2. **Múltiplas intenções** - Uma pergunta de cada vez
3. **Ignorar sugestões** - Agentes analisam com profundidade
4. **Pular contexto** - Sempre consulte status primeiro

---

## 🚀 Início Rápido

### Seu Primeiro Uso

```bash
# 1. Entenda o projeto
Você: "👋 Onboarding"

# 2. Veja status
Você: "📊 Status"

# 3. Identifique tarefa
Você: "📋 Próximos passos"

# 4. Escolha uma
Você: "⚡ Implementar [tarefa escolhida]"
```

### Uso Diário

```bash
# Manhã
Você: "📊 Status"
Você: "📋 O que fazer hoje?"

# Durante o dia
Você: "💡 [ideias que surgirem]"
Você: "⚡ Implementar [tarefa]"

# Fim do dia
Você: "📜 O que fiz hoje?"
Você: "📊 Progresso geral"
```

---

## 📞 Suporte

### Dúvidas?

```
"❓ Como usar o orquestrador?"
"❓ Qual a diferença entre Insights e Resumo?"
"❓ Como consultar um agente específico?"
"❓ Onde fica a documentação?"
```

### Feedback

```
"💡 Sugestão: melhorar detecção de intenção"
"💡 O agente X poderia fazer Y também"
"💡 Adicionar atalho para Z"
```

---

**O orquestrador foi projetado para ser invisível. Você só precisa expressar o que quer - nós descobrimos como fazer!**

🎯 **Orquestrador** - Tornando complexidade simples.
