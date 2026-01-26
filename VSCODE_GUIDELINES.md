# VSCode Guidelines - MCPs Project

## Extensões Recomendadas

### Essenciais
- **Claude Code Extension** - Integração nativa com MCPs
- **Docker** - Gerenciar containers visualmente
- **Python** - Suporte completo Python
- **Pylance** - Type checking e IntelliSense
- **Remote - Containers** - Desenvolvimento em containers

### Úteis
- **GitLens** - Git super-powered
- **Error Lens** - Erros inline
- **Todo Tree** - Gerenciar TODOs
- **Thunder Client** - Testar APIs

## Configuração do VSCode

### settings.json
```json
{
  // Python
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,

  // Editor
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "editor.rulers": [88, 120],

  // Files
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/.ruff_cache": true,
    "**/node_modules": true
  },

  // Docker
  "docker.showStartPage": false,

  // Git
  "git.enableSmartCommit": true,
  "git.confirmSync": false
}
```

### tasks.json
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start All MCPs",
      "type": "shell",
      "command": "docker-compose up -d",
      "problemMatcher": [],
      "group": {
        "kind": "build",
        "isDefault": true
      }
    },
    {
      "label": "Stop All MCPs",
      "type": "shell",
      "command": "docker-compose down",
      "problemMatcher": []
    },
    {
      "label": "MCP Health Check",
      "type": "shell",
      "command": "docker-compose ps",
      "problemMatcher": []
    },
    {
      "label": "View MCP Logs",
      "type": "shell",
      "command": "docker-compose logs -f",
      "problemMatcher": []
    }
  ]
}
```

### launch.json
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Debug MCP Server",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/${input:mcpServer}/server.py",
      "console": "integratedTerminal",
      "justMyCode": false
    },
    {
      "name": "Python: Pytest Current File",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["${file}", "-v"],
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ],
  "inputs": [
    {
      "id": "mcpServer",
      "type": "pickString",
      "description": "Select MCP Server",
      "options": [
        "excel-server",
        "agente-orchestrator",
        "memory-manager",
        "checklist-validator",
        "agente-insights",
        "agente-resumo",
        "docker-admin",
        "igo-openai-gateway"
      ]
    }
  ]
}
```

## Atalhos de Teclado Úteis

### Claude Code
- `Cmd/Ctrl + Shift + P` → "Claude Code: Start Chat"
- `Cmd/Ctrl + K` → Quick command
- `Cmd/Ctrl + L` → Open Claude panel

### Docker
- `Cmd/Ctrl + Shift + P` → "Docker: Compose Up"
- `Cmd/Ctrl + Shift + P` → "Docker: View Logs"
- `Cmd/Ctrl + Shift + P` → "Docker: Prune System"

### Git
- `Cmd/Ctrl + Shift + G` → Source Control
- `Cmd/Ctrl + Enter` → Commit
- `Cmd/Ctrl + Shift + P` → "Git: Pull"

## Workflow no VSCode

### 1. Início do Dia
```bash
# Terminal integrado (Ctrl + `)
docker-compose up -d
```

Ou use Task: `Cmd/Ctrl + Shift + P` → "Tasks: Run Task" → "Start All MCPs"

### 2. Verificar Status
Na paleta de comandos:
1. Abrir Claude Code chat
2. Executar:
```
docker-admin.health_check()
memory-manager.load_context()
agente-resumo.get_next_steps()
```

### 3. Durante Desenvolvimento

#### Explorar Código
- `Cmd/Ctrl + P` → Quick Open
- `Cmd/Ctrl + T` → Go to Symbol
- `Cmd/Ctrl + Shift + F` → Search in files
- `F12` → Go to Definition
- `Shift + F12` → Find References

#### Com Claude Code
- Selecione código
- `Cmd/Ctrl + K` → Pergunte ao Claude
- Use comandos inline: `/edit`, `/review`, `/explain`

#### Invocar Agentes
No Claude Code chat:
```python
# Análise de arquitetura
agente-orchestrator.invoke_agent(
    agent_name="agente-arquiteto-igo",
    task="Revisar essa implementação"
)

# Code review
igo-openai-gateway.run_code_analysis(
    code="[código selecionado]",
    analysis_type="review",
    reasoning_effort="high"
)
```

### 4. Debugging

#### Python Debug
1. Set breakpoints: `F9`
2. Start debugging: `F5`
3. Step over: `F10`
4. Step into: `F11`
5. Continue: `F5`

#### Docker Logs
- View → Docker → Right-click container → "View Logs"
- Ou terminal: `docker-compose logs -f [service-name]`

### 5. Testes

#### Rodar Testes
- `Cmd/Ctrl + Shift + P` → "Python: Run All Tests"
- Ou terminal: `pytest tests/`
- Debug test: Click on "Debug Test" acima da função

#### Gerar Testes
No Claude Code:
```python
igo-openai-gateway.generate_tests(
    code="[código selecionado]",
    test_type="unit",
    framework="pytest"
)
```

### 6. Git Workflow

#### Commit
1. `Cmd/Ctrl + Shift + G` → Source Control
2. Stage changes (+ icon)
3. Write message
4. `Cmd/Ctrl + Enter` → Commit

#### Com Claude Code
```python
# Claude pode ajudar com mensagem de commit
# Selecione as mudanças e peça:
"Gere uma mensagem de commit para essas mudanças"
```

### 7. Fim do Dia
No Claude Code:
```python
# Salvar contexto
memory-manager.save_context(
    module="Transfer",
    status="in_progress",
    details="Implementado validação de dados"
)

