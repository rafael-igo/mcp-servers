#!/usr/bin/env python3
"""
Agente Insights MCP - Multi-Project/Branch Support
==================================================
Captura de ideias, consulta a especialistas e tomada de decisões.

Suporta múltiplos projetos e branches com contexto híbrido.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("agente-insights")

# Caminhos
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DOCS_DIR = Path(__file__).parent.parent / "docs"
INSIGHTS_BASE_DIR = DOCS_DIR / "insights"

# Contexto global (híbrido)
_GLOBAL_CONTEXT = {
    "project": "default",
    "branch": "main"
}


def _get_project_dir(project: Optional[str] = None, branch: Optional[str] = None) -> Path:
    """Retorna diretório do projeto/branch usando contexto híbrido."""
    proj = project or _GLOBAL_CONTEXT["project"]
    brch = branch or _GLOBAL_CONTEXT["branch"]

    project_dir = INSIGHTS_BASE_DIR / proj / brch
    project_dir.mkdir(parents=True, exist_ok=True)

    return project_dir


def _get_insights_file(project: Optional[str] = None, branch: Optional[str] = None) -> Path:
    """Retorna arquivo de insights do projeto/branch."""
    return _get_project_dir(project, branch) / "insights.json"


def _load_insights(project: Optional[str] = None, branch: Optional[str] = None) -> List[Dict]:
    """Carrega insights do arquivo JSON."""
    insights_file = _get_insights_file(project, branch)
    if insights_file.exists():
        with open(insights_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def _save_insights(insights: List[Dict], project: Optional[str] = None, branch: Optional[str] = None):
    """Salva insights no arquivo JSON."""
    insights_file = _get_insights_file(project, branch)
    with open(insights_file, 'w', encoding='utf-8') as f:
        json.dump(insights, f, indent=2, ensure_ascii=False)


def _get_next_id(project: Optional[str] = None, branch: Optional[str] = None) -> str:
    """Retorna próximo ID disponível para o projeto/branch."""
    insights = _load_insights(project, branch)
    if not insights:
        return "INS-0001"

    last_id = max(int(i['id'].split('-')[1]) for i in insights)
    return f"INS-{last_id + 1:04d}"


@mcp.tool()
def set_project_context(project: str, branch: str = "main") -> str:
    """
    Define o contexto global do projeto/branch.

    Args:
        project: Nome do projeto (ex: "igo-journey", "sigaevento")
        branch: Nome da branch (ex: "main", "feature-rooming")

    Returns:
        JSON confirmando configuração
    """
    try:
        _GLOBAL_CONTEXT["project"] = project
        _GLOBAL_CONTEXT["branch"] = branch

        # Criar diretórios
        _get_project_dir(project, branch)

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
def capture_insight(
    idea: str,
    insight_type: str = "feature",
    complexity: str = "medium",
    modules: Optional[List[str]] = None,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """
    Captura um novo insight do usuário.

    Args:
        idea: Descrição da ideia ou sugestão
        insight_type: Tipo (feature, bug, improvement, decision, exploration)
        complexity: Complexidade (low, medium, high)
        modules: Lista de módulos impactados
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)

    Returns:
        JSON com insight criado
    """
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        insights = _load_insights(project, branch)

        insight = {
            "id": _get_next_id(project, branch),
            "timestamp": datetime.now().isoformat(),
            "type": insight_type,
            "complexity": complexity,
            "status": "captured",
            "idea": idea,
            "modules": modules or [],
            "agents_consulted": [],
            "analysis": {},
            "decision": None,
            "next_steps": [],
            "project": proj,
            "branch": brch
        }

        insights.append(insight)
        _save_insights(insights, project, branch)

        return json.dumps({
            "success": True,
            "insight": insight,
            "message": f"✅ Insight {insight['id']} capturado em {proj}/{brch}"
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_insights(
    status: Optional[str] = None,
    insight_type: Optional[str] = None,
    limit: int = 10,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """
    Lista insights capturados com filtros.

    Args:
        status: Filtrar por status (captured, analyzing, approved, rejected, implemented)
        insight_type: Filtrar por tipo (feature, bug, improvement, decision, exploration)
        limit: Número máximo de resultados
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)

    Returns:
        JSON com lista de insights
    """
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        insights = _load_insights(project, branch)

        # Aplicar filtros
        if status:
            insights = [i for i in insights if i['status'] == status]
        if insight_type:
            insights = [i for i in insights if i['type'] == insight_type]

        # Ordenar por data (mais recentes primeiro)
        insights.sort(key=lambda x: x['timestamp'], reverse=True)

        # Limitar resultados
        insights = insights[:limit]

        return json.dumps({
            "success": True,
            "count": len(insights),
            "insights": insights,
            "project": proj,
            "branch": brch
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def update_insight_status(
    insight_id: str,
    new_status: str,
    notes: Optional[str] = None,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """
    Atualiza status de um insight.

    Args:
        insight_id: ID do insight (ex: INS-0001)
        new_status: Novo status (captured, analyzing, approved, rejected, implemented)
        notes: Notas sobre a mudança de status
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)

    Returns:
        JSON confirmando atualização
    """
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        insights = _load_insights(project, branch)

        insight = next((i for i in insights if i['id'] == insight_id), None)
        if not insight:
            return json.dumps({
                "success": False,
                "error": f"Insight {insight_id} não encontrado em {proj}/{brch}"
            })

        old_status = insight['status']
        insight['status'] = new_status
        insight['updated_at'] = datetime.now().isoformat()

        if notes:
            if 'status_history' not in insight:
                insight['status_history'] = []
            insight['status_history'].append({
                "from": old_status,
                "to": new_status,
                "timestamp": datetime.now().isoformat(),
                "notes": notes
            })

        _save_insights(insights, project, branch)

        return json.dumps({
            "success": True,
            "insight_id": insight_id,
            "old_status": old_status,
            "new_status": new_status,
            "project": proj,
            "branch": brch,
            "message": f"✅ Status atualizado: {old_status} → {new_status}"
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def add_agent_feedback(
    insight_id: str,
    agent_name: str,
    feedback: str,
    recommendation: Optional[str] = None,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """
    Adiciona feedback de um agente especialista a um insight.

    Args:
        insight_id: ID do insight
        agent_name: Nome do agente consultado
        feedback: Feedback do agente
        recommendation: Recomendação do agente
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)

    Returns:
        JSON confirmando adição
    """
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        insights = _load_insights(project, branch)

        insight = next((i for i in insights if i['id'] == insight_id), None)
        if not insight:
            return json.dumps({
                "success": False,
                "error": f"Insight {insight_id} não encontrado em {proj}/{brch}"
            })

        if 'agents_consulted' not in insight:
            insight['agents_consulted'] = []

        insight['agents_consulted'].append({
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "feedback": feedback,
            "recommendation": recommendation
        })

        _save_insights(insights, project, branch)

        return json.dumps({
            "success": True,
            "insight_id": insight_id,
            "agent": agent_name,
            "project": proj,
            "branch": brch,
            "message": f"✅ Feedback de {agent_name} adicionado"
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def make_decision(
    insight_id: str,
    decision_status: str,
    rationale: str,
    priority: Optional[str] = "medium",
    effort_estimate: Optional[str] = None,
    project: Optional[str] = None,
    branch: Optional[str] = None
) -> str:
    """
    Registra decisão sobre um insight.

    Args:
        insight_id: ID do insight
        decision_status: Decisão (approved, rejected, deferred)
        rationale: Justificativa da decisão
        priority: Prioridade (critical, high, medium, low)
        effort_estimate: Estimativa de esforço
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)

    Returns:
        JSON confirmando decisão
    """
    try:
        proj = project or _GLOBAL_CONTEXT["project"]
        brch = branch or _GLOBAL_CONTEXT["branch"]

        insights = _load_insights(project, branch)

        insight = next((i for i in insights if i['id'] == insight_id), None)
        if not insight:
            return json.dumps({
                "success": False,
                "error": f"Insight {insight_id} não encontrado em {proj}/{brch}"
            })

        insight['decision'] = {
            "status": decision_status,
            "rationale": rationale,
            "priority": priority,
            "effort_estimate": effort_estimate,
            "decided_at": datetime.now().isoformat()
        }

        if decision_status == "approved":
            insight['status'] = "approved"
        elif decision_status == "rejected":
            insight['status'] = "rejected"

        _save_insights(insights, project, branch)

        return json.dumps({
            "success": True,
            "insight_id": insight_id,
            "decision": decision_status,
            "project": proj,
            "branch": brch,
            "message": f"✅ Decisão registrada: {decision_status.upper()}"
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_statistics(
    project: Optional[str] = None,
    branch: Optional[str] = None,
    cross_project: bool = False
) -> str:
    """
    Retorna estatísticas dos insights capturados.

    Args:
        project: Nome do projeto (opcional, usa contexto global)
        branch: Nome da branch (opcional, usa contexto global)
        cross_project: Se True, retorna estatísticas de todos os projetos

    Returns:
        JSON com estatísticas
    """
    try:
        if cross_project:
            # Estatísticas cross-project
            all_insights = []
            projects_stats = {}

            if INSIGHTS_BASE_DIR.exists():
                for project_dir in INSIGHTS_BASE_DIR.iterdir():
                    if project_dir.is_dir():
                        proj_name = project_dir.name
                        projects_stats[proj_name] = {"branches": {}, "total": 0}

                        for branch_dir in project_dir.iterdir():
                            if branch_dir.is_dir():
                                brch_name = branch_dir.name
                                insights_file = branch_dir / "insights.json"

                                if insights_file.exists():
                                    with open(insights_file, 'r', encoding='utf-8') as f:
                                        branch_insights = json.load(f)
                                        all_insights.extend(branch_insights)
                                        projects_stats[proj_name]["branches"][brch_name] = len(branch_insights)
                                        projects_stats[proj_name]["total"] += len(branch_insights)

            stats = {
                "total": len(all_insights),
                "by_project": projects_stats,
                "by_status": {},
                "by_type": {},
                "by_complexity": {}
            }

            for insight in all_insights:
                status = insight['status']
                stats['by_status'][status] = stats['by_status'].get(status, 0) + 1

                itype = insight['type']
                stats['by_type'][itype] = stats['by_type'].get(itype, 0) + 1

                complexity = insight['complexity']
                stats['by_complexity'][complexity] = stats['by_complexity'].get(complexity, 0) + 1

            return json.dumps({
                "success": True,
                "statistics": stats,
                "mode": "cross_project"
            }, indent=2)

        else:
            # Estatísticas de um projeto/branch específico
            proj = project or _GLOBAL_CONTEXT["project"]
            brch = branch or _GLOBAL_CONTEXT["branch"]

            insights = _load_insights(project, branch)

            stats = {
                "total": len(insights),
                "by_status": {},
                "by_type": {},
                "by_complexity": {},
                "recent_count": 0
            }

            for insight in insights:
                status = insight['status']
                stats['by_status'][status] = stats['by_status'].get(status, 0) + 1

                itype = insight['type']
                stats['by_type'][itype] = stats['by_type'].get(itype, 0) + 1

                complexity = insight['complexity']
                stats['by_complexity'][complexity] = stats['by_complexity'].get(complexity, 0) + 1

                timestamp = datetime.fromisoformat(insight['timestamp'])
                if (datetime.now() - timestamp).days <= 7:
                    stats['recent_count'] += 1

            return json.dumps({
                "success": True,
                "statistics": stats,
                "project": proj,
                "branch": brch
            }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def compare_branch_insights(
    project: str,
    branch_a: str,
    branch_b: str
) -> str:
    """
    Compara insights entre duas branches do mesmo projeto.

    Args:
        project: Nome do projeto
        branch_a: Primeira branch
        branch_b: Segunda branch

    Returns:
        JSON com comparação
    """
    try:
        insights_a = _load_insights(project, branch_a)
        insights_b = _load_insights(project, branch_b)

        comparison = {
            "success": True,
            "project": project,
            "branch_a": branch_a,
            "branch_b": branch_b,
            "count_a": len(insights_a),
            "count_b": len(insights_b),
            "diff": len(insights_b) - len(insights_a),
            "unique_to_a": [],
            "unique_to_b": [],
            "common": []
        }

        ids_a = set(i['id'] for i in insights_a)
        ids_b = set(i['id'] for i in insights_b)

        comparison["unique_to_a"] = list(ids_a - ids_b)
        comparison["unique_to_b"] = list(ids_b - ids_a)
        comparison["common"] = list(ids_a & ids_b)

        return json.dumps(comparison, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def list_all_project_insights() -> str:
    """
    Lista todos os projetos e suas branches com contagem de insights.

    Returns:
        JSON com estrutura completa
    """
    try:
        INSIGHTS_BASE_DIR.mkdir(parents=True, exist_ok=True)

        projects = {}

        for project_dir in INSIGHTS_BASE_DIR.iterdir():
            if project_dir.is_dir():
                project_name = project_dir.name
                branches = []

                for branch_dir in project_dir.iterdir():
                    if branch_dir.is_dir():
                        branch_name = branch_dir.name
                        insights_file = branch_dir / "insights.json"

                        insight_count = 0
                        if insights_file.exists():
                            with open(insights_file, 'r', encoding='utf-8') as f:
                                insights = json.load(f)
                                insight_count = len(insights)

                        branches.append({
                            "name": branch_name,
                            "insights": insight_count,
                            "path": str(branch_dir)
                        })

                projects[project_name] = {
                    "branches": branches,
                    "total_branches": len(branches),
                    "total_insights": sum(b["insights"] for b in branches)
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
