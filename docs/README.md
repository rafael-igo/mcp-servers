# MCPs - Model Context Protocol Servers

MCPs especializados para o projeto I GO Experience.

## 🚀 Para Continuar o Desenvolvimento (IA)

**Se você é uma IA continuando este projeto, COMECE AQUI:**

1. **[RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md)** ⭐ - **Leia primeiro!** Visão geral completa em 5 minutos
2. **[ESTRUTURA_COMPLETA.md](ESTRUTURA_COMPLETA.md)** 📖 - Referência técnica detalhada (70KB)

**Depois siga o workflow:**
```python
# 1. Contextualize-se
load_context()
get_project_status(include_details=True)

# 2. Identifique a tarefa e invoque agente especializado
invoke_agent("agente-transfer", "sua tarefa")

# 3. Execute e atualize memória
save_context(module="...", status="...", details="...")
```

---

## 📚 Documentação Completa

### Essencial
- **[RESUMO_EXECUTIVO.md](RESUMO_EXECUTIVO.md)** ⭐ - Quick start para IAs (7 min de leitura)
- **[ESTRUTURA_COMPLETA.md](ESTRUTURA_COMPLETA.md)** - Referência técnica completa
- **[LISTA_MCPS.md](LISTA_MCPS.md)** - Lista detalhada de todos os MCPs e ferramentas
- **[SETUP.md](SETUP.md)** - Guia completo de instalação e configuração

### Avançado
- **[REORGANIZACAO.md](REORGANIZACAO.md)** - Estrutura e arquitetura do projeto
- **[ORQUESTRADOR.md](ORQUESTRADOR.md)** - Como usar o orquestrador de agentes
- **[GUIA_USO_RAPIDO.md](GUIA_USO_RAPIDO.md)** - Exemplos práticos de uso
- **[DOCKER-ADMIN.md](DOCKER-ADMIN.md)** - Gerenciamento de infraestrutura

### Scripts
- **[test-mcps.sh](test-mcps.sh)** - Script de testes automatizados
- **[install-claude-config.sh](install-claude-config.sh)** - Instalador automático para Claude Desktop

## 📦 MCPs Disponíveis

### 1. **excel-server**
Leitura avançada de arquivos Excel.

**Ferramentas:**
- `read_excel_tabs(file_path)` - Lê todas as abas
- `read_excel_with_formulas(file_path, sheet_name)` - Preserva fórmulas
- `get_excel_metadata(file_path)` - Metadados do arquivo

### 2. **agente-orchestrator**
Orquestração de agentes especializados.

**Ferramentas:**
- `list_agents()` - Lista agentes disponíveis
- `invoke_agent(agent_name, task)` - Invoca agente específico
- `get_agent_docs(agent_name)` - Documentação do agente
- `update_agent_memory(action, details)` - Atualiza memória

### 3. **memory-manager**
Gerenciamento de memória persistente.

**Ferramentas:**
- `save_context(module, status, details)` - Salva contexto
- `load_context()` - Carrega contexto atual
- `update_progress(task, status, notes)` - Atualiza progresso
- `get_next_steps()` - Próximos passos
- `add_decision(...)` - Registra decisão técnica (ADR)
- `get_memory_summary()` - Resumo da memória

### 4. **checklist-validator**
Validação e gestão de checklists.

**Ferramentas:**
- `validate_checklist(checklist_path)` - Valida checklist
- `mark_completed(checklist_path, task_pattern)` - Marca tarefa completa
- `get_pending_tasks(checklist_path)` - Lista pendentes
- `list_checklists()` - Lista todos os checklists
- `create_checklist(name, title, sections)` - Cria novo checklist

### 5. **agente-insights**
Captura ideias, consulta especialistas, toma decisões.

**Ferramentas:**
- `capture_insight(idea, insight_type, complexity, modules)` - Captura novo insight
- `get_insights(status, insight_type, limit)` - Lista insights
- `update_insight_status(insight_id, new_status, notes)` - Atualiza status
- `add_agent_feedback(insight_id, agent_name, feedback)` - Adiciona feedback
- `make_decision(insight_id, decision_status, rationale)` - Registra decisão
- `get_statistics()` - Estatísticas dos insights

