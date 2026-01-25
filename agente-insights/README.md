# 🧠 Agente de Insights MCP

Captura de ideias, consulta a especialistas e tomada de decisões técnicas.

## Ferramentas Disponíveis

### 1. `capture_insight`
Captura uma nova ideia ou sugestão.

**Parâmetros:**
- `idea` (string, obrigatório): Descrição da ideia
- `insight_type` (string): Tipo do insight
  - `feature` (padrão)
  - `bug`
  - `improvement`
  - `decision`
  - `exploration`
- `complexity` (string): Complexidade estimada
  - `low`
  - `medium` (padrão)
  - `high`
- `modules` (array): Lista de módulos impactados

**Exemplo:**
```python
capture_insight(
    idea="Adicionar busca por nome no Transfer",
    insight_type="feature",
    complexity="low",
    modules=["transfer"]
)
```

### 2. `get_insights`
Lista insights com filtros.

**Parâmetros:**
- `status` (string): Filtrar por status
  - `captured`
  - `analyzing`
  - `approved`
  - `rejected`
  - `implemented`
- `insight_type` (string): Filtrar por tipo
- `limit` (int): Máximo de resultados (padrão: 10)

**Exemplo:**
```python
get_insights(status="approved", limit=5)
```

### 3. `update_insight_status`
Atualiza status de um insight.

**Parâmetros:**
- `insight_id` (string, obrigatório): ID do insight (ex: INS-0001)
- `new_status` (string, obrigatório): Novo status
- `notes` (string): Notas sobre a mudança

**Exemplo:**
```python
update_insight_status(
    insight_id="INS-0001",
    new_status="approved",
    notes="Aprovado após consulta aos agentes"
)
```

### 4. `add_agent_feedback`
Adiciona feedback de agente especialista.

**Parâmetros:**
- `insight_id` (string, obrigatório): ID do insight
- `agent_name` (string, obrigatório): Nome do agente
- `feedback` (string, obrigatório): Feedback do agente
- `recommendation` (string): Recomendação específica

**Exemplo:**
```python
add_agent_feedback(
    insight_id="INS-0001",
    agent_name="agente-transfer",
    feedback="Implementação simples, estimada em 30min",
    recommendation="Aprovar com prioridade média"
)
```

### 5. `make_decision`
Registra decisão final sobre insight.

**Parâmetros:**
- `insight_id` (string, obrigatório): ID do insight
- `decision_status` (string, obrigatório): Decisão
  - `approved`
  - `rejected`
  - `deferred`
- `rationale` (string, obrigatório): Justificativa
- `priority` (string): Prioridade (critical, high, medium, low)
- `effort_estimate` (string): Estimativa de esforço

**Exemplo:**
```python
make_decision(
    insight_id="INS-0001",
    decision_status="approved",
    rationale="Feature de alto valor, baixo esforço",
    priority="high",
    effort_estimate="2 horas"
)
```

### 6. `get_statistics`
Retorna estatísticas dos insights.

**Exemplo:**
```python
get_statistics()
```

## Estrutura de Dados

### Insight
```json
{
  "id": "INS-0001",
  "timestamp": "2026-01-25T16:30:00",
  "type": "feature",
  "complexity": "low",
  "status": "approved",
  "idea": "Adicionar busca no Transfer",
  "modules": ["transfer"],
  "agents_consulted": [
    {
      "agent": "agente-transfer",
      "timestamp": "2026-01-25T16:35:00",
      "feedback": "Implementação simples",
      "recommendation": "Aprovar"
    }
  ],
  "decision": {
    "status": "approved",
    "rationale": "Alto valor, baixo esforço",
    "priority": "high",
    "effort_estimate": "2 horas",
    "decided_at": "2026-01-25T16:40:00"
  },
  "next_steps": []
}
```

## Uso no Claude

```
Use agente-insights para capturar ideia: "Adicionar busca no Transfer"

Use agente-insights para listar insights aprovados

Use agente-insights para obter estatísticas
```

## Persistência

Os insights são salvos em:
- `/app/docs/insights_capturados.json` (dentro do container)
- Volume montado em `api/mcp-servers/docs/`

## Status do Insight

1. **captured** - Recém capturado
2. **analyzing** - Em análise pelos agentes
3. **approved** - Aprovado para implementação
4. **rejected** - Rejeitado
5. **implemented** - Já implementado
