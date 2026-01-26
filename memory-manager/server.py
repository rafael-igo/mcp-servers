#!/usr/bin/env python3
"""
Memory Manager MCP - Multi-Project/Branch Support
==================================================
Gerenciamento de memória persistente do sistema de agentes.

Suporta múltiplos projetos e branches com contexto híbrido:
- Contexto global configurável (projeto/branch padrão)
- Override por parâmetros em cada chamada
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
MEMORIA_BASE_DIR = DOCS_DIR / "memoria"

# Contexto global (híbrido)
_GLOBAL_CONTEXT = {
    "project": "default",
    "branch": "main"
}


def _get_project_dir(project: Optional[str] = None, branch: Optional[str] = None) -> Path:
    """
    Retorna diretório do projeto/branch usando contexto híbrido.

    Args:
        project: Nome do projeto (override do global)
        branch: Nome da branch (override do global)

    Returns:
        Path do diretório memoria/{projeto}/{branch}/
    """
    proj = project or _GLOBAL_CONTEXT["project"]
    brch = branch or _GLOBAL_CONTEXT["branch"]

    project_dir = MEMORIA_BASE_DIR / proj / brch
    project_dir.mkdir(parents=True, exist_ok=True)

    return project_dir


def _get_core_dir(project: Optional[str] = None) -> Path:
    """
    Retorna diretório core do projeto (dados globais do projeto).

    Args:
        project: Nome do projeto (override do global)

    Returns:
        Path do diretório memoria/{projeto}/core/
    """
    proj = project or _GLOBAL_CONTEXT["project"]

    core_dir = MEMORIA_BASE_DIR / proj / "core"
    core_dir.mkdir(parents=True, exist_ok=True)

    return core_dir


@mcp.tool()
def set_project_context(project: str, branch: str = "main") -> str:
    """
    Define o contexto global do projeto/branch.

    Todas as próximas chamadas usarão este contexto por padrão,
    a menos que sejam sobrescritas com parâmetros explícitos.

    Args:
        project: Nome do projeto (ex: "igo-journey", "sigaevento")
        branch: Nome da branch (ex: "main", "feature-rooming")

    Returns:
        JSON confirmando configuração

    Exemplo:
        set_project_context(project="igo-journey", branch="feature-transfer")
        # Todas as próximas chamadas usarão igo-journey/feature-transfer
    """
    try:
        _GLOBAL_CONTEXT["project"] = project
        _GLOBAL_CONTEXT["branch"] = branch

        # Criar diretórios
        _get_project_dir(project, branch)
        _get_core_dir(project)

        return json.dumps({
            "success": True,
            "message": f"Contexto global configurado: {project}/{branch}",
            "context": {
                "project": project,
                "branch": branch
            }
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_project_context() -> str:
    """
    Retorna o contexto global atual.

    Returns:
        JSON com projeto e branch atuais
    """
    return json.dumps({
        "success": True,
        "context": _GLOBAL_CONTEXT
    }, indent=2)


@mcp.tool()
def save_context(
    module: str,
    status: str,
    details: str,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """
    Salva contexto atual de um módulo.

    Args:
        module: Nome do módulo (ex: "Rooming List")
        status: Status (ex: "completed", "in_progress", "pending")
        details: Detalhes do status
        project: Nome do projeto (opcional, usa contexto global se omitido)
        branch: Nome da branch (opcional, usa contexto global se omitido)

    Returns:
        JSON string confirmando salvamento

    Exemplo:
        # Usa contexto global
        save_context(module="Transfer", status="completed", details="...")

        # Override do contexto
        save_context(module="Transfer", status="completed", details="...",
                    project="igo-journey", branch="feature-transfer")
    """
    try:
        project_dir = _get_project_dir(project, branch)
        context_file = project_dir / "contexto-atual.md"

        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        if not context_file.exists():
            # Criar arquivo inicial
            with open(context_file, 'w', encoding='utf-8') as f:
                f.write(f"# Contexto Atual - {proj}/{brch}\n\n")
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
            "timestamp": timestamp,
            "project": proj,
            "branch": brch
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def load_context(
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """
    Carrega o contexto atual completo do projeto.

    Args:
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)

    Returns:
        JSON string com todo o contexto
    """
    try:
        project_dir = _get_project_dir(project, branch)
        context_file = project_dir / "contexto-atual.md"

        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        if not context_file.exists():
            return json.dumps({
                "success": False,
                "error": f"Contexto não encontrado para {proj}/{brch}. Use save_context() primeiro.",
                "project": proj,
                "branch": brch
            })

        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return json.dumps({
            "success": True,
            "content": content,
            "project": proj,
            "branch": brch
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def update_progress(
    task: str,
    status: str,
    notes: Optional[str] = None,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """
    Atualiza progresso de uma tarefa específica.

    Args:
        task: Nome da tarefa
        status: completed | in_progress | pending | blocked
        notes: Notas adicionais (opcional)
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)

    Returns:
        JSON string confirmando atualização
    """
    try:
        project_dir = _get_project_dir(project, branch)
        ultimas_acoes_file = project_dir / "ultimas-acoes.md"

        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        if not ultimas_acoes_file.exists():
            # Criar arquivo inicial
            with open(ultimas_acoes_file, 'w', encoding='utf-8') as f:
                f.write(f"# Últimas Ações - {proj}/{brch}\n\n")
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
            "timestamp": timestamp,
            "project": proj,
            "branch": brch
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_next_steps(
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """
    Retorna os próximos passos planejados.

    Args:
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)

    Returns:
        JSON string com próximos passos
    """
    try:
        project_dir = _get_project_dir(project, branch)
        proximos_passos_file = project_dir / "proximos-passos.md"

        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        if not proximos_passos_file.exists():
            # Criar arquivo inicial
            with open(proximos_passos_file, 'w', encoding='utf-8') as f:
                f.write(f"# Próximos Passos - {proj}/{brch}\n\n")
                f.write("Lista de próximas tarefas a serem realizadas.\n\n")
                f.write("---\n\n")

        with open(proximos_passos_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return json.dumps({
            "success": True,
            "content": content,
            "project": proj,
            "branch": brch
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def add_decision(
    decision: str,
    context: str,
    alternatives: str,
    chosen: str,
    reason: str,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """
    Registra uma decisão técnica importante (ADR).

    Args:
        decision: Título da decisão
        context: Contexto da decisão
        alternatives: Alternativas consideradas
        chosen: Alternativa escolhida
        reason: Razão da escolha
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)

    Returns:
        JSON string confirmando registro
    """
    try:
        project_dir = _get_project_dir(project, branch)
        decisoes_file = project_dir / "decisoes-tecnicas.md"

        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        timestamp = datetime.now().strftime("%Y-%m-%d")

        # Preparar entrada ADR (Architecture Decision Record)
        entry = f"""
