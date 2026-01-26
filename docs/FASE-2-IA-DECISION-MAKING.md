# Fase 2: IA Decision Making - Orchestrator + Gateway Integration

**Data Início:** 2026-01-26
**Status:** ✅ COMPLETO (100%)

## 🎯 Objetivo

Integrar o agente-orchestrator com o igo-openai-gateway para criar um sistema de decisão inteligente usando GPT-5.2, permitindo:
- IA decide qual agente usar baseado na requisição do usuário
- Análise com reasoning (low, medium, high, xhigh)
- Recomendações estruturadas com explicações detalhadas
- Fluxo completo: User → Orchestrator → Gateway → Decisão → Execução

## ✅ Implementação

### 1. **Nova Tool no igo-openai-gateway** ✅ COMPLETO

**Tool:** `decide_agent`

**Funcionalidade:**
- Recebe requisição ambígua do usuário
- Analisa lista de agentes disponíveis
- Considera contexto do projeto
- Usa GPT-5.2 com reasoning alto
- Retorna recomendação estruturada em JSON

**Assinatura:**
```python
@mcp.tool()
def decide_agent(
    user_request: str,
    available_agents: str,
    project_context: Optional[str] = None,
    reasoning_effort: str = "high",
) -> str:
```

**Prompt Especializado:**
```
Você é um especialista em arquitetura de sistemas de agentes de IA.

Sua tarefa é analisar a requisição do usuário e decidir qual(is) agente(s) especializado(s)
deve(m) ser utilizado(s) para resolver o problema.

REGRAS DE DECISÃO:
1. Analise a natureza da tarefa (desenvolvimento, negócio, módulo específico)
2. Considere se a tarefa requer múltiplos agentes trabalhando em sequência
3. Prefira agentes especializados para tarefas focadas
4. Use agentes de desenvolvimento para tarefas técnicas amplas
5. Use agentes de módulo para features/bugs específicos de um módulo
6. Use agentes de negócio para análises de KPI, comerciais ou estratégicas
```

**Formato de Resposta:**
```json
{
  "recommended_agents": [
    {
      "agent_name": "nome-do-agente",
      "priority": "primary|secondary",
      "reason": "explicação detalhada"
    }
  ],
  "reasoning": "análise completa da decisão",
  "execution_plan": "como os agentes devem trabalhar juntos",
  "confidence": "high|medium|low"
}
```

---

### 2. **Nova Tool no agente-orchestrator** ✅ COMPLETO

**Tool:** `ask_ai_to_decide`

**Funcionalidade:**
- Ponto de entrada para decisão de IA
- Coleta lista de agentes disponíveis
- Carrega contexto do projeto (multi-projeto/branch)
- Prepara dados para o gateway
- Retorna instruções claras para próximo passo

**Assinatura:**
```python
@mcp.tool()
def ask_ai_to_decide(
    user_request: str,
    project: str = "default",
    branch: str = "main"
) -> str:
```

**Fluxo Interno:**
1. Chama `list_agents()` para obter agentes disponíveis
2. Carrega contexto de `memoria/{project}/{branch}/contexto-atual.md`
3. Prepara payload para `igo-openai-gateway::decide_agent`
4. Retorna instruções estruturadas

**Retorno:**
```json
{
  "success": true,
  "message": "Dados preparados para decisão de IA",
  "next_step": {
    "action": "call_gateway",
    "mcp": "igo-openai-gateway",
    "tool": "decide_agent",
    "parameters": { ... }
  },
  "instructions": "...",
  "prepared_data": { ... },
  "agents_available": { ... }
}
```

---

### 3. **Compatibilidade Windows/Docker** ✅ COMPLETO

Ambos os MCPs agora detectam automaticamente o ambiente:

```python
import sys
if sys.platform == "win32":
    # Windows local
    PROJECT_ROOT = Path("c:/GIT-RAFAEL/mcp-servers")
    DOCS_DIR = PROJECT_ROOT / "docs"
else:
    # Docker (Linux)
    PROJECT_ROOT = Path("/project")
    DOCS_DIR = PROJECT_ROOT / "GIT-RAFAEL" / "mcp-servers" / "docs"
```

