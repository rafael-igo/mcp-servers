# Configuração MCP em Servidor Remoto (Docker)

Este guia mostra como rodar os MCPs em um servidor remoto (ex.: `15.15.255.9`) e como apontar clientes locais (Claude Desktop / VSCode) via SSH.

## ✅ Pré-requisitos no servidor

- Docker e Docker Compose instalados
- Repositório `mcp-servers` disponível no servidor
- Acesso SSH ao servidor

## 1) Subir MCPs no servidor

No servidor remoto:

```bash
cd /caminho/para/mcp-servers

docker-compose up -d
```

Verifique se os containers estão ativos:

```bash
docker-compose ps
```

## 2) Acesso remoto via SSH (recomendado)

Como os MCPs usam **stdio**, o jeito mais simples é executar o `docker exec` via SSH.

Exemplo para Claude Desktop / VSCode (no arquivo `mcp.json` ou `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "agente-orchestrator": {
      "command": "ssh",
      "args": [
        "usuario@15.15.255.9",
        "docker",
        "exec",
        "-i",
        "igo-agente-orchestrator",
        "python",
        "server.py"
      ],
      "env": {}
    }
  }
}
```

> Dica: configure chave SSH para não pedir senha.

## 3) Sobre expor portas na rede

Os MCPs padrão **não expõem portas** (usam `stdio`).
Se você precisar compartilhar acesso na rede local sem SSH, será necessário um **bridge** para TCP/HTTP (fora do escopo deste repo) e então expor a porta via `docker-compose` e firewall.

## 4) Checklist rápido

- [ ] SSH funcionando
- [ ] Containers ativos no servidor
- [ ] `mcp.json` local aponta para `ssh user@15.15.255.9 docker exec ...`
- [ ] Claude Desktop / VSCode reiniciado após alteração
