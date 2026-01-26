# Fase 2: Exemplo de Uso - IA Decision Making

**Data:** 2026-01-26

## 📚 Introdução

Este documento demonstra como usar o sistema de decisão inteligente de agentes implementado na Fase 2.

## 🎯 O Que Foi Implementado

### Novas Ferramentas

1. **agente-orchestrator::ask_ai_to_decide**
   - Ponto de entrada para decisão de IA
   - Coleta agentes disponíveis e contexto do projeto
   - Prepara dados para o gateway

2. **igo-openai-gateway::decide_agent**
   - Usa GPT-5.2 com reasoning para analisar requisição
   - Recomenda agente(s) adequado(s)
   - Retorna decisão estruturada com explicação

## 🚀 Cenários de Uso

### Cenário 1: Requisição Ambígua - "Melhorar Performance"

**Problema:** Usuário pede "Preciso melhorar a performance do rooming list" mas não especifica qual agente usar.

#### Passo 1: Chamar Orchestrator

```javascript
// Claude Code chama automaticamente via MCP:
mcp__agente_orchestrator__ask_ai_to_decide({
  user_request: "Preciso melhorar a performance do rooming list",
  project: "igo-journey",
  branch: "main"
})
```

#### Resposta do Orchestrator

```json
{
  "success": true,
  "message": "Dados preparados para decisão de IA",
  "next_step": {
    "action": "call_gateway",
    "mcp": "igo-openai-gateway",
    "tool": "decide_agent",
    "parameters": {
      "user_request": "Preciso melhorar a performance do rooming list",
      "available_agents": "{...26 agentes...}",
      "project_context": "...histórico do projeto...",
      "reasoning_effort": "high"
    }
  },
  "instructions": "Chame igo-openai-gateway::decide_agent com os parâmetros acima",
  "agents_available": {
    "mcps": [9 MCPs],
    "agents": [17 agentes especializados],
    "total": 26
  }
}
```

**O que aconteceu:**
- ✅ Orchestrator coletou lista de 26 agentes/MCPs
- ✅ Carregou contexto do projeto igo-journey/main
- ✅ Preparou todos os dados necessários
- ✅ Retornou instruções claras para próximo passo

#### Passo 2: Chamar Gateway (GPT-5.2)

```javascript
// Claude Code chama:
mcp__igo_openai_gateway__decide_agent({
  user_request: "Preciso melhorar a performance do rooming list",
  available_agents: "{...todos os agentes...}",
  project_context: "...contexto do igo-journey/main...",
  reasoning_effort: "high"
})
```

#### Resposta do Gateway (GPT-5.2 com Reasoning)

```json
{
  "success": true,
  "decision": {
    "recommended_agents": [
      {
        "agent_name": "agente-rooming-list",
        "priority": "primary",
        "reason": "Este agente é especialista no módulo específico de rooming list e conhece profundamente as regras de negócio e pontos de gargalo específicos deste módulo."
      },
      {
        "agent_name": "agente-backend",
        "priority": "primary",
        "reason": "Performance issues geralmente envolvem otimização de queries SQL, cache, e algoritmos de processamento backend. Este agente pode implementar as otimizações técnicas."
      },
      {
        "agent_name": "agente-qa-testes",
        "priority": "secondary",
        "reason": "Após implementar otimizações, é essencial criar testes de performance para validar as melhorias e prevenir regressões futuras."
      }
    ],
    "reasoning": "A requisição menciona 'performance' (problema técnico) e 'rooming list' (módulo específico). A solução ideal requer:\n\n1. Conhecimento profundo do módulo rooming-list para identificar gargalos específicos\n2. Expertise backend para implementar otimizações (queries, cache, algoritmos)\n3. QA para garantir que as melhorias foram efetivas\n\nA combinação destes 3 agentes fornece cobertura completa: análise especializada + implementação técnica + validação.",
    "execution_plan": "1. Invocar agente-rooming-list para análise detalhada do módulo e identificação de gargalos específicos\n2. Invocar agente-backend para implementar otimizações baseadas nos gargalos identificados\n3. Invocar agente-qa-testes para criar suite de testes de performance e validar melhorias",
    "confidence": "high"
  },
  "model": "gpt-5.2-2025-12-11",
  "reasoning_effort": "high"
}
```

**O que aconteceu:**
- ✅ GPT-5.2 analisou a requisição com reasoning alto
- ✅ Identificou que é problema de performance em módulo específico
- ✅ Recomendou 3 agentes com prioridades claras
- ✅ Explicou o raciocínio completo
- ✅ Forneceu plano de execução passo a passo
- ✅ Indicou confiança alta na decisão

#### Passo 3: Executar Agentes Recomendados