**Benefícios:**
- ✅ Funciona em Windows local (8 MCPs)
- ✅ Funciona em Docker Linux (2 MCPs)
- ✅ Sem necessidade de configuração manual

---

## 📊 Arquitetura do Fluxo

```
┌─────────────────────────────────────────────────────────────────┐
│                          USUÁRIO                                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ "Preciso melhorar performance do rooming list"
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AGENTE-ORCHESTRATOR                          │
│                                                                 │
│  Tool: ask_ai_to_decide(                                       │
│    user_request="Preciso melhorar performance...",             │
│    project="igo-journey",                                      │
│    branch="main"                                               │
│  )                                                              │
│                                                                 │
│  Ações:                                                         │
│  1. ✓ Coletar lista de agentes (list_agents)                  │
│  2. ✓ Carregar contexto do projeto                            │
│  3. ✓ Preparar dados                                           │
│  4. ✓ Retornar instruções                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Dados preparados + instruções
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CLAUDE CODE (Usuário)                         │
│                                                                 │
│  Recebe instruções e chama:                                     │
│  igo-openai-gateway::decide_agent(...)                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Chamada para GPT-5.2
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    IGO-OPENAI-GATEWAY                           │
│                                                                 │
│  Tool: decide_agent(                                           │
│    user_request="...",                                         │
│    available_agents="{...}",                                   │
│    project_context="...",                                      │
│    reasoning_effort="high"                                     │
│  )                                                              │
│                                                                 │
│  Ações:                                                         │
│  1. ✓ Criar prompt especializado                              │
│  2. ✓ Chamar GPT-5.2 com reasoning=high                       │
│  3. ✓ Processar resposta                                       │
│  4. ✓ Retornar decisão estruturada                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Decisão + Reasoning
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GPT-5.2 RESPONSES API                      │
│                                                                 │
│  Reasoning Effort: HIGH                                         │
│  Verbosity: HIGH                                                │
│                                                                 │
│  Análise:                                                       │
│  • Tarefa é sobre performance                                   │
│  • Módulo específico: rooming-list                             │
│  • Requer otimização backend + testes                          │
│                                                                 │
│  Decisão:                                                       │
│  {                                                              │
│    "recommended_agents": [                                      │
│      {                                                          │
│        "agent_name": "agente-backend",                         │
│        "priority": "primary",                                   │
│        "reason": "Otimizar queries e lógica do rooming list"   │
│      },                                                         │
│      {                                                          │
│        "agent_name": "agente-qa-testes",                       │
│        "priority": "secondary",                                 │
│        "reason": "Criar testes de performance"                 │
│      }                                                          │
│    ],                                                           │
│    "reasoning": "Performance issues require backend...",        │
│    "execution_plan": "1. Backend optimizes 2. QA tests",       │
│    "confidence": "high"                                         │
│  }                                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Retorna decisão
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   CLAUDE CODE (Usuário)                         │
│                                                                 │
│  Recebe decisão e executa agente recomendado:                   │
│  orchestrator::invoke_agent("agente-backend", "...")           │
│  OU                                                             │
│  gateway::run_agent("agente-backend", "...")                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Exemplo de Uso Completo

### Cenário: Requisição Ambígua

**Usuário:** "Preciso melhorar a performance do rooming list"

**Passo 1: Chamar Orchestrator**
```python
# Claude Code chama:
mcp__agente-orchestrator__ask_ai_to_decide(
    user_request="Preciso melhorar a performance do rooming list",
    project="igo-journey",
    branch="main"
)
```

**Resposta do Orchestrator:**
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
      "available_agents": "{...todos os agentes...}",
      "project_context": "...contexto do igo-journey/main...",
      "reasoning_effort": "high"
    }
  },
  "instructions": "Chame igo-openai-gateway::decide_agent com os parâmetros acima",
  "agents_available": {
    "mcps": [...],
    "agents": [...],
    "total": 26
  }
}
```

**Passo 2: Chamar Gateway**
```python
# Claude Code chama:
mcp__igo_openai_gateway__decide_agent(
    user_request="Preciso melhorar a performance do rooming list",
    available_agents="{...}",
    project_context="...",
    reasoning_effort="high"
)
```

