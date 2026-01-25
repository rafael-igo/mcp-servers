#!/usr/bin/env python3
"""
I Go OpenAI Gateway MCP
=======================
Gateway para executar tarefas via OpenAI Responses API.
"""

import json
import os
from pathlib import Path
from typing import List

from mcp.server.fastmcp import FastMCP
from openai import OpenAI

mcp = FastMCP("igo-openai-gateway")

PROJECT_ROOT = Path("/project")
DOCS_DIR = PROJECT_ROOT / "api" / "mcp-servers" / "docs"
AGENTES_DIR = DOCS_DIR / "agentes"
MEMORIA_DIR = DOCS_DIR / "memoria"


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
    model: str = "gpt-5.1-chat-latest",
    temperature: float = 0.2,
    max_output_tokens: int = 1200,
) -> str:
    """
    Executa um prompt diretamente via OpenAI Responses API.
    """
    try:
        client = _client()
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": input_text},
            ],
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
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
    model: str = "gpt-5.1-chat-latest",
    temperature: float = 0.2,
    max_output_tokens: int = 1600,
    include_context: bool = True,
) -> str:
    """
    Executa um agente baseado em docs/agentes/<agent_name>/PROMPT.md
    e injeta contexto atual do projeto (opcional).
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
            temperature=temperature,
            max_output_tokens=max_output_tokens,
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
