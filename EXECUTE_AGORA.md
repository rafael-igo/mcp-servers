# 🚀 Execute Estes Comandos Agora

## Abra o PowerShell

1. Pressione `Win + X`
2. Selecione "Windows PowerShell" ou "Terminal"
3. Execute os comandos abaixo:

## Comandos

```powershell
# 1. Parar containers existentes
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose down"

# 2. Subir todos os 10 MCPs
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose up -d"

# 3. Verificar status (deve mostrar 10 containers)
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose ps"
```

## Alternativa: Script Automático

Ou execute o script que criei:

```powershell
cd C:\GIT-RAFAEL\mcp-servers
.\restart-mcps.ps1
```

Se der erro de "execução de scripts desabilitada", execute primeiro:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Ou pelo CMD

```cmd
cd C:\GIT-RAFAEL\mcp-servers
restart-mcps.bat
```

---

## O que deve acontecer:

### 1. docker-compose down
```
Stopping igo-docker-admin ... done
Stopping igo-api-database-tester ... done
Removing igo-docker-admin ... done
Removing igo-api-database-tester ... done
Removing network mcp-servers_mcp-network ... done
```

### 2. docker-compose up -d
```
Creating network "mcp-servers_mcp-network" with driver "bridge"
Creating igo-excel-server ... done
Creating igo-agente-orchestrator ... done
Creating igo-memory-manager ... done
Creating igo-checklist-validator ... done
Creating igo-agente-insights ... done
Creating igo-agente-resumo ... done
Creating igo-docker-admin ... done
Creating igo-openai-gateway ... done
Creating igo-api-database-tester ... done
Creating igo-vuetify-uiux ... done
```

### 3. docker-compose ps
```
NAME                          STATUS
igo-agente-insights           Up
igo-agente-orchestrator       Up
igo-agente-resumo             Up
igo-api-database-tester       Up
igo-checklist-validator       Up
igo-docker-admin              Up
igo-excel-server              Up
igo-memory-manager            Up
igo-openai-gateway            Up
igo-vuetify-uiux              Up
```

**Deve mostrar 10 containers com status "Up"!**

---

## Após Executar

1. ✅ Verifique que 10 containers estão rodando
2. ✅ Abra VSCode/Cursor
3. ✅ Reload Window: `Ctrl+Shift+P` → "Reload Window"
4. ✅ Teste: `docker-admin.health_check()`

---

## Troubleshooting

### "Permission denied"
```powershell
# Verificar chave SSH
ssh rafael@15.15.255.9 echo "OK"
```

### "No such file or directory"
```powershell
# Verificar caminho no servidor
ssh rafael@15.15.255.9 "ls -la /home/rafael/"
```

### Containers não sobem
```powershell
# Ver logs
ssh rafael@15.15.255.9 "cd /home/rafael/mcp-servers && docker-compose logs"
```

---

**Pronto para executar!** 🚀

Copie e cole os comandos no PowerShell.