**Resposta do Gateway:**
```json
{
  "success": true,
  "decision": {
    "recommended_agents": [
      {
        "agent_name": "agente-backend",
        "priority": "primary",
        "reason": "O rooming list é um módulo backend que processa listas de hospedagem. Para melhorar performance, é necessário otimizar queries SQL, adicionar cache, e melhorar algoritmos de processamento."
      },
      {
        "agent_name": "agente-rooming-list",
        "priority": "primary",
        "reason": "Este agente é especialista no módulo específico de rooming list e conhece profundamente as regras de negócio e pontos de gargalo."
      },
      {
        "agent_name": "agente-qa-testes",
        "priority": "secondary",
        "reason": "Após otimizações, é essencial criar testes de performance para garantir que as melhorias foram efetivas e prevenir regressões."
      }
    ],
    "reasoning": "A requisição menciona 'performance' e 'rooming list', indicando um problema de velocidade em um módulo específico. A solução requer: 1) Análise técnica do backend para identificar gargalos, 2) Conhecimento específico do módulo rooming-list, 3) Validação com testes de performance.",
    "execution_plan": "1. Invocar agente-rooming-list para análise do módulo e identificação de gargalos específicos. 2. Invocar agente-backend para implementar otimizações (queries, cache, algoritmos). 3. Invocar agente-qa-testes para criar suite de testes de performance.",
    "confidence": "high"
  },
  "model": "gpt-5.2-2025-12-11",
  "reasoning_effort": "high"
}
```

**Passo 3: Executar Agente Recomendado**
```python
# Claude Code executa:
mcp__agente_orchestrator__invoke_agent(
    agent_name="agente-rooming-list",
    task="Analisar performance do módulo rooming list e identificar gargalos"
)
```

---

## 💡 Decisões Técnicas (ADRs)

### ADR-004: Orchestrator Retorna Instruções ao Invés de Chamar Diretamente

**Decisão:** `ask_ai_to_decide` retorna instruções para Claude Code chamar o gateway, ao invés de chamar diretamente.

**Alternativas Consideradas:**
1. Orchestrator chama gateway diretamente (comunicação MCP-to-MCP)
2. **Orchestrator retorna instruções para Claude Code** ✅ Escolhido
3. Gateway chama orchestrator (fluxo reverso)

**Razão:**
- MCPs comunicam via stdio (stdin/stdout) e não podem chamar outros MCPs diretamente
- Claude Code é o único que pode chamar múltiplos MCPs
- Transparência: usuário vê cada etapa do processo
- Flexibilidade: Claude Code pode ajustar parâmetros antes de chamar

**Trade-off:** Requer 2 chamadas (orchestrator → gateway), mas ganha transparência e controle.

---

### ADR-005: Reasoning Effort Padrão = High

**Decisão:** Usar `reasoning_effort="high"` por padrão no `decide_agent`.

**Razão:**
- Decisão de qual agente usar é crítica
- Erro na escolha desperdiça tempo e recursos
- High reasoning balanceia qualidade vs custo
- XHigh seria overkill para maioria dos casos

**Quando usar XHIGH:**
- Decisões arquiteturais complexas
- Múltiplos agentes possíveis com trade-offs sutis
- Projetos com alta criticidade

---

### ADR-006: Compatibilidade Windows/Docker Automática

**Decisão:** Detectar ambiente (Windows vs Docker) automaticamente via `sys.platform`.

**Razão:**
- 8 MCPs rodam local Windows
- 2 MCPs rodam em Docker (docker-admin, api-database-tester)
- Mesma codebase para ambos os ambientes
- Zero configuração manual

**Implementação:**
```python
if sys.platform == "win32":
    PROJECT_ROOT = Path("c:/GIT-RAFAEL/mcp-servers")
else:
    PROJECT_ROOT = Path("/project")
```

---

## 🚀 Benefícios Implementados

### 1. ✅ Decisão Inteligente de Agentes
- GPT-5.2 analisa requisição e recomenda agente(s)
- Reasoning alto garante análise profunda
- Suporte a múltiplos agentes em sequência

### 2. ✅ Integração Orchestrator + Gateway
- Fluxo completo funcionando
- Comunicação via Claude Code (intermediário)
- Instruções claras em cada etapa

