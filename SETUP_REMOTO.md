# Setup Remoto - MCPs via SSH

## 🌐 Visão Geral

Este guia mostra como usar os MCPs rodando no **servidor remoto** `15.15.255.9` a partir do seu **PC local** (VSCode/Cursor/Codex).

## 🏗️ Arquitetura Remota

```
┌─────────────────────────────┐
│    PC LOCAL (Windows/Mac)   │
│                             │
│  VSCode / Cursor / Codex    │
│         ↓ SSH               │
└─────────────┬───────────────┘
              │
              │ Internet/LAN
              │
              ▼
┌─────────────────────────────┐
│  SERVIDOR 15.15.255.9       │
│  (Linux)                    │
│                             │
│  ┌──────────────────────┐   │
│  │  8 MCPs Python       │   │
│  │  - excel-server      │   │
│  │  - orchestrator      │   │
│  │  - memory-manager    │   │
│  │  - checklist         │   │
│  │  - insights          │   │
│  │  - resumo            │   │
│  │  - openai-gateway    │   │
│  │  - vuetify-uiux      │   │
│  └──────────────────────┘   │
│                             │
│  ┌──────────────────────┐   │
│  │  2 MCPs Docker       │   │
│  │  - docker-admin      │   │
│  │  - api-db-tester     │   │
│  └──────────────────────┘   │
└─────────────────────────────┘
```

## 📋 Pré-requisitos

### No Servidor (15.15.255.9)
- ✅ Python 3.11+ instalado
- ✅ Docker e Docker Compose instalados
- ✅ Repositório `mcp-servers` clonado
- ✅ SSH Server configurado

### No PC Local
- ✅ Cliente SSH instalado (Windows: OpenSSH, Mac/Linux: nativo)
- ✅ Chave SSH configurada (sem senha)
- ✅ VSCode/Cursor instalado

## 🔑 1. Configurar SSH

### 1.1. Gerar Chave SSH (se não tiver)

**Windows:**
```powershell
ssh-keygen -t ed25519 -C "seu-email@example.com"
```

**Mac/Linux:**
```bash
ssh-keygen -t ed25519 -C "seu-email@example.com"
```

Pressione Enter para aceitar o local padrão. **Não defina senha** (pressione Enter).

### 1.2. Copiar Chave para o Servidor

**Windows:**
```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh rafael@15.15.255.9 "cat >> ~/.ssh/authorized_keys"
```

**Mac/Linux:**
```bash
ssh-copy-id rafael@15.15.255.9
```

### 1.3. Testar Conexão

```bash
ssh rafael@15.15.255.9
```

Deve conectar **sem pedir senha**. Se pedir senha, veja [SSH_WINDOWS_KEYS.md](docs/SSH_WINDOWS_KEYS.md).

### 1.4. Configurar SSH Config (Recomendado)

Crie/edite `~/.ssh/config` (Windows: `C:\Users\SeuUsuario\.ssh\config`):

```
Host mcp-server
    HostName 15.15.255.9
    User rafael
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

Teste:
```bash
ssh mcp-server
```

## 🚀 2. Setup no Servidor

### 2.1. Instalar Dependências Python

```bash
# Conectar ao servidor
ssh rafael@15.15.255.9

# Navegar para o projeto
cd /home/rafael/mcp-servers

# Instalar dependências de cada MCP
for dir in excel-server agente-orchestrator memory-manager checklist-validator agente-insights agente-resumo igo-openai-gateway vuetify-uiux; do
    cd $dir
    pip3 install -r requirements.txt
    cd ..
done
```

### 2.2. Iniciar Containers Docker

```bash
# No servidor
cd /home/rafael/mcp-servers

# Subir apenas os 2 containers Docker
docker-compose up -d

