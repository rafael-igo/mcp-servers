#!/usr/bin/env python3
"""
I Go OpenAI Gateway MCP
=======================
Gateway para executar tarefas via OpenAI Responses API com suporte a:
- GPT-5.2 Responses API
- Custom Tools (apply_patch, shell)
- Preambles
- 17 agentes especializados
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from mcp.server.fastmcp import FastMCP
from openai import OpenAI

mcp = FastMCP("igo-openai-gateway")

PROJECT_ROOT = Path("/project")
MCP_SERVERS_DIR = PROJECT_ROOT / "GIT-RAFAEL" / "mcp-servers"
DOCS_DIR = MCP_SERVERS_DIR / "docs"
AGENTES_DIR = DOCS_DIR / "agentes"
MEMORIA_DIR = DOCS_DIR / "memoria"

# Available agent categories
DEVELOPMENT_AGENTS = [
    "agente-arquiteto-igo",
    "agente-frontend-igo",
    "agente-integracoes-igo",
    "agente-qa-testes",
    "agente-solucoes",
]

MODULE_AGENTS = [
    "agente-backend",
    "agente-checkin",
    "agente-rooming-list",
    "agente-transfer",
    "agente-rsvp",
    "agente-tracking",
    "agente-credenciamento",
]

BUSINESS_AGENTS = [
    "agente-analytics-kpi",
    "agente-comercial-igo",
    "agente-diretoria-igo",
    "agente-marketing-igo",
    "agente-operacao-igo",
]


def _client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY não definido no ambiente do container.")
    return OpenAI(api_key=api_key)


def _load_context() -> str:
    context_file = MEMORIA_DIR / "contexto-atual.md"
    if context_file.exists():
        return context_file.read_text(encoding="utf-8")
    return ""


def _load_agent_prompt(agent_name: str) -> str:
    prompt_file = AGENTES_DIR / agent_name / "PROMPT.md"
    if not prompt_file.exists():
        raise FileNotFoundError(f"PROMPT.md não encontrado para o agente: {agent_name}")
    return prompt_file.read_text(encoding="utf-8")


def _extract_text(response) -> str:
    if hasattr(response, "output_text"):
        return response.output_text or ""
    parts: List[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                parts.append(text)
    return "\n".join(parts).strip() if parts else str(response)


@mcp.tool()
def run_prompt(
    prompt: str,
    input_text: str,
    model: str = "gpt-5.2-2025-12-11",
    reasoning_effort: str = "none",
    verbosity: str = "medium",
    max_output_tokens: int = 1200,
) -> str:
    """
    Executa um prompt diretamente via OpenAI Responses API.

    Args:
        prompt: System prompt
        input_text: User input
        model: Model to use (default: gpt-5.2-2025-12-11)
        reasoning_effort: none, low, medium, high, xhigh (default: none)
        verbosity: low, medium, high (default: medium)
        max_output_tokens: Maximum output tokens
    """
    try:
        client = _client()

        # Build request parameters
        params = {
            "model": model,
            "input": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text},
            ],
            "max_output_tokens": max_output_tokens,
        }

        # Add reasoning effort if not none
        if reasoning_effort != "none":
            params["reasoning"] = {"effort": reasoning_effort}

        # Add verbosity
        params["text"] = {"verbosity": verbosity}

        response = client.responses.create(**params)
        return json.dumps(
            {"success": True, "model": model, "text": _extract_text(response)},
            ensure_ascii=False,
            indent=2,
        )
    except Exception as exc:
        return json.dumps(
            {"success": False, "error": str(exc)},
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
def run_agent(
    agent_name: str,
    task: str,
    model: str = "gpt-5.2-2025-12-11",
    reasoning_effort: str = "none",
    verbosity: str = "medium",
    max_output_tokens: int = 1600,
    include_context: bool = True,
) -> str:
    """
    Executa um agente baseado em docs/agentes/<agent_name>/PROMPT.md
    e injeta contexto atual do projeto (opcional).

    Args:
        agent_name: Nome do agente (ex: agente-resumo)
        task: Tarefa a ser executada
        model: Model to use (default: gpt-5.2-2025-12-11)
        reasoning_effort: none, low, medium, high, xhigh (default: none)
        verbosity: low, medium, high (default: medium)
        max_output_tokens: Maximum output tokens
        include_context: Include project context from memoria
    """
    try:
        agent_prompt = _load_agent_prompt(agent_name)
        context = _load_context() if include_context else ""
        full_user = f"""# Tarefa
{task}

