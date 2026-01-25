#!/usr/bin/env python3
"""
Checklist Validator MCP
=======================
Validação e gerenciamento de checklists de implementação.
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("checklist-validator")

# Caminho base do projeto
# Usar /project como base (volume montado pelo docker-compose)
PROJECT_ROOT = Path("/project")
DOCS_DIR = PROJECT_ROOT / "api" / "mcp-servers" / "docs"
CHECKLISTS_DIR = DOCS_DIR / "checklists"


def _ensure_checklists_dir():
    """Garante que diretório de checklists existe."""
    CHECKLISTS_DIR.mkdir(parents=True, exist_ok=True)


@mcp.tool()
def validate_checklist(checklist_path: str) -> str:
    """
    Valida um checklist e retorna estatísticas.

    Args:
        checklist_path: Caminho relativo ao diretório de checklists

    Returns:
        JSON string com estatísticas do checklist
    """
    try:
        _ensure_checklists_dir()
        file_path = CHECKLISTS_DIR / checklist_path

        if not file_path.exists():
            return json.dumps({
                "success": False,
                "error": f"Checklist não encontrado: {checklist_path}"
            })

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Contar tarefas
        total_tasks = len(re.findall(r'- \[[ x]\]', content))
        completed_tasks = len(re.findall(r'- \[x\]', content, re.IGNORECASE))
        pending_tasks = total_tasks - completed_tasks

        # Calcular percentual
        percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Extrair tarefas pendentes
        pending_list = []
        for line in content.split('\n'):
            if '- [ ]' in line:
                task = line.replace('- [ ]', '').strip()
                pending_list.append(task)

        result = {
            "success": True,
            "file": checklist_path,
            "stats": {
                "total": total_tasks,
                "completed": completed_tasks,
                "pending": pending_tasks,
                "percentage": round(percentage, 1)
            },
            "pending_tasks": pending_list[:10]  # Limitar a 10
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def mark_completed(checklist_path: str, task_pattern: str) -> str:
    """
    Marca uma tarefa como completa no checklist.

    Args:
        checklist_path: Caminho relativo ao diretório de checklists
        task_pattern: Padrão de texto da tarefa a marcar

    Returns:
        JSON string confirmando atualização
    """
    try:
        _ensure_checklists_dir()
        file_path = CHECKLISTS_DIR / checklist_path

        if not file_path.exists():
            return json.dumps({
                "success": False,
                "error": f"Checklist não encontrado: {checklist_path}"
            })

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Procurar e marcar tarefa
        lines = content.split('\n')
        marked = False
        marked_task = None

        for i, line in enumerate(lines):
            if '- [ ]' in line and task_pattern.lower() in line.lower():
                lines[i] = line.replace('- [ ]', '- [x]')
                marked = True
                marked_task = line.replace('- [ ]', '').strip()
                break

        if not marked:
            return json.dumps({
                "success": False,
                "error": f"Tarefa com padrão '{task_pattern}' não encontrada"
            })

        # Salvar arquivo
        new_content = '\n'.join(lines)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return json.dumps({
            "success": True,
            "message": f"Tarefa marcada como completa",
            "task": marked_task,
            "file": checklist_path
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_pending_tasks(checklist_path: Optional[str] = None) -> str:
    """
    Lista todas as tarefas pendentes de um ou todos os checklists.

    Args:
        checklist_path: Caminho específico ou None para todos

    Returns:
        JSON string com tarefas pendentes
    """
    try:
        _ensure_checklists_dir()

        result = {
            "success": True,
            "checklists": []
        }

        # Determinar quais arquivos processar
        if checklist_path:
            files = [CHECKLISTS_DIR / checklist_path]
        else:
            files = list(CHECKLISTS_DIR.glob("*.md"))

        for file_path in files:
            if not file_path.exists():
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extrair tarefas pendentes
            pending = []
            current_section = None

            for line in content.split('\n'):
                # Capturar seção
                if line.startswith('###'):
                    current_section = line.replace('###', '').strip()
                elif line.startswith('##'):
                    current_section = line.replace('##', '').strip()

                # Capturar tarefa pendente
                if '- [ ]' in line:
                    task = line.replace('- [ ]', '').strip()
                    pending.append({
                        "section": current_section,
                        "task": task
                    })

            if pending:
                result["checklists"].append({
                    "file": file_path.name,
                    "pending_count": len(pending),
                    "tasks": pending[:20]  # Limitar a 20
                })

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def list_checklists() -> str:
    """
    Lista todos os checklists disponíveis.

    Returns:
        JSON string com lista de checklists
    """
    try:
        _ensure_checklists_dir()

        result = {
            "success": True,
            "checklists": []
        }

        for file_path in CHECKLISTS_DIR.glob("*.md"):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Contar tarefas
            total = len(re.findall(r'- \[[ x]\]', content))
            completed = len(re.findall(r'- \[x\]', content, re.IGNORECASE))
            percentage = (completed / total * 100) if total > 0 else 0

            # Extrair título
            title = None
            for line in content.split('\n'):
                if line.startswith('# '):
                    title = line.replace('#', '').strip()
                    break

            result["checklists"].append({
                "file": file_path.name,
                "title": title,
                "total_tasks": total,
                "completed": completed,
                "percentage": round(percentage, 1)
            })

        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def create_checklist(name: str, title: str, sections: str) -> str:
    """
    Cria um novo checklist.

    Args:
        name: Nome do arquivo (sem extensão)
        title: Título do checklist
        sections: Seções e tarefas em formato JSON

    Returns:
        JSON string confirmando criação
    """
    try:
        _ensure_checklists_dir()
        file_path = CHECKLISTS_DIR / f"{name}.md"

        if file_path.exists():
            return json.dumps({
                "success": False,
                "error": f"Checklist '{name}' já existe"
            })

        # Montar conteúdo
        content = f"# {title}\n\n"
        content += f"**Criado em:** {datetime.now().strftime('%Y-%m-%d')}\n\n"
        content += "---\n\n"

        # Adicionar seções (espera JSON)
        try:
            sections_data = json.loads(sections)
            for section in sections_data:
                content += f"## {section['name']}\n\n"
                for task in section.get('tasks', []):
                    content += f"- [ ] {task}\n"
                content += "\n"
        except json.JSONDecodeError:
            # Se não for JSON, usar como texto simples
            content += sections

        # Salvar
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return json.dumps({
            "success": True,
            "message": f"Checklist '{name}' criado",
            "path": str(file_path)
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
