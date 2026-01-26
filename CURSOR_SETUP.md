# Configuração do Cursor para MCPs

## Passo 1: Instalar Cursor

Se ainda não instalou:
1. Download: https://cursor.sh
2. Instale e abra o projeto
3. Cursor automaticamente detecta `.cursorrules`

## Passo 2: Configurar MCPs no Cursor

### Opção A: Via UI (Recomendado)

1. Abra Settings (Cmd/Ctrl + ,)
2. Busque "MCP"
3. Adicione o caminho do `.mcp.json`:
   ```
   /caminho/para/mcp-servers/.mcp.json
   ```

### Opção B: Via settings.json

Abra settings do Cursor e adicione:

```json
{
  "mcp.configPath": "${workspaceFolder}/.mcp.json",
  "mcp.enabled": true,
  "mcp.autoStart": true
}
```

## Passo 3: Verificar Configuração

1. Abra o Chat do Cursor (Cmd/Ctrl + L)
2. Digite:
   ```
   Use docker-admin.health_check() para verificar MCPs
   ```
3. Se funcionar, está configurado corretamente!

## Passo 4: Ativar .cursorrules

O arquivo `.cursorrules` já existe na raiz. O Cursor o carrega automaticamente.

Para verificar:
1. Abra Command Palette (Cmd/Ctrl + Shift + P)
2. Digite "Cursor: Show Rules"
3. Você deve ver as regras carregadas

## Features Exclusivas do Cursor

### 1. Cmd K para Edição Inline
1. Selecione código
2. Pressione `Cmd/Ctrl + K`
3. Peça para usar MCPs:
   - "Use agente-arquiteto-igo para revisar isso"
   - "Use igo-openai-gateway para analisar bugs"

### 2. Chat com Contexto do Projeto
O Cursor mantém contexto entre mensagens:
```
Você: Carregue o contexto do projeto
Cursor: [usa memory-manager.load_context()]

Você: Quais são os próximos passos?
Cursor: [usa agente-resumo.get_next_steps()]

Você: Crie um checklist para a feature X
Cursor: [usa checklist-validator.create_checklist()]
```

### 3. Composer Mode
1. Cmd/Ctrl + Shift + I
2. Abre editor multi-arquivo
3. Pode usar MCPs em múltiplos arquivos simultaneamente

### 4. Terminal Integration
O Cursor pode sugerir comandos Docker automaticamente:
```
Você: Os MCPs estão rodando?
Cursor: Vou verificar [executa docker-compose ps]
```

## Configurações Recomendadas

Adicione ao `settings.json` do Cursor:

```json
{
  // MCPs
  "mcp.configPath": "${workspaceFolder}/.mcp.json",
  "mcp.enabled": true,
  "mcp.autoStart": true,

  // AI Features
  "cursor.chat.model": "claude-3.5-sonnet",
  "cursor.composer.model": "claude-3.5-sonnet",
  "cursor.autocomplete.enabled": true,

  // Python
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",

  // Editor
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },

  // Git
  "git.enableSmartCommit": true,
  "git.confirmSync": false,

  // Files
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/.ruff_cache": true
  }
}
```

## Atalhos Essenciais do Cursor

| Atalho | Ação |
|--------|------|
| `Cmd/Ctrl + K` | Edit inline com AI |
| `Cmd/Ctrl + L` | Open chat |
| `Cmd/Ctrl + Shift + L` | Open chat com código selecionado |
| `Cmd/Ctrl + I` | Composer mode |
| `Cmd/Ctrl + Shift + I` | Composer multi-file |
| `Cmd/Ctrl + .` | Quick fix |

## Workflows com Cursor

### Workflow 1: Code Review com MCP
```
1. Selecione código para review
2. Cmd/Ctrl + K
3. Digite: "Use igo-openai-gateway.run_code_analysis para revisar com reasoning alto"
4. Cursor analisa e sugere mudanças inline
```

### Workflow 2: Criar Feature com Agentes
```
1. Cmd/Ctrl + L (abrir chat)
2. "Quero criar feature X, consulte o agente-arquiteto-igo"
3. Cursor usa agente-orchestrator.invoke_agent
4. Recebe plano arquitetural
5. "Agora consulte agente-frontend-igo para componentes"
6. Cursor implementa componentes
7. "Use agente-qa-testes para gerar testes"
```

### Workflow 3: Debugging com Contexto
```
1. Cmd/Ctrl + L
2. "Carregue o contexto do projeto com memory-manager"
3. Cole o código com bug
4. "Use igo-openai-gateway.run_code_analysis com type=debug e reasoning=high"
5. Recebe análise detalhada
6. "Aplique as sugestões"
```