### 3. ✅ Contexto Multi-Projeto
- `ask_ai_to_decide` usa contexto de projeto/branch
- Decisões levam em conta histórico e estado atual
- Compatível com sistema multi-projeto da Fase 1

### 4. ✅ Transparência Total
- Cada etapa retorna JSON estruturado
- Reasoning visível no output
- Fácil debug e auditoria

### 5. ✅ Extensibilidade
- Fácil adicionar novos agentes à lista
- Gateway pode ser usado para outras decisões de IA
- Reasoning effort configurável por caso de uso

---

## 📈 Estatísticas

| Item | Valor |
|------|-------|
| **Ferramentas Criadas** | 2 |
| **MCPs Modificados** | 2 |
| **Linhas de Código** | ~200 |
| **Agentes Suportados** | 26 (9 MCPs + 17 agentes) |
| **Categorias de Agentes** | 3 (development, module, business) |
| **Reasoning Levels** | 5 (none, low, medium, high, xhigh) |
| **Compatibilidade** | Windows + Docker |

---

## 🎯 Casos de Uso

### Caso 1: Requisição Técnica Genérica
**Input:** "Tenho um bug no frontend"
**Decisão IA:** agente-frontend-igo (primary)
**Razão:** Requisição menciona frontend explicitamente

### Caso 2: Requisição de Feature Complexa
**Input:** "Adicionar sistema de notificações push"
**Decisão IA:**
- agente-arquiteto-igo (primary) - Design arquitetura
- agente-backend (secondary) - Implementar backend
- agente-frontend-igo (secondary) - Implementar UI
**Razão:** Feature complexa requer múltiplos agentes

### Caso 3: Requisição de Negócio
**Input:** "Quero analisar KPIs do Q1"
**Decisão IA:** agente-analytics-kpi (primary)
**Razão:** Tarefa de análise de métricas de negócio

### Caso 4: Requisição Ambígua
**Input:** "O check-in está lento"
**Decisão IA:**
- agente-checkin (primary) - Especialista do módulo
- agente-backend (secondary) - Otimizar backend
- agente-qa-testes (tertiary) - Performance tests
**Razão:** "Lento" = problema de performance, módulo específico

### Caso 5: Múltiplos Módulos
**Input:** "Integrar transfer com rooming list"
**Decisão IA:**
- agente-integracoes-igo (primary) - Especialista em integrações
- agente-transfer (secondary) - Conhecimento módulo transfer
- agente-rooming-list (secondary) - Conhecimento módulo rooming
**Razão:** Integração entre módulos requer especialista + conhecimento de ambos

---

## 🔮 Próximos Passos (Fase 3)

### 1. Analytics & Auto-Learning
- [ ] Registrar decisões de IA em banco
- [ ] Analisar padrões de decisões
- [ ] Melhorar prompt baseado em histórico
- [ ] Sugerir agentes baseado em decisões passadas similares

### 2. Feedback Loop
- [ ] Registrar se decisão foi boa (usuário aprova resultado)
- [ ] Ajustar pesos de agentes baseado em sucesso
- [ ] Auto-melhorar reasoning prompts

### 3. Advanced Orchestration
- [ ] Executar múltiplos agentes em paralelo
- [ ] Pipeline de agentes (output de um → input de outro)
- [ ] Aprovação de usuário antes de executar agentes
- [ ] Rollback de ações de agentes

### 4. Monitoring & Observability
- [ ] Dashboard de decisões de IA
- [ ] Métricas de reasoning effort vs qualidade
- [ ] Custo por decisão (tokens)
- [ ] Latência de decisões

---

## ✅ Checklist de Implementação

- [x] Criar tool `decide_agent` no igo-openai-gateway
- [x] Criar tool `ask_ai_to_decide` no agente-orchestrator
- [x] Implementar prompt especializado de decisão
- [x] Adicionar suporte a reasoning effort
- [x] Adicionar compatibilidade Windows/Docker
- [x] Testar integração completa
- [x] Documentar arquitetura e fluxo
- [x] Documentar casos de uso
- [x] Documentar ADRs
- [x] Atualizar LISTA_MCPS.md

**STATUS FINAL: ✅ FASE 2 COMPLETA**

---

**Criado em:** 2026-01-26
**Última atualização:** 2026-01-26 02:00
**Autor:** Claude Sonnet 4.5
