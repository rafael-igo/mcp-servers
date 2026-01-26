# Setup Windows → Servidor Linux Remoto

## 🎯 Problema

Windows não consegue acessar diretamente arquivos Python no servidor Linux via SSH (diferente de Mac/Linux).

## ✅ Soluções

### Opção 1: Todos MCPs via Docker + SSH ⭐ (Recomendado)

**Prós:**
- ✅ Mais confiável
- ✅ Funciona 100% no Windows
- ✅ Não precisa mapear filesystem
- ✅ Já testado e funcionando

**Contras:**
- ⚠️ Todos os MCPs em Docker (mais recursos no servidor)
- ⚠️ Latência ~50-100ms

**Setup:**

1. **No servidor (15.15.255.9):**
   ```bash
   cd /home/rafael/mcp-servers

   # Usar docker-compose COMPLETO (todos os 10 MCPs)
   docker-compose -f docker-compose.full.yml up -d

   # Ou se tiver apenas docker-compose.yml padrão:
   # Adicione os 8 MCPs Python de volta ao docker-compose.yml
   ```

2. **No Windows:**
   ```powershell
   # Renomear configuração
   cd C:\GIT-RAFAEL\mcp-servers

   # Backup configs locais
   Rename-Item .mcp.json .mcp.local.json

   # Usar config Docker remota
   Rename-Item .mcp.remote-docker.json .mcp.json
   ```

3. **Testar:**
   ```powershell
   # Testar SSH
   ssh rafael@15.15.255.9 docker ps

   # Deve listar todos os 10 containers
   ```

---

### Opção 2: VSCode Remote SSH 🔥 (Melhor UX)

**Prós:**
- ✅ VSCode monta filesystem automaticamente
- ✅ Debug remoto nativo
- ✅ Terminal remoto
- ✅ Pode usar MCPs Python direto

**Contras:**
- ⚠️ Só funciona no VSCode
- ⚠️ Requer extensão

**Setup:**

1. **Instalar extensão VSCode:**
   - Abra VSCode
   - Extensions (Ctrl+Shift+X)
   - Busque: "Remote - SSH"
   - Instale: `ms-vscode-remote.remote-ssh`

2. **Conectar ao servidor:**
   ```
   Ctrl+Shift+P → "Remote-SSH: Connect to Host"
   Digite: rafael@15.15.255.9
   ```

3. **Abrir projeto remoto:**
   ```
   File → Open Folder
   Navegue: /home/rafael/mcp-servers
   ```

4. **Usar .mcp.json local no servidor:**
   - Arquivo `.mcp.json` do servidor aponta para Python local
   - MCPs rodam no servidor como se fosse local
   - VSCode acessa via SSH automaticamente

**Arquitetura:**
```
Windows VSCode
    │
    │ Remote SSH Extension
    │
    ▼
Servidor Linux
    │
    ├─ VSCode Server (auto-instalado)
    ├─ Projeto /home/rafael/mcp-servers
    └─ MCPs Python rodando localmente no servidor
```

---

### Opção 3: Híbrido (Apenas 2 Docker Remotos)

Rodar apenas `docker-admin` e `api-database-tester` remotamente, o resto localmente no Windows.

**Prós:**
- ✅ Menos recursos no servidor
- ✅ Desenvolvimento local rápido

**Contras:**
- ⚠️ Dados ficam divididos (servidor + local)
- ⚠️ Precisa instalar Python/deps no Windows

**Setup:**

1. **Instalar Python 3.11+ no Windows**

2. **Instalar dependências:**
   ```powershell
   cd C:\GIT-RAFAEL\mcp-servers

   # Para cada MCP Python
   cd excel-server
   pip install -r requirements.txt
   cd ..

   # Repetir para os 8 MCPs
   ```

3. **Usar configuração híbrida:**
   ```json
   {
     "mcpServers": {
       // Locais (Windows)
       "excel-server": {
         "command": "python",
         "args": ["C:/GIT-RAFAEL/mcp-servers/excel-server/server.py"]
       },

       // Remotos (via SSH)
       "docker-admin": {
         "command": "ssh",
         "args": ["rafael@15.15.255.9", "docker", "exec", "-i", "igo-docker-admin", "python", "server.py"]
       }
     }
   }
   ```

---

## 🎯 Qual Escolher?

### Desenvolvimento Ativo no Projeto
**Use: Opção 2 (VSCode Remote SSH)**
- Melhor experiência de desenvolvimento
- Debug nativo
- Terminal remoto
- Hot reload

### Uso Produtivo/Estável
**Use: Opção 1 (Todos via Docker)**
- Mais confiável
- Testado e funcionando
- Não depende de VSCode

### Recursos Limitados no Servidor
**Use: Opção 3 (Híbrido)**
- Menos carga no servidor
- Desenvolvimento local rápido

---

## 📋 Setup Opção 1 (Todos Docker) - Passo a Passo

### 1. Configurar SSH (Windows)

**Instalar OpenSSH (se não tiver):**
```powershell
# Verificar se está instalado
ssh -V

# Se não estiver, instalar via Settings:
# Settings → Apps → Optional Features → OpenSSH Client
```

**Gerar chave SSH:**
```powershell
ssh-keygen -t ed25519 -C "rafael@windows"
# Pressione Enter 3x (sem senha)
```

**Copiar chave para servidor:**
```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh rafael@15.15.255.9 "cat >> ~/.ssh/authorized_keys"
```

**Testar:**
```powershell
ssh rafael@15.15.255.9 echo "OK"
# Deve imprimir: OK (sem pedir senha)
```

### 2. Configurar Servidor

