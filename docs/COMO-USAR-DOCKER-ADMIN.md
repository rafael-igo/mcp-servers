# Como Usar o docker-admin MCP

## Uso Básico

O docker-admin é chamado **automaticamente** quando você precisa trabalhar com Docker ou MCPs.

### Quando Começar uma Tarefa

Sempre que você pedir para trabalhar em algo, o docker-admin será ativado para:

1. **Verificar Docker está rodando**
2. **Garantir MCPs estão ativos**
3. **Auto-corrigir problemas**

```python
# Chamada automática ao iniciar trabalho
auto_heal()
```

### Cenários Comuns

#### 1. Containers Parados

Se algum MCP parar:

```python
# Verifica e reinicia automaticamente
health_check()
```

#### 2. Após Mudanças no Código

Quando você fizer alterações em um MCP:

```python
# Rebuild do MCP específico
manage_mcp("excel-server", "rebuild")
```

#### 3. Problemas Gerais

Se algo não funcionar:

```python
# Auto-healing completo
auto_heal()
```

#### 4. Ver Logs de Erro

```python
# Últimas 100 linhas de um MCP
get_logs("agente-orchestrator", 100)
```

#### 5. Restart Completo

```python
# Reinicia todos os MCPs
manage_mcps("restart")
```

## Comandos Disponíveis

### check_docker_status()
Verifica se Docker está rodando, inicia se necessário.

```python
check_docker_status()
# Retorna: {"status": "running|started", "success": true}
```

### manage_mcps(action)
Gerencia todos os MCPs.

**Ações:** `start`, `stop`, `restart`, `rebuild`, `status`

```python
# Ver status
manage_mcps("status")

# Rebuild tudo
manage_mcps("rebuild")

# Parar todos
manage_mcps("stop")

# Iniciar todos
manage_mcps("start")
```

### manage_mcp(name, action)
Gerencia MCP específico.

**Ações:** `start`, `stop`, `restart`, `rebuild`, `logs`

```python
# Reiniciar excel-server
manage_mcp("excel-server", "restart")

# Ver logs
manage_mcp("agente-orchestrator", "logs")

# Rebuild
manage_mcp("memory-manager", "rebuild")
```

### health_check()
Verifica saúde completa e auto-corrige.

```python
health_check()
# Retorna:
# {
#   "docker": {"running": true},
#   "mcps": {"igo-excel-server": "running"},
#   "actions_taken": [...],
#   "overall_health": "healthy"
# }
```

### get_logs(service, lines)
Obtém logs de um serviço.

```python
# Últimas 50 linhas (padrão)
get_logs("excel-server", 50)

# Últimas 200 linhas
get_logs("agente-orchestrator", 200)
```

### auto_heal()
Auto-healing completo da infraestrutura.

```python
auto_heal()
# Executa:
# 1. Inicia Docker se parado
# 2. Verifica saúde de todos MCPs
# 3. Reinicia containers parados
# 4. Rebuild de containers com falha
# 5. Retorna relatório completo
```

### manage_api(action)
Gerencia API (se usar Docker).

**Ações:** `start`, `stop`, `restart`, `rebuild`, `status`, `logs`

```python
manage_api("restart")
manage_api("logs")
```

## Fluxo de Trabalho Recomendado

### Ao Iniciar o Dia

```python
# 1. Garantir tudo está funcionando
auto_heal()

# 2. Verificar status
manage_mcps("status")
```

### Durante Desenvolvimento

```python
# 1. Fazer mudanças no código
# ... editar arquivos ...

# 2. Rebuild do serviço modificado
manage_mcp("excel-server", "rebuild")

# 3. Ver logs para confirmar
get_logs("excel-server", 50)
```

### Troubleshooting

```python
# 1. Ver logs do problema
get_logs("nome-do-mcp", 100)

# 2. Tentar restart
manage_mcp("nome-do-mcp", "restart")

# 3. Se não resolver, rebuild
manage_mcp("nome-do-mcp", "rebuild")

# 4. Se ainda houver problema, auto-heal completo
auto_heal()
```

## Automação

O docker-admin pode ser configurado para:

### 1. Verificação Periódica

```python
# A cada X minutos, verificar saúde
health_check()
```

### 2. Auto-Rebuild Após Git Pull

```python
# Após atualizar código
manage_mcps("rebuild")
```

### 3. Recuperação Automática

```python
# Se detectar falha, tentar recuperar
auto_heal()
```

## Notas Técnicas

- Container roda com `privileged: true`
- Tem acesso ao socket do Docker
- Timeout de 30s por comando
- Auto-restart em caso de falha
- Logs persistidos em `/app/docs`

## Exemplos Práticos

### Exemplo 1: Atualização de Código

```python
# Você fez mudanças no agente-orchestrator

# 1. Rebuild
manage_mcp("agente-orchestrator", "rebuild")

# 2. Verificar logs
get_logs("agente-orchestrator", 50)

# 3. Se OK, continuar trabalhando
# Se erro, ver logs completos
get_logs("agente-orchestrator", 200)
```

### Exemplo 2: Container Travado

```python
# Um container não responde

# 1. Ver logs primeiro
get_logs("memory-manager", 100)

# 2. Tentar restart
manage_mcp("memory-manager", "restart")

# 3. Se não resolver, rebuild
manage_mcp("memory-manager", "rebuild")
```

### Exemplo 3: Tudo Parado

```python
# Nada funciona

# 1. Auto-healing completo
auto_heal()

# 2. Ver relatório
# O auto_heal retorna todas ações tomadas

# 3. Verificar status final
manage_mcps("status")
```

## Integração com Outros MCPs

O docker-admin trabalha **em conjunto** com outros MCPs:

```python
# 1. Garantir infraestrutura OK
health_check()

# 2. Usar outros MCPs normalmente
# - read_excel_tabs(...)
# - invoke_agent(...)
# - save_context(...)

# 3. Se houver problema, docker-admin resolve
auto_heal()
```

## FAQ

**P: Quando o docker-admin é chamado?**
R: Automaticamente quando você precisar trabalhar com Docker/MCPs.

**P: Preciso gerenciar containers manualmente?**
R: Não. O docker-admin faz tudo automaticamente.

**P: E se o Docker estiver parado?**
R: O docker-admin tenta iniciar automaticamente.

**P: Como ver se há problemas?**
R: Use `health_check()` - retorna relatório completo.

**P: Posso rebuild tudo de uma vez?**
R: Sim. `manage_mcps("rebuild")`

**P: Como ver logs de erro?**
R: `get_logs("nome-do-mcp", 100)`