```javascript
// Claude Code executa sequencialmente:

// 1. Análise do módulo
mcp__agente_orchestrator__invoke_agent({
  agent_name: "agente-rooming-list",
  task: "Analisar performance do módulo rooming list e identificar gargalos específicos"
})

// 2. Implementar otimizações
mcp__agente_orchestrator__invoke_agent({
  agent_name: "agente-backend",
  task: "Implementar otimizações de performance baseadas nos gargalos identificados no rooming list"
})

// 3. Criar testes
mcp__agente_orchestrator__invoke_agent({
  agent_name: "agente-qa-testes",
  task: "Criar suite de testes de performance para validar otimizações do rooming list"
})
```

---

### Cenário 2: Feature Complexa - "Notificações Push"

**Requisição:** "Adicionar sistema de notificações push para eventos"

#### Decisão de IA Esperada

```json
{
  "recommended_agents": [
    {
      "agent_name": "agente-arquiteto-igo",
      "priority": "primary",
      "reason": "Feature complexa requer decisões arquiteturais: escolha de tecnologia (WebSockets, SSE, Firebase), design de infraestrutura, e padrões de mensageria."
    },
    {
      "agent_name": "agente-backend",
      "priority": "secondary",
      "reason": "Implementação da infraestrutura de notificações no backend após aprovação da arquitetura."
    },
    {
      "agent_name": "agente-frontend-igo",
      "priority": "secondary",
      "reason": "Implementação da UI de notificações e integração com backend."
    },
    {
      "agent_name": "agente-qa-testes",
      "priority": "tertiary",
      "reason": "Testes de integração e E2E do fluxo de notificações."
    }
  ],
  "execution_plan": "1. Arquiteto define tecnologia e arquitetura\n2. Backend implementa infraestrutura\n3. Frontend implementa UI\n4. QA valida integração completa",
  "confidence": "high"
}
```

---

### Cenário 3: Bug Genérico - "Bug no Frontend"

**Requisição:** "Tenho um bug no frontend"

#### Decisão de IA Esperada

```json
{
  "recommended_agents": [
    {
      "agent_name": "agente-frontend-igo",
      "priority": "primary",
      "reason": "Requisição menciona explicitamente 'frontend', portanto o agente especialista em frontend é a escolha óbvia."
    }
  ],
  "reasoning": "Requisição direta e sem ambiguidade - menciona 'bug no frontend' explicitamente.",
  "execution_plan": "Invocar agente-frontend-igo para debug e correção do bug.",
  "confidence": "high"
}
```

---

### Cenário 4: Análise de Negócio - "KPIs do Q1"

**Requisição:** "Preciso analisar os KPIs do Q1 2025"

#### Decisão de IA Esperada

```json
{
  "recommended_agents": [
    {
      "agent_name": "agente-analytics-kpi",
      "priority": "primary",
      "reason": "Agente especializado em análise de KPIs e métricas de negócio. Conhece as métricas da empresa e sabe como extrair insights."
    },
    {
      "agent_name": "api-database-tester",
      "priority": "secondary",
      "reason": "Pode ser necessário executar queries SQL para extrair dados de KPIs do banco de produção."
    }
  ],
  "execution_plan": "1. Analytics-KPI define quais métricas analisar\n2. API-Database-Tester extrai dados se necessário\n3. Analytics-KPI gera relatório com insights",
  "confidence": "high"
}
```

---

### Cenário 5: Integração Entre Módulos

**Requisição:** "Integrar dados de transfer com rooming list"

#### Decisão de IA Esperada

```json
{
  "recommended_agents": [
    {
      "agent_name": "agente-integracoes-igo",
      "priority": "primary",
      "reason": "Especialista em integrações entre módulos. Conhece padrões de integração, APIs internas, e como conectar diferentes partes do sistema."
    },
    {
      "agent_name": "agente-transfer",
      "priority": "secondary",
      "reason": "Conhecimento profundo do módulo transfer, seus dados e APIs."
    },
    {
      "agent_name": "agente-rooming-list",
      "priority": "secondary",
      "reason": "Conhecimento profundo do módulo rooming-list, suas necessidades e estrutura de dados."
    },
    {
      "agent_name": "agente-backend",
      "priority": "tertiary",
      "reason": "Implementação técnica da integração após design."
    }
  ],
  "reasoning": "Integração entre módulos requer:\n1. Especialista em integrações para design\n2. Conhecimento de ambos os módulos\n3. Implementação backend",
  "execution_plan": "1. Integracoes-igo + Transfer + Rooming-list definem interface\n2. Backend implementa integração\n3. Agentes de módulo validam resultado",
  "confidence": "high"
}
```

---

## 🎨 Reasoning Effort Levels - Quando Usar

### none (padrão)
**Quando usar:**
- Requisições simples e diretas
- Agente já está claro
- Baixo custo/latência é prioridade

**Exemplo:** "Use agente-frontend para corrigir o botão"

### low
**Quando usar:**
- Requisições relativamente diretas
- Pouca ambiguidade
- Decisão de baixa complexidade

**Exemplo:** "Corrigir bug de validação no formulário"