**SSH no servidor:**
```powershell
ssh rafael@15.15.255.9
```

**No servidor:**
```bash
cd /home/rafael/mcp-servers

# Subir TODOS os containers (precisa docker-compose completo)
docker-compose up -d

# Verificar (deve mostrar 10 containers)
docker-compose ps
```

**Se docker-compose.yml tem apenas 2 serviços:**

Você precisa adicionar os outros 8 de volta. Use o arquivo antigo ou crie:

```bash
# Voltar para versão com todos os MCPs
git checkout <commit-anterior-com-8-containers>

# Ou criar manualmente adicionando os 8 serviços
```

### 3. Configurar Windows

**No Windows:**
```powershell
cd C:\GIT-RAFAEL\mcp-servers

# Backup config local
Rename-Item .mcp.json .mcp.local.json

# Usar config Docker remota
Rename-Item .mcp.remote-docker.json .mcp.json

# Verificar
Get-Content .mcp.json
```

### 4. Configurar Editor

**VSCode:**
```
1. Reload Window (Ctrl+Shift+P → "Reload Window")
2. Abrir Claude Code chat
3. Testar: docker-admin.health_check()
```

**Cursor:**
```
1. Restart Cursor
2. Abrir chat (Ctrl+L)
3. Testar: memory-manager.load_context()
```

### 5. Verificar

```powershell
# Teste 1: SSH funciona sem senha
ssh rafael@15.15.255.9 echo "OK"

# Teste 2: Docker está rodando
ssh rafael@15.15.255.9 docker ps

# Teste 3: Container responde
ssh rafael@15.15.255.9 docker exec -i igo-memory-manager python server.py
# Ctrl+C para sair

# Teste 4: No editor
# docker-admin.health_check()
# Deve retornar status de todos containers
```

---

## 📋 Setup Opção 2 (VSCode Remote SSH) - Passo a Passo

### 1. Instalar Extensão

**VSCode:**
```
1. Ctrl+Shift+X (Extensions)
2. Buscar: "Remote - SSH"
3. Instalar: ms-vscode-remote.remote-ssh
4. Reload VSCode
```

### 2. Configurar SSH

Mesmo processo da Opção 1 (gerar chave, copiar, testar).

### 3. Conectar ao Servidor

**VSCode:**
```
1. Ctrl+Shift+P
2. "Remote-SSH: Connect to Host..."
3. Digite: rafael@15.15.255.9
4. Selecione: Linux
5. Aguarde VSCode instalar server remoto
```

### 4. Abrir Projeto Remoto

**VSCode (já conectado via SSH):**
```
1. File → Open Folder
2. Navegue: /home/rafael/mcp-servers
3. Click "OK"
```

Agora você está trabalhando DIRETAMENTE no servidor!

### 5. Configurar MCPs

**No servidor (via VSCode Remote):**

O arquivo `.mcp.json` já existe e aponta para Python local:
```json
{
  "excel-server": {
    "command": "python3",
    "args": ["/home/rafael/mcp-servers/excel-server/server.py"]
  }
}
```

Mas como você está no VSCode Remote, "local" = servidor!

### 6. Instalar Dependências

**Terminal VSCode (já no servidor):**
```bash
# Você já está em /home/rafael/mcp-servers
for dir in excel-server agente-orchestrator memory-manager checklist-validator agente-insights agente-resumo igo-openai-gateway vuetify-uiux; do
    cd $dir
    pip3 install -r requirements.txt
    cd ..
done

# Subir apenas os 2 Docker containers
docker-compose up -d
```

### 7. Testar

**VSCode Remote:**
```
1. Abrir Claude Code chat
2. docker-admin.health_check()
3. memory-manager.load_context()
```

Tudo roda no servidor, mas você desenvolve como se fosse local!

---

## 🆚 Comparação

| Aspecto | Opção 1 (Docker) | Opção 2 (Remote SSH) | Opção 3 (Híbrido) |
|---------|------------------|----------------------|-------------------|
| **Latência** | 50-100ms | 20-60ms | <1ms + 50ms |
| **Setup** | Simples | Médio | Complexo |
| **Recursos Servidor** | Alto (10 containers) | Médio (8 Python + 2 Docker) | Baixo (2 Docker) |
| **VSCode** | Funciona | Funciona melhor | Funciona |
| **Cursor** | Funciona | Não funciona | Funciona |
| **Codex** | Funciona | Não funciona | Funciona |
| **Debug** | Logs | Nativo VSCode | Misto |

---

## 🎯 Recomendação Final

**Para você (Windows → Servidor Linux):**

1. **Desenvolvimento:** Opção 2 (VSCode Remote SSH)
   - Melhor experiência
   - Debug nativo
   - Trabalha como se fosse local

2. **Produção/Estável:** Opção 1 (Todos Docker)
   - Mais confiável
   - Funciona em qualquer editor
   - Testado e aprovado

---

## 🐛 Troubleshooting

### SSH pede senha
```powershell
# Copiar chave novamente
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh rafael@15.15.255.9 "cat >> ~/.ssh/authorized_keys"
```

### Container não existe
```bash
# No servidor
docker-compose ps  # Ver quais estão rodando
docker-compose up -d  # Subir todos
```

### VSCode Remote não conecta
```
1. Verificar SSH funciona: ssh rafael@15.15.255.9
2. Remover host: Ctrl+Shift+P → "Remote-SSH: Kill Current Server"
3. Conectar novamente
```

---

**📞 Qual opção você prefere?**
- Opção 1: Simples, todos Docker via SSH
- Opção 2: VSCode Remote SSH (melhor UX)
- Opção 3: Híbrido (local + remoto)