# Contexto atual (se houver)
{context}
"""
        return run_prompt(
            prompt=agent_prompt,
            input_text=full_user,
            model=model,
            reasoning_effort=reasoning_effort,
            verbosity=verbosity,
            max_output_tokens=max_output_tokens,
        )
    except Exception as exc:
        return json.dumps(
            {"success": False, "error": str(exc)},
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
def list_available_agents(category: Optional[str] = None) -> str:
    """
    Lista todos os agentes disponíveis, opcionalmente filtrados por categoria.

    Args:
        category: development, module, business, ou None para todos

    Returns:
        JSON com lista de agentes disponíveis
    """
    try:
        agents_map = {
            "development": DEVELOPMENT_AGENTS,
            "module": MODULE_AGENTS,
            "business": BUSINESS_AGENTS,
        }

        if category:
            if category not in agents_map:
                return json.dumps(
                    {
                        "success": False,
                        "error": f"Categoria inválida: {category}. Use: development, module, business",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            agents = agents_map[category]
            result = {"category": category, "agents": agents, "count": len(agents)}
        else:
            result = {
                "categories": {
                    "development": {"agents": DEVELOPMENT_AGENTS, "count": len(DEVELOPMENT_AGENTS)},
                    "module": {"agents": MODULE_AGENTS, "count": len(MODULE_AGENTS)},
                    "business": {"agents": BUSINESS_AGENTS, "count": len(BUSINESS_AGENTS)},
                },
                "total": len(DEVELOPMENT_AGENTS) + len(MODULE_AGENTS) + len(BUSINESS_AGENTS),
            }

        return json.dumps(
            {"success": True, **result},
            ensure_ascii=False,
            indent=2,
        )
    except Exception as exc:
        return json.dumps(
            {"success": False, "error": str(exc)},
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
def run_development_agent(
    agent_name: str,
    task: str,
    reasoning_effort: str = "medium",
    verbosity: str = "high",
    use_preambles: bool = True,
) -> str:
    """
    Executa um agente de desenvolvimento (arquiteto, frontend, QA, etc).
    Usa reasoning médio e alta verbosidade por padrão para análises detalhadas.

    Args:
        agent_name: Nome do agente (ex: agente-arquiteto-igo, agente-frontend-igo)
        task: Tarefa a ser executada
        reasoning_effort: none, low, medium, high, xhigh (default: medium)
        verbosity: low, medium, high (default: high)
        use_preambles: Adicionar preambles antes de tool calls

    Returns:
        JSON com resultado da execução
    """
    try:
        if agent_name not in DEVELOPMENT_AGENTS:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Agente '{agent_name}' não é um agente de desenvolvimento. Disponíveis: {DEVELOPMENT_AGENTS}",
                },
                ensure_ascii=False,
                indent=2,
            )

        # Add preamble instruction if enabled
        agent_prompt = _load_agent_prompt(agent_name)
        if use_preambles:
            agent_prompt += "\n\nIMPORTANTE: Antes de chamar qualquer ferramenta, explique brevemente por que você está chamando ela."

        context = _load_context()
        full_user = f"""# Tarefa de Desenvolvimento
{task}