### medium
**Quando usar:**
- Requisições com alguma ambiguidade
- Múltiplas opções viáveis
- Decisão moderadamente complexa

**Exemplo:** "Melhorar UX do check-in"

### high (recomendado)
**Quando usar:**
- Requisições ambíguas ou complexas
- Múltiplos agentes podem ser necessários
- Decisão crítica para o projeto
- **Este é o padrão no ask_ai_to_decide**

**Exemplo:** "Melhorar performance do rooming list"

### xhigh
**Quando usar:**
- Decisões arquiteturais críticas
- Trade-offs complexos entre múltiplas abordagens
- Alto impacto no projeto
- Requer análise profunda

**Exemplo:** "Escolher arquitetura de notificações para 100k eventos simultâneos"

---

## 📊 Estatísticas de Agentes

### Categorias

**Development (5 agentes):**
- agente-arquiteto-igo
- agente-frontend-igo
- agente-integracoes-igo
- agente-qa-testes
- agente-solucoes

**Module (7 agentes):**
- agente-backend
- agente-checkin
- agente-rooming-list
- agente-transfer
- agente-rsvp
- agente-tracking
- agente-credenciamento

**Business (5 agentes):**
- agente-analytics-kpi
- agente-comercial-igo
- agente-diretoria-igo
- agente-marketing-igo
- agente-operacao-igo

**MCPs (9 ferramentas):**
- agente-insights
- agente-resumo
- igo-openai-gateway
- api-database-tester
- excel-server
- memory-manager
- checklist-validator
- docker-admin
- vuetify-uiux

**Total: 26 agentes/MCPs disponíveis**

---

## 🔍 Como a IA Decide

### Fatores Considerados

1. **Palavras-chave na requisição**
   - "performance" → agente-backend
   - "frontend" → agente-frontend-igo
   - "KPI" → agente-analytics-kpi
   - "integração" → agente-integracoes-igo

2. **Complexidade da tarefa**
   - Simples → 1 agente
   - Moderada → 2-3 agentes
   - Complexa → 3+ agentes em sequência

3. **Tipo de tarefa**
   - Desenvolvimento → Development agents
   - Módulo específico → Module agents
   - Negócio → Business agents

4. **Contexto do projeto**
   - Histórico de decisões
   - Módulos já implementados
   - Padrões do projeto

5. **Priorização**
   - primary: Agente principal
   - secondary: Agente de apoio
   - tertiary: Agente opcional/validação

---

## ✅ Checklist de Uso

Antes de usar o sistema de decisão de IA:

- [ ] Verificar que igo-openai-gateway tem OPENAI_API_KEY configurada
- [ ] Configurar contexto do projeto com memory-manager::set_project_context
- [ ] Formular requisição clara (mas pode ser ambígua)
- [ ] Chamar ask_ai_to_decide com project e branch corretos
- [ ] Ler decisão de IA cuidadosamente
- [ ] Executar agentes na ordem recomendada
- [ ] Validar resultado de cada agente antes de próximo

---

## 💡 Dicas

1. **Seja específico no user_request**
   - Ruim: "Melhorar app"
   - Bom: "Melhorar performance do rooming list"

2. **Use o contexto do projeto**
   - IA leva em conta histórico e decisões passadas
   - Configure project/branch corretos

3. **Confie no reasoning**
   - GPT-5.2 com high reasoning é muito preciso
   - Leia a explicação para entender o "por quê"

4. **Execute em sequência**
   - Siga o execution_plan recomendado
   - Cada agente depende do anterior

5. **Valide as decisões**
   - Se discordar, pode chamar agente diferente
   - Mas geralmente a IA acerta

---

## 🐛 Troubleshooting

### Erro: "OPENAI_API_KEY não definido"
**Solução:** Configure variável de ambiente antes de iniciar igo-openai-gateway
```bash
export OPENAI_API_KEY="sk-..."
python igo-openai-gateway/server.py
```

### Erro: "Agente não encontrado"
**Solução:** Verifique que o agente existe em docs/agentes/
```bash
ls docs/agentes/
```

### Decisão de IA não faz sentido
**Solução:**
1. Reformule a requisição com mais contexto
2. Aumente reasoning_effort para "xhigh"
3. Verifique se contexto do projeto está atualizado

### Latência alta
**Solução:**
- Use reasoning_effort="low" ou "none" para requisições simples
- High e xhigh são mais lentos mas mais precisos

---

## 📈 Benefícios do Sistema

✅ **Não precisa conhecer todos os agentes** - IA decide por você
✅ **Recomendações explicadas** - Entende o "por quê" da decisão
✅ **Múltiplos agentes coordenados** - IA planeja sequência completa
✅ **Contexto do projeto** - Decisões baseadas em histórico
✅ **Confiança alta** - GPT-5.2 reasoning é muito preciso
✅ **Transparência total** - Cada etapa é documentada

---

**Criado em:** 2026-01-26
**Autor:** Claude Sonnet 4.5
