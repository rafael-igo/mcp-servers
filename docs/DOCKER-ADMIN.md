# Docker Admin MCP

**Container:** `igo-docker-admin`
**Localização:** `/api/mcp-servers/docker-admin`

## Descrição

MCP especializado em gerenciamento automático de infraestrutura:
- Monitoramento e controle de Docker
- Gestão automática de todos os MCPs
- Gestão da API
- Auto-healing de containers
- Logs centralizados

## Ferramentas Disponíveis

### 1. check_docker_status()

Verifica se Docker está rodando e tenta iniciar automaticamente se necessário.

**Retorno:**
```json
{
  "success": true,
  "status": "running|started|failed",
  "message": "Docker está rodando normalmente"
}
```

**Exemplo:**
```python
check_docker_status()
```

### 2. manage_mcps(action)

Gerencia todos os MCPs de uma vez.

**Parâmetros:**
- `action`: start | stop | restart | rebuild | status

**Retorno:**
```json
{
  "success": true,
  "action": "start",
  "output": "Container logs..."
}
```

**Exemplos:**
```python
# Iniciar todos os MCPs
manage_mcps("start")

# Rebuild completo
manage_mcps("rebuild")

# Ver status
manage_mcps("status")
```

### 3. manage_mcp(name, action)

Gerencia um MCP específico.

**Parâmetros:**
- `name`: Nome do MCP (ex: excel-server, agente-orchestrator)
- `action`: start | stop | restart | rebuild | logs

**Retorno:**
```json
{
  "success": true,
  "mcp": "excel-server",
  "action": "restart",
  "output": "Container restarted"
}
```

**Exemplos:**
```python
# Reiniciar excel-server
manage_mcp("excel-server", "restart")

# Ver logs do agente-orchestrator
manage_mcp("agente-orchestrator", "logs")

# Rebuild do memory-manager
manage_mcp("memory-manager", "rebuild")
```

### 4. manage_api(action)

Gerencia a API do projeto.

**Parâmetros:**
- `action`: start | stop | restart | rebuild | status | logs

**Retorno:**
```json
{
  "success": true,
  "action": "start",
  "output": "API started"
}
```

**Exemplos:**
```python
# Iniciar API
manage_api("start")

# Ver logs
manage_api("logs")

# Rebuild
manage_api("rebuild")
```

### 5. health_check()

Verifica saúde completa da infraestrutura e executa auto-healing.

**Retorno:**
```json
{
  "success": true,
  "timestamp": "2026-01-25 18:00:00",
  "docker": {"running": true},
  "mcps": {
    "igo-excel-server": "running",
    "igo-agente-orchestrator": "running"
  },
  "api": {"running": true},
  "actions_taken": ["Container X reiniciado"],
  "overall_health": "healthy|recovered"
}
```

**Exemplo:**
```python
health_check()
```

### 6. get_logs(service, lines)

Obtém logs de um serviço específico.

**Parâmetros:**
- `service`: Nome do serviço/container
- `lines`: Número de linhas (padrão: 50)

**Retorno:**
```json
{
  "success": true,
  "service": "excel-server",
  "lines": 50,
  "logs": "Container logs..."
}
```

**Exemplos:**
```python
# Últimas 50 linhas
get_logs("excel-server", 50)

# Últimas 100 linhas
get_logs("agente-orchestrator", 100)
```

### 7. auto_heal()

Executa auto-healing completo da infraestrutura.

**O que faz:**
1. Verifica Docker e inicia se necessário
2. Detecta containers parados e reinicia
3. Identifica containers com falha e faz rebuild
4. Retorna relatório completo

**Retorno:**
```json
{
  "success": true,
  "timestamp": "2026-01-25 18:00:00",
  "actions_taken": [
    {"action": "start_docker", "status": "success"},
    {"action": "rebuild_failed_containers", "status": "success"}
  ],
  "message": "Auto-healing completo. 2 ações executadas."
}
```

**Exemplo:**
```python
auto_heal()
```

## Casos de Uso

### Startup Automático

Quando você pedir para trabalhar em algo e os MCPs estiverem parados:

```python
# Garante que tudo está funcionando
auto_heal()
```

### Problema em Container Específico

```python
# Ver logs do problema
get_logs("excel-server", 100)

# Tentar reiniciar
manage_mcp("excel-server", "restart")

# Se não resolver, rebuild
manage_mcp("excel-server", "rebuild")
```

### Atualização de Código

```python
# Rebuild de tudo após mudanças
manage_mcps("rebuild")
```

### Monitoramento de Saúde

```python
# Verificação periódica
health_check()
```

## Integração Automática

O docker-admin pode ser chamado automaticamente:

1. **Ao iniciar qualquer tarefa:** Verifica saúde primeiro
2. **Ao detectar erro:** Tenta auto-healing
3. **Ao fazer mudanças:** Rebuild automático

## Exemplo de Workflow

```python
# 1. Garantir infraestrutura OK
health_check()

# 2. Trabalhar no código
# ... fazer alterações ...

# 3. Rebuild do serviço modificado
manage_mcp("excel-server", "rebuild")

# 4. Verificar logs
get_logs("excel-server", 50)

# 5. Se tudo OK, continuar
# Se houver problema, auto_heal()
```

## Notas Técnicas

- Container roda com `privileged: true` para gerenciar Docker
- Tem acesso ao socket do Docker: `/var/run/docker.sock`
- Timeout de 30s para comandos (previne travamentos)
- Auto-restart em caso de falha
