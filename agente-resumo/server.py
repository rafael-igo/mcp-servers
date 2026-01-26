#!/usr/bin/env python3
"""
Agente Resumo MCP - Multi-Project/Branch Support
=================================================
Status do projeto, progresso, relatórios e métricas.

Suporta múltiplos projetos e branches com contexto híbrido.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("agente-resumo")

# Caminhos
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DOCS_DIR = Path(__file__).parent.parent / "docs"
RESUMO_BASE_DIR = DOCS_DIR / "resumo"

# Contexto global (híbrido)
_GLOBAL_CONTEXT = {
    "project": "default",
    "branch": "main"
}


def _get_project_dir(project: Optional[str] = None, branch: Optional[str] = None) -> Path:
    """Retorna diretório do projeto/branch usando contexto híbrido."""
    proj = project or _GLOBAL_CONTEXT["project"]
    brch = branch or _GLOBAL_CONTEXT["branch"]

    project_dir = RESUMO_BASE_DIR / proj / brch
    project_dir.mkdir(parents=True, exist_ok=True)

    return project_dir


def _load_progress(project: Optional[str] = None, branch: Optional[str] = None) -> Dict:
    """Carrega dados de progresso."""
    project_dir = _get_project_dir(project, branch)
    progress_file = project_dir / "progresso.json"

    if progress_file.exists():
        with open(progress_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    return {
        "project_name": "Novo Projeto",
        "phase": "Planejamento",
        "overall_progress": 0,
        "modules": {},
        "next_steps": [],
        "blockers": []
    }


def _save_progress(data: Dict, project: Optional[str] = None, branch: Optional[str] = None):
    """Salva dados de progresso."""
    project_dir = _get_project_dir(project, branch)
    progress_file = project_dir / "progresso.json"

    data['last_updated'] = datetime.now().isoformat()
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@mcp.tool()
def set_project_context(project: str, branch: str = "main") -> str:
    """Define o contexto global do projeto/branch."""
    try:
        _GLOBAL_CONTEXT["project"] = project
        _GLOBAL_CONTEXT["branch"] = branch
        _get_project_dir(project, branch)

        return json.dumps({
            "success": True,
            "message": f"Contexto global configurado: {project}/{branch}",
            "context": {"project": project, "branch": branch}
        }, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def get_project_context() -> str:
    """Retorna o contexto global atual."""
    return json.dumps({"success": True, "context": _GLOBAL_CONTEXT}, indent=2)


@mcp.tool()
def get_project_status(
    include_details: bool = False,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """Retorna status geral do projeto."""
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        progress = _load_progress(project, branch)

        status = {
            "project": progress.get("project_name", proj),
            "branch": brch,
            "phase": progress.get("phase", "Planejamento"),
            "overall_progress": progress.get("overall_progress", 0),
            "last_updated": progress.get("last_updated"),
            "modules_summary": {}
        }

        for name, module in progress.get('modules', {}).items():
            status['modules_summary'][name] = {
                "progress": module.get('progress', 0),
                "status": module.get('status', 'planned')
            }

        if include_details:
            status['modules_detailed'] = progress.get('modules', {})
            status['next_steps'] = progress.get('next_steps', [])
            status['blockers'] = progress.get('blockers', [])

        return json.dumps({"success": True, "status": status}, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def get_module_status(
    module_name: str,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """Retorna status detalhado de um módulo específico."""
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        progress = _load_progress(project, branch)
        module = progress.get('modules', {}).get(module_name)

        if not module:
            return json.dumps({
                "success": False,
                "error": f"Módulo '{module_name}' não encontrado em {proj}/{brch}"
            })

        return json.dumps({
            "success": True,
            "module": module_name,
            "project": proj,
            "branch": brch,
            "details": module
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def update_module_progress(
    module_name: str,
    progress_pct: int,
    status: Optional[str] = None,
    notes: Optional[str] = None,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """Atualiza progresso de um módulo."""
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        data = _load_progress(project, branch)

        if 'modules' not in data:
            data['modules'] = {}

        if module_name not in data['modules']:
            data['modules'][module_name] = {
                "progress": 0,
                "status": "planned",
                "features_total": 0,
                "features_done": 0,
                "history": []
            }

        module = data['modules'][module_name]
        old_progress = module.get('progress', 0)

        module['progress'] = max(0, min(100, progress_pct))
        if status:
            module['status'] = status

        if 'history' not in module:
            module['history'] = []

        module['history'].append({
            "timestamp": datetime.now().isoformat(),
            "progress_change": f"{old_progress}% → {progress_pct}%",
            "notes": notes or "Atualização de progresso"
        })

        # Recalcular progresso geral
        total_progress = sum(m['progress'] for m in data['modules'].values())
        module_count = len(data['modules'])
        data['overall_progress'] = int(total_progress / module_count) if module_count > 0 else 0

        _save_progress(data, project, branch)

        return json.dumps({
            "success": True,
            "module": module_name,
            "old_progress": old_progress,
            "new_progress": progress_pct,
            "project": proj,
            "branch": brch,
            "message": f"✅ {module_name}: {old_progress}% → {progress_pct}%"
        }, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def get_next_steps(
    limit: int = 10,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """Lista próximos passos priorizados."""
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        progress = _load_progress(project, branch)
        next_steps = progress.get('next_steps', [])[:limit]

        return json.dumps({
            "success": True,
            "count": len(next_steps),
            "next_steps": next_steps,
            "project": proj,
            "branch": brch
        }, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def add_next_step(
    task: str,
    priority: str = "medium",
    estimate: Optional[str] = None,
    module: Optional[str] = None,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """Adiciona um novo próximo passo."""
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        progress = _load_progress(project, branch)

        step = {
            "task": task,
            "priority": priority,
            "estimate": estimate,
            "module": module,
            "added_at": datetime.now().isoformat()
        }

        if 'next_steps' not in progress:
            progress['next_steps'] = []

        progress['next_steps'].append(step)
        _save_progress(progress, project, branch)

        return json.dumps({
            "success": True,
            "step": step,
            "project": proj,
            "branch": brch,
            "message": f"✅ Próximo passo adicionado: {task}"
        }, indent=2)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def generate_report(
    report_type: str = "executive",
    audience: str = "team",
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """Gera relatório formatado do projeto."""
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        progress = _load_progress(project, branch)

        report = {
            "title": f"Relatório {report_type.title()} - {progress.get('project_name', proj)}",
            "generated_at": datetime.now().isoformat(),
            "project": proj,
            "branch": brch,
            "audience": audience,
            "content": {}
        }

        modules = progress.get('modules', {})
        next_steps = progress.get('next_steps', [])

        if report_type == "executive":
            report['content'] = {
                "summary": f"Projeto em fase {progress.get('phase', 'N/A')}",
                "progress": f"{progress.get('overall_progress', 0)}% completo",
                "modules": {name: f"{mod.get('progress', 0)}% - {mod.get('status', 'planned')}" for name, mod in modules.items()},
                "next_milestone": next_steps[0]['task'] if next_steps else "N/A",
                "blockers_count": len(progress.get('blockers', []))
            }
        elif report_type == "technical":
            report['content'] = {
                "phase": progress.get('phase', 'N/A'),
                "overall_progress": progress.get('overall_progress', 0),
                "modules_detailed": modules,
                "next_steps": next_steps,
                "blockers": progress.get('blockers', []),
                "last_updated": progress.get('last_updated')
            }

        return json.dumps({"success": True, "report": report}, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def get_metrics(
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """Retorna métricas e estatísticas do projeto."""
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        progress = _load_progress(project, branch)
        modules = progress.get('modules', {})

        metrics = {
            "overall_progress": progress.get('overall_progress', 0),
            "modules": {
                "total": len(modules),
                "completed": sum(1 for m in modules.values() if m.get('status') == 'completed'),
                "active": sum(1 for m in modules.values() if m.get('status') == 'active'),
                "planned": sum(1 for m in modules.values() if m.get('status') == 'planned')
            },
            "next_steps": {
                "total": len(progress.get('next_steps', [])),
                "critical": sum(1 for s in progress.get('next_steps', []) if s.get('priority') == 'critical'),
                "high": sum(1 for s in progress.get('next_steps', []) if s.get('priority') == 'high')
            },
            "blockers": len(progress.get('blockers', [])),
            "last_updated": progress.get('last_updated'),
            "project": proj,
            "branch": brch
        }

        return json.dumps({"success": True, "metrics": metrics}, indent=2, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def list_all_projects() -> str:
    """Lista todos os projetos e suas branches."""
    try:
        RESUMO_BASE_DIR.mkdir(parents=True, exist_ok=True)
        projects = {}

        for project_dir in RESUMO_BASE_DIR.iterdir():
            if project_dir.is_dir():
                project_name = project_dir.name
                branches = []

                for branch_dir in project_dir.iterdir():
                    if branch_dir.is_dir():
                        branch_name = branch_dir.name
                        progress_file = branch_dir / "progresso.json"

                        progress_pct = 0
                        if progress_file.exists():
                            with open(progress_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                progress_pct = data.get('overall_progress', 0)

                        branches.append({
                            "name": branch_name,
                            "progress": progress_pct,
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
        return json.dumps({"success": False, "error": str(e)})


def main():
    """Entry point for the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
