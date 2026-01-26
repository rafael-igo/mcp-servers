# 🚀 Quick Start - Acesso Remoto (Windows → Servidor)

## ⚡ Setup em 5 Minutos

### 1. Configure SSH no Windows

```powershell
# Gerar chave SSH (se não tiver)
ssh-keygen -t ed25519 -C "rafael@windows"
# Pressione Enter 3x (sem senha)

# Copiar chave para servidor
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh rafael@15.15.255.9 "cat >> ~/.ssh/authorized_keys"

# Testar (não deve pedir senha)
ssh rafael@15.15.255.9 echo "OK"
```

### 2. Subir Containers no Servidor

```bash
# Conectar ao servidor
ssh rafael@15.15.255.9

# Navegar para o projeto
cd /home/rafael/mcp-servers

# Subir TODOS os 10 containers
docker-compose up -d

# Verificar (deve mostrar 10 containers "Up")
docker-compose ps

# Sair
exit
```

### 3. Configurar Windows

```powershell
# No diretório do projeto
cd C:\GIT-RAFAEL\mcp-servers

# Backup da config local
Rename-Item .mcp.json .mcp.local.json -ErrorAction SilentlyContinue

# Usar config remota (todos via Docker)
Copy-Item .mcp.remote-docker.json .mcp.json

# Verificar
Get-Content .mcp.json
```

### 4. Testar

```powershell
# Teste 1: SSH funciona?
ssh rafael@15.15.255.9 echo "OK"

# Teste 2: Containers estão rodando?
ssh rafael@15.15.255.9 docker ps

# Teste 3: MCP responde?
ssh rafael@15.15.255.9 docker exec -i igo-memory-manager python server.py
# Pressione Ctrl+C para sair
```

### 5. Abrir Editor

**VSCode:**
1. Abra o projeto: `code C:\GIT-RAFAEL\mcp-servers`
2. Reload Window: `Ctrl+Shift+P` → "Reload Window"
3. Abra Claude Code chat
4. Teste: `docker-admin.health_check()`

**Cursor:**
1. Abra o projeto: `cursor C:\GIT-RAFAEL\mcp-servers`
2. Restart Cursor
3. Abra chat: `Ctrl+L`
4. Teste: `memory-manager.load_context()`

---

## ✅ Checklist

- [ ] SSH configurado (sem senha)
- [ ] Servidor com 10 containers rodando
- [ ] `.mcp.remote-docker.json` copiado para `.mcp.json`
- [ ] Editor recarregado
- [ ] MCPs funcionando

---

## 🎯 Comandos Úteis

### No Windows

```powershell
# Ver containers remotos
ssh rafael@15.15.255.9 docker-compose ps

# Restart todos containers
ssh rafael@15.15.255.9 docker-compose restart

# Ver logs de um container
ssh rafael@15.15.255.9 docker-compose logs -f memory-manager

# Parar todos
ssh rafael@15.15.255.9 docker-compose down

# Subir todos
ssh rafael@15.15.255.9 docker-compose up -d
```

### No Servidor (via SSH)

```bash
# Conectar
ssh rafael@15.15.255.9

# Navegar para projeto
cd /home/rafael/mcp-servers

# Ver status
docker-compose ps

# Restart específico
docker-compose restart excel-server

# Ver logs
docker-compose logs -f agente-orchestrator

# Rebuild e restart
docker-compose up -d --build excel-server
```

---

## 🐛 Troubleshooting Rápido

### SSH pede senha
```powershell
# Copiar chave novamente
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh rafael@15.15.255.9 "cat >> ~/.ssh/authorized_keys"
```

### "No such container"
```bash
ssh rafael@15.15.255.9
cd /home/rafael/mcp-servers
docker-compose up -d
```

### MCP não responde
```bash
# No servidor
docker-compose restart nome-do-container
docker-compose logs nome-do-container
```

### Editor não detecta MCPs
```powershell
# Windows
# 1. Verificar .mcp.json aponta para .mcp.remote-docker.json
Get-Content .mcp.json

# 2. Reload editor
# VSCode: Ctrl+Shift+P → "Reload Window"
# Cursor: Restart
```

---

## 📊 Performance Esperada

| Operação | Latência |
|----------|----------|
| Carregar contexto | 50-100ms |
| Processar Excel | 150-250ms |
| Invocar agente | 50-100ms |
| Health check | 30-60ms |

---

## 🎓 Próximos Passos

1. ✅ Leia: [GUIDELINES.md](GUIDELINES.md) - Entender MCPs
2. ✅ Leia: [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md) - Comandos rápidos
3. ✅ Configure: Atalhos do editor
4. ✅ Otimize: SSH ControlMaster (ver SETUP_WINDOWS_REMOTO.md)

---

## 📚 Arquivos de Configuração

| Arquivo | Uso |
|---------|-----|
| `.mcp.json` | Config LOCAL (Python no PC) |
| `.mcp.remote-docker.json` | Config REMOTA (Docker via SSH) ⭐ |
| `.mcp.remote.json` | Config Python remoto (não funciona no Windows) |

Para Windows → Linux: **Use `.mcp.remote-docker.json`**

---

**🎉 Pronto!** Agora você pode usar os MCPs do servidor de qualquer PC Windows!

**💡 Dica:** Para melhor performance, veja otimizações SSH em [SETUP_WINDOWS_REMOTO.md](SETUP_WINDOWS_REMOTO.md)
