# I Go OpenAI Gateway MCP

Gateway MCP para executar tarefas via OpenAI Responses API.

## ✅ Configuração

Defina a variável de ambiente no host ou via Docker:

```bash
export OPENAI_API_KEY="sua-chave-aqui"
```

## 🐳 Docker Compose

Adicione o serviço no `docker-compose.yml`:

```yaml
  igo-openai-gateway:
    build: ./igo-openai-gateway
    container_name: igo-openai-gateway
    stdin_open: true
    tty: true
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    volumes:
      - ../../:/project:ro
    restart: unless-stopped
    networks:
      - mcp-network
```

## 🔧 Ferramentas

- `run_prompt(prompt, input_text, model, temperature, max_output_tokens)`
- `run_agent(agent_name, task, model, temperature, max_output_tokens, include_context)`

## 🧪 Teste rápido

```bash
echo '{"method":"tools/list"}' | docker exec -i igo-openai-gateway python server.py
```