## {decision}

**Data:** {timestamp}
**Projeto/Branch:** {proj}/{brch}

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
                f.write(f"# Decisões Técnicas - ADRs - {proj}/{brch}\n\n")
                f.write("Registro de decisões arquiteturais importantes.\n\n")
                f.write("---\n")

        # Adicionar decisão
        with open(decisoes_file, 'a', encoding='utf-8') as f:
            f.write(entry)

        return json.dumps({
            "success": True,
            "message": f"Decisão '{decision}' registrada",
            "date": timestamp,
            "project": proj,
            "branch": brch
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_memory_summary(
    project: Optional[str] = None,
    branch: Optional[str] = None,
    include_all_branches: bool = False
) -> str:
    """
    Retorna resumo de toda a memória do sistema.

    Args:
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)
        include_all_branches: Se True, retorna todas as branches do projeto

    Returns:
        JSON string com resumo completo
    """
    try:
        proj = project or _GLOBAL_CONTEXT["project"]

        summary = {
            "success": True,
            "project": proj,
            "files": {}
        }

        if include_all_branches:
            # Listar todas as branches
            project_base = MEMORIA_BASE_DIR / proj
            if project_base.exists():
                branches = [d.name for d in project_base.iterdir() if d.is_dir()]
                summary["branches"] = branches

                for brch in branches:
                    branch_dir = project_base / brch
                    summary["files"][brch] = {}

                    for file in branch_dir.glob("*.md"):
                        with open(file, 'r', encoding='utf-8') as f:
                            summary["files"][brch][file.name] = {
                                "size": len(f.read()),
                                "modified": datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
                            }
        else:
            # Apenas branch específica
            brch = branch or _GLOBAL_CONTEXT["branch"]
            project_dir = _get_project_dir(project, branch)
            summary["branch"] = brch

            for file in project_dir.glob("*.md"):
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


@mcp.tool()
def compare_branches(
    project: str,
    branch_a: str,
    branch_b: str
) -> str:
    """
    Compara duas branches do mesmo projeto.

    Args:
        project: Nome do projeto
        branch_a: Primeira branch
        branch_b: Segunda branch

    Returns:
        JSON com comparação

    Exemplo:
        compare_branches(
            project="igo-journey",
            branch_a="main",
            branch_b="feature-rooming"
        )
    """
    try:
        dir_a = MEMORIA_BASE_DIR / project / branch_a
        dir_b = MEMORIA_BASE_DIR / project / branch_b

        if not dir_a.exists():
            return json.dumps({
                "success": False,
                "error": f"Branch '{branch_a}' não encontrada em {project}"
            })

        if not dir_b.exists():
            return json.dumps({
                "success": False,
                "error": f"Branch '{branch_b}' não encontrada em {project}"
            })

        comparison = {
            "success": True,
            "project": project,
            "branch_a": branch_a,
            "branch_b": branch_b,
            "files_only_in_a": [],
            "files_only_in_b": [],
            "common_files": [],
            "differences": {}
        }

        files_a = set(f.name for f in dir_a.glob("*.md"))
        files_b = set(f.name for f in dir_b.glob("*.md"))

        comparison["files_only_in_a"] = list(files_a - files_b)
        comparison["files_only_in_b"] = list(files_b - files_a)
        comparison["common_files"] = list(files_a & files_b)

        # Comparar arquivos comuns (tamanho e data)
        for filename in comparison["common_files"]:
            file_a = dir_a / filename
            file_b = dir_b / filename

            size_a = file_a.stat().st_size
            size_b = file_b.stat().st_size

            modified_a = datetime.fromtimestamp(file_a.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            modified_b = datetime.fromtimestamp(file_b.stat().st_mtime).strftime("%Y-%m-%d %H:%M")

            comparison["differences"][filename] = {
                "size_a": size_a,
                "size_b": size_b,
                "size_diff": size_b - size_a,
                "modified_a": modified_a,
                "modified_b": modified_b,
                "is_different": size_a != size_b or modified_a != modified_b
            }

        return json.dumps(comparison, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def list_all_projects() -> str:
    """
    Lista todos os projetos e suas branches.

    Returns:
        JSON com estrutura completa de projetos
    """
    try:
        MEMORIA_BASE_DIR.mkdir(parents=True, exist_ok=True)

        projects = {}

        for project_dir in MEMORIA_BASE_DIR.iterdir():
            if project_dir.is_dir():
                project_name = project_dir.name
                branches = []

                for branch_dir in project_dir.iterdir():
                    if branch_dir.is_dir():
                        branch_name = branch_dir.name
                        file_count = len(list(branch_dir.glob("*.md")))

                        branches.append({
                            "name": branch_name,
                            "files": file_count,
                            "path": str(branch_dir)
                        })

                projects[project_name] = {
                    "branches": branches,
                    "total_branches": len(branches)
                }

        return json.dumps({
            "success": True,
            "total_projects": len(projects),
            "projects": projects,
            "current_context": _GLOBAL_CONTEXT
        }, indent=2)

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
