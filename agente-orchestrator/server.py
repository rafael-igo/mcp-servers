#!/usr/bin/env python3
"""
Agente Orchestrator MCP
=======================
Orquestração de agentes especializados do projeto.
"""

import errno
import sys
import json
from pathlib import Path
from typing import Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("agente-orchestrator")

# Caminho base do projeto
# Detectar se está rodando em Docker ou Windows local
import sys
if sys.platform == "win32":
    # Windows local
    PROJECT_ROOT = Path("c:/GIT-RAFAEL/mcp-servers")
    DOCS_DIR = PROJECT_ROOT / "docs"
else:
    # Docker (Linux)
    PROJECT_ROOT = Path("/project")
    DOCS_DIR = PROJECT_ROOT / "GIT-RAFAEL" / "mcp-servers" / "docs"

AGENTES_DIR = DOCS_DIR / "agentes"
MEMORIA_DIR = DOCS_DIR / "memoria"


@mcp.tool()
def list_agents() -> str:
    """
    Lista todos os agentes disponíveis e seus status.

    Returns:
        JSON string com lista de agentes
    """
    try:
        # Garantir que diretório de agentes existe (se o volume permitir escrita)
        read_only = False
        try:
            AGENTES_DIR.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            if e.errno in (errno.EROFS, errno.EACCES):
                read_only = True
            else:
                raise

        # Listar MCPs disponíveis (serviços Docker independentes)
        mcps = [
            {
                "name": "agente-insights",
                "type": "mcp",
                "title": "Agente de Insights",
                "description": "Captura ideias, consulta especialistas, toma decisões"
            },
            {
                "name": "agente-resumo",
                "type": "mcp",
                "title": "Agente de Resumo",
                "description": "Status, progresso, relatórios e métricas"
            },
            {
                "name": "igo-openai-gateway",
                "type": "mcp",
                "title": "OpenAI Gateway",
                "description": "Gateway GPT-5.2 para agentes de IA, análise de código e arquitetura"
            },
            {
                "name": "api-database-tester",
                "type": "mcp",
                "title": "API & Database Tester",
                "description": "Executa requisições HTTP e queries SQL em SQL Server/PostgreSQL"
            },
            {
                "name": "excel-server",
                "type": "mcp",
                "title": "Excel Server",
                "description": "Leitura e manipulação de arquivos Excel"
            },
            {
                "name": "memory-manager",
                "type": "mcp",
                "title": "Memory Manager",
                "description": "Gerenciamento de contexto e memória do projeto"
            },
            {
                "name": "checklist-validator",
                "type": "mcp",
                "title": "Checklist Validator",
                "description": "Validação e gerenciamento de checklists"
            },
            {
                "name": "docker-admin",
                "type": "mcp",
                "title": "Docker Admin",
                "description": "Gerenciamento de containers Docker e infraestrutura"
            },
            {
                "name": "vuetify-uiux",
                "type": "mcp",
                "title": "Vuetify UI/UX Assistant",
                "description": "Consultor de design Vuetify 3: componentes, layouts, cores e acessibilidade"
            }
        ]

        # Verificar agentes em /docs/agentes
        agents = []
        if AGENTES_DIR.exists():
            for agent_dir in AGENTES_DIR.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("agente-"):
                    prompt_file = agent_dir / "PROMPT.md"
                    resp_file = agent_dir / "RESPONSABILIDADES.md"

                    agent_info = {
                        "name": agent_dir.name,
                        "path": str(agent_dir),
                        "has_prompt": prompt_file.exists(),
                        "has_responsibilities": resp_file.exists()
                    }

                    # Ler primeira linha do PROMPT para pegar especialidade
                    if prompt_file.exists():
                        with open(prompt_file, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                            for line in lines:
                                if line.startswith("# Prompt"):
                                    agent_info["title"] = line.strip("# \n")
                                    break

                    agents.append(agent_info)

        note = "MCPs ativos. Use tools diretas dos MCPs ou agentes em /docs/agentes."
        if read_only and not AGENTES_DIR.exists():
            note = (
                "MCPs ativos. Diretório /docs/agentes em modo somente leitura; "
                "nenhum diretório foi criado."
            )

        return json.dumps({
            "success": True,
            "count": len(mcps) + len(agents),
            "mcps": mcps,
            "agents": agents,
            "note": note
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def invoke_agent(agent_name: str, task: str) -> str:
    """
    Invoca um agente especializado com uma tarefa específica.

    Args:
        agent_name: Nome do agente (ex: "agente-rooming-list")
        task: Descrição da tarefa a ser executada

    Returns:
        JSON string com prompt completo do agente + contexto + tarefa
    """
    try:
        agent_dir = AGENTES_DIR / agent_name

        if not agent_dir.exists():
            return json.dumps({
                "success": False,
                "error": f"Agente '{agent_name}' não encontrado"
            })

        prompt_file = agent_dir / "PROMPT.md"
        if not prompt_file.exists():
            return json.dumps({
                "success": False,
                "error": f"Prompt do agente '{agent_name}' não encontrado"
            })

        # Ler prompt do agente
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read()

        # Ler contexto atual
        context = ""
        context_file = MEMORIA_DIR / "contexto-atual.md"
        if context_file.exists():
            with open(context_file, 'r', encoding='utf-8') as f:
                context = f.read()

        # Montar resposta
        result = {
            "success": True,
            "agent": agent_name,
            "task": task,
            "prompt": prompt,
            "context": context,
            "instructions": f"""
# Você foi invocado como: {agent_name}

## Tarefa Solicitada:
{task}

## Seu Prompt Especializado:
{prompt}

## Contexto Atual do Projeto:
{context}

## Instruções:
1. Siga rigorosamente seu prompt especializado acima
2. Use o contexto do projeto para entender o estado atual
3. Execute a tarefa solicitada
4. Atualize a memória após completar
"""
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_agent_docs(agent_name: str) -> str:
    """
    Retorna toda a documentação de um agente específico.

    Args:
        agent_name: Nome do agente

    Returns:
        JSON string com todos os documentos do agente
    """
    try:
        agent_dir = AGENTES_DIR / agent_name

        if not agent_dir.exists():
            return json.dumps({
                "success": False,
                "error": f"Agente '{agent_name}' não encontrado"
            })

        docs = {
            "success": True,
            "agent": agent_name,
            "files": {}
        }

        # Ler todos os arquivos .md do agente
        for file in agent_dir.glob("*.md"):
            with open(file, 'r', encoding='utf-8') as f:
                docs["files"][file.name] = f.read()

        return json.dumps(docs, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def update_agent_memory(action: str, details: str) -> str:
    """
    Atualiza a memória do sistema de agentes.

    Args:
        action: Ação realizada (ex: "completed_task")
        details: Detalhes da ação

    Returns:
        JSON string confirmando atualização
    """
    try:
        # Garantir que diretório de memória existe (se o volume permitir escrita)
        try:
            MEMORIA_DIR.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            if e.errno in (errno.EROFS, errno.EACCES):
                return json.dumps({
                    "success": False,
                    "error": "Memoria em modo somente leitura; use memory-manager para atualizar."
                })
            raise
        ultimas_acoes_file = MEMORIA_DIR / "ultimas-acoes.md"

        if not ultimas_acoes_file.exists():
            # Criar arquivo inicial
            with open(ultimas_acoes_file, 'w', encoding='utf-8') as f:
                f.write("# Últimas Ações\n\n")
                f.write("Histórico de ações realizadas pelos agentes.\n\n")
                f.write("---\n\n")

        # Ler conteúdo atual
        with open(ultimas_acoes_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Preparar nova entrada
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        new_entry = f"""
### {action} - {timestamp}
{details}

"""

        # Inserir após o primeiro cabeçalho de data
        lines = content.split('\n')
        insert_index = len(lines)  # Default: fim do arquivo
        for i, line in enumerate(lines):
            if line.startswith('## '):
                insert_index = i + 1
                break

        lines.insert(insert_index, new_entry)
        new_content = '\n'.join(lines)

        # Salvar
        with open(ultimas_acoes_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return json.dumps({
            "success": True,
            "message": "Memória atualizada com sucesso",
            "timestamp": timestamp
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def ask_ai_to_decide(
    user_request: str,
    project: str = "default",
    branch: str = "main"
) -> str:
    """
    Usa IA (GPT-5.2) para decidir qual agente usar baseado na requisição do usuário.

    Esta é a funcionalidade "cérebro" do orchestrator - quando você não sabe qual
    agente chamar, pergunte à IA!

    IMPORTANTE: Esta tool prepara os dados e retorna instruções para Claude Code
    chamar o igo-openai-gateway::decide_agent com reasoning.

    Args:
        user_request: Requisição do usuário (pode ser ambígua ou complexa)
        project: Nome do projeto (default: "default")
        branch: Nome da branch (default: "main")

    Returns:
        JSON com dados preparados e próximos passos

    Exemplo de uso:
        ask_ai_to_decide(
            user_request="Preciso melhorar a performance do rooming list",
            project="igo-journey",
            branch="main"
        )

        Resultado: Dados preparados para chamar igo-openai-gateway::decide_agent
    """
    try:
        # 1. Coletar lista de agentes disponíveis
        agents_result = list_agents()
        agents_data = json.loads(agents_result)

        if not agents_data.get("success"):
            return json.dumps({
                "success": False,
                "error": "Falha ao coletar lista de agentes",
                "details": agents_data
            })

        # 2. Carregar contexto do projeto
        context = ""
        context_file = MEMORIA_DIR / project / branch / "contexto-atual.md"
        if context_file.exists():
            with open(context_file, 'r', encoding='utf-8') as f:
                context = f.read()
        else:
            # Tentar contexto flat (backwards compatibility)
            old_context_file = MEMORIA_DIR / "contexto-atual.md"
            if old_context_file.exists():
                with open(old_context_file, 'r', encoding='utf-8') as f:
                    context = f.read()

        # 3. Preparar dados para o gateway
        gateway_input = {
            "user_request": user_request,
            "available_agents": json.dumps(agents_data, ensure_ascii=False),
            "project_context": context,
            "project": project,
            "branch": branch
        }

        # 4. Retornar instruções e dados
        return json.dumps({
            "success": True,
            "message": "Dados preparados para decisão de IA",
            "next_step": {
                "action": "call_gateway",
                "mcp": "igo-openai-gateway",
                "tool": "decide_agent",
                "parameters": {
                    "user_request": user_request,
                    "available_agents": json.dumps(agents_data, ensure_ascii=False),
                    "project_context": context,
                    "reasoning_effort": "high"
                }
            },
            "instructions": """
PRÓXIMO PASSO:
Chame o MCP 'igo-openai-gateway' com a tool 'decide_agent' usando os parâmetros acima.

A IA irá analisar a requisição e recomendar qual(is) agente(s) usar com explicação detalhada.

Após receber a decisão, você pode:
1. Invocar o agente recomendado usando invoke_agent()
2. Ou usar run_agent() do igo-openai-gateway se preferir execução direta com GPT-5.2
""",
            "prepared_data": gateway_input,
            "agents_available": {
                "mcps": agents_data.get("mcps", []),
                "agents": agents_data.get("agents", []),
                "total": agents_data.get("count", 0)
            }
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
