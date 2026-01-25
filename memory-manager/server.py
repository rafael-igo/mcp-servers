#!/usr/bin/env python3
"""
Memory Manager MCP
==================
Gerenciamento de memória persistente do sistema de agentes.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("memory-manager")

# Caminho base do projeto
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DOCS_DIR = Path(__file__).parent.parent / "docs"
MEMORIA_DIR = DOCS_DIR / "memoria"


def _ensure_memoria_dir():
    """Garante que diretório de memória existe."""
    MEMORIA_DIR.mkdir(parents=True, exist_ok=True)


@mcp.tool()
def save_context(module: str, status: str, details: str) -> str:
    """
    Salva contexto atual de um módulo.

    Args:
        module: Nome do módulo (ex: "Rooming List")
        status: Status (ex: "completed", "in_progress", "pending")
        details: Detalhes do status

    Returns:
        JSON string confirmando salvamento
    """
    try:
        _ensure_memoria_dir()
        context_file = MEMORIA_DIR / "contexto-atual.md"

        if not context_file.exists():
            # Criar arquivo inicial
            with open(context_file, 'w', encoding='utf-8') as f:
                f.write("# Contexto Atual do Projeto\n\n")
                f.write(f"**Última atualização:** {datetime.now().strftime('%Y-%m-%d (%H:%M)')}\n\n")
                f.write("---\n\n")

        # Ler conteúdo atual
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Atualizar timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d (%H:%M)")
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("**Última atualização:**"):
                lines[i] = f"**Última atualização:** {timestamp}"
                break

        content = '\n'.join(lines)

        # Adicionar/atualizar módulo
        module_section = f"\n## {module}\n\n**Status:** {status}\n\n{details}\n"
        content += module_section

        # Salvar
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return json.dumps({
            "success": True,
            "message": f"Contexto de '{module}' atualizado",
            "timestamp": timestamp
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def load_context() -> str:
    """
    Carrega o contexto atual completo do projeto.

    Returns:
        JSON string com todo o contexto
    """
    try:
        _ensure_memoria_dir()
        context_file = MEMORIA_DIR / "contexto-atual.md"

        if not context_file.exists():
            return json.dumps({
                "success": False,
                "error": "Arquivo contexto-atual.md não encontrado. Use save_context() primeiro."
            })

        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return json.dumps({
            "success": True,
            "content": content
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def update_progress(task: str, status: str, notes: Optional[str] = None) -> str:
    """
    Atualiza progresso de uma tarefa específica.

    Args:
        task: Nome da tarefa
        status: completed | in_progress | pending | blocked
        notes: Notas adicionais (opcional)

    Returns:
        JSON string confirmando atualização
    """
    try:
        _ensure_memoria_dir()
        ultimas_acoes_file = MEMORIA_DIR / "ultimas-acoes.md"

        if not ultimas_acoes_file.exists():
            # Criar arquivo inicial
            with open(ultimas_acoes_file, 'w', encoding='utf-8') as f:
                f.write("# Últimas Ações\n\n")
                f.write("Histórico de progresso das tarefas.\n\n")
                f.write(f"## {datetime.now().strftime('%Y-%m-%d')}\n\n")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Preparar entrada
        status_emoji = {
            "completed": "✅",
            "in_progress": "⚠️",
            "pending": "🔴",
            "blocked": "🚫"
        }.get(status, "📝")

        entry = f"\n### {status_emoji} {task}\n"
        entry += f"**Status:** {status}\n"
        entry += f"**Timestamp:** {timestamp}\n"
        if notes:
            entry += f"**Notas:** {notes}\n"
        entry += "\n"

        # Adicionar ao arquivo
        with open(ultimas_acoes_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Inserir após primeiro cabeçalho de data
        lines = content.split('\n')
        insert_index = len(lines)
        for i, line in enumerate(lines):
            if line.startswith('## '):
                insert_index = i + 1
                break

        lines.insert(insert_index, entry)
        new_content = '\n'.join(lines)

        with open(ultimas_acoes_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return json.dumps({
            "success": True,
            "message": f"Progresso de '{task}' atualizado para '{status}'",
            "timestamp": timestamp
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_next_steps() -> str:
    """
    Retorna os próximos passos planejados.

    Returns:
        JSON string com próximos passos
    """
    try:
        _ensure_memoria_dir()
        proximos_passos_file = MEMORIA_DIR / "proximos-passos.md"

        if not proximos_passos_file.exists():
            # Criar arquivo inicial
            with open(proximos_passos_file, 'w', encoding='utf-8') as f:
                f.write("# Próximos Passos\n\n")
                f.write("Lista de próximas tarefas a serem realizadas.\n\n")
                f.write("---\n\n")

        with open(proximos_passos_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return json.dumps({
            "success": True,
            "content": content
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def add_decision(decision: str, context: str, alternatives: str, chosen: str, reason: str) -> str:
    """
    Registra uma decisão técnica importante (ADR).

    Args:
        decision: Título da decisão
        context: Contexto da decisão
        alternatives: Alternativas consideradas
        chosen: Alternativa escolhida
        reason: Razão da escolha

    Returns:
        JSON string confirmando registro
    """
    try:
        _ensure_memoria_dir()
        decisoes_file = MEMORIA_DIR / "decisoes-tecnicas.md"

        timestamp = datetime.now().strftime("%Y-%m-%d")

        # Preparar entrada ADR (Architecture Decision Record)
        entry = f"""
## {decision}

**Data:** {timestamp}

### Contexto
{context}

### Alternativas Consideradas
{alternatives}

### Decisão
{chosen}

### Razão
{reason}

---
"""

        # Verificar se arquivo existe
        if not decisoes_file.exists():
            # Criar arquivo
            with open(decisoes_file, 'w', encoding='utf-8') as f:
                f.write("# Decisões Técnicas - ADRs\n\n")
                f.write("Registro de decisões arquiteturais importantes.\n\n")
                f.write("---\n")

        # Adicionar decisão
        with open(decisoes_file, 'a', encoding='utf-8') as f:
            f.write(entry)

        return json.dumps({
            "success": True,
            "message": f"Decisão '{decision}' registrada",
            "date": timestamp
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_memory_summary() -> str:
    """
    Retorna resumo de toda a memória do sistema.

    Returns:
        JSON string com resumo completo
    """
    try:
        _ensure_memoria_dir()

        summary = {
            "success": True,
            "files": {}
        }

        # Ler todos os arquivos de memória
        for file in MEMORIA_DIR.glob("*.md"):
            with open(file, 'r', encoding='utf-8') as f:
                summary["files"][file.name] = {
                    "size": len(f.read()),
                    "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                }

        return json.dumps(summary, indent=2)

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
