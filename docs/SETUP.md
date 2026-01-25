# Setup dos MCPs - Guia Completo

## 📚 Documentação

**Ver lista completa de MCPs e suas funcionalidades:** [LISTA_MCPS.md](LISTA_MCPS.md)

Este guia cobre a instalação e configuração de **7 MCPs** para o projeto I GO Experience.

## 🎯 Passo a Passo

### 1. Subir os Containers Docker

```bash
cd /Users/rafamacpro/Projetos/GIT/Transfer-logistica/api/mcp-servers

# Subir todos os MCPs


# Verificar se estão rodando
docker-compose ps
```

**Containers esperados:**
- igo-excel-server
- igo-agente-orchestrator
- igo-memory-manager
- igo-checklist-validator
- igo-agente-insights
- igo-agente-resumo
- igo-docker-admin

### 2. Configurar Claude Desktop

**Localização do arquivo de config:**

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```bash
~/.config/claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

### 3. Configurar Claude Desktop

**Opção A: Instalação Automática (Recomendado)**

```bash
cd /Users/rafamacpro/Projetos/GIT/Transfer-logistica/api/mcp-servers/docs

# Executar o instalador
./install-claude-config.sh
```

O script irá:
- Detectar automaticamente seu sistema operacional
- Fazer backup da configuração atual
- Instalar a nova configuração com todos os MCPs
- Mostrar instruções para reiniciar o Claude Desktop

**Opção B: Instalação Manual**

```bash
# Fazer backup do config atual (se existir)
cp ~/Library/Application\ Support/Claude/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json.backup

# Copiar a configuração de exemplo
cp claude_desktop_config.example.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Ou editar manualmente
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

Cole o conteúdo de `claude_desktop_config.example.json` ou merge com sua configuração existente.

### 4. Reiniciar Claude Desktop

**macOS:**
```bash
killall Claude && sleep 2 && open -a Claude
```

**Linux:**
```bash
pkill -f claude && sleep 2 && claude &
```

**Windows:**
- Fechar Claude pela bandeja do sistema
- Reabrir Claude

### 5. Verificar MCPs Carregados

No Claude Desktop, você deve ver novos MCPs disponíveis:

- ✅ igo-memory (já existia)
- ✅ excel-server
- ✅ agente-orchestrator
- ✅ memory-manager
- ✅ checklist-validator
- ✅ agente-insights
- ✅ agente-resumo
- ✅ docker-admin

## 🧪 Testar MCPs

### Teste Rápido

```bash
cd /Users/rafamacpro/Projetos/GIT/Transfer-logistica/api/mcp-servers

# Testar todos
./test-mcps.sh

# Ou individualmente
docker exec -i igo-excel-server python server.py <<< '{"method":"tools/list"}'
docker exec -i igo-agente-orchestrator python server.py <<< '{"method":"tools/list"}'
docker exec -i igo-memory-manager python server.py <<< '{"method":"tools/list"}'
docker exec -i igo-checklist-validator python server.py <<< '{"method":"tools/list"}'
docker exec -i igo-agente-insights python server.py <<< '{"method":"tools/list"}'
docker exec -i igo-agente-resumo python server.py <<< '{"method":"tools/list"}'
docker exec -i igo-docker-admin python server.py <<< '{"method":"tools/list"}'
```

### Teste no Claude

**Excel Server:**
```
Use excel-server para ler o arquivo /project/docs/exemplo.xlsx
```

**Agente Orchestrator:**
```
Use agente-orchestrator para listar todos os agentes disponíveis
```

**Memory Manager:**
```
Use memory-manager para carregar o contexto atual do projeto
```

**Checklist Validator:**
```
Use checklist-validator para validar o checklist mvp.md
```

**Agente Insights:**
```
Use agente-insights para listar insights capturados
```

**Agente Resumo:**
```
Use agente-resumo para ver o status do projeto
```

**Docker Admin:**
```
Use docker-admin para verificar o status dos containers
```

## 🔧 Troubleshooting

### Container não inicia

```bash
# Ver logs
docker logs igo-excel-server

# Rebuild
docker-compose build --no-cache excel-server
docker-compose up -d excel-server
```

### Claude não reconhece MCP

1. Verificar que container está rodando:
```bash
docker ps | grep igo
```

2. Verificar config JSON:
```bash
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq .
```

3. Reiniciar Claude completamente

### Erro de permissão

```bash
# Dar permissões corretas
chmod +x api/mcp-servers/*/server.py
```

### Ver todos os logs

```bash
docker-compose logs -f
```

## 📊 Status de Saúde

```bash
# Ver status de todos os containers
docker-compose ps

# Ver uso de recursos
docker stats --no-stream

# Ver logs das últimas 50 linhas
docker-compose logs --tail=50
```

## 🔄 Atualizar MCPs

```bash
cd /Users/rafamacpro/Projetos/GIT/Transfer-logistica/api/mcp-servers

# Parar containers
docker-compose down

# Rebuild
docker-compose build --no-cache

# Subir novamente
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 🧹 Limpar e Reinstalar

```bash
# Parar e remover tudo
docker-compose down -v

# Remover imagens
docker rmi igo-excel-server igo-agente-orchestrator igo-memory-manager igo-checklist-validator igo-agente-insights igo-agente-resumo igo-docker-admin

# Rebuild do zero
docker-compose up -d --build
```

## ✅ Checklist de Verificação

- [ ] Docker está rodando
- [ ] `docker-compose ps` mostra 7 containers UP
- [ ] Config do Claude Desktop atualizado
- [ ] Claude Desktop foi reiniciado
- [ ] MCPs aparecem na lista de ferramentas do Claude
- [ ] Teste de `list_agents()` funciona
- [ ] Teste de `load_context()` funciona
- [ ] Teste de `get_insights()` funciona
- [ ] Teste de `get_project_status()` funciona
- [ ] Teste de `check_docker_status()` funciona

## 📞 Suporte

Se tiver problemas:

1. Ver logs: `docker-compose logs -f`
2. Verificar lista de MCPs: [LISTA_MCPS.md](LISTA_MCPS.md)
3. Verificar documentação: `README.md`
4. Usar docker-admin: `Use docker-admin para executar auto-healing completo`

## 🎉 Sucesso!

Se tudo funcionou, você agora tem 8 MCPs ativos:

1. ✅ igo-memory (original)
2. ✅ excel-server
3. ✅ agente-orchestrator
4. ✅ memory-manager
5. ✅ checklist-validator
6. ✅ agente-insights
7. ✅ agente-resumo
8. ✅ docker-admin

Pode usar todos eles conversando naturalmente com o Claude!
