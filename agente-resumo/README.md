# 📊 Agente de Resumo MCP

Status do projeto, progresso, relatórios e métricas em tempo real.

## Ferramentas Disponíveis

### 1. `get_project_status`
Retorna status geral do projeto.

**Parâmetros:**
- `include_details` (bool): Incluir detalhes de cada módulo (padrão: false)

**Exemplo:**
```python
get_project_status(include_details=True)
```

**Resposta:**
```json
{
  "project": "I GO Experience",
  "phase": "MVP Development",
  "overall_progress": 80,
  "modules_summary": {
    "Transfer": {"progress": 90, "status": "active"},
    "Rooming List": {"progress": 100, "status": "completed"},
    "Backend API": {"progress": 100, "status": "completed"},
    "Check-in": {"progress": 0, "status": "planned"}
  }
}
```

### 2. `get_module_status`
Status detalhado de módulo específico.

**Parâmetros:**
- `module_name` (string, obrigatório): Nome do módulo
  - Transfer
  - Rooming List
  - Backend API
  - Check-in

**Exemplo:**
```python
get_module_status(module_name="Transfer")
```

### 3. `update_module_progress`
Atualiza progresso de um módulo.

**Parâmetros:**
- `module_name` (string, obrigatório): Nome do módulo
- `progress` (int, obrigatório): Progresso em % (0-100)
- `status` (string): Status do módulo
  - active
  - completed
  - blocked
  - planned
- `notes` (string): Notas sobre a atualização

**Exemplo:**
```python
update_module_progress(
    module_name="Transfer",
    progress=95,
    status="active",
    notes="Otimizações de performance implementadas"
)
```

### 4. `get_next_steps`
Lista próximos passos priorizados.

**Parâmetros:**
- `limit` (int): Máximo de itens (padrão: 10)

**Exemplo:**
```python
get_next_steps(limit=5)
```

### 5. `add_next_step`
Adiciona novo próximo passo.

**Parâmetros:**
- `task` (string, obrigatório): Descrição da tarefa
- `priority` (string): Prioridade
  - critical
  - high
  - medium (padrão)
  - low
- `estimate` (string): Estimativa de tempo
- `module` (string): Módulo relacionado

**Exemplo:**
```python
add_next_step(
    task="Implementar cache de resultados",
    priority="high",
    estimate="4 horas",
    module="Transfer"
)
```

### 6. `generate_report`
Gera relatório formatado.

**Parâmetros:**
- `report_type` (string): Tipo de relatório
  - executive: Resumo executivo (padrão)
  - technical: Detalhes técnicos
  - onboarding: Para novos membros
  - stakeholder: Para stakeholders
- `audience` (string): Público-alvo
  - team
  - management
  - client

**Exemplo:**
```python
generate_report(report_type="executive", audience="management")
```

### 7. `get_metrics`
Retorna métricas e estatísticas do projeto.

**Exemplo:**
```python
get_metrics()
```

**Resposta:**
```json
{
  "overall_progress": 80,
  "modules": {
    "total": 4,
    "completed": 2,
    "active": 1,
    "planned": 1
  },
  "features": {
    "total": 72,
    "completed": 58,
    "remaining": 14,
    "completion_rate": 80
  },
  "next_steps": {
    "total": 3,
    "critical": 1,
    "high": 1
  },
  "blockers": 0
}
```

## Uso no Claude

### Status Rápido
```
Use agente-resumo para obter status do projeto
```

### Status de Módulo
```
Use agente-resumo para ver status do Transfer
```

### Próximos Passos
```
Use agente-resumo para listar próximos passos
```

### Relatórios
```
Use agente-resumo para gerar relatório executivo

Use agente-resumo para gerar relatório de onboarding
```

### Métricas
```
Use agente-resumo para obter métricas do projeto
```

## Persistência

Os dados são salvos em:
- `/app/docs/memoria/contexto-atual.json` - Contexto geral
- `/app/docs/memoria/progresso.json` - Progresso detalhado

Volume montado em: `api/mcp-servers/docs/`

## Status dos Módulos

- **active** - Em desenvolvimento ativo
- **completed** - 100% completo
- **blocked** - Bloqueado por dependência
- **planned** - Planejado para futuro

## Prioridades

- **critical** - Urgente, bloqueador
- **high** - Alta prioridade
- **medium** - Prioridade normal
- **low** - Pode esperar