### 6. **agente-resumo**
Status, progresso, relatórios e métricas.

**Ferramentas:**
- `get_project_status(include_details)` - Status geral do projeto
- `get_module_status(module_name)` - Status de módulo específico
- `update_module_progress(module_name, progress, status)` - Atualiza progresso
- `get_next_steps(limit)` - Lista próximos passos
- `add_next_step(task, priority, estimate)` - Adiciona próximo passo
- `generate_report(report_type, audience)` - Gera relatório formatado
- `get_metrics()` - Métricas do projeto

### 7. **docker-admin**
Gerenciamento automático de Docker e infraestrutura.

**Ferramentas:**
- `check_docker_status()` - Verifica Docker e auto-inicia
- `manage_mcps(action)` - Gerencia todos MCPs (start/stop/rebuild)
- `manage_mcp(name, action)` - Gerencia MCP específico
- `manage_api(action)` - Gerencia API
- `health_check()` - Verifica saúde e auto-corrige
- `get_logs(service, lines)` - Obtém logs
- `auto_heal()` - Auto-healing completo
- `get_mcp_status()` - Status de containers e configuração
- `sync_mcp_config()` - Sincroniza .mcp.json
- `update_and_restart_mcps()` - Atualiza e reinicia todos

**Para detalhes completos de todos os MCPs, veja:** [LISTA_MCPS.md](LISTA_MCPS.md)

## 🚀 Início Rápido

**NOVO:** Use o instalador automático para configurar o Claude Desktop:

```bash
cd api/mcp-servers/docs
./install-claude-config.sh
```

Para setup completo, veja: **[SETUP.md](SETUP.md)**

### Opção 1: Docker Compose (Recomendado)

```bash
cd api/mcp-servers

# Subir todos os MCPs
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### Opção 2: Execução Individual

```bash
cd api/mcp-servers/excel-server

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar
python server.py
```

## ⚙️ Configuração Claude Desktop

Adicione ao seu `claude_desktop_config.json`:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "excel-server": {
      "command": "docker",
      "args": ["exec", "-i", "igo-excel-server", "python", "server.py"],
      "env": {}
    },
    "agente-orchestrator": {
      "command": "docker",
      "args": ["exec", "-i", "igo-agente-orchestrator", "python", "server.py"],
      "env": {}
    },
    "memory-manager": {
      "command": "docker",
      "args": ["exec", "-i", "igo-memory-manager", "python", "server.py"],
      "env": {}
    },
    "checklist-validator": {
      "command": "docker",
      "args": ["exec", "-i", "igo-checklist-validator", "python", "server.py"],
      "env": {}
    },
    "agente-insights": {
      "command": "docker",
      "args": ["exec", "-i", "igo-agente-insights", "python", "server.py"],
      "env": {}
    },
    "agente-resumo": {
      "command": "docker",
      "args": ["exec", "-i", "igo-agente-resumo", "python", "server.py"],
      "env": {}
    },
    "docker-admin": {
      "command": "docker",
      "args": ["exec", "-i", "igo-docker-admin", "python", "server.py"],
      "env": {}
    },
    "igo-openai-gateway": {
      "command": "docker",
      "args": ["exec", "-i", "igo-openai-gateway", "python", "server.py"],
      "env": {}
    }
  }
}
```

**Reinicie o Claude Desktop após configurar.**

<<<<<<< ours
=======
### Variáveis de Ambiente (OpenAI)

Para o `igo-openai-gateway`, defina `OPENAI_API_KEY` no host ou via `.env` do Docker Compose.

>>>>>>> theirs
### Configuração Remota (Servidor Docker)

Se os MCPs estiverem rodando em um servidor remoto, use SSH para executar os containers via `docker exec`.

➡️ Consulte: [Configuração MCP em Servidor Remoto](SETUP_REMOTE_MCP.md)

## 🧪 Testar MCPs

**NOVO:** Use o script automatizado:

```bash
cd api/mcp-servers/docs
./test-mcps.sh
```

Ou teste individualmente:

