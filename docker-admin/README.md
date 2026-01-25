# Docker Admin MCP

Gerenciamento automático de Docker, MCPs e API com auto-healing e sincronização de configuração.

## 🎯 Funcionalidades

### 1. Gerenciamento de Docker
- `check_docker_status()` - Verifica e inicia Docker se necessário
- `health_check()` - Verificação completa com auto-correção
- `auto_heal()` - Auto-healing completo da infraestrutura

### 2. Gerenciamento de MCPs

#### Todos os MCPs
- `manage_mcps(action)` - Gerencia todos os MCPs
  - `action`: start | stop | restart | rebuild | status

#### MCP Específico
- `manage_mcp(name, action)` - Gerencia um MCP específico
  - `name`: excel-server, agente-orchestrator, memory-manager, etc.
  - `action`: start | stop | restart | rebuild | logs

### 3. Sincronização de Configuração (.mcp.json) ⭐ NOVO

#### `get_mcp_status()`
Retorna status completo dos MCPs:
- Status dos containers Docker
- Configuração no .mcp.json
- Problemas de sincronização

**Exemplo de uso:**
```python
# Verificar status completo
status = get_mcp_status()
```

**Retorno:**
```json
{
  "success": true,
  "containers": {
    "excel-server": {"state": "running", "status": "Up 5 minutes"},
    "docker-admin": {"state": "running", "status": "Up 5 minutes"}
  },
  "config": {
    "exists": true,
    "servers": ["excel-server", "docker-admin", "agente-orchestrator"]
  },
  "sync_issues": [],
  "is_synced": true
}
```

#### `sync_mcp_config()` ⭐ PRINCIPAL
**Sincroniza automaticamente o .mcp.json com os containers em execução.**

- Detecta todos os containers MCP rodando
- Gera configuração correta para cada um
- Atualiza o arquivo .mcp.json
- Garante que Claude Code tenha acesso a todos os MCPs

**Quando usar:**
- Após reiniciar/atualizar containers
- Quando adicionar novos MCPs
- Se o .mcp.json estiver desatualizado

**Exemplo de uso:**
```python
# Sincronizar configuração
result = sync_mcp_config()
```

**Retorno:**
```json
{
  "success": true,
  "message": "Configuração .mcp.json atualizada com 7 MCPs",
  "mcps_configured": [
    "excel-server",
    "docker-admin",
    "agente-orchestrator",
    "memory-manager",
    "checklist-validator",
    "agente-insights",
    "agente-resumo"
  ],
  "config_path": "/project/.mcp.json"
}
```

#### `verify_mcp_config()`
Verifica se a configuração está sincronizada.

**Exemplo de uso:**
```python
# Verificar sincronização
verification = verify_mcp_config()
```

**Retorno:**
```json
{
  "success": true,
  "is_synced": true,
  "containers_count": 7,
  "configured_count": 7,
  "issues": []
}
```

Se houver problemas:
```json
{
  "success": true,
  "is_synced": false,
  "issues": [
    "Container 'agente-orchestrator' rodando mas não configurado em .mcp.json"
  ],
  "recommendation": "Execute sync_mcp_config() para sincronizar"
}
```

#### `update_and_restart_mcps()` ⭐ TUDO-EM-UM
**Atualização completa com um único comando:**
1. Para todos os containers
2. Reconstrói imagens (aplica alterações)
3. Inicia containers
4. Sincroniza .mcp.json automaticamente

**Quando usar:**
- Após fazer alterações no código dos MCPs
- Para garantir que tudo está atualizado
- Reinicialização completa da infraestrutura

**Exemplo de uso:**
```python
# Atualizar tudo de uma vez
result = update_and_restart_mcps()
```

**Retorno:**
```json
{
  "success": true,
  "message": "✅ MCPs atualizados, reiniciados e configurados com sucesso!",
  "actions": [
    {"step": "stop", "success": true},
    {"step": "rebuild", "success": true},
    {"step": "sync_config", "success": true}
  ],
  "mcps_configured": ["excel-server", "docker-admin", ...]
}
```

