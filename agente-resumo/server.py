#!/usr/bin/env python3
"""
Agente Resumo MCP
=================
Status do projeto, progresso, relatórios e métricas.
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
MEMORIA_DIR = DOCS_DIR / "memoria"
CONTEXT_FILE = MEMORIA_DIR / "contexto-atual.json"
PROGRESS_FILE = MEMORIA_DIR / "progresso.json"


def _ensure_dirs():
    """Garante que diretórios existam."""
    DOCS_DIR.mkdir(exist_ok=True)
    MEMORIA_DIR.mkdir(exist_ok=True)


def _load_context() -> Dict:
    """Carrega contexto atual do projeto."""
    _ensure_dirs()
    if CONTEXT_FILE.exists():
        with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "project_name": "I GO Experience",
        "phase": "MVP Development",
        "overall_progress": 80,
        "last_updated": datetime.now().isoformat(),
        "modules": {}
    }


def _save_context(context: Dict):
    """Salva contexto do projeto."""
    _ensure_dirs()
    context['last_updated'] = datetime.now().isoformat()
    with open(CONTEXT_FILE, 'w', encoding='utf-8') as f:
        json.dump(context, f, indent=2, ensure_ascii=False)


def _load_progress() -> Dict:
    """Carrega dados de progresso detalhado."""
    _ensure_dirs()
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "modules": {
            "Transfer": {
                "progress": 90,
                "status": "active",
                "features_total": 20,
                "features_done": 18,
                "pending": ["Otimizações de performance", "Testes com datasets grandes"]
            },
            "Rooming List": {
                "progress": 100,
                "status": "completed",
                "features_total": 15,
                "features_done": 15,
                "pending": []
            },
            "Backend API": {
                "progress": 100,
                "status": "completed",
                "features_total": 25,
                "features_done": 25,
                "pending": []
            },
            "Check-in": {
                "progress": 0,
                "status": "planned",
                "features_total": 12,
                "features_done": 0,
                "pending": ["Interface de check-in", "Web NFC API", "Dashboard de presença"]
            }
        },
        "next_steps": [
            {"task": "Conectar Frontend com Backend", "priority": "critical", "estimate": "3-5 dias"},
            {"task": "Implementar Check-in frontend", "priority": "high", "estimate": "1-2 semanas"},
            {"task": "Real-time com WebSockets", "priority": "medium", "estimate": "1 semana"}
        ],
        "blockers": []
    }


@mcp.tool()
def get_project_status(include_details: bool = False) -> str:
    """
    Retorna status geral do projeto.

    Args:
        include_details: Incluir detalhes de cada módulo

    Returns:
        JSON com status do projeto
    """
    try:
        context = _load_context()
        progress = _load_progress()

        status = {
            "project": context.get("project_name", "I GO Experience"),
            "phase": context.get("phase", "MVP Development"),
            "overall_progress": context.get("overall_progress", 80),
            "last_updated": context.get("last_updated"),
            "modules_summary": {}
        }

        # Resumo dos módulos
        for name, module in progress['modules'].items():
            status['modules_summary'][name] = {
                "progress": module['progress'],
                "status": module['status']
            }

        if include_details:
            status['modules_detailed'] = progress['modules']
            status['next_steps'] = progress['next_steps']
            status['blockers'] = progress['blockers']

        return json.dumps({
            "success": True,
            "status": status
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_module_status(module_name: str) -> str:
    """
    Retorna status detalhado de um módulo específico.

    Args:
        module_name: Nome do módulo (Transfer, Rooming List, Backend API, Check-in)

    Returns:
        JSON com status do módulo
    """
    try:
        progress = _load_progress()

        module = progress['modules'].get(module_name)
        if not module:
            return json.dumps({
                "success": False,
                "error": f"Módulo '{module_name}' não encontrado"
            })

        return json.dumps({
            "success": True,
            "module": module_name,
            "details": module
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def update_module_progress(
    module_name: str,
    progress: int,
    status: Optional[str] = None,
    notes: Optional[str] = None
) -> str:
    """
    Atualiza progresso de um módulo.

    Args:
        module_name: Nome do módulo
        progress: Progresso em % (0-100)
        status: Status (active, completed, blocked, planned)
        notes: Notas sobre a atualização

    Returns:
        JSON confirmando atualização
    """
    try:
        data = _load_progress()

        if module_name not in data['modules']:
            return json.dumps({
                "success": False,
                "error": f"Módulo '{module_name}' não encontrado"
            })

        module = data['modules'][module_name]
        old_progress = module['progress']

        module['progress'] = max(0, min(100, progress))
        if status:
            module['status'] = status

        # Histórico de atualizações
        if 'history' not in module:
            module['history'] = []

        module['history'].append({
            "timestamp": datetime.now().isoformat(),
            "progress_change": f"{old_progress}% → {progress}%",
            "notes": notes or "Atualização de progresso"
        })

        # Salvar
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Atualizar contexto geral
        _update_overall_progress()

        return json.dumps({
            "success": True,
            "module": module_name,
            "old_progress": old_progress,
            "new_progress": progress,
            "message": f"✅ {module_name}: {old_progress}% → {progress}%"
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


def _update_overall_progress():
    """Recalcula progresso geral do projeto."""
    progress = _load_progress()
    context = _load_context()

    # Média ponderada dos módulos
    total = 0
    count = 0
    for module in progress['modules'].values():
        total += module['progress']
        count += 1

    if count > 0:
        context['overall_progress'] = int(total / count)
        _save_context(context)


@mcp.tool()
def get_next_steps(limit: int = 10) -> str:
    """
    Lista próximos passos priorizados.

    Args:
        limit: Número máximo de itens

    Returns:
        JSON com próximos passos
    """
    try:
        progress = _load_progress()
        next_steps = progress.get('next_steps', [])[:limit]

        return json.dumps({
            "success": True,
            "count": len(next_steps),
            "next_steps": next_steps
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def add_next_step(
    task: str,
    priority: str = "medium",
    estimate: Optional[str] = None,
    module: Optional[str] = None
) -> str:
    """
    Adiciona um novo próximo passo.

    Args:
        task: Descrição da tarefa
        priority: Prioridade (critical, high, medium, low)
        estimate: Estimativa de tempo
        module: Módulo relacionado

    Returns:
        JSON confirmando adição
    """
    try:
        progress = _load_progress()

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

        # Salvar
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

        return json.dumps({
            "success": True,
            "step": step,
            "message": f"✅ Próximo passo adicionado: {task}"
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def generate_report(
    report_type: str = "executive",
    audience: str = "team"
) -> str:
    """
    Gera relatório formatado do projeto.

    Args:
        report_type: Tipo de relatório
          - executive: Resumo executivo
          - technical: Detalhes técnicos
          - onboarding: Para novos membros
          - stakeholder: Para stakeholders
        audience: Público-alvo (team, management, client)

    Returns:
        JSON com relatório formatado
    """
    try:
        context = _load_context()
        progress = _load_progress()

        report = {
            "title": f"Relatório {report_type.title()} - {context['project_name']}",
            "generated_at": datetime.now().isoformat(),
            "audience": audience,
            "content": {}
        }

        if report_type == "executive":
            report['content'] = {
                "summary": f"Projeto em fase {context['phase']}",
                "progress": f"{context['overall_progress']}% completo",
                "modules": {
                    name: f"{mod['progress']}% - {mod['status']}"
                    for name, mod in progress['modules'].items()
                },
                "next_milestone": progress['next_steps'][0]['task'] if progress['next_steps'] else "N/A",
                "blockers_count": len(progress.get('blockers', []))
            }

        elif report_type == "technical":
            report['content'] = {
                "phase": context['phase'],
                "overall_progress": context['overall_progress'],
                "modules_detailed": progress['modules'],
                "next_steps": progress['next_steps'],
                "blockers": progress.get('blockers', []),
                "last_updated": context['last_updated']
            }

        elif report_type == "onboarding":
            report['content'] = {
                "welcome": f"Bem-vindo ao projeto {context['project_name']}!",
                "current_phase": context['phase'],
                "what_is": "Sistema de gestão de eventos e viagens de incentivo internacionais",
                "modules": list(progress['modules'].keys()),
                "how_to_start": [
                    "1. Entender arquitetura geral",
                    "2. Escolher módulo para trabalhar",
                    "3. Consultar próximos passos",
                    "4. Usar agentes especialistas"
                ],
                "next_priorities": progress['next_steps'][:3]
            }

        elif report_type == "stakeholder":
            completed = sum(1 for m in progress['modules'].values() if m['status'] == 'completed')
            total = len(progress['modules'])

            report['content'] = {
                "project": context['project_name'],
                "status": f"{context['overall_progress']}% completo",
                "modules_completed": f"{completed}/{total} módulos",
                "current_focus": progress['next_steps'][0]['task'] if progress['next_steps'] else "N/A",
                "estimated_completion": "4-6 semanas (MVP completo)",
                "blockers": "Nenhum crítico" if not progress.get('blockers') else f"{len(progress['blockers'])} bloqueadores"
            }

        return json.dumps({
            "success": True,
            "report": report
        }, indent=2, ensure_ascii=False)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@mcp.tool()
def get_metrics() -> str:
    """
    Retorna métricas e estatísticas do projeto.

    Returns:
        JSON com métricas
    """
    try:
        context = _load_context()
        progress = _load_progress()

        # Calcular métricas
        modules = progress['modules']
        total_features = sum(m['features_total'] for m in modules.values())
        done_features = sum(m['features_done'] for m in modules.values())

        metrics = {
            "overall_progress": context['overall_progress'],
            "modules": {
                "total": len(modules),
                "completed": sum(1 for m in modules.values() if m['status'] == 'completed'),
                "active": sum(1 for m in modules.values() if m['status'] == 'active'),
                "planned": sum(1 for m in modules.values() if m['status'] == 'planned')
            },
            "features": {
                "total": total_features,
                "completed": done_features,
                "remaining": total_features - done_features,
                "completion_rate": int((done_features / total_features * 100)) if total_features > 0 else 0
            },
            "next_steps": {
                "total": len(progress.get('next_steps', [])),
                "critical": sum(1 for s in progress.get('next_steps', []) if s.get('priority') == 'critical'),
                "high": sum(1 for s in progress.get('next_steps', []) if s.get('priority') == 'high')
            },
            "blockers": len(progress.get('blockers', [])),
            "last_updated": context.get('last_updated')
        }

        return json.dumps({
            "success": True,
            "metrics": metrics
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
