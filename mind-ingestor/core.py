#!/usr/bin/env python3
"""
Mind Ingestor — núcleo compartilhado (MCP stdio + API HTTP usam este módulo).

Motor de Memória da Mind:
- converte documentos (PDF/DOCX/XLSX/PPTX/HTML...) para Markdown (markitdown);
- curadoria opcional via LLM (igo-ai-gateway, contrato /v1/batch com chave tnt_);
- alimenta o cofre Obsidian = pasta memoria/ da Mind, organizada em comunidades:
    _inbox/   pré-memória (aguarda aprovação — o "freio")
    recente/  memória episódica (chat, notas rápidas) — escrita automática
    profunda/ memória semântica (consolidada/curada) — só entra via aprovação
- mantém o padrão (validar_padrao), consolida recente→profunda (consolidar)
  e regenera as notas-hub das comunidades (atualizar_hubs).
"""

import json
import os
import re
import unicodedata
import urllib.request
from datetime import datetime, date
from pathlib import Path

import yaml

SENSIBILIDADES = ["publico", "interno", "restrito", "confidencial"]
COMUNIDADES = ["recente", "profunda"]
CAMPOS_OBRIGATORIOS = ["id", "titulo", "tipo", "sensibilidade", "fonte", "atualizado_em"]

HUB_INFO = {
    "recente": ("⚡ Memória Recente (episódica)",
                "Capturas de chat da Mind e notas rápidas do usuário. Alimentada automaticamente "
                # wikilink do Obsidian resolve por NOME DE ARQUIVO, não pelo id do frontmatter
                "pelo mind-ingestor; candidatas à consolidação em [[_Comunidade — Profunda]]."),
    "profunda": ("🧠 Memória Profunda (semântica)",
                 "Conhecimento consolidado e curado — a Mind responde a partir daqui com confiança."),
}


# ------------------------- Localização dos dados -------------------------

def raiz_dados() -> Path:
    """MIND_DADOS deve apontar para a raiz do projeto Mind (pasta com memoria/)."""
    env = os.environ.get("MIND_DADOS", "").strip()
    if env and (Path(env) / "memoria").is_dir():
        return Path(env)
    raise RuntimeError("Defina MIND_DADOS apontando para a raiz do projeto Mind (pasta com memoria/).")


def dir_memoria() -> Path:
    return raiz_dados() / "memoria"


def dir_comunidade(nome: str) -> Path:
    d = dir_memoria() / nome
    d.mkdir(parents=True, exist_ok=True)
    return d


# ------------------------- Frontmatter / documentos -------------------------

def slugify(texto: str) -> str:
    s = unicodedata.normalize("NFD", texto.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80] or "documento"


def montar_doc(meta: dict, corpo: str) -> str:
    fm = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, default_flow_style=None).strip()
    return f"---\n{fm}\n---\n\n{corpo.strip()}\n"


def parse_doc(caminho: Path) -> tuple[dict, str]:
    texto = caminho.read_text(encoding="utf-8")
    if not texto.startswith("---"):
        return {}, texto
    fim = texto.find("\n---", 3)
    if fim == -1:
        return {}, texto
    try:
        meta = yaml.safe_load(texto[3:fim]) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), texto[fim + 4:].strip()


def _docs_da_comunidade(nome: str) -> list[Path]:
    d = dir_memoria() / nome
    if not d.is_dir():
        return []
    return sorted(p for p in d.glob("*.md") if not p.name.startswith("_"))


# ------------------------- Conversão (determinística) -------------------------

def converter_documento(caminho: str) -> dict:
    """Converte um arquivo local (ou URL) para Markdown com markitdown."""
    from markitdown import MarkItDown  # import tardio: dependência pesada
    origem = caminho.strip()
    if not origem.startswith(("http://", "https://")) and not Path(origem).expanduser().is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {origem}")
    resultado = MarkItDown().convert(str(Path(origem).expanduser()) if not origem.startswith("http") else origem)
    titulo = (resultado.title or Path(origem).stem).strip()
    return {"titulo_sugerido": titulo, "markdown": resultado.text_content.strip()}


# ------------------------- Curadoria (LLM via gateway IGO) -------------------------