### 4. Gerenciamento de API
- `manage_api(action)` - Gerencia a API do projeto
  - `action`: start | stop | restart | rebuild | status | logs

### 5. Logs
- `get_logs(service, lines)` - Obtém logs de um serviço
  - `lines`: Número de linhas (padrão: 50)

## 🚀 Fluxo de Trabalho Recomendado

### Cenário 1: Atualizar MCPs após alterações
```python
# Opção 1: Comando único (RECOMENDADO)
update_and_restart_mcps()

# Opção 2: Passo a passo
manage_mcps("stop")
manage_mcps("rebuild")
sync_mcp_config()
```

### Cenário 2: Verificar se MCPs estão rodando
```python
# Verificar status
status = get_mcp_status()

# Se não estiverem sincronizados
if not status["is_synced"]:
    sync_mcp_config()
```

### Cenário 3: Adicionar novo MCP
1. Criar pasta em `/api/mcp-servers/novo-mcp`
2. Adicionar ao docker-compose.yml
3. Executar:
```python
manage_mcps("rebuild")
sync_mcp_config()
```

## 📋 Permissões e Configuração

### Permissões do Container
O docker-admin roda com:
- `privileged: true` - Necessário para gerenciar Docker
- Volume `/var/run/docker.sock` - Acesso ao Docker daemon
- Volume `/project/.mcp.json` - Acesso ao arquivo de configuração

### Auto-atualização do .mcp.json
O docker-admin tem permissão para:
- Ler containers em execução
- Atualizar o arquivo .mcp.json
- Garantir sincronização automática

## 🔧 Troubleshooting

### MCPs não aparecem no Claude Code
```python
# 1. Verificar se containers estão rodando
manage_mcps("status")

# 2. Sincronizar configuração
sync_mcp_config()

# 3. Reiniciar Claude Code para recarregar .mcp.json
```

### Container não inicia
```python
# Ver logs do container
get_logs("nome-do-mcp", 100)

# Tentar rebuild
manage_mcp("nome-do-mcp", "rebuild")
```

### .mcp.json desatualizado
```python
# Verificar problemas
verify_mcp_config()

# Corrigir automaticamente
sync_mcp_config()
```

## 📊 Monitoramento

### Health Check Automático
O docker-admin monitora continuamente:
- Status do Docker
- Containers parados (reinicia automaticamente)
- Sincronização do .mcp.json

```python
# Executar health check manual
health_check()

# Auto-healing completo
auto_heal()
```

## 🎯 Resumo dos Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `update_and_restart_mcps()` | **Atualiza tudo** (rebuild + restart + sync) |
| `sync_mcp_config()` | Sincroniza .mcp.json com containers |
| `get_mcp_status()` | Status completo (containers + config) |
| `verify_mcp_config()` | Verifica sincronização |
| `manage_mcps("restart")` | Reinicia todos os MCPs |
| `health_check()` | Verifica saúde da infraestrutura |

## 📝 Notas Importantes

1. **Sempre sincronize após mudanças**: Após qualquer alteração nos containers, execute `sync_mcp_config()`
2. **Reinicie Claude Code**: Após atualizar .mcp.json, reinicie Claude Code para aplicar
3. **Use update_and_restart_mcps()**: Para atualizações completas, use este comando único
4. **Verifique logs**: Se algo falhar, use `get_logs()` para investigar

## 🔗 Integração com Outros MCPs

O docker-admin trabalha em conjunto com:
- **agente-orchestrator**: Orquestração de agentes
- **memory-manager**: Gestão de memória persistente
- **checklist-validator**: Validação de checklists
- **agente-insights**: Captura de insights
- **agente-resumo**: Relatórios e métricas
- **excel-server**: Leitura de arquivos Excel
