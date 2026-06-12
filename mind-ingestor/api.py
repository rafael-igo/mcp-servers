#!/usr/bin/env python3
"""
Mind Ingestor API (HTTP)
========================
Mesmo motor do MCP, exposto por HTTP para o mind-web (upload de docs, captura de chat).

Rodar: .venv/bin/uvicorn api:app --port 4180
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import core

app = FastAPI(title="mind-ingestor", version="0.1.0")


class IngerirReq(BaseModel):
    caminho: str
    titulo: str | None = None
    dominio: str | None = None
    sensibilidade: str | None = None
    usar_llm: bool = True


class ChatReq(BaseModel):
    usuario: str
    pergunta: str
    resposta: str
    contexto: list[str] = []


class NotaReq(BaseModel):
    usuario: str
    texto: str
    titulo: str | None = None


class AprovarReq(BaseModel):
    doc_id: str
    comunidade: str = "profunda"


@app.get("/saude")
def saude():
    return {"ok": True, "memoria": str(core.dir_memoria())}


@app.post("/converter")
def converter(req: IngerirReq):
    try:
        return core.converter_documento(req.caminho)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))


@app.post("/ingerir")
def ingerir(req: IngerirReq):
    try:
        return core.ingerir_documento(req.caminho, req.titulo, req.dominio, req.sensibilidade, req.usar_llm)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))


@app.post("/chat")
def chat(req: ChatReq):
    return core.capturar_chat(req.usuario, req.pergunta, req.resposta, req.contexto)


@app.post("/nota")
def nota(req: NotaReq):
    return core.capturar_nota(req.usuario, req.texto, req.titulo)


@app.get("/inbox")
def inbox():
    return core.listar_inbox()


@app.post("/aprovar")
def aprovar(req: AprovarReq):
    try:
        return core.aprovar(req.doc_id, req.comunidade)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/validar")
def validar(corrigir: bool = False):
    return core.validar_padrao(corrigir)


@app.post("/consolidar")
def consolidar(dominio: str | None = None):
    return core.consolidar(dominio)