### Workflow 4: Documentação Automática
```
1. Selecione função
2. Cmd/Ctrl + K
3. "Gere docstring no formato Google"
4. Cursor gera inline
```

## Dicas Específicas do Cursor

### 1. Use @-mentions no Chat
```
@workspace: Inclui contexto de todo workspace
@folder: Contexto de pasta específica
@file: Contexto de arquivo específico
@code: Código selecionado
```

Exemplo:
```
@workspace Use memory-manager.load_context e me dê um resumo do projeto
```

### 2. Aproveite o Autocomplete
Cursor sugere código enquanto você digita. Ele entende os MCPs:
```python
# Apenas comece a digitar:
def check_status():
    # Cursor sugere: docker-admin.health_check()
```

### 3. Multi-file Editing no Composer
1. Cmd/Ctrl + Shift + I
2. "Refatore o módulo X usando agente-backend"
3. Cursor edita múltiplos arquivos relacionados
4. Review e accept/reject cada mudança

### 4. Regras Personalizadas
Além do `.cursorrules`, você pode adicionar regras por pasta:

```
mcp-servers/excel-server/.cursorrules
```

Conteúdo:
```
Quando trabalhar neste MCP:
- Sempre adicione type hints
- Sempre adicione docstrings
- Sempre adicione error handling
- Teste com pytest
```

## Integração com Docker

### Ver Status de Containers
No chat:
```
Mostre status de todos os containers MCP
```

Cursor executa:
```bash
docker-compose ps
```

### Auto-healing
```
Os MCPs não estão respondendo
```

Cursor automaticamente:
1. `docker-admin.check_docker_status()`
2. `docker-admin.auto_heal()`
3. Reporta resultados

## Troubleshooting Cursor

### MCPs não aparecem no Cursor
1. Verifique `mcp.configPath` em settings
2. Restart Cursor
3. Check `.mcp.json` existe e é válido

### Cursor não usa MCPs automaticamente
1. Seja explícito: "Use o MCP X para..."
2. Verifique `.cursorrules` está sendo lido
3. Settings → MCP → Enabled deve estar ✓

### Performance lenta
1. Settings → MCPs → Desative MCPs não usados temporariamente
2. Use `reasoning_effort="low"` em análises simples
3. Limite contexto com @mentions específicos

### Erro de permissão
1. Verifique Docker está rodando
2. Containers estão up: `docker-compose ps`
3. Logs: `docker-compose logs [service]`

## Diferenças: Cursor vs VSCode vs Codex

| Feature | Cursor | VSCode + Claude Code | Codex |
|---------|--------|---------------------|-------|
| MCPs | ✅ Nativo | ✅ Via Extension | ✅ Via PR |
| Inline Edit | ✅ Cmd+K | ⚠️ Limitado | ❌ Não |
| Composer | ✅ Sim | ❌ Não | ❌ Não |
| Autocomplete AI | ✅ Sim | ⚠️ Copilot | ✅ Sim |
| Chat Persistente | ✅ Sim | ✅ Sim | ❌ Por PR |
| Multi-file Edit | ✅ Sim | ⚠️ Manual | ❌ Não |
| @-mentions | ✅ Sim | ❌ Não | ⚠️ Limitado |

## Recursos Adicionais

- [Cursor Docs](https://docs.cursor.sh)
- [Cursor Discord](https://discord.gg/cursor)
- [GUIDELINES.md](GUIDELINES.md) - Guidelines gerais
- [.cursorrules](.cursorrules) - Regras ativas

## Template de Pergunta Otimizada

Para melhor uso dos MCPs no Cursor:

```
Contexto: [descrição breve]

Objetivo: [o que quer fazer]

MCPs relevantes:
- [listar MCPs que podem ajudar]

Passos:
1. [passo 1 usando MCP X]
2. [passo 2 usando MCP Y]
3. [etc]

Entregável: [o que espera como resultado]
```

Exemplo:
```
Contexto: Implementando módulo de Transfer

Objetivo: Revisar arquitetura antes de implementar

MCPs relevantes:
- agente-orchestrator (consultar agente-arquiteto-igo)
- memory-manager (carregar contexto)
- igo-openai-gateway (análise profunda)

Passos:
1. Carregar contexto do projeto
2. Consultar agente-arquiteto-igo sobre módulo Transfer
3. Usar igo-openai-gateway para análise arquitetural com reasoning xhigh
4. Capturar insights e decisões

Entregável: Plano arquitetural detalhado + ADRs registradas
```

---

**Pronto!** Agora o Cursor está configurado para usar todos os 8 MCPs com máxima eficiência.