# Verificar (deve mostrar 2 containers)
docker-compose ps
```

Deve mostrar:
- `igo-docker-admin` - Up
- `igo-api-database-tester` - Up

### 2.3. Testar MCPs Manualmente

**Testar MCP Python:**
```bash
# No servidor
python3 /home/rafael/mcp-servers/memory-manager/server.py
# Ctrl+C para sair
```

**Testar MCP Docker:**
```bash
# No servidor
docker exec -i igo-docker-admin python server.py
# Ctrl+C para sair
```

## ⚙️ 3. Configurar PC Local

### 3.1. Escolher Arquivo de Configuração

Você tem 2 opções:

#### Opção A: Renomear para usar remoto como padrão
```bash
# No diretório mcp-servers do PC local
mv .mcp.json .mcp.local.json      # Backup da config local
mv .mcp.remote.json .mcp.json     # Usar config remota
```

#### Opção B: Usar arquivo específico
Alguns editores permitem especificar o arquivo de config:
- VSCode: `"mcp.configPath": "${workspaceFolder}/.mcp.remote.json"`
- Cursor: Similar

### 3.2. Verificar Configuração

Abra `.mcp.remote.json` e verifique:

```json
{
  "mcpServers": {
    "excel-server": {
      "command": "ssh",
      "args": [
        "rafael@15.15.255.9",
        "python3",
        "/home/rafael/mcp-servers/excel-server/server.py"
      ]
    },
    "docker-admin": {
      "command": "ssh",
      "args": [
        "rafael@15.15.255.9",
        "docker",
        "exec",
        "-i",
        "igo-docker-admin",
        "python",
        "server.py"
      ]
    }
  }
}
```

**Importante:** Ajuste o caminho `/home/rafael/mcp-servers/` se o projeto estiver em outro lugar no servidor.

### 3.3. Testar Conexão SSH + MCP

**No PC local:**
```bash
# Testar MCP Python via SSH
ssh rafael@15.15.255.9 python3 /home/rafael/mcp-servers/memory-manager/server.py

# Testar MCP Docker via SSH
ssh rafael@15.15.255.9 docker exec -i igo-docker-admin python server.py
```

Se funcionar sem pedir senha e o MCP iniciar, está pronto!

## 💻 4. Configurar Editor

### VSCode + Claude Code

1. **Abrir projeto no VSCode**
   ```bash
   code c:\GIT-RAFAEL\mcp-servers
   ```

2. **Verificar configuração**
   - Arquivo `.mcp.json` deve apontar para config remota
   - Ou renomeie `.mcp.remote.json` para `.mcp.json`

3. **Recarregar VSCode**
   - `Cmd/Ctrl + Shift + P` → "Reload Window"

4. **Testar Claude Code**
   - Abra chat do Claude Code
   - Execute: `docker-admin.health_check()`

### Cursor

1. **Abrir projeto no Cursor**
   ```bash
   cursor c:\GIT-RAFAEL\mcp-servers
   ```

2. **Configurar MCP path**
   - Settings → MCP
   - Config Path: `${workspaceFolder}/.mcp.remote.json`
   - Ou renomeie para `.mcp.json`

3. **Reload Cursor**
   - Restart Cursor

4. **Testar**
   - `Cmd/Ctrl + L` → Chat
   - "Use docker-admin.health_check()"

### GitHub Codex

Codex detecta `.mcp.json` automaticamente. Use `.mcp.remote.json` renomeado para `.mcp.json`.

## 🔍 5. Verificação e Testes

### Checklist de Verificação

No PC local, execute:

```bash
# 1. SSH sem senha funciona?
ssh rafael@15.15.255.9 echo "OK"
# Deve imprimir: OK

# 2. Python no servidor funciona?
ssh rafael@15.15.255.9 python3 --version
# Deve mostrar: Python 3.11.x

# 3. Docker no servidor funciona?
ssh rafael@15.15.255.9 docker ps
# Deve listar containers

# 4. MCP Python via SSH funciona?
ssh rafael@15.15.255.9 python3 /home/rafael/mcp-servers/memory-manager/server.py
# Deve iniciar (Ctrl+C para sair)

# 5. MCP Docker via SSH funciona?
ssh rafael@15.15.255.9 docker exec -i igo-docker-admin python server.py
# Deve iniciar (Ctrl+C para sair)
```

### Teste nos Editores

**VSCode/Cursor:**
```python
# No chat do editor:
docker-admin.health_check()
memory-manager.load_context()
agente-resumo.get_next_steps()
```

Se todos funcionarem, **setup completo**! ✅

## ⚡ 6. Performance Remota

### Latência Esperada

```
┌─────────────────────┬──────────┬────────────┐
│ Operação            │ Local    │ Remoto     │
├─────────────────────┼──────────┼────────────┤
│ MCP Python          │ <1ms     │ 10-50ms    │
│ MCP Docker          │ 10-50ms  │ 50-100ms   │
│ Carregar contexto   │ 1ms      │ 20-60ms    │
│ Processar Excel     │ 100ms    │ 120-180ms  │
│ Invocar agente      │ 1ms      │ 20-60ms    │
└─────────────────────┴──────────┴────────────┘
```

### Otimizações

1. **SSH KeepAlive** (já configurado em `.ssh/config`)
2. **Conexão persistente** (SSH ControlMaster)
3. **Compressão SSH**

Adicione ao `~/.ssh/config`:

```
Host mcp-server
    HostName 15.15.255.9
    User rafael
    IdentityFile ~/.ssh/id_ed25519

    # Keep connection alive
    ServerAliveInterval 60
    ServerAliveCountMax 3

    # Reuse connections (faster)
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

    # Compression
    Compression yes