# Contexto do Projeto
{context}
"""
        return run_prompt(
            prompt=agent_prompt,
            input_text=full_user,
            reasoning_effort=reasoning_effort,
            verbosity=verbosity,
            max_output_tokens=2500,
        )
    except Exception as exc:
        return json.dumps(
            {"success": False, "error": str(exc)},
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
def run_code_analysis(
    code: str,
    analysis_type: str = "review",
    language: str = "python",
    reasoning_effort: str = "high",
) -> str:
    """
    Executa análise de código usando GPT-5.2 com reasoning alto.

    Args:
        code: Código a ser analisado
        analysis_type: review, refactor, debug, optimize, security
        language: Linguagem do código (python, javascript, typescript, etc)
        reasoning_effort: none, low, medium, high, xhigh (default: high)

    Returns:
        JSON com análise detalhada
    """
    try:
        analysis_prompts = {
            "review": "Você é um expert code reviewer. Analise o código abaixo e forneça feedback detalhado sobre qualidade, boas práticas, possíveis bugs e melhorias.",
            "refactor": "Você é um expert em refatoração. Analise o código e sugira melhorias de estrutura, legibilidade e manutenibilidade.",
            "debug": "Você é um expert debugger. Analise o código e identifique possíveis bugs, edge cases não tratados e problemas lógicos.",
            "optimize": "Você é um expert em otimização. Analise o código e sugira melhorias de performance, complexidade e uso de recursos.",
            "security": "Você é um expert em segurança. Analise o código e identifique vulnerabilidades, falhas de segurança e boas práticas de segurança.",
        }

        if analysis_type not in analysis_prompts:
            return json.dumps(
                {
                    "success": False,
                    "error": f"Tipo de análise inválido: {analysis_type}. Use: review, refactor, debug, optimize, security",
                },
                ensure_ascii=False,
                indent=2,
            )

        prompt = analysis_prompts[analysis_type]
        input_text = f"""Linguagem: {language}

Código:
```{language}
{code}
```

Forneça uma análise detalhada e estruturada."""

        return run_prompt(
            prompt=prompt,
            input_text=input_text,
            reasoning_effort=reasoning_effort,
            verbosity="high",
            max_output_tokens=3000,
        )
    except Exception as exc:
        return json.dumps(
            {"success": False, "error": str(exc)},
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
def run_architectural_review(
    description: str,
    context: Optional[str] = None,
    reasoning_effort: str = "xhigh",
) -> str:
    """
    Executa revisão arquitetural usando o agente-arquiteto-igo com reasoning xhigh.
    Ideal para decisões de arquitetura complexas.

    Args:
        description: Descrição do problema/feature a ser analisado
        context: Contexto adicional específico (opcional)
        reasoning_effort: none, low, medium, high, xhigh (default: xhigh)

    Returns:
        JSON com análise arquitetural detalhada
    """
    try:
        task = f"""Realize uma análise arquitetural completa:

{description}

Considere:
1. Padrões de arquitetura adequados
2. Escalabilidade e manutenibilidade
3. Trade-offs técnicos
4. Riscos e mitigações
5. Recomendações específicas

{f'Contexto adicional: {context}' if context else ''}
"""
        return run_development_agent(
            agent_name="agente-arquiteto-igo",
            task=task,
            reasoning_effort=reasoning_effort,
            verbosity="high",
            use_preambles=True,
        )
    except Exception as exc:
        return json.dumps(
            {"success": False, "error": str(exc)},
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
def generate_tests(
    code: str,
    test_type: str = "unit",
    framework: str = "pytest",
    reasoning_effort: str = "medium",
) -> str:
    """
    Gera testes usando o agente-qa-testes com GPT-5.2.

    Args:
        code: Código para gerar testes
        test_type: unit, integration, e2e
        framework: pytest, jest, vitest, etc
        reasoning_effort: none, low, medium, high, xhigh (default: medium)

    Returns:
        JSON com código de testes gerado
    """
    try:
        task = f"""Gere testes {test_type} para o código abaixo usando {framework}.

Código:
```
{code}
```

Inclua:
- Casos de teste positivos e negativos
- Edge cases
- Mocks quando necessário
- Cobertura completa
"""
        return run_development_agent(
            agent_name="agente-qa-testes",
            task=task,
            reasoning_effort=reasoning_effort,
            verbosity="high",
        )
    except Exception as exc:
        return json.dumps(
            {"success": False, "error": str(exc)},
            ensure_ascii=False,
            indent=2,
        )


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