```bash
# Testar excel-server
echo '{"method":"tools/list"}' | docker exec -i igo-excel-server python server.py

# Testar agente-orchestrator
echo '{"method":"tools/list"}' | docker exec -i igo-agente-orchestrator python server.py

# Testar memory-manager
echo '{"method":"tools/list"}' | docker exec -i igo-memory-manager python server.py

# Testar checklist-validator
echo '{"method":"tools/list"}' | docker exec -i igo-checklist-validator python server.py

# Testar agente-insights
echo '{"method":"tools/list"}' | docker exec -i igo-agente-insights python server.py

# Testar agente-resumo
echo '{"method":"tools/list"}' | docker exec -i igo-agente-resumo python server.py

# Testar docker-admin
echo '{"method":"tools/list"}' | docker exec -i igo-docker-admin python server.py

# Testar igo-openai-gateway
echo '{"method":"tools/list"}' | docker exec -i igo-openai-gateway python server.py
```

## 📊 Status dos MCPs

Verificar containers ativos:

```bash
cd api/mcp-servers
docker-compose ps
```

Deve mostrar 7 containers UP:
- ✅ igo-excel-server
- ✅ igo-agente-orchestrator
- ✅ igo-memory-manager
- ✅ igo-checklist-validator
- ✅ igo-agente-insights
- ✅ igo-agente-resumo
- ✅ igo-docker-admin

Ou use o docker-admin MCP:
```
Use docker-admin para verificar o status completo dos containers
```

## 🔧 Troubleshooting

### Containers não iniciam

```bash
# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Permissões de arquivo

```bash
# Dar permissão de execução aos server.py
chmod +x */server.py
```

### Ver logs específicos

```bash
docker logs igo-excel-server -f
docker logs igo-agente-orchestrator -f
docker logs igo-memory-manager -f
docker logs igo-checklist-validator -f
```

## 📝 Exemplos de Uso

### Excel Server

```python
# Ler todas as abas de um Excel
read_excel_tabs("/project/docs/exemplo.xlsx")

# Ler com fórmulas preservadas
read_excel_with_formulas("/project/uploads/rooming.xlsx", "Rooming List")

# Metadados
get_excel_metadata("/project/uploads/transfer.xlsx")
```

### Agente Orchestrator

```python
# Listar agentes
list_agents()

# Invocar agente específico
invoke_agent("agente-rooming-list", "Adicionar coluna de observações")

# Documentação do agente
get_agent_docs("agente-transfer")
```

### Memory Manager

```python
# Salvar contexto
save_context("Rooming List", "completed", "Modal de detalhes implementado")

# Carregar contexto
load_context()

# Atualizar progresso
update_progress("Implementar Check-in", "in_progress", "Backend pronto, falta frontend")

# Registrar decisão
add_decision(
    "Escolha de PostgreSQL",
    "Precisávamos de um banco robusto",
    "MySQL, PostgreSQL, MongoDB",
    "PostgreSQL 16",
    "Melhor suporte a JSON, open-source, performance"
)
```

### Checklist Validator

```python
# Validar checklist
validate_checklist("mvp.md")

# Marcar tarefa completa
mark_completed("mvp.md", "Rooming List")

# Listar tarefas pendentes
get_pending_tasks()

# Listar todos os checklists
list_checklists()
```

## 🏗️ Estrutura

```
mcp-servers/
├── excel-server/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── agente-orchestrator/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── memory-manager/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── checklist-validator/
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 📖 Documentação Adicional

- **[SETUP.md](SETUP.md)** - Guia completo de instalação (passo a passo detalhado)
- **[LISTA_MCPS.md](LISTA_MCPS.md)** - Referência completa de todos os MCPs e ferramentas
- **[REORGANIZACAO.md](REORGANIZACAO.md)** - Arquitetura e decisões técnicas
- **[claude_desktop_config.example.json](claude_desktop_config.example.json)** - Exemplo de configuração

## 🔗 Referências

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Python](https://github.com/jlowin/fastmcp)
- [Docker Compose File](../docker-compose.yml)
- [Configuração MCP](.mcp.json)
