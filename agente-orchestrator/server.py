#!/usr/bin/env python3
"""
Agente Orchestrator MCP
=======================
Orquestração de agentes especializados do projeto.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("agente-orchestrator")

# Caminho base do projeto
# Usar /project como base (volume montado pelo docker-compose)
PROJECT_ROOT = Path("/project")
DOCS_DIR = PROJECT_ROOT / "api" / "mcp-servers" / "docs"
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
        # Garantir que diretório de agentes existe
        AGENTES_DIR.mkdir(parents=True, exist_ok=True)

        # Listar MCPs disponíveis
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
                "name": "vuetify-uiux",
                "type": "mcp",
                "title": "Agente UI/UX Design",
                "description": "Design, layouts Vuetify 3, boas práticas e padrões visuais"
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

        return json.dumps({
            "success": True,
            "count": len(mcps) + len(agents),
            "mcps": mcps,
            "agents": agents,
            "note": "MCPs ativos. Use tools diretas dos MCPs ou agentes em /docs/agentes."
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
        # Garantir que diretório de memória existe
        MEMORIA_DIR.mkdir(parents=True, exist_ok=True)
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


def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