```

Criar diretório para sockets:
```bash
mkdir -p ~/.ssh/sockets
```

## 🐛 Troubleshooting

### SSH pede senha

**Causa:** Chave SSH não configurada

**Solução:**
```bash
ssh-copy-id rafael@15.15.255.9
```

Veja: [SSH_WINDOWS_KEYS.md](docs/SSH_WINDOWS_KEYS.md)

### "Connection refused"

**Causa:** Servidor offline ou SSH Server não rodando

**Solução:**
```bash
# Verificar se servidor está online
ping 15.15.255.9

# Tentar SSH direto
ssh rafael@15.15.255.9
```

### "Command not found: docker"

**Causa:** Docker não está no PATH do SSH

**Solução:**
No servidor, edite `~/.bashrc`:
```bash
export PATH="/usr/local/bin:/usr/bin:$PATH"
```

Ou use caminho completo no `.mcp.remote.json`:
```json
{
  "args": [
    "rafael@15.15.255.9",
    "/usr/bin/docker",
    "exec",
    ...
  ]
}
```

### MCP Python: "ModuleNotFoundError"

**Causa:** Dependências não instaladas no servidor

**Solução:**
```bash
ssh rafael@15.15.255.9
cd /home/rafael/mcp-servers/nome-do-mcp
pip3 install -r requirements.txt
```

### MCP Docker: "No such container"

**Causa:** Container não está rodando

**Solução:**
```bash
ssh rafael@15.15.255.9
cd /home/rafael/mcp-servers
docker-compose up -d
docker-compose ps  # Verificar
```

### Latência muito alta (>500ms)

**Causa:** Rede lenta ou sem otimizações SSH

**Solução:**
1. Configurar SSH ControlMaster (veja seção Otimizações)
2. Verificar conexão de rede
3. Considerar usar VPN se estiver acessando pela internet

### Editor não detecta MCPs

**Causa:** Arquivo de config errado ou não recarregou

**Solução:**
1. Verificar que `.mcp.json` aponta para config remota
2. Reload do editor
3. Verificar logs do editor

## 📊 Comparação: Local vs Remoto

| Aspecto | Local | Remoto |
|---------|-------|--------|
| **Latência** | <1ms | 20-100ms |
| **Setup** | Simples | Requer SSH |
| **Recursos** | PC local | Servidor |
| **Acesso** | Apenas local | De qualquer lugar |
| **Compartilhamento** | Não | Sim (múltiplos PCs) |
| **Manutenção** | Local | Centralizada |

## 🎯 Casos de Uso

### Use Local quando:
- Desenvolvimento ativo
- Latência crítica
- Sem acesso à internet
- Recursos locais suficientes

### Use Remoto quando:
- Trabalhar de múltiplos PCs
- Servidor tem mais recursos
- Compartilhar MCPs com equipe
- Dados precisam ficar no servidor

## 📚 Arquivos Relacionados

- [.mcp.json](.mcp.json) - Config local
- [.mcp.remote.json](.mcp.remote.json) - Config remota
- [docs/SETUP_REMOTE_MCP.md](docs/SETUP_REMOTE_MCP.md) - Doc original
- [docs/SSH_WINDOWS_KEYS.md](docs/SSH_WINDOWS_KEYS.md) - SSH no Windows

## 🎓 Próximos Passos

Após configurar o acesso remoto:

1. ✅ Leia: [GUIDELINES.md](GUIDELINES.md) - Entender MCPs
2. ✅ Leia: [MCP_QUICK_REFERENCE.md](MCP_QUICK_REFERENCE.md) - Comandos rápidos
3. ✅ Configure: Atalhos do seu editor
4. ✅ Teste: Todos os 10 MCPs
5. ✅ Otimize: SSH ControlMaster

---

**🌐 Setup remoto completo!** Agora você pode usar os MCPs do servidor `15.15.255.9` de qualquer PC.

**💡 Dica:** Para melhor performance, configure SSH ControlMaster na seção Otimizações.
