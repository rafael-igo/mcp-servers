#!/usr/bin/env python3
"""
LP Guardian - MCP Especializado para nova-plataforma-lp_v1

Um "guardião do sistema" com conhecimento completo de:
- Todos os fluxos de negócio (RSVP, Link Cripto, Chave, Optin)
- Estrutura de componentes (Vue 3 + Vuetify 3)
- Stores Pinia (mainStore, formularioStore, colaboradorStore)
- Regras de validação e configurações de admin
"""

import json
import os
from pathlib import Path
from typing import Optional
from mcp.server.fastmcp import FastMCP

# Inicializar servidor
mcp = FastMCP("lp-guardian")

# Caminho base para os arquivos de conhecimento
KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"


def load_knowledge(filename: str) -> dict:
    """Carrega arquivo JSON de conhecimento."""
    filepath = KNOWLEDGE_DIR / filename
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# Carregar conhecimento em memória
FLOWS = load_knowledge("flows.json")
COMPONENTS = load_knowledge("components.json")
STORES = load_knowledge("stores.json")
RULES = load_knowledge("rules.json")


@mcp.tool()
def explain_flow(nome_fluxo: str) -> str:
    """
    Explica um fluxo específico do sistema.

    Args:
        nome_fluxo: Nome do fluxo (link_cripto, rsvp, chave, optin, cadastro_igo, upload)

    Returns:
        JSON com diagrama, arquivos envolvidos, regras e exemplos
    """
    fluxo = FLOWS.get(nome_fluxo)

    if not fluxo:
        fluxos_disponiveis = list(FLOWS.keys())
        return json.dumps({
            "erro": f"Fluxo '{nome_fluxo}' não encontrado",
            "fluxos_disponiveis": fluxos_disponiveis
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "fluxo": nome_fluxo,
        "descricao": fluxo.get("descricao", ""),
        "diagrama": fluxo.get("diagrama", ""),
        "arquivos": fluxo.get("arquivos", []),
        "regras": fluxo.get("regras", []),
        "exemplo": fluxo.get("exemplo", ""),
        "relacionados": fluxo.get("relacionados", [])
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def explain_component(nome_componente: str) -> str:
    """
    Detalha um componente Vue específico.

    Args:
        nome_componente: Nome do componente (ex: ModuloFormulario, FormularioSistemaPadrao)

    Returns:
        JSON com props, emits, slots, dependências e exemplos de uso
    """
    componente = COMPONENTS.get(nome_componente)

    if not componente:
        componentes_disponiveis = list(COMPONENTS.keys())
        return json.dumps({
            "erro": f"Componente '{nome_componente}' não encontrado",
            "componentes_disponiveis": componentes_disponiveis
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "componente": nome_componente,
        "arquivo": componente.get("arquivo", ""),
        "responsabilidade": componente.get("responsabilidade", ""),
        "props": componente.get("props", {}),
        "emits": componente.get("emits", []),
        "slots": componente.get("slots", []),
        "dependencias": componente.get("dependencias", []),
        "usa_stores": componente.get("usa_stores", []),
        "exemplo_uso": componente.get("exemplo_uso", "")
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def validate_config(config_json: str, tipo_config: str = "lp_flow") -> str:
    """
    Valida uma configuração de lp_flow ou lp_formulario.

    Args:
        config_json: JSON string da configuração a validar
        tipo_config: Tipo de config (lp_flow, lp_formulario, lp_conteudo)

    Returns:
        JSON com erros, warnings e sugestões de correção
    """
    try:
        config = json.loads(config_json)
    except json.JSONDecodeError as e:
        return json.dumps({
            "valido": False,
            "erros": [f"JSON inválido: {str(e)}"],
            "warnings": [],
            "sugestoes": ["Verifique a sintaxe do JSON"]
        }, ensure_ascii=False, indent=2)

    erros = []
    warnings = []
    sugestoes = []

    regras = RULES.get(tipo_config, {})
    campos_obrigatorios = regras.get("campos_obrigatorios", [])
    campos_validos = regras.get("campos_validos", [])

    # Verificar campos obrigatórios
    for campo in campos_obrigatorios:
        if campo not in config:
            erros.append(f"Campo obrigatório ausente: {campo}")

    # Verificar campos desconhecidos
    for campo in config.keys():
        if campos_validos and campo not in campos_validos:
            warnings.append(f"Campo desconhecido: {campo}")

    # Validações específicas por tipo
    if tipo_config == "lp_flow":
        if "status_rules" in config and not isinstance(config["status_rules"], list):
            erros.append("status_rules deve ser um array")

        if "runtime_rules" in config and not isinstance(config["runtime_rules"], list):
            erros.append("runtime_rules deve ser um array")

        if "mapa_formularios" in config:
            mapa = config["mapa_formularios"]
            if "principal" not in mapa:
                warnings.append("mapa_formularios sem 'principal' definido")

    elif tipo_config == "lp_formulario":
        if "formularios" in config and not isinstance(config["formularios"], list):
            erros.append("formularios deve ser um array")

        if "layoutFormulario" in config:
            layout = config["layoutFormulario"]
            if "estilosVisuais" not in layout:
                warnings.append("layoutFormulario sem estilosVisuais")

    return json.dumps({
        "valido": len(erros) == 0,
        "erros": erros,
        "warnings": warnings,
        "sugestoes": sugestoes
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def suggest_fix(descricao_erro: str) -> str:
    """
    Sugere correção para um erro comum.

    Args:
        descricao_erro: Descrição do erro ou problema encontrado

    Returns:
        JSON com causa provável, solução e código exemplo
    """
    # Base de conhecimento de erros comuns
    erros_conhecidos = {
        "link cripto não funciona": {
            "causa": "Parâmetros obrigatórios ausentes ou evento_rsvp_lp desabilitado",
            "solucao": "Verificar se URL tem id, w!, y! e se evento_rsvp_lp=true nos controles",
            "arquivo": "src/Funcoes/VerificaURL.js",
            "codigo": "// Verificar em EComLinkCrypto() se params.codigo existe e query.id, query.w!, query.y! estão presentes"
        },
        "formulário não abre": {
            "causa": "Flags do formulário não estão sendo setadas ou flow não configurado",
            "solucao": "Verificar mostraFormulario_padrao, mostraChave e lpFlow no mainStore",
            "arquivo": "src/stores/formularioStore.js",
            "codigo": "// Verificar: formularioStore.mostraFormulario_padrao, mainStore.formularioAtivoId"
        },
        "mensagem hardcoded": {
            "causa": "Funções aplicarRegrasXXX usando mensagens fixas ao invés do lp_flow",
            "solucao": "Usar getMensagemDoFlow() que respeita hierarquia de mensagens",
            "arquivo": "src/Funcoes/verificaPresencaFn.js",
            "codigo": "const msg = getMensagemDoFlow('confirmado', pax, mainStore);"
        },
        "acompanhante não adiciona": {
            "causa": "Cota zerada ou colaboradorStore não configurado",
            "solucao": "Verificar cota no pax.generico1 e colaboradorStore.cota",
            "arquivo": "src/stores/colaboradorStore.js",
            "codigo": "// Verificar: colaboradorStore.cota > colaboradorStore.colaboradores.length"
        },
        "submit duplo": {
            "causa": "Flag submitting não sendo respeitada",
            "solucao": "Garantir que submitting=true bloqueia watchers e botões",
            "arquivo": "src/stores/formularioStore.js",
            "codigo": "if (this.submitting) return; this.submitting = true; try { ... } finally { this.submitting = false; }"
        },
        "placeholder não mescla": {
            "causa": "Formato incorreto do placeholder ou contexto incompleto",
            "solucao": "Usar formato <<tabela_campo>> e garantir contexto tem a tabela",
            "arquivo": "src/components/ModulosDinamicos/utils/mescla-condicional.js",
            "codigo": "// Formato: <<pax_nome>>, <<evento_nome_evento>>, <<pax_status_presenca>>"
        },
        "drawer mobile não abre": {
            "causa": "windowWidth não reativo ou listener de resize ausente",
            "solucao": "Usar ref para windowWidth e adicionar listener no onMounted",
            "arquivo": "src/components/ModulosDinamicos/ModuloCabecalho.vue",
            "codigo": "const windowWidth = ref(window.innerWidth); onMounted(() => window.addEventListener('resize', updateWidth));"
        }
    }

    # Buscar erro mais similar
    descricao_lower = descricao_erro.lower()
    melhor_match = None
    melhor_score = 0

    for erro_key, erro_info in erros_conhecidos.items():
        # Calcular similaridade simples
        palavras_chave = erro_key.split()
        score = sum(1 for p in palavras_chave if p in descricao_lower)
        if score > melhor_score:
            melhor_score = score
            melhor_match = (erro_key, erro_info)

    if melhor_match:
        erro_key, erro_info = melhor_match
        return json.dumps({
            "erro_identificado": erro_key,
            "causa": erro_info["causa"],
            "solucao": erro_info["solucao"],
            "arquivo": erro_info["arquivo"],
            "codigo": erro_info["codigo"]
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "erro_identificado": None,
        "sugestao": "Erro não encontrado na base de conhecimento. Tente descrever com mais detalhes ou consulte a documentação em /docs/",
        "documentacao": [
            "docs/novoflow_rsvp/01-ARQUITETURA.md",
            "docs/MANUAL-MENSAGENS-STATUS-ADMIN.md",
            "docs/admin/step-by-step-runtime-flow-rsvp.md"
        ]
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def search_docs(query: str, limite: int = 5) -> str:
    """
    Busca na documentação do projeto.

    Args:
        query: Termo de busca
        limite: Número máximo de resultados (default: 5)

    Returns:
        JSON com documentos relevantes e trechos
    """
    # Base de documentação indexada
    docs_index = {
        "link cripto": {
            "arquivo": ".claude/CLAUDE.md",
            "secao": "Sistema de Link Criptografado",
            "relevancia": "Documentação completa do fluxo de link criptografado"
        },
        "cadastro igo": {
            "arquivo": ".claude/CLAUDE.md",
            "secao": "Redirecionamento para Hotsite IGO",
            "relevancia": "Como funciona o redirecionamento para sistema IGO"
        },
        "flow rsvp": {
            "arquivo": "docs/novoflow_rsvp/01-ARQUITETURA.md",
            "secao": "Arquitetura do Flow RSVP v2.0",
            "relevancia": "FlowResolver, ActionExecutor, ConditionEvaluator"
        },
        "campos pax": {
            "arquivo": "docs/novoflow_rsvp/02-CAMPOS-PAX.md",
            "secao": "Campos do PAX",
            "relevancia": "138+ campos disponíveis no banco de dados"
        },
        "uploads": {
            "arquivo": "docs/novoflow_rsvp/03-UPLOADS.md",
            "secao": "Sistema de Uploads",
            "relevancia": "UploadProcessor, UploadRules"
        },
        "formularios v5": {
            "arquivo": "docs/admin/FORMULARIOS-V5-CONDICIONAIS-VALIDACOES-LAYOUT.md",
            "secao": "Formulários Dinâmicos V5",
            "relevancia": "Campos condicionais, validações, layout"
        },
        "runtime rules": {
            "arquivo": "docs/admin/step-by-step-runtime-flow-rsvp.md",
            "secao": "Runtime Rules",
            "relevancia": "Configuração de runtime_rules no admin"
        },
        "mensagens status": {
            "arquivo": "docs/MANUAL-MENSAGENS-STATUS-ADMIN.md",
            "secao": "Mensagens Dinâmicas por Status",
            "relevancia": "Hierarquia de mensagens, presets, dialog_config"
        },
        "presets dinamicos": {
            "arquivo": ".claude/CLAUDE.md",
            "secao": "Sistema de Presets Dinâmicos",
            "relevancia": "Customização de textos, ícones, estilos via admin"
        },
        "mescla condicional": {
            "arquivo": "docs/step-by-step/MESCLA_CONDICIONAL_IMPLEMENTACAO.md",
            "secao": "Mescla Condicional",
            "relevancia": "Placeholders, condicionais {{#if}}, operadores"
        },
        "status rules": {
            "arquivo": "docs/novoflow_rsvp/01-ARQUITETURA.md",
            "secao": "Status Rules",
            "relevancia": "Regras baseadas em status_presenca"
        },
        "chave unica": {
            "arquivo": ".claude/CLAUDE.md",
            "secao": "Runtime Rules - Chave",
            "relevancia": "pesquisa_cpf_email vs chave_unica"
        },
        "acompanhante": {
            "arquivo": "src/stores/colaboradorStore.js",
            "secao": "Colaborador Store",
            "relevancia": "Gerenciamento de acompanhantes"
        },
        "submit": {
            "arquivo": "docs/SUBMIT-ROBUSTO.md",
            "secao": "Submit Robusto",
            "relevancia": "Proteção anti-conflito, submitting flag"
        },
        "drawer mobile": {
            "arquivo": ".claude/CLAUDE.md",
            "secao": "Bugs Corrigidos",
            "relevancia": "Correção do drawer mobile com Teleport"
        }
    }

    query_lower = query.lower()
    resultados = []

    for termo, doc in docs_index.items():
        # Calcular relevância
        palavras_query = query_lower.split()
        palavras_termo = termo.split()

        # Match exato ou parcial
        score = 0
        for pq in palavras_query:
            for pt in palavras_termo:
                if pq in pt or pt in pq:
                    score += 1

        if score > 0:
            resultados.append({
                "termo": termo,
                "score": score,
                **doc
            })

    # Ordenar por score e limitar
    resultados.sort(key=lambda x: x["score"], reverse=True)
    resultados = resultados[:limite]

    if not resultados:
        return json.dumps({
            "query": query,
            "resultados": [],
            "sugestao": "Tente buscar por: link cripto, flow rsvp, formularios v5, mensagens status, runtime rules"
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "query": query,
        "total": len(resultados),
        "resultados": resultados
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_store_structure(nome_store: str) -> str:
    """
    Retorna estrutura completa de uma store Pinia.

    Args:
        nome_store: Nome da store (mainStore, formularioStore, colaboradorStore, eventoStore, adminStore)

    Returns:
        JSON com state, actions, getters e conexões
    """
    store = STORES.get(nome_store)

    if not store:
        stores_disponiveis = list(STORES.keys())
        return json.dumps({
            "erro": f"Store '{nome_store}' não encontrada",
            "stores_disponiveis": stores_disponiveis
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "store": nome_store,
        "arquivo": store.get("arquivo", ""),
        "responsabilidade": store.get("responsabilidade", ""),
        "state": store.get("state", {}),
        "actions": store.get("actions", []),
        "getters": store.get("getters", []),
        "conexoes": store.get("conexoes", []),
        "persistencia": store.get("persistencia", None)
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def trace_data_flow(campo: str) -> str:
    """
    Rastreia o fluxo de dados de um campo específico.

    Args:
        campo: Nome do campo (ex: status_presenca, pax.nome, cadastroIgo)

    Returns:
        JSON com origem, transformações e destino do campo
    """
    # Mapa de fluxo de dados
    data_flows = {
        "status_presenca": {
            "origem": "API /verificapresenca → pax.status_presenca",
            "transformacoes": [
                "VerifcaStatusPadrao() avalia valor",
                "StatusRules.parse() normaliza",
                "FlowResolver.evaluateStatusRules() decide ação"
            ],
            "destino": [
                "formularioStore.pax.status_presenca",
                "Exibido em FormularioSistemaPadrao (card de status)"
            ],
            "valores_possiveis": ["PENDENTE", "CONFIRMADO", "INSCRITO", "EM ANALISE", "CANCELADO", "PRAZO VENCIDO"]
        },
        "cadastroIgo": {
            "origem": "verificaUrl() quando detecta link cripto + evento_cadastroIgo=true",
            "transformacoes": [
                "ativarFormularios('CADASTRO_IGO')",
                "mainStore.cadastroIgo = true"
            ],
            "destino": [
                "ModuloSobre.vue (botão de redirecionamento)",
                "ModuloCabecalho.vue (botão inteligente)",
                "LandingPageDinamica.vue (botão fallback)"
            ],
            "valores_possiveis": [true, false]
        },
        "lpFlow": {
            "origem": "API /puxaevento → campo lp_flow (JSON string)",
            "transformacoes": [
                "mainStore.puxaDadosAppData() parseia JSON",
                "mainStore.lpFlow = JSON.parse()"
            ],
            "destino": [
                "FlowResolver.resolve() lê rules",
                "ActionExecutor.execute() executa ações",
                "getMensagemDoFlow() busca mensagens"
            ],
            "estrutura": {
                "status_rules": "Array de regras por status",
                "runtime_rules": "Array de regras de runtime",
                "mapa_formularios": "Mapeamento de form_id",
                "condicoes_fluxo": "Condições globais",
                "mensagens": "Mensagens por status"
            }
        },
        "pax": {
            "origem": "API /verificapresenca ou /gravapaxevento",
            "transformacoes": [
                "fnVerificaPresenca() popula formularioStore.pax",
                "submit() atualiza com resposta da API"
            ],
            "destino": [
                "formularioStore.pax (state central)",
                "FormularioSistemaPadrao (campos do formulário)",
                "VerifcaStatusPadrao (processamento de regras)"
            ],
            "campos_principais": [
                "id_pax_evento", "nome", "email", "cpf", "celular",
                "status_presenca", "generico1-10", "upload1-5"
            ]
        },
        "universalMsg": {
            "origem": "Qualquer lugar que chame mostraUniversalMsg()",
            "transformacoes": [
                "mainStore.mostraUniversalMsg(dados) faz merge",
                "dialog_config pode customizar visual"
            ],
            "destino": [
                "DialogoUniversal.vue renderiza",
                "Overlay modal sobre a página"
            ],
            "campos": {
                "titulo": "Título do dialog",
                "texto": "Corpo principal",
                "texto2": "Texto secundário",
                "dialog": "boolean - mostra/esconde",
                "dialog_config": "Customização visual"
            }
        }
    }

    # Buscar campo (com ou sem prefixo)
    campo_limpo = campo.replace("pax.", "").replace("mainStore.", "").replace("formularioStore.", "")

    fluxo = data_flows.get(campo_limpo) or data_flows.get(campo)

    if not fluxo:
        campos_disponiveis = list(data_flows.keys())
        return json.dumps({
            "erro": f"Campo '{campo}' não mapeado",
            "campos_disponiveis": campos_disponiveis
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "campo": campo,
        **fluxo
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def check_compatibility(versao_flow: str) -> str:
    """
    Verifica compatibilidade de versão do flow RSVP.

    Args:
        versao_flow: Versão do flow (ex: "1.0", "2.0", "2.1")

    Returns:
        JSON com compatibilidade, features e migração necessária
    """
    versoes = {
        "1.0": {
            "compativel": True,
            "status": "DEPRECADO",
            "features": [
                "Status rules básico",
                "Mapa de formulários simples"
            ],
            "limitacoes": [
                "Sem runtime_rules",
                "Sem condições complexas",
                "Sem pesquisa_cpf_email"
            ],
            "migracao": "Recomendado migrar para 2.0 adicionando runtime_rules"
        },
        "2.0": {
            "compativel": True,
            "status": "ATUAL",
            "features": [
                "FlowResolver modular",
                "ActionExecutor com múltiplas ações",
                "ConditionEvaluator com 10+ operadores",
                "runtime_rules (OPTIN, chave, email)",
                "status_rules com match complexo",
                "condicoes_fluxo globais",
                "pesquisa_cpf_email (3 tentativas)",
                "chave_unica",
                "acao_submit com transicoes/comparadores"
            ],
            "limitacoes": [],
            "migracao": None
        },
        "2.1": {
            "compativel": False,
            "status": "FUTURO",
            "features": [
                "Tudo do 2.0",
                "Workflow multi-step",
                "Branching condicional",
                "Rollback de ações"
            ],
            "limitacoes": ["Não implementado ainda"],
            "migracao": "Aguardar implementação"
        }
    }

    versao_info = versoes.get(versao_flow)

    if not versao_info:
        return json.dumps({
            "erro": f"Versão '{versao_flow}' desconhecida",
            "versoes_disponiveis": list(versoes.keys())
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "versao": versao_flow,
        **versao_info
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
