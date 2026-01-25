#!/usr/bin/env python3
"""
Agente Insights MCP
===================
Captura de ideias, consulta a especialistas e tomada de decisões.
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
INSIGHTS_FILE = DOCS_DIR / "insights_capturados.json"
MEMORIA_DIR = DOCS_DIR / "memoria"


def _ensure_dirs():
    """Garante que diretórios existam."""
    DOCS_DIR.mkdir(exist_ok=True)
    MEMORIA_DIR.mkdir(exist_ok=True)


def _load_insights() -> List[Dict]:
    """Carrega insights do arquivo JSON."""
    _ensure_dirs()
    if INSIGHTS_FILE.exists():
        with open(INSIGHTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def _save_insights(insights: List[Dict]):
    """Salva insights no arquivo JSON."""
    _ensure_dirs()
    with open(INSIGHTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(insights, f, indent=2, ensure_ascii=False)


def _get_next_id() -> str:
    """Retorna próximo ID disponível."""
    insights = _load_insights()
    if not insights:
        return "INS-0001"

    last_id = max(int(i['id'].split('-')[1]) for i in insights)
    return f"INS-{last_id + 1:04d}"


@mcp.tool()
def capture_insight(
    idea: str,
    insight_type: str = "feature",
    complexity: str = "medium",
    modules: Optional[List[str]] = None
) -> str:
    """
    Captura um novo insight do usuário.

    Args:
        idea: Descrição da ideia ou sugestão
        insight_type: Tipo (feature, bug, improvement, decision, exploration)
        complexity: Complexidade (low, medium, high)
        modules: Lista de módulos impactados

    Returns:
        JSON com insight criado
    """
    try:
        insights = _load_insights()

        insight = {
            "id": _get_next_id(),
            "timestamp": datetime.now().isoformat(),
            "type": insight_type,
            "complexity": complexity,
            "status": "captured",  # captured, analyzing, approved, rejected, implemented
            "idea": idea,
            "modules": modules or [],
            "agents_consulted": [],
            "analysis": {},
            "decision": None,
            "next_steps": []
        }

        insights.append(insight)
        _save_insights(insights)

        return json.dumps({
            "success": True,
            "insight": insight,
            "message": f"✅ Insight {insight['id']} capturado!"
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
    limit: int = 10
) -> str:
    """
    Lista insights capturados com filtros.

    Args:
        status: Filtrar por status (captured, analyzing, approved, rejected, implemented)
        insight_type: Filtrar por tipo (feature, bug, improvement, decision, exploration)
        limit: Número máximo de resultados

    Returns:
        JSON com lista de insights
    """
    try:
        insights = _load_insights()

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
            "insights": insights
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
    notes: Optional[str] = None
) -> str:
    """
    Atualiza status de um insight.

    Args:
        insight_id: ID do insight (ex: INS-0001)
        new_status: Novo status (captured, analyzing, approved, rejected, implemented)
        notes: Notas sobre a mudança de status

    Returns:
        JSON confirmando atualização
    """
    try:
        insights = _load_insights()

        # Encontrar insight
        insight = next((i for i in insights if i['id'] == insight_id), None)
        if not insight:
            return json.dumps({
                "success": False,
                "error": f"Insight {insight_id} não encontrado"
            })

        # Atualizar
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

        _save_insights(insights)

        return json.dumps({
            "success": True,
            "insight_id": insight_id,
            "old_status": old_status,
            "new_status": new_status,
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
    recommendation: Optional[str] = None
) -> str:
    """
    Adiciona feedback de um agente especialista a um insight.

    Args:
        insight_id: ID do insight
        agent_name: Nome do agente consultado
        feedback: Feedback do agente
        recommendation: Recomendação do agente

    Returns:
        JSON confirmando adição
    """
    try:
        insights = _load_insights()

        insight = next((i for i in insights if i['id'] == insight_id), None)
        if not insight:
            return json.dumps({
                "success": False,
                "error": f"Insight {insight_id} não encontrado"
            })

        # Adicionar feedback
        if 'agents_consulted' not in insight:
            insight['agents_consulted'] = []

        insight['agents_consulted'].append({
            "agent": agent_name,
            "timestamp": datetime.now().isoformat(),
            "feedback": feedback,
            "recommendation": recommendation
        })

        _save_insights(insights)

        return json.dumps({
            "success": True,
            "insight_id": insight_id,
            "agent": agent_name,
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
    effort_estimate: Optional[str] = None
) -> str:
    """
    Registra decisão sobre um insight.

    Args:
        insight_id: ID do insight
        decision_status: Decisão (approved, rejected, deferred)
        rationale: Justificativa da decisão
        priority: Prioridade (critical, high, medium, low)
        effort_estimate: Estimativa de esforço

    Returns:
        JSON confirmando decisão
    """
    try:
        insights = _load_insights()

        insight = next((i for i in insights if i['id'] == insight_id), None)
        if not insight:
            return json.dumps({
                "success": False,
                "error": f"Insight {insight_id} não encontrado"
            })

        # Registrar decisão
        insight['decision'] = {
            "status": decision_status,
            "rationale": rationale,
            "priority": priority,
            "effort_estimate": effort_estimate,
            "decided_at": datetime.now().isoformat()
        }

        # Atualizar status do insight
        if decision_status == "approved":
            insight['status'] = "approved"
        elif decision_status == "rejected":
            insight['status'] = "rejected"

        _save_insights(insights)

        return json.dumps({
            "success": True,
            "insight_id": insight_id,
            "decision": decision_status,
            "message": f"✅ Decisão registrada: {decision_status.upper()}"
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_statistics() -> str:
    """
    Retorna estatísticas dos insights capturados.

    Returns:
        JSON com estatísticas
    """
    try:
        insights = _load_insights()

        stats = {
            "total": len(insights),
            "by_status": {},
            "by_type": {},
            "by_complexity": {},
            "recent_count": 0
        }

        # Contadores
        for insight in insights:
            # Por status
            status = insight['status']
            stats['by_status'][status] = stats['by_status'].get(status, 0) + 1

            # Por tipo
            itype = insight['type']
            stats['by_type'][itype] = stats['by_type'].get(itype, 0) + 1

            # Por complexidade
            complexity = insight['complexity']
            stats['by_complexity'][complexity] = stats['by_complexity'].get(complexity, 0) + 1

            # Recentes (últimos 7 dias)
            timestamp = datetime.fromisoformat(insight['timestamp'])
            if (datetime.now() - timestamp).days <= 7:
                stats['recent_count'] += 1

        return json.dumps({
            "success": True,
            "statistics": stats
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
