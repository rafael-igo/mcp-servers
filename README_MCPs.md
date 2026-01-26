# MCPs - Guia Completo de Configuração

Este projeto possui 8 MCPs (Model Context Protocol Servers) que funcionam como ferramentas especializadas para assistentes de IA.

## 🚀 Quick Start

### 1. Iniciar MCPs
```bash
docker-compose up -d
```

### 2. Verificar Status
```bash
docker-compose ps
```

### 3. Testar MCPs
Abra seu editor e use:
```python
docker-admin.health_check()
```

## 📚 Documentação por Editor

Escolha seu editor e siga o guia específico:

### [VSCode](VSCODE_GUIDELINES.md)
- Configuração do VSCode
- Extensões recomendadas
- Atalhos e workflows
- Integração com Claude Code

### [Cursor](CURSOR_SETUP.md)
- Setup completo do Cursor
- Features exclusivas (Cmd+K, Composer)
- Workflows otimizados
- @-mentions e context

### [GitHub Codex](CODEX_GUIDELINES.md)
- Templates para code review
- Workflows de PR
- Análises profundas
- Gestão de insights

### [Claude Code CLI](GUIDELINES.md)
- Documentação completa de todos os MCPs
- Boas práticas
- Fluxos de trabalho
- Troubleshooting

## 🛠️ MCPs Disponíveis

| MCP | Container | Descrição |
|-----|-----------|-----------|
| **excel-server** | igo-excel-server | Leitura e processamento de Excel |
| **agente-orchestrator** | igo-agente-orchestrator | Orquestração de agentes especializados |
| **memory-manager** | igo-memory-manager | Gerenciamento de contexto do projeto |
| **checklist-validator** | igo-checklist-validator | Validação de checklists |
| **agente-insights** | igo-agente-insights | Captura e análise de insights |
| **agente-resumo** | igo-agente-resumo | Resumos e status do projeto |
| **docker-admin** | igo-docker-admin | Administração de Docker e MCPs |
| **igo-openai-gateway** | igo-openai-gateway | Gateway OpenAI/GPT-5.2 com reasoning |

## 🎯 Qual Arquivo Ler?

**Escolha baseado no seu caso de uso:**

| Quero... | Leia... |
|----------|---------|
| Configurar VSCode | [VSCODE_GUIDELINES.md](VSCODE_GUIDELINES.md) |
| Configurar Cursor | [CURSOR_SETUP.md](CURSOR_SETUP.md) |
| Usar no GitHub Codex | [CODEX_GUIDELINES.md](CODEX_GUIDELINES.md) |
| Entender todos os MCPs | [GUIDELINES.md](GUIDELINES.md) |
| Saber o que mudou | Este arquivo (README_MCPs.md) |
| Configurar .cursorrules | [.cursorrules](.cursorrules) |
| Configurar Claude Code | [.claude/README.md](.claude/README.md) |

## 🔧 Configuração Rápida por Editor

### VSCode
1. Instale extensão "Claude Code"
2. Arquivo `.mcp.json` já configurado
3. Permissões em `.claude/settings.local.json`
4. Leia: [VSCODE_GUIDELINES.md](VSCODE_GUIDELINES.md)

### Cursor
1. Instale Cursor de https://cursor.sh
2. Arquivo `.cursorrules` já configurado
3. Configure `mcp.configPath` em settings
4. Leia: [CURSOR_SETUP.md](CURSOR_SETUP.md)

### GitHub Codex
1. Codex detecta `.mcp.json` automaticamente
2. Use templates em [CODEX_GUIDELINES.md](CODEX_GUIDELINES.md)
3. Sempre comece com `memory-manager.load_context()`

### Claude Code CLI
1. Já configurado via `.mcp.json`
2. Execute: `claude chat`
3. Use: `docker-admin.health_check()`

## 📋 Arquivos Importantes

```
mcp-servers/
├── .mcp.json                      # Config MCPs (todos os editores)
├── .cursorrules                   # Regras do Cursor
├── .claude/
│   ├── settings.local.json        # Permissões Claude Code
│   └── README.md                  # Docs configuração Claude
├── GUIDELINES.md                  # 📘 Documentação completa MCPs
├── VSCODE_GUIDELINES.md           # 📗 Guia VSCode
├── CURSOR_SETUP.md                # 📙 Guia Cursor
├── CODEX_GUIDELINES.md            # 📕 Guia Codex
├── README_MCPs.md                 # 📄 Este arquivo
└── docker-compose.yml             # Orquestração containers
```

