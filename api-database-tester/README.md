# API & Database Tester MCP

MCP para executar requisições HTTP e queries SQL, permitindo que agentes de IA interajam com APIs e bancos de dados.

## 🎯 Funcionalidades

- ✅ Requisições HTTP (GET, POST, PUT, DELETE, PATCH)
- ✅ Queries SQL em **SQL Server** (ODBC Driver 18)
- ✅ Queries SQL em **PostgreSQL**
- ✅ Suporte a Bearer Token
- ✅ Teste rápido de APIs
- ✅ Consulta de schemas de tabelas

## 🔧 Ferramentas Disponíveis

### 1. `execute_http_request`

Executa requisições HTTP flexíveis.

**Parâmetros:**
- `url` (str): URL completa
- `method` (str): GET, POST, PUT, DELETE, PATCH (default: GET)
- `headers` (str): JSON string com headers
- `body` (str): JSON string com body
- `timeout` (int): Timeout em segundos (default: 30)

**Exemplo:**
```python
mcp__api-database-tester__execute_http_request(
    url="https://api.example.com/eventos/200",
    method="GET",
    headers='{"Authorization": "Bearer token123"}',
    timeout=30
)
```

### 2. `execute_sql_query`

Executa queries SQL em SQL Server ou PostgreSQL.

**Parâmetros:**
- `query` (str): Query SQL
- `connection_string` (str): String de conexão
- `database_type` (str): "sqlserver" ou "postgresql"
- `fetch_limit` (int): Limite de registros (default: 100)

**Exemplo SQL Server:**
```python
mcp__api-database-tester__execute_sql_query(
    query="SELECT TOP 10 * FROM Notas WHERE id_evento = 200",
    connection_string="DRIVER={ODBC Driver 18 for SQL Server};SERVER=prod;DATABASE=Astrazeneca;UID=user;PWD=pass;TrustServerCertificate=yes",
    database_type="sqlserver"
)
```

**Exemplo PostgreSQL:**
```python
mcp__api-database-tester__execute_sql_query(
    query="SELECT * FROM notas WHERE id_evento = 200 LIMIT 10",
    connection_string="postgresql://user:pass@host:5432/dbname",
    database_type="postgresql"
)
```

### 3. `quick_api_test`

Teste rápido de API com Bearer Token.

**Parâmetros:**
- `endpoint` (str): URL do endpoint
- `bearer_token` (str): Token JWT (opcional)
- `method` (str): Método HTTP (default: GET)

**Exemplo:**
```python
mcp__api-database-tester__quick_api_test(
    endpoint="https://api.igojourney.com/eventos/200",
    bearer_token="eyJhbGc...",
    method="GET"
)
```

### 4. `get_table_schema`

Retorna schema de uma tabela.

**Parâmetros:**
- `table_name` (str): Nome da tabela
- `connection_string` (str): String de conexão
- `database_type` (str): "sqlserver" ou "postgresql"

**Exemplo:**
```python
mcp__api-database-tester__get_table_schema(
    table_name="Notas",
    connection_string="...",
    database_type="sqlserver"
)
```

## 🧪 Testes com APIs Públicas

### Teste 1: JSONPlaceholder API

```python
execute_http_request(
    url="https://jsonplaceholder.typicode.com/posts/1",
    method="GET"
)
```

**Resultado:**
```json
{
  "success": true,
  "status_code": 200,
  "body": {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "..."
  }
}
```

### Teste 2: HTTPBin Echo

```python
execute_http_request(
    url="https://httpbin.org/anything",
    method="POST",
    body='{"teste": "I Go Journey MCP"}',
    headers='{"Content-Type": "application/json"}'
)
```

**Resultado:**
```json
{
  "success": true,
  "status_code": 200,
  "body": {
    "json": {
      "teste": "I Go Journey MCP"
    }
  }
}
```

### Teste 3: GitHub API

```python
quick_api_test(
    endpoint="https://api.github.com/users/github",
    method="GET"
)
```

**Resultado:**
```json
{
  "success": true,
  "status_code": 200,
  "body": {
    "login": "github",
    "name": "GitHub",
    "public_repos": 533
  }
}
```

## 🔐 Segurança

- Timeouts configuráveis (default: 30s)
- Fetch limit para queries SQL (default: 100 registros)
- Suporte a TrustServerCertificate para SQL Server

## 📦 Dependências

- `mcp>=1.0.0` - Framework MCP
- `httpx>=0.27.0` - Requisições HTTP
- `pyodbc>=5.1.0` - SQL Server connector
- `psycopg2-binary>=2.9.0` - PostgreSQL connector
- `sqlparse>=0.4.4` - SQL formatting

## 🐳 Container

**Nome:** `igo-api-database-tester`
**Imagem:** Python 3.11-slim + ODBC Driver 18
**Status:** ✅ Rodando

## 💡 Exemplos de Uso

### Cenário 1: Testar API de Eventos

```python
# Via agente OpenAI Gateway
run_agent(
    agent_name="agente-backend",
    task="Teste a API de eventos do I Go Journey no endpoint /api/eventos/200"
)

# O agente chamaria internamente:
quick_api_test(
    endpoint="https://api.igojourney.com/api/eventos/200",
    bearer_token="<token>",
    method="GET"
)
```

### Cenário 2: Listar Notas do Banco

```python
# Via agente de IA
task = "Liste as 10 primeiras notas do evento 200 do banco Astrazeneca"

# O agente chamaria:
execute_sql_query(
    query="SELECT TOP 10 * FROM Notas WHERE id_evento = 200",
    connection_string="DRIVER={ODBC Driver 18 for SQL Server};SERVER=prod;DATABASE=Astrazeneca;UID=user;PWD=pass;TrustServerCertificate=yes",
    database_type="sqlserver"
)
```

### Cenário 3: Verificar Schema de Tabela

```python
get_table_schema(
    table_name="Participantes",
    connection_string="...",
    database_type="sqlserver"
)
```

**Retorna:**
```json
{
  "success": true,
  "row_count": 15,
  "columns": ["column_name", "data_type", "max_length", "is_nullable"],
  "data": [
    {
      "column_name": "id",
      "data_type": "int",
      "max_length": null,
      "is_nullable": "NO"
    },
    ...
  ]
}
```

## 🚀 Como Usar

1. **Certifique-se que o container está rodando:**
   ```bash
   docker ps | grep igo-api-database-tester
   ```

2. **Teste diretamente:**
   ```bash
   docker exec -i igo-api-database-tester python -c "
   from server import quick_api_test
   print(quick_api_test('https://httpbin.org/get'))
   "
   ```

3. **Use via Claude Code:**
   As ferramentas estarão disponíveis automaticamente com prefixo `mcp__api-database-tester__`

## ⚠️ Notas Importantes

### SQL Server
- Driver: **ODBC Driver 18 for SQL Server**
- Adicione `TrustServerCertificate=yes` se tiver problemas de certificado
- Use `TOP N` para limitar resultados

### PostgreSQL
- Use `LIMIT N` para limitar resultados
- Connection string: `postgresql://user:pass@host:5432/dbname`

### HTTP Requests
- Headers e body devem ser JSON strings
- Suporte a redirect automático
- Timeout padrão: 30 segundos

## 🔄 Atualização

Para reconstruir o container:
```bash
docker-compose build api-database-tester
docker-compose up -d api-database-tester
```

## 📝 Logs

Ver logs do container:
```bash
docker logs igo-api-database-tester -f
```

---

**Criado em:** 2026-01-25
**Última atualização:** 2026-01-25
**Status:** ✅ Produção
