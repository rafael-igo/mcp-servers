# Docker vs Python - Arquitetura dos MCPs

## 📋 Resumo

Este projeto possui **10 MCPs** divididos em 2 categorias:

### 🐳 MCPs via Docker (2)
Rodam em containers Docker por necessidades específicas:

| MCP | Por que Docker? |
|-----|-----------------|
| **docker-admin** | Precisa de acesso ao Docker socket (`/var/run/docker.sock`) para gerenciar containers |
| **api-database-tester** | Precisa do ODBC Driver 18 para SQL Server (disponível apenas no Linux) |

### 🐍 MCPs via Python Local (8)
Rodam diretamente via Python no sistema host:

| MCP | Benefícios |
|-----|-----------|
| **excel-server** | Acesso direto aos arquivos locais, sem overhead de container |
| **agente-orchestrator** | Comunicação mais rápida com agentes locais |
| **memory-manager** | Acesso direto ao sistema de arquivos para memória persistente |
| **checklist-validator** | Leitura/escrita direta de arquivos markdown |
| **agente-insights** | Armazenamento local de insights |
| **agente-resumo** | Geração rápida de relatórios |
| **igo-openai-gateway** | Chamadas API OpenAI sem latência de container |
| **vuetify-uiux** | Componentes UI sem necessidade de isolamento |

## 🎯 Por que essa Arquitetura?

### Vantagens de Python Local

1. **Performance:** Sem overhead de container
2. **Desenvolvimento:** Mais rápido para iterar e testar
3. **Simplicidade:** Menos dependências de Docker
4. **Recursos:** Menor uso de memória e CPU
5. **Acesso a arquivos:** Direto ao sistema de arquivos do host

### Quando Usar Docker

Use Docker **apenas** quando houver necessidade real:

- ✅ Acesso a recursos do sistema (Docker socket)
- ✅ Drivers específicos de sistema operacional (ODBC Linux)
- ✅ Isolamento de rede necessário
- ✅ Conflitos de dependências com sistema host
- ❌ Conveniência (não é justificativa suficiente)

## 📁 Estrutura do Projeto

```
mcp-servers/
├── docker-compose.yml          # APENAS docker-admin + api-database-tester
├── .mcp.json                   # Configuração de TODOS os MCPs
│
├── 🐳 Docker MCPs (2):
│   ├── docker-admin/
│   │   ├── Dockerfile
│   │   └── server.py
│   └── api-database-tester/
│       ├── Dockerfile
│       └── server.py
│
└── 🐍 Python MCPs (8):
    ├── excel-server/server.py
    ├── agente-orchestrator/server.py
    ├── memory-manager/server.py
    ├── checklist-validator/server.py
    ├── agente-insights/server.py
    ├── agente-resumo/server.py
    ├── igo-openai-gateway/server.py
    └── vuetify-uiux/server.py
```

## 🔧 Configuração no .mcp.json

### MCPs Python Local
```json
{
  "excel-server": {
    "command": "python",
    "args": ["c:/GIT-RAFAEL/mcp-servers/excel-server/server.py"],
    "env": {}
  }
}
```

### MCPs Docker
```json
{
  "docker-admin": {
    "command": "docker",
    "args": ["exec", "-i", "igo-docker-admin", "python", "server.py"],
    "env": {},
    "comment": "Precisa de Docker (gerencia containers)"
  }
}
```

## 🚀 Como Usar

### Iniciar Ambiente

```bash
# 1. Iniciar containers Docker (apenas 2)
docker-compose up -d

# 2. Verificar status
docker-compose ps
# Deve mostrar:
# - igo-docker-admin       Up
# - igo-api-database-tester Up

# 3. MCPs Python iniciam automaticamente quando você usa os editores
```

### Verificar MCPs

```python
# No seu editor (VSCode/Cursor/Codex):

# Docker MCP
docker-admin.health_check()

# Python MCPs (iniciam automaticamente)
memory-manager.load_context()
agente-orchestrator.list_agents()
excel-server.get_excel_metadata("arquivo.xlsx")
```

## 🔄 Fluxo de Trabalho

### Desenvolvimento Local

1. **Editar código Python:**
   - Abra o arquivo `server.py` do MCP
   - Faça suas alterações
   - Salve
   - MCP reinicia automaticamente (depende do editor)

2. **Testar:**
   - Use diretamente do editor
   - Sem necessidade de rebuild

### Desenvolvimento Docker

1. **Editar código Docker:**
   - Abra o arquivo `server.py` do MCP
   - Faça suas alterações
   - Salve

2. **Rebuild:**
   ```bash
   docker-compose up -d --build docker-admin
   # ou
   docker-compose up -d --build api-database-tester
   ```

3. **Testar:**
   - Use do editor após rebuild

## 💡 Dicas

### Performance

- **Python local:** ~0ms de overhead
- **Docker:** ~10-50ms de overhead por chamada

Para MCPs que fazem muitas chamadas rápidas (como `memory-manager`), Python local é significativamente mais rápido.

### Debug

**Python local:**
```python
# Adicione print statements
print(f"Debug: {variable}")

# Ou use debugger do VSCode/Cursor
```

**Docker:**
```bash
# Ver logs
docker-compose logs -f docker-admin

# Ou attach ao container
docker exec -it igo-docker-admin bash
```

### Quando Migrar de Python para Docker

Migre um MCP Python para Docker se:

1. Precisar de drivers/libs específicos do Linux
2. Tiver conflitos de dependências com sistema host
3. Precisar de isolamento de rede
4. Precisar de acesso a recursos do Docker

**Não migre** apenas por:
- "Ser mais organizado"
- "Todos em containers"
- Conveniência

## 📊 Comparação

| Aspecto | Python Local | Docker |
|---------|--------------|--------|
| **Startup** | Instantâneo | 2-5 segundos |
| **Performance** | Nativa | Overhead 10-50ms |
| **Memória** | ~50MB por MCP | ~200MB por container |
| **Desenvolvimento** | Edit & reload | Edit → rebuild → restart |
| **Debug** | Fácil (IDE) | Logs + attach |
| **Portabilidade** | Requer Python no host | Self-contained |
| **Isolamento** | Compartilha deps | Totalmente isolado |

## 🎓 Casos de Uso

### Use Python Local para:
- ✅ Processamento de arquivos locais
- ✅ APIs externas (OpenAI, etc)
- ✅ Leitura/escrita de arquivos
- ✅ Chamadas rápidas frequentes
- ✅ Desenvolvimento ativo

### Use Docker para:
- ✅ Acesso ao Docker socket
- ✅ Drivers de sistema específicos
- ✅ Isolamento necessário
- ✅ Deploy em produção
- ✅ CI/CD pipelines

## 🔐 Segurança

### Python Local
- Roda com permissões do usuário
- Acesso completo ao sistema de arquivos
- Sem isolamento de rede

### Docker
- Pode usar usuário não-root
- Acesso limitado via volumes
- Isolamento de rede via bridge

## 📝 Resumo

**Regra de ouro:** Use Python local por padrão, Docker apenas quando necessário.

**2 MCPs em Docker:**
- docker-admin (precisa Docker socket)
- api-database-tester (precisa ODBC Driver)

**8 MCPs em Python local:**
- Todos os outros (performance + simplicidade)

---

**Arquitetura híbrida:** O melhor dos dois mundos! 🚀
