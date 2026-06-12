#!/usr/bin/env python3
"""
Mind Ingestor MCP
=================
Motor de Memória da Mind via MCP (stdio): converte documentos para Markdown,
alimenta o cofre Obsidian (memoria/ com comunidades recente/profunda),
captura chat/notas e mantém o padrão. Requer env MIND_DADOS.
"""

import json

from mcp.server.fastmcp import FastMCP

import core

mcp = FastMCP("mind-ingestor")


def _json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)


@mcp.tool()
def converter_documento(caminho: str) -> str:
    """Converte um documento (PDF/DOCX/XLSX/PPTX/HTML/URL) para Markdown, sem gravar nada."""
    return _json(core.converter_documento(caminho))


@mcp.tool()
def ingerir_documento(caminho: str, titulo: str = "", dominio: str = "",
                      sensibilidade: str = "", usar_llm: bool = True) -> str:
    """Converte um documento e grava em memoria/_inbox/ aguardando aprovação (freio).
    Com gateway configurado, o LLM sugere frontmatter (tipo, domínio, sensibilidade, tags, links)."""
    return _json(core.ingerir_documento(caminho, titulo or None, dominio or None,
                                        sensibilidade or None, usar_llm))


@mcp.tool()
def capturar_chat(usuario: str, pergunta: str, resposta: str, contexto: list[str] | None = None) -> str:
    """Grava uma troca do chat da Mind na memória recente (episódica)."""
    return _json(core.capturar_chat(usuario, pergunta, resposta, contexto))


@mcp.tool()
def capturar_nota(usuario: str, texto: str, titulo: str = "") -> str:
    """Grava uma nota rápida do usuário na memória recente (episódica)."""
    return _json(core.capturar_nota(usuario, texto, titulo or None))


@mcp.tool()
def listar_inbox() -> str:
    """Lista documentos no _inbox aguardando aprovação."""
    return _json(core.listar_inbox())


@mcp.tool()
def aprovar(doc_id: str, comunidade: str = "profunda") -> str:
    """Aprova um doc do _inbox movendo-o para a comunidade destino (recente|profunda)."""
    return _json(core.aprovar(doc_id, comunidade))


@mcp.tool()
def validar_padrao(corrigir: bool = False) -> str:
    """Valida o padrão de frontmatter de toda a memória; corrigir=True conserta o mecânico."""
    return _json(core.validar_padrao(corrigir))


@mcp.tool()
def consolidar(dominio: str = "") -> str:
    """Propõe consolidação da memória recente em profunda (proposta vai pro _inbox, nunca direto)."""
    return _json(core.consolidar(dominio or None))


@mcp.tool()
def atualizar_hubs() -> str:
    """Regenera as notas-hub _Comunidade — *.md (visíveis só no Obsidian)."""
    return _json(core.atualizar_hubs())


if __name__ == "__main__":
    mcp.run()
