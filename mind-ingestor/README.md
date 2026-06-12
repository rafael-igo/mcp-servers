# mind-ingestor — Motor de Memória da Mind

MCP **híbrido** (stdio para LLMs + API HTTP para o mind-web) que alimenta o cofre Obsidian
da Mind (`memoria/` do projeto Mind) com documentos convertidos para Markdown, capturas de
chat e notas — organizados em **comunidades** (camadas de memória):

| Comunidade | Papel cerebral | Como entra |
|---|---|---|
| `_inbox/` | pré-memória | `ingerir_documento` / `consolidar` — aguarda aprovação (**freio**) |
| `recente/` | memória episódica | `capturar_chat` / `capturar_nota` — automático |
| `profunda/` | memória semântica | só via `aprovar` (decisão humana) |

A pasta `memoria/` **é** o cofre Obsidian (abra-a como vault). As notas-hub
`_Comunidade — *.md` e o `.obsidian/graph.json` colorem as comunidades no grafo.
Arquivos com prefixo `_` são invisíveis para a Mind (core.ts ignora).

## Conversão híbrida

1. **Determinística:** `markitdown` (PDF, DOCX, XLSX, PPTX, HTML, URL) → Markdown bruto.
2. **Curadoria LLM (opcional):** igo-ai-gateway (`/v1/batch`, chave `tnt_`) sugere frontmatter
   (tipo, domínio, **sensibilidade**, tags, `relacionados` com docs existentes). Sem gateway,
   segue com heurística — nada quebra.

## Setup

```bash
cd /Users/rafamacpro/Projetos/GIT-RAFAEL/mcp-servers/mind-ingestor
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Env obrigatória: `MIND_DADOS=/Users/rafamacpro/Projetos/MIND/Mind`
Env opcional (curadoria LLM): `MIND_LLM_BASE_URL`, `MIND_LLM_API_KEY` (tnt_...) — as mesmas do mind-web.

**MCP (stdio):** registrado no `.mcp.json` do projeto Mind.
**API (HTTP):** `.venv/bin/uvicorn api:app --port 4180` — o mind-web manda o chat pra cá
(`MIND_INGESTOR_URL=http://localhost:4180`).

## Tools / endpoints

| MCP tool | HTTP | Função |
|---|---|---|
| `converter_documento` | `POST /converter` | doc → MD (não grava) |
| `ingerir_documento` | `POST /ingerir` | doc → `_inbox/` com frontmatter |
| `capturar_chat` | `POST /chat` | troca do chat → `recente/` |
| `capturar_nota` | `POST /nota` | nota do usuário → `recente/` |
| `listar_inbox` | `GET /inbox` | pendências do freio |
| `aprovar` | `POST /aprovar` | `_inbox/` → comunidade destino |
| `validar_padrao` | `POST /validar` | lint do frontmatter (corrigir=True conserta) |
| `consolidar` | `POST /consolidar` | recente → proposta consolidada no `_inbox/` |
| `atualizar_hubs` | — | regenera notas-hub das comunidades |

## Gatilhos PT-BR

| Gatilho | Tool |
|---|---|
| "ingere o documento [caminho] na Mind" | `ingerir_documento` |
| "converte [caminho] pra markdown" | `converter_documento` |
| "o que tem no inbox da Mind?" | `listar_inbox` |
| "aprova [id] na memória profunda" | `aprovar` |
| "valida o padrão da memória" | `validar_padrao` |
| "consolida a memória recente" | `consolidar` |
