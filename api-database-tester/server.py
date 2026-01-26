#!/usr/bin/env python3
"""
API & Database Tester MCP
==========================
MCP para executar requisições HTTP e queries SQL em bancos de dados.
Suporta SQL Server e PostgreSQL.

Ferramentas:
- execute_http_request: Requisições HTTP flexíveis
- execute_sql_query: Queries SQL em SQL Server ou PostgreSQL
- quick_api_test: Teste rápido de API com Bearer Token
- get_table_schema: Obter schema de tabelas
"""

import json
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("api-database-tester")


@mcp.tool()
def execute_http_request(
    url: str,
    method: str = "GET",
    headers: Optional[str] = None,
    body: Optional[str] = None,
    timeout: int = 30,
) -> str:
    """
    Executa requisição HTTP e retorna resposta formatada.

    Args:
        url: URL completa da requisição
        method: GET, POST, PUT, DELETE, PATCH (default: GET)
        headers: Headers HTTP como JSON string (ex: '{"Authorization": "Bearer token"}')
        body: Request body como JSON string (para POST/PUT)
        timeout: Timeout em segundos (default: 30)

    Returns:
        JSON com resultado da requisição

    Exemplo:
        execute_http_request(
            url="https://api.example.com/eventos/200",
            method="GET",
            headers='{"Authorization": "Bearer token123"}'
        )
    """
    try:
        import httpx

        # Parse headers
        parsed_headers = {}
        if headers:
            parsed_headers = json.loads(headers)

        # Parse body
        parsed_body = None
        if body:
            try:
                parsed_body = json.loads(body)
            except json.JSONDecodeError:
                # Se não for JSON, mandar como texto
                parsed_body = body

        # Execute request
        client = httpx.Client(timeout=timeout)
        response = client.request(
            method=method.upper(),
            url=url,
            headers=parsed_headers,
            json=parsed_body if isinstance(parsed_body, dict) else None,
            content=parsed_body if isinstance(parsed_body, str) else None,
        )
        client.close()

        # Try to parse response as JSON
        try:
            response_body = response.json()
        except Exception:
            response_body = response.text

        # Format response
        result = {
            "success": True,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response_body,
            "url": url,
            "method": method.upper(),
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps(
            {
                "success": False,
                "error": str(e),
                "url": url,
                "method": method.upper(),
            },
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
def execute_sql_query(
    query: str,
    connection_string: str,
    database_type: str = "sqlserver",
    fetch_limit: int = 100,
) -> str:
    """
    Executa query SQL e retorna resultados formatados.

    Args:
        query: Query SQL a executar
        connection_string: String de conexão ao banco
        database_type: "sqlserver" ou "postgresql" (default: sqlserver)
        fetch_limit: Limite de registros a retornar (default: 100)

    Returns:
        JSON com resultados da query

    Exemplo SQL Server:
        execute_sql_query(
            query="SELECT TOP 10 * FROM Notas WHERE id_evento = 200",
            connection_string="DRIVER={ODBC Driver 17 for SQL Server};SERVER=server;DATABASE=db;UID=user;PWD=pass",
            database_type="sqlserver"
        )

    Exemplo PostgreSQL:
        execute_sql_query(
            query="SELECT * FROM notas WHERE id_evento = 200 LIMIT 10",
            connection_string="postgresql://user:pass@host:5432/dbname",
            database_type="postgresql"
        )
    """
    try:
        if database_type.lower() == "sqlserver":
            import pyodbc

            conn = pyodbc.connect(connection_string, timeout=30)
        elif database_type.lower() == "postgresql":
            import psycopg2

            conn = psycopg2.connect(connection_string, connect_timeout=30)
        else:
            raise ValueError(
                f"Database type '{database_type}' não suportado. Use 'sqlserver' ou 'postgresql'"
            )

        cursor = conn.cursor()

        # Execute query
        cursor.execute(query)

        # Check if query returns results (SELECT) or just executes (INSERT/UPDATE/DELETE)
        if cursor.description:
            # Fetch results for SELECT queries
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchmany(fetch_limit)

            # Convert to list of dicts
            results = []
            for row in rows:
                row_dict = {}
                for i, value in enumerate(row):
                    # Convert special types to strings
                    if value is not None:
                        row_dict[columns[i]] = value
                    else:
                        row_dict[columns[i]] = None
                results.append(row_dict)

            cursor.close()
            conn.close()

            return json.dumps(
                {
                    "success": True,
                    "row_count": len(results),
                    "columns": columns,
                    "data": results,
                    "query": query,
                    "database_type": database_type,
                },
                ensure_ascii=False,
                indent=2,
                default=str,  # Handle datetime/decimal serialization
            )
        else:
            # For INSERT/UPDATE/DELETE queries
            conn.commit()
            affected_rows = cursor.rowcount

            cursor.close()
            conn.close()

            return json.dumps(
                {
                    "success": True,
                    "affected_rows": affected_rows,
                    "query": query,
                    "database_type": database_type,
                },
                ensure_ascii=False,
                indent=2,
            )

    except Exception as e:
        return json.dumps(
            {
                "success": False,
                "error": str(e),
                "query": query,
                "database_type": database_type,
            },
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
def quick_api_test(
    endpoint: str,
    bearer_token: Optional[str] = None,
    method: str = "GET",
) -> str:
    """
    Teste rápido de API com Bearer Token.

    Args:
        endpoint: URL do endpoint
        bearer_token: Token JWT (opcional)
        method: Método HTTP (default: GET)

    Returns:
        JSON com resultado da requisição

    Exemplo:
        quick_api_test(
            endpoint="https://api.example.com/eventos/200",
            bearer_token="eyJhbGc...",
            method="GET"
        )
    """
    headers = {}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"

    headers_str = json.dumps(headers) if headers else None

    return execute_http_request(
        url=endpoint,
        method=method,
        headers=headers_str,
    )


@mcp.tool()
def get_table_schema(
    table_name: str,
    connection_string: str,
    database_type: str = "sqlserver",
) -> str:
    """
    Retorna schema de uma tabela (colunas e tipos).

    Args:
        table_name: Nome da tabela
        connection_string: String de conexão ao banco
        database_type: "sqlserver" ou "postgresql" (default: sqlserver)

    Returns:
        JSON com schema da tabela

    Útil para o agente de IA saber quais campos consultar.

    Exemplo:
        get_table_schema(
            table_name="Notas",
            connection_string="...",
            database_type="sqlserver"
        )
    """
    try:
        if database_type.lower() == "sqlserver":
            query = f"""
                SELECT
                    COLUMN_NAME as column_name,
                    DATA_TYPE as data_type,
                    CHARACTER_MAXIMUM_LENGTH as max_length,
                    IS_NULLABLE as is_nullable
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """
        elif database_type.lower() == "postgresql":
            query = f"""
                SELECT
                    column_name,
                    data_type,
                    character_maximum_length as max_length,
                    is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """
        else:
            raise ValueError(
                f"Database type '{database_type}' não suportado. Use 'sqlserver' ou 'postgresql'"
            )

        return execute_sql_query(query, connection_string, database_type, 1000)

    except Exception as e:
        return json.dumps(
            {
                "success": False,
                "error": str(e),
                "table": table_name,
                "database_type": database_type,
            },
            ensure_ascii=False,
            indent=2,
        )


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
