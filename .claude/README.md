# Claude Code Configuration

## Arquivos nesta pasta

### settings.local.json
Configurações locais do Claude Code, incluindo permissões para ferramentas MCP.

**Permissões configuradas:**
- Comandos Docker e Docker Compose
- Todos os comandos do `docker-admin` MCP
- Todos os comandos do `agente-orchestrator` MCP
- Comandos de leitura/contexto do `memory-manager`
- Comandos de status/métricas do `agente-resumo`
- Captura de insights do `agente-insights`
- Validação de checklists
- Todos os comandos do `excel-server`

## Como Adicionar Novas Permissões

Edite `settings.local.json` e adicione à lista `permissions.allow`:

### Padrões de Permissões

#### Permitir todos comandos de um MCP
```json
"mcp__nome-do-mcp__*"
```

#### Permitir comando específico
```json
"mcp__nome-do-mcp__nome_da_funcao"
```

#### Permitir comandos Bash específicos
```json
"Bash(comando:*)"
```

### Exemplos

```json
{
  "permissions": {
    "allow": [
      // Todos comandos Docker
      "Bash(docker:*)",

      // Apenas docker ps
      "Bash(docker ps:*)",

      // Todos comandos de um MCP
      "mcp__docker-admin__*",

      // Comando específico
      "mcp__memory-manager__load_context",

      // PowerShell commands
      "Bash(powershell:*)"
    ]
  }
}
```

## MCPs Disponíveis

1. `docker-admin` - Administração Docker
2. `agente-orchestrator` - Orquestração de agentes
3. `memory-manager` - Gerenciamento de memória
4. `checklist-validator` - Validação de checklists
5. `agente-insights` - Captura de insights
6. `agente-resumo` - Resumos e status
7. `excel-server` - Processamento Excel
8. `igo-openai-gateway` - Gateway OpenAI/GPT-5.2

## Flag enableAllProjectMcpServers

Quando `true`, habilita automaticamente todos os MCPs configurados no `.mcp.json` do projeto.

```json
{
  "enableAllProjectMcpServers": true
}
```

## Troubleshooting

### Claude Code não encontra MCPs
1. Verifique se Docker está rodando
2. Execute: `docker-compose ps`
3. Verifique `.mcp.json` na raiz do projeto

### Permissões negadas
1. Adicione a permissão necessária em `permissions.allow`
2. Reload window do VSCode
3. Tente novamente

### MCPs não inicializam
Execute no terminal:
```bash
docker-compose up -d
```

Ou use Claude Code:
```
docker-admin.health_check()
docker-admin.auto_heal()
```