## 🎬 Workflows Essenciais

### Início do Dia
```python
# 1. Verificar infraestrutura
docker-admin.health_check()

# 2. Carregar contexto
memory-manager.load_context()

# 3. Ver próximos passos
agente-resumo.get_next_steps()
```

### Durante Desenvolvimento
```python
# Consultar especialista
agente-orchestrator.invoke_agent("agente-arquiteto-igo", "sua tarefa")

# Análise profunda
igo-openai-gateway.run_architectural_review(description, reasoning_effort="xhigh")

# Atualizar progresso
memory-manager.update_progress(task, status, notes)
```

### Fim do Dia
```python
# Salvar contexto
memory-manager.save_context(module, status, details)

# Marcar tarefas completadas
checklist-validator.mark_completed(checklist_path, task_pattern)

# Adicionar próximos passos
agente-resumo.add_next_step(task, priority, estimate)
```

## 🆘 Troubleshooting

### MCPs não respondem
```python
docker-admin.auto_heal()
```

### Docker não está rodando
```bash
# Verificar
docker ps

# Iniciar MCPs
docker-compose up -d
```

### Ver logs de um MCP
```python
docker-admin.get_logs("igo-memory-manager", lines=50)
```

### Reiniciar tudo
```bash
docker-compose restart
```

## 🌟 Features Destacadas

### 1. Auto-Healing
MCPs se auto-corrigem:
```python
docker-admin.auto_heal()  # Detecta e corrige problemas automaticamente
```

### 2. Agentes Especializados
Delegue para especialistas:
- `agente-arquiteto-igo` - Arquitetura
- `agente-frontend-igo` - Frontend
- `agente-backend` - Backend
- `agente-qa-testes` - QA e testes

### 3. Reasoning com GPT-5.2
Análises profundas:
```python
igo-openai-gateway.run_architectural_review(
    description="Problema complexo",
    reasoning_effort="xhigh"  # Máximo reasoning
)
```

### 4. Memória Persistente
Contexto entre sessões:
```python
memory-manager.load_context()  # Carrega tudo da última sessão
```

### 5. Insights Automáticos
Captura sugestões:
```python
agente-insights.capture_insight(idea, insight_type, complexity)
```

## 🎓 Ordem de Leitura Recomendada

**Para iniciantes:**
1. 📄 Este arquivo (README_MCPs.md)
2. 📘 [GUIDELINES.md](GUIDELINES.md) - Entender todos os MCPs
3. 📗 Guia do seu editor (VSCode/Cursor/Codex)
4. 🚀 Começar a usar!

**Para desenvolvedores experientes:**
1. 📄 Este arquivo
2. 📗 Guia do editor que usa
3. 📕 [.cursorrules](.cursorrules) - Ver regras
4. 🚀 Direto ao código!

**Para code reviews:**
1. 📕 [CODEX_GUIDELINES.md](CODEX_GUIDELINES.md)
2. Templates de workflow
3. Usar `igo-openai-gateway` para análises

## 💡 Dicas de Ouro

### 1. Sempre Comece com Contexto
```python
memory-manager.load_context()
```

### 2. Use Auto-Healing Primeiro
Antes de debugar manualmente:
```python
docker-admin.auto_heal()
```

### 3. Delegue para Especialistas
Não faça tudo sozinho:
```python
agente-orchestrator.invoke_agent("agente-apropriado", task)
```

### 4. Capture Insights
Toda sugestão/ideia:
```python
agente-insights.capture_insight(idea)
```

### 5. Documente Decisões
Decisões técnicas importantes:
```python
memory-manager.add_decision(decision, context, alternatives, chosen, reason)
```

## 🔗 Links Úteis

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [MCP Protocol](https://modelcontextprotocol.io)
- [Claude Code](https://docs.anthropic.com/claude/docs)
- [Cursor](https://docs.cursor.sh)

## 📞 Suporte

- Problemas com MCPs: `docker-admin.auto_heal()`
- Ver logs: `docker-admin.get_logs(service)`
- Status geral: `docker-admin.health_check()`

## 🎉 Próximos Passos

1. ✅ Iniciar Docker: `docker-compose up -d`
2. ✅ Escolher seu editor
3. ✅ Ler o guia específico
4. ✅ Testar com `docker-admin.health_check()`
5. ✅ Começar a desenvolver!

---

**Pronto para começar?** Escolha seu editor e leia o guia correspondente! 🚀