# Adicionar próximos passos
agente-resumo.add_next_step(
    task="Completar testes de integração",
    priority="high",
    estimate="2h"
)
```

## Snippets Úteis

### Python Snippets
Crie em: `.vscode/python.json`

```json
{
  "MCP Tool Function": {
    "prefix": "mcptool",
    "body": [
      "@mcp.tool()",
      "async def ${1:function_name}(${2:params}) -> dict:",
      "    \"\"\"",
      "    ${3:Description}",
      "    ",
      "    Args:",
      "        ${4:arg}: ${5:description}",
      "    ",
      "    Returns:",
      "        JSON ${6:description}",
      "    \"\"\"",
      "    try:",
      "        ${7:# Implementation}",
      "        return {\"success\": True, \"data\": ${8:result}}",
      "    except Exception as e:",
      "        return {\"success\": False, \"error\": str(e)}"
    ]
  },
  "Async Function with Logging": {
    "prefix": "aflog",
    "body": [
      "async def ${1:function_name}(${2:params}) -> ${3:ReturnType}:",
      "    \"\"\"${4:Description}\"\"\"",
      "    logger.info(f\"${5:Starting} {${6:param}}\")",
      "    try:",
      "        ${7:# Implementation}",
      "        logger.info(\"${8:Completed successfully}\")",
      "        return ${9:result}",
      "    except Exception as e:",
      "        logger.error(f\"Error: {e}\")",
      "        raise"
    ]
  }
}
```

## Multi-root Workspace

Para trabalhar com múltiplos MCPs simultaneamente:

### workspace.code-workspace
```json
{
  "folders": [
    {
      "name": "Root",
      "path": "."
    },
    {
      "name": "Excel Server",
      "path": "excel-server"
    },
    {
      "name": "Memory Manager",
      "path": "memory-manager"
    },
    {
      "name": "Docker Admin",
      "path": "docker-admin"
    },
    {
      "name": "Docs",
      "path": "docs"
    }
  ],
  "settings": {
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python"
  }
}
```

## Terminal Integrado

### Múltiplos Terminais
1. Docker Logs: `docker-compose logs -f`
2. Python REPL: `python`
3. Git: Para comandos git
4. General: Para comandos gerais

### Shell Tasks
Adicione ao `tasks.json`:
```json
{
  "label": "Quick MCP Test",
  "type": "shell",
  "command": "python -c 'import sys; sys.path.insert(0, \"${input:mcpServer}\"); from server import *; print(\"MCP loaded successfully\")'",
  "problemMatcher": []
}
```

## Dicas de Produtividade

### 1. Use Claude Code para Code Review
Antes de commit:
1. Selecione mudanças
2. `Cmd/Ctrl + K`
3. "Review this code for issues"

### 2. Navegação Rápida
- `Cmd/Ctrl + P` + `@` → Symbols in file
- `Cmd/Ctrl + P` + `#` → Symbols in workspace
- `Cmd/Ctrl + P` + `:` → Go to line

### 3. Multi-cursor Editing
- `Alt + Click` → Add cursor
- `Cmd/Ctrl + Alt + Up/Down` → Add cursor above/below
- `Cmd/Ctrl + D` → Select next occurrence

### 4. Integração com MCPs
Use Claude Code para:
- Gerar código: "Generate a function to..."
- Explicar: "Explain this code"
- Refatorar: "Refactor this to use async/await"
- Testes: "Generate unit tests for this"

### 5. Git Lens Features
- Inline blame
- File history
- Compare with previous version
- Search commits

## Troubleshooting no VSCode

### Claude Code não conecta aos MCPs
1. Verificar Docker: `docker-compose ps`
2. No Claude Code: `docker-admin.health_check()`
3. Restart MCPs: `docker-admin.manage_mcps("restart")`

### Python IntelliSense não funciona
1. Select interpreter: `Cmd/Ctrl + Shift + P` → "Python: Select Interpreter"
2. Escolha a venv do projeto
3. Reload window: `Cmd/Ctrl + Shift + P` → "Reload Window"

### Docker não aparece
1. Verificar Docker Desktop está rodando
2. Restart VSCode
3. Reinstalar extensão Docker

### Testes não aparecem
1. `Cmd/Ctrl + Shift + P` → "Python: Configure Tests"
2. Selecione pytest
3. Root directory: `./tests`

## Recursos Adicionais

### Extensions Marketplace
- Claude Code: Busque "Claude Code"
- Docker: Busque "Docker"
- Python: Busque "Python"

### Documentação
- [VSCode Python](https://code.visualstudio.com/docs/python/python-tutorial)
- [VSCode Docker](https://code.visualstudio.com/docs/containers/overview)
- [Claude Code Docs](https://docs.anthropic.com/claude/docs)

### Atalhos Completos
`Cmd/Ctrl + K Cmd/Ctrl + S` → Keyboard Shortcuts

---

**Dica Final:** Configure Claude Code como seu copilot principal. Ele tem acesso direto aos MCPs e pode invocar agentes especializados automaticamente!