def curadoria_llm(markdown: str, titulo: str, modelo: str = "claude-haiku-4-5") -> dict | None:
    """Pede ao gateway frontmatter sugerido (mesmo contrato tnt_/v1/batch do core.ts da Mind).
    Modelo por tamanho da tarefa: curadoria simples = haiku; consolidação passa sonnet."""
    base = os.environ.get("MIND_LLM_BASE_URL", "").rstrip("/")
    key = os.environ.get("MIND_LLM_API_KEY", "")
    if not base or not key.startswith("tnt_"):
        return None
    docs_existentes = [p.stem for c in COMUNIDADES for p in _docs_da_comunidade(c)]
    pedido = {
        "system": (
            "Você cura documentos para a memória da Mind (cérebro digital da empresa). "
            "Responda APENAS um JSON com: titulo, tipo (processo|regra|papel|conceito|doc-dev), "
            "dominio (kebab-case), sensibilidade (publico|interno|restrito|confidencial), "
            "tags (lista), relacionados (lista de ids existentes que tenham relação real), "
            "resumo (1 frase)."
        ),
        "messages": [{"role": "user", "content":
            f"Título: {titulo}\nIds existentes na memória: {docs_existentes}\n\nDocumento:\n{markdown[:6000]}"}],
        "model_hint": modelo,
        "task_type": "chat",
        "agent": "mind-ingestor",
        "temperature": 0.1,
    }
    req = urllib.request.Request(
        f"{base}/v1/batch",
        data=json.dumps(pedido).encode(),
        headers={"content-type": "application/json", "x-igo-ai-key": key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            texto = json.loads(r.read()).get("text", "")
        m = re.search(r"\{.*\}", texto, re.DOTALL)
        return json.loads(m.group(0)) if m else None
    except Exception:
        return None  # curadoria é opcional: sem gateway, segue com heurística


# ------------------------- Ingestão (documentos → _inbox) -------------------------

def ingerir_documento(caminho: str, titulo: str | None = None, dominio: str | None = None,
                      sensibilidade: str | None = None, usar_llm: bool = True) -> dict:
    """Converte e grava em memoria/_inbox/ aguardando aprovação (freio)."""
    conv = converter_documento(caminho)
    titulo = titulo or conv["titulo_sugerido"]
    sugestao = (curadoria_llm(conv["markdown"], titulo) or {}) if usar_llm else {}

    doc_id = slugify(titulo)
    meta = {
        "id": doc_id,
        "comunidade": "profunda",  # destino padrão após aprovação
        "titulo": sugestao.get("titulo", titulo),
        "tipo": sugestao.get("tipo", "conceito"),
        "dominio": dominio or sugestao.get("dominio", "geral"),
        "sensibilidade": _sens(sensibilidade or sugestao.get("sensibilidade")),
        "tags": sugestao.get("tags", []),
        "nos": [],
        "relacionados": sugestao.get("relacionados", []),
        "fonte": f"documento convertido pelo mind-ingestor: {caminho}",
        "atualizado_em": date.today().isoformat(),
    }
    destino = dir_comunidade("_inbox") / f"{doc_id}.md"
    destino.write_text(montar_doc(meta, conv["markdown"]), encoding="utf-8")
    return {"id": doc_id, "arquivo": str(destino), "curadoria_llm": bool(sugestao),
            "sensibilidade_sugerida": meta["sensibilidade"],
            "resumo": sugestao.get("resumo", ""), "status": "aguardando aprovação (_inbox)"}


def _sens(v: str | None) -> str:
    v = (v or "").lower().strip()
    return v if v in SENSIBILIDADES else "interno"


# ------------------------- Captura (chat / notas → recente) -------------------------

def capturar_chat(usuario: str, pergunta: str, resposta: str,
                  contexto: list[str] | None = None, sensibilidade: str = "interno") -> dict:
    """Grava uma troca do chat da Mind como memória episódica (recente/)."""
    agora = datetime.now()
    doc_id = f"chat-{agora.strftime('%Y%m%d-%H%M%S')}-{slugify(usuario)}"
    meta = {
        "id": doc_id, "comunidade": "recente",
        "titulo": f"Chat — {usuario}: {pergunta[:60]}",
        "tipo": "chat", "dominio": "geral", "sensibilidade": _sens(sensibilidade),
        "tags": ["chat"], "nos": [], "relacionados": contexto or [],
        "fonte": "chat-mind", "atualizado_em": agora.date().isoformat(),
    }
    corpo = (f"# {meta['titulo']}\n\n**Pergunta ({usuario}):** {pergunta}\n\n"
             f"**Resposta da Mind:** {resposta}\n\n"
             f"**Contexto usado:** {', '.join(f'[[{c}]]' for c in (contexto or [])) or '—'}")
    destino = dir_comunidade("recente") / f"{doc_id}.md"
    destino.write_text(montar_doc(meta, corpo), encoding="utf-8")
    atualizar_hubs()
    return {"id": doc_id, "arquivo": str(destino)}


def capturar_nota(usuario: str, texto: str, titulo: str | None = None) -> dict:
    """Grava uma nota rápida do usuário como memória episódica (recente/)."""
    agora = datetime.now()
    titulo = titulo or texto.strip().split("\n")[0][:60]
    doc_id = f"nota-{agora.strftime('%Y%m%d-%H%M%S')}-{slugify(titulo)[:40]}"
    meta = {
        "id": doc_id, "comunidade": "recente", "titulo": titulo,
        "tipo": "nota", "dominio": "geral", "sensibilidade": "interno",
        "tags": ["nota"], "nos": [], "relacionados": [],
        "fonte": f"nota de {usuario}", "atualizado_em": agora.date().isoformat(),
    }
    destino = dir_comunidade("recente") / f"{doc_id}.md"
    destino.write_text(montar_doc(meta, f"# {titulo}\n\n{texto.strip()}"), encoding="utf-8")
    atualizar_hubs()
    return {"id": doc_id, "arquivo": str(destino)}


# ------------------------- Freio: inbox e aprovação -------------------------

def listar_inbox() -> list[dict]:
    itens = []
    for p in _docs_da_comunidade("_inbox"):
        meta, _ = parse_doc(p)
        itens.append({"id": meta.get("id", p.stem), "titulo": meta.get("titulo", p.stem),
                      "sensibilidade": meta.get("sensibilidade"), "fonte": meta.get("fonte"),
                      "arquivo": str(p)})
    return itens


def aprovar(doc_id: str, comunidade: str = "profunda") -> dict:
    """Move um doc do _inbox para a comunidade destino (decisão humana — o freio)."""
    if comunidade not in COMUNIDADES:
        raise ValueError(f"Comunidade inválida: {comunidade} (use {COMUNIDADES})")
    origem = dir_memoria() / "_inbox" / f"{doc_id}.md"
    if not origem.is_file():
        raise FileNotFoundError(f"Não há '{doc_id}' no _inbox.")
    meta, corpo = parse_doc(origem)
    meta["comunidade"] = comunidade
    meta["atualizado_em"] = date.today().isoformat()
    destino = dir_comunidade(comunidade) / f"{doc_id}.md"
    destino.write_text(montar_doc(meta, corpo), encoding="utf-8")
    origem.unlink()
    atualizar_hubs()
    return {"id": doc_id, "movido_para": str(destino)}


# ------------------------- Padrão: validação e correção -------------------------

def validar_padrao(corrigir: bool = False) -> dict:
    """Confere o padrão de toda a memória; corrigir=True conserta o que é mecânico."""
    problemas, corrigidos = [], []
    for com in COMUNIDADES:
        for p in _docs_da_comunidade(com):
            meta, corpo = parse_doc(p)
            mudou = False
            for campo in CAMPOS_OBRIGATORIOS:
                if not meta.get(campo):
                    if corrigir and campo == "id":
                        meta["id"], mudou = p.stem, True
                    elif corrigir and campo == "atualizado_em":
                        meta["atualizado_em"], mudou = date.today().isoformat(), True
                    else:
                        problemas.append(f"{com}/{p.name}: falta '{campo}'")
            if meta.get("sensibilidade") not in SENSIBILIDADES:
                if corrigir:
                    meta["sensibilidade"], mudou = _sens(str(meta.get("sensibilidade"))), True
                else:
                    problemas.append(f"{com}/{p.name}: sensibilidade inválida '{meta.get('sensibilidade')}'")
            if meta.get("comunidade") != com:
                if corrigir:
                    meta["comunidade"], mudou = com, True
                else:
                    problemas.append(f"{com}/{p.name}: comunidade '{meta.get('comunidade')}' ≠ pasta '{com}'")
            if mudou:
                p.write_text(montar_doc(meta, corpo), encoding="utf-8")
                corrigidos.append(f"{com}/{p.name}")
    if corrigir:
        atualizar_hubs()
    return {"problemas": problemas, "corrigidos": corrigidos,
            "ok": not problemas, "docs_verificados": sum(len(_docs_da_comunidade(c)) for c in COMUNIDADES)}


# ------------------------- Hubs das comunidades (visual Obsidian) -------------------------

def atualizar_hubs() -> dict:
    """Regenera as notas _Comunidade — *.md (prefixo _ = invisíveis para a Mind, só Obsidian)."""
    nomes = {"recente": "Recente", "profunda": "Profunda"}
    gerados = []
    for com, rotulo in nomes.items():
        titulo, descricao = HUB_INFO[com]
        docs = _docs_da_comunidade(com)
        linhas = [f"- [[{p.stem}]]" for p in docs] or ["(vazia por enquanto)"]
        conteudo = (f"---\nid: _comunidade-{com}\ntitulo: \"Comunidade: Memória {rotulo}\"\n"
                    f"gerado_por: mind-ingestor (atualizar_hubs)\n---\n\n"
                    f"# {titulo}\n\n{descricao}\n\n" + "\n".join(linhas) + "\n")
        destino = dir_memoria() / f"_Comunidade — {rotulo}.md"
        destino.write_text(conteudo, encoding="utf-8")
        gerados.append(str(destino))
    return {"hubs": gerados}


# ------------------------- Consolidação (recente → profunda) -------------------------

def consolidar(dominio: str | None = None) -> dict:
    """
    Propõe consolidar a memória recente em conhecimento profundo.
    Com gateway: o LLM redige um doc consolidado → vai para _inbox (freio, nunca direto).
    Sem gateway: devolve o relatório de candidatos agrupados por domínio.
    """
    recentes = []
    for p in _docs_da_comunidade("recente"):
        meta, corpo = parse_doc(p)
        if dominio and meta.get("dominio") != dominio:
            continue
        recentes.append({"id": meta.get("id", p.stem), "dominio": meta.get("dominio", "geral"),
                         "titulo": meta.get("titulo", p.stem), "corpo": corpo})
    if not recentes:
        return {"status": "nada a consolidar", "candidatos": []}

    grupos: dict[str, list[dict]] = {}
    for r in recentes:
        grupos.setdefault(r["dominio"], []).append(r)

    base = os.environ.get("MIND_LLM_BASE_URL", "")
    if not base:
        return {"status": "sem gateway — relatório de candidatos",
                "candidatos": {d: [r["id"] for r in rs] for d, rs in grupos.items()}}

    propostas = []
    for dom, grupo in grupos.items():
        if len(grupo) < 2:
            continue  # consolidar exige padrão repetido, não nota isolada
        blocos = "\n\n".join(f"## {r['titulo']} ({r['id']})\n{r['corpo'][:2000]}" for r in grupo)
        sugestao = curadoria_llm(
            f"Consolide as memórias episódicas abaixo em UM documento de conhecimento "
            f"permanente do domínio '{dom}' (remova redundância, preserve regras e fatos):\n\n{blocos}",
            f"Consolidado — {dom}", modelo="claude-sonnet-4-6")
        titulo = (sugestao or {}).get("titulo", f"Consolidado — {dom}")
        meta = {
            "id": slugify(titulo), "comunidade": "profunda", "titulo": titulo,
            "tipo": (sugestao or {}).get("tipo", "conceito"), "dominio": dom,
            "sensibilidade": _sens((sugestao or {}).get("sensibilidade")),
            "tags": (sugestao or {}).get("tags", ["consolidado"]),
            "nos": [], "relacionados": [r["id"] for r in grupo],
            "fonte": f"consolidação de {len(grupo)} memórias recentes (mind-ingestor)",
            "atualizado_em": date.today().isoformat(),
        }
        corpo = (sugestao or {}).get("resumo", "") or blocos
        destino = dir_comunidade("_inbox") / f"{meta['id']}.md"
        destino.write_text(montar_doc(meta, f"# {titulo}\n\n{corpo}"), encoding="utf-8")
        propostas.append({"dominio": dom, "id": meta["id"], "origem": [r["id"] for r in grupo]})
    return {"status": "propostas no _inbox aguardando aprovação", "propostas": propostas}
