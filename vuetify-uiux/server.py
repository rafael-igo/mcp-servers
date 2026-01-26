#!/usr/bin/env python3
"""
Vuetify UI/UX Assistant MCP
============================
MCP consultor de design web com Vuetify 3.
Fornece sugestões de componentes, padrões de layout, cores e acessibilidade.

Ferramentas:
- suggest_component: Sugere componentes para casos de uso
- component_info: Info detalhada de componentes
- layout_pattern: Padrões de layout completos
- color_scheme: Esquemas de cores profissionais
- accessibility_guide: Guia de acessibilidade
- spacing_guide: Guia de espaçamento
- typography_guide: Guia de tipografia
- breakpoints_guide: Guia de breakpoints
- review_code: Análise de código Vue/Vuetify
- design_tips: Dicas contextuais de design
"""

import json
import re
from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("vuetify-uiux")


# ==================== DADOS BASE ====================

COMPONENTS_DB = {
    "v-text-field": {
        "description": "Campo de texto para entrada de dados",
        "props": ["label", "placeholder", "type", "rules", "hint", "persistent-hint"],
        "best_practices": [
            "Sempre use label para acessibilidade",
            "Use rules para validação",
            "Use hint para ajudar o usuário",
            "Use :error-messages para feedback de erro"
        ],
        "example": '''<v-text-field
  label="Nome completo"
  placeholder="Digite seu nome"
  :rules="[rules.required]"
  hint="Digite seu nome completo"
  persistent-hint
/>'''
    },
    "v-select": {
        "description": "Campo de seleção com dropdown",
        "props": ["items", "item-title", "item-value", "label", "multiple", "chips"],
        "best_practices": [
            "Use item-title e item-value para controle preciso",
            "Use chips com multiple para melhor UX",
            "Considere v-autocomplete para listas grandes"
        ],
        "example": '''<v-select
  label="Selecione uma opção"
  :items="['Opção 1', 'Opção 2']"
  item-title="label"
  item-value="id"
/>'''
    },
    "v-data-table": {
        "description": "Tabela de dados com ordenação, paginação e busca",
        "props": ["headers", "items", "search", "items-per-page", "loading"],
        "best_practices": [
            "Use :headers com key, title e sortable",
            "Implemente paginação server-side para grandes volumes",
            "Use skeleton-loader durante carregamento",
            "Adicione filtros com v-text-field + search"
        ],
        "example": '''<v-data-table
  :headers="headers"
  :items="items"
  :search="search"
  :loading="loading"
  items-per-page="10"
>
  <template v-slot:top>
    <v-text-field
      v-model="search"
      label="Buscar"
      prepend-inner-icon="mdi-magnify"
    />
  </template>
</v-data-table>'''
    },
    "v-btn": {
        "description": "Botão com múltiplas variações",
        "props": ["color", "variant", "size", "icon", "loading", "disabled"],
        "best_practices": [
            "Use variant='elevated' para ações primárias",
            "Use variant='text' para ações secundárias",
            "Sempre adicione aria-label em botões icon",
            "Use :loading para operações assíncronas"
        ],
        "example": '''<v-btn
  color="primary"
  variant="elevated"
  :loading="loading"
  @click="salvar"
>
  Salvar
</v-btn>'''
    },
    "v-card": {
        "description": "Container para agrupar conteúdo relacionado",
        "props": ["title", "subtitle", "elevation", "variant"],
        "best_practices": [
            "Use v-card-title para títulos",
            "Use v-card-text para conteúdo",
            "Use v-card-actions para botões",
            "Evite elevação muito alta (max 8)"
        ],
        "example": '''<v-card>
  <v-card-title>Título</v-card-title>
  <v-card-subtitle>Subtítulo</v-card-subtitle>
  <v-card-text>
    Conteúdo do card
  </v-card-text>
  <v-card-actions>
    <v-btn>Cancelar</v-btn>
    <v-btn color="primary">Salvar</v-btn>
  </v-card-actions>
</v-card>'''
    },
    "v-dialog": {
        "description": "Modal dialog para conteúdo sobreposto",
        "props": ["v-model", "max-width", "persistent", "scrollable"],
        "best_practices": [
            "Sempre defina max-width (recomendado: 500-800px)",
            "Use persistent para modals importantes",
            "Use scrollable para conteúdo longo",
            "Adicione botão de fechar"
        ],
        "example": '''<v-dialog
  v-model="dialog"
  max-width="600"
  persistent
>
  <v-card>
    <v-card-title>Título</v-card-title>
    <v-card-text>
      Conteúdo
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn @click="dialog = false">Fechar</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>'''
    }
}

USE_CASES = {
    "formulario": ["v-form", "v-text-field", "v-select", "v-checkbox", "v-btn", "v-card"],
    "tabela": ["v-data-table", "v-text-field", "v-btn", "v-chip", "v-icon"],
    "lista": ["v-list", "v-list-item", "v-list-item-title", "v-divider", "v-icon"],
    "card": ["v-card", "v-card-title", "v-card-text", "v-card-actions", "v-btn"],
    "navegacao": ["v-app-bar", "v-navigation-drawer", "v-list", "v-tabs"],
    "modal": ["v-dialog", "v-card", "v-card-title", "v-card-actions", "v-btn"],
    "alerta": ["v-snackbar", "v-alert", "v-icon"],
    "loading": ["v-progress-linear", "v-progress-circular", "v-skeleton-loader"],
    "upload": ["v-file-input", "v-btn", "v-progress-linear", "v-list"],
    "dashboard": ["v-container", "v-row", "v-col", "v-card", "v-data-table", "v-chart"]
}

COLOR_SCHEMES = {
    "professional_blue": {
        "name": "Profissional Azul",
        "description": "Esquema clássico corporativo",
        "colors": {
            "primary": "#1976D2",
            "secondary": "#424242",
            "accent": "#82B1FF",
            "error": "#FF5252",
            "warning": "#FB8C00",
            "info": "#2196F3",
            "success": "#4CAF50",
            "background": "#FAFAFA",
            "surface": "#FFFFFF"
        },
        "usage": "Sistemas corporativos, dashboards, aplicações financeiras"
    },
    "modern_purple": {
        "name": "Moderno Roxo",
        "description": "Esquema criativo e moderno",
        "colors": {
            "primary": "#9C27B0",
            "secondary": "#E1BEE7",
            "accent": "#FF4081",
            "error": "#F44336",
            "warning": "#FF9800",
            "info": "#00BCD4",
            "success": "#8BC34A",
            "background": "#F5F5F5",
            "surface": "#FFFFFF"
        },
        "usage": "Startups, apps criativos, plataformas de mídia"
    },
    "dark_mode": {
        "name": "Modo Escuro",
        "description": "Tema escuro para apps noturnos",
        "colors": {
            "primary": "#BB86FC",
            "secondary": "#03DAC6",
            "accent": "#CF6679",
            "error": "#CF6679",
            "warning": "#FFC107",
            "info": "#2196F3",
            "success": "#4CAF50",
            "background": "#121212",
            "surface": "#1E1E1E"
        },
        "usage": "Apps noturnos, ferramentas dev, plataformas de streaming"
    }
}


# ==================== FERRAMENTAS ====================

@mcp.tool()
def suggest_component(use_case: str) -> str:
    """
    Sugere componentes Vuetify para um caso de uso específico.

    Args:
        use_case: Descrição do caso de uso (formulário, tabela, modal, etc)

    Returns:
        JSON com componentes sugeridos e exemplos

    Exemplo:
        suggest_component(use_case="formulário de cadastro")
    """
    try:
        # Normalizar use case
        use_case_lower = use_case.lower()

        # Buscar matches
        matched_components = []
        for key, components in USE_CASES.items():
            if key in use_case_lower or use_case_lower in key:
                matched_components = components
                break

        if not matched_components:
            # Fallback para busca parcial
            for key, components in USE_CASES.items():
                if any(word in use_case_lower for word in key.split()):
                    matched_components = components
                    break

        if not matched_components:
            matched_components = USE_CASES.get("card", [])

        # Montar resposta
        suggestions = []
        for comp_name in matched_components[:6]:  # Limitar a 6 componentes
            comp_info = COMPONENTS_DB.get(comp_name, {})
            if comp_info:
                suggestions.append({
                    "component": comp_name,
                    "description": comp_info.get("description", ""),
                    "example": comp_info.get("example", "")
                })
            else:
                suggestions.append({
                    "component": comp_name,
                    "description": f"Componente {comp_name}",
                    "example": f"<{comp_name} />"
                })

        return json.dumps({
            "success": True,
            "use_case": use_case,
            "suggestions": suggestions,
            "count": len(suggestions)
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def component_info(component: str) -> str:
    """
    Retorna informações detalhadas de um componente Vuetify.

    Args:
        component: Nome do componente (ex: v-data-table)

    Returns:
        JSON com description, props, best_practices, example
    """
    try:
        comp_info = COMPONENTS_DB.get(component)

        if not comp_info:
            return json.dumps({
                "success": False,
                "error": f"Componente '{component}' não encontrado na base"
            }, ensure_ascii=False, indent=2)

        return json.dumps({
            "success": True,
            "component": component,
            **comp_info
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def layout_pattern(pattern: str) -> str:
    """
    Retorna um padrão de layout completo com código.

    Args:
        pattern: Nome do padrão (dashboard, form_page, list_page, etc)

    Returns:
        JSON com description, structure, best_practices, example
    """
    try:
        patterns = {
            "dashboard": {
                "description": "Layout para painel administrativo",
                "structure": ["v-app", "v-navigation-drawer", "v-app-bar", "v-main", "v-container"],
                "best_practices": [
                    "Use v-navigation-drawer para menu lateral",
                    "Cards com métricas no topo",
                    "Gráficos e tabelas abaixo",
                    "Responsivo com v-row e v-col"
                ],
                "example": '''<template>
  <v-app>
    <v-navigation-drawer permanent>
      <v-list>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.to"
        >
          <template v-slot:prepend>
            <v-icon>{{ item.icon }}</v-icon>
          </template>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar color="primary">
      <v-app-bar-title>Dashboard</v-app-bar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <v-row>
          <v-col cols="12" md="3">
            <v-card>
              <v-card-text>
                <div class="text-h4">1,234</div>
                <div class="text-caption">Total de Vendas</div>
              </v-card-text>
            </v-card>
          </v-col>
          <!-- Mais cards de métricas -->
        </v-row>

        <v-row>
          <v-col cols="12">
            <v-card>
              <v-card-title>Gráfico de Vendas</v-card-title>
              <v-card-text>
                <!-- Gráfico aqui -->
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>'''
            },
            "form_page": {
                "description": "Página de formulário (criar/editar)",
                "structure": ["v-container", "v-card", "v-form", "v-row", "v-col"],
                "best_practices": [
                    "Agrupe campos relacionados",
                    "Use v-row/v-col para layout responsivo",
                    "Valide com :rules",
                    "Botões sempre no final"
                ],
                "example": '''<template>
  <v-container>
    <v-card max-width="800" class="mx-auto">
      <v-card-title>Cadastro de Usuário</v-card-title>

      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.nome"
                label="Nome completo"
                :rules="[rules.required]"
              />
            </v-col>

            <v-col cols="12" md="6">
              <v-text-field
                v-model="form.email"
                label="E-mail"
                type="email"
                :rules="[rules.required, rules.email]"
              />
            </v-col>

            <v-col cols="12">
              <v-select
                v-model="form.tipo"
                label="Tipo de usuário"
                :items="['Admin', 'Usuário', 'Visitante']"
                :rules="[rules.required]"
              />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn @click="cancelar">Cancelar</v-btn>
        <v-btn
          color="primary"
          :disabled="!valid"
          :loading="loading"
          @click="salvar"
        >
          Salvar
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>'''
            }
        }

        pattern_data = patterns.get(pattern)

        if not pattern_data:
            return json.dumps({
                "success": False,
                "error": f"Padrão '{pattern}' não encontrado. Disponíveis: {list(patterns.keys())}"
            }, ensure_ascii=False, indent=2)

        return json.dumps({
            "success": True,
            "pattern": pattern,
            **pattern_data
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def color_scheme(scheme: Optional[str] = None) -> str:
    """
    Retorna esquemas de cores profissionais.

    Args:
        scheme: Nome do esquema (opcional, None retorna todos)

    Returns:
        JSON com esquema(s) de cores
    """
    try:
        if scheme:
            scheme_data = COLOR_SCHEMES.get(scheme)
            if not scheme_data:
                return json.dumps({
                    "success": False,
                    "error": f"Esquema '{scheme}' não encontrado. Disponíveis: {list(COLOR_SCHEMES.keys())}"
                }, ensure_ascii=False, indent=2)

            return json.dumps({
                "success": True,
                "scheme": scheme,
                **scheme_data
            }, ensure_ascii=False, indent=2)
        else:
            # Retornar todos
            return json.dumps({
                "success": True,
                "schemes": COLOR_SCHEMES,
                "count": len(COLOR_SCHEMES)
            }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def accessibility_guide(topic: Optional[str] = None) -> str:
    """
    Retorna guia de acessibilidade.

    Args:
        topic: Tópico específico (opcional)

    Returns:
        JSON com guia de acessibilidade
    """
    try:
        guides = {
            "color_contrast": {
                "title": "Contraste de Cores",
                "guidelines": [
                    "Textos normais: mínimo 4.5:1",
                    "Textos grandes (18pt+): mínimo 3:1",
                    "Elementos interativos: mínimo 3:1",
                    "Use ferramentas para testar contraste"
                ],
                "tools": ["WebAIM Contrast Checker", "Color Oracle"]
            },
            "keyboard_navigation": {
                "title": "Navegação por Teclado",
                "guidelines": [
                    "Todos os elementos interativos devem ser acessíveis via Tab",
                    "Use :tabindex corretamente",
                    "Implemente @keydown.enter e @keydown.space",
                    "Indique foco visualmente"
                ],
                "examples": [
                    "<v-btn tabindex=\"0\" @keydown.enter=\"action\">",
                    "Adicione outline visível no :focus"
                ]
            },
            "screen_readers": {
                "title": "Leitores de Tela",
                "guidelines": [
                    "Use aria-label em botões icon",
                    "Use aria-describedby para hints",
                    "Use role quando apropriado",
                    "Teste com NVDA ou JAWS"
                ],
                "examples": [
                    "<v-btn icon aria-label=\"Fechar\">",
                    "<v-text-field aria-describedby=\"hint-1\">"
                ]
            }
        }

        if topic:
            guide = guides.get(topic)
            if not guide:
                return json.dumps({
                    "success": False,
                    "error": f"Tópico '{topic}' não encontrado. Disponíveis: {list(guides.keys())}"
                }, ensure_ascii=False, indent=2)

            return json.dumps({
                "success": True,
                "topic": topic,
                **guide
            }, ensure_ascii=False, indent=2)
        else:
            return json.dumps({
                "success": True,
                "guides": guides,
                "count": len(guides)
            }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def spacing_guide() -> str:
    """
    Retorna guia completo de espaçamento do Vuetify.

    Returns:
        JSON com guia de espaçamento
    """
    try:
        return json.dumps({
            "success": True,
            "scale": "Baseada em 4px (0-16)",
            "classes": {
                "margin": {
                    "all": "ma-{0-16}",
                    "top": "mt-{0-16}",
                    "bottom": "mb-{0-16}",
                    "left": "ml-{0-16}",
                    "right": "mr-{0-16}",
                    "horizontal": "mx-{0-16}",
                    "vertical": "my-{0-16}"
                },
                "padding": {
                    "all": "pa-{0-16}",
                    "top": "pt-{0-16}",
                    "bottom": "pb-{0-16}",
                    "left": "pl-{0-16}",
                    "right": "pr-{0-16}",
                    "horizontal": "px-{0-16}",
                    "vertical": "py-{0-16}"
                }
            },
            "best_practices": [
                "Use 4 (16px) para espaçamento padrão entre elementos",
                "Use 2 (8px) para espaçamento compacto",
                "Use 8 (32px) para seções distintas",
                "Mantenha consistência no projeto"
            ],
            "examples": [
                "<v-card class=\"ma-4 pa-4\">",
                "<v-row class=\"mt-8\">",
                "<v-col class=\"px-2\">"
            ]
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def typography_guide() -> str:
    """
    Retorna guia de tipografia do Vuetify.

    Returns:
        JSON com guia de tipografia
    """
    try:
        return json.dumps({
            "success": True,
            "classes": {
                "text-h1": "96px - Títulos principais",
                "text-h2": "60px - Subtítulos principais",
                "text-h3": "48px - Seções importantes",
                "text-h4": "34px - Cards, dialogs",
                "text-h5": "24px - List headers",
                "text-h6": "20px - Small headers",
                "text-subtitle-1": "16px - Subtítulos (weight 500)",
                "text-subtitle-2": "14px - Subtítulos menores",
                "text-body-1": "16px - Corpo de texto padrão",
                "text-body-2": "14px - Corpo de texto secundário",
                "text-button": "14px - Texto de botões (uppercase)",
                "text-caption": "12px - Captions, hints",
                "text-overline": "10px - Overlines (uppercase)"
            },
            "best_practices": [
                "Use text-h4 para títulos de cards",
                "Use text-body-1 para texto principal",
                "Use text-caption para hints e metadata",
                "Limite hierarquia a 3-4 níveis"
            ],
            "examples": [
                "<div class=\"text-h4 mb-2\">Título</div>",
                "<div class=\"text-body-1\">Texto</div>",
                "<div class=\"text-caption grey--text\">12/01/2026</div>"
            ]
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def breakpoints_guide() -> str:
    """
    Retorna guia de breakpoints responsivos.

    Returns:
        JSON com guia de breakpoints
    """
    try:
        return json.dumps({
            "success": True,
            "breakpoints": {
                "xs": "0-599px (Mobile portrait)",
                "sm": "600-959px (Mobile landscape, tablet portrait)",
                "md": "960-1279px (Tablet landscape)",
                "lg": "1280-1919px (Desktop)",
                "xl": "1920-2559px (Large desktop)",
                "xxl": "2560px+ (4K)"
            },
            "display_classes": {
                "hidden": "d-none - Esconde em todos",
                "xs_only": "d-sm-none - Esconde a partir de sm",
                "sm_and_up": "d-none d-sm-flex - Mostra a partir de sm",
                "md_and_down": "d-lg-none - Esconde a partir de lg"
            },
            "grid_system": {
                "description": "Sistema de 12 colunas",
                "example": "<v-col cols=\"12\" sm=\"6\" md=\"4\" lg=\"3\">"
            },
            "best_practices": [
                "Pense mobile-first",
                "Use cols=\"12\" para mobile (1 coluna)",
                "Use md=\"6\" para tablet (2 colunas)",
                "Use lg=\"4\" para desktop (3 colunas)",
                "Teste em todos os tamanhos"
            ]
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def review_code(code: str) -> str:
    """
    Analisa código Vue/Vuetify e sugere melhorias.

    Args:
        code: Código Vue para analisar

    Returns:
        JSON com issues encontrados e sugestões
    """
    try:
        issues = []

        # Verificar v-for sem :key
        if "v-for" in code and ":key" not in code:
            issues.append({
                "severity": "error",
                "issue": "v-for sem :key",
                "suggestion": "Adicione :key=\"item.id\" em loops para performance"
            })

        # Verificar campos sem label
        if re.search(r"<v-text-field[^>]*>", code):
            if "label=" not in code:
                issues.append({
                    "severity": "warning",
                    "issue": "v-text-field sem label",
                    "suggestion": "Adicione label para acessibilidade"
                })

        # Verificar botões icon sem aria-label
        if re.search(r"<v-btn[^>]*icon[^>]*>", code):
            if "aria-label" not in code:
                issues.append({
                    "severity": "warning",
                    "issue": "Botão icon sem aria-label",
                    "suggestion": "Adicione aria-label=\"descrição\" para acessibilidade"
                })

        # Verificar dialog sem max-width
        if "<v-dialog" in code and "max-width" not in code:
            issues.append({
                "severity": "warning",
                "issue": "v-dialog sem max-width",
                "suggestion": "Adicione max-width=\"600\" para melhor UX"
            })

        # Verificar uso de !important
        if "!important" in code:
            issues.append({
                "severity": "info",
                "issue": "Uso de !important",
                "suggestion": "Evite !important, use especificidade CSS correta"
            })

        return json.dumps({
            "success": True,
            "issues_found": len(issues),
            "issues": issues,
            "passed": len(issues) == 0
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def design_tips(context: str) -> str:
    """
    Retorna dicas de design para um contexto.

    Args:
        context: Contexto para as dicas (mobile, form, dashboard, table, color)

    Returns:
        JSON com dicas contextuais
    """
    try:
        tips_db = {
            "mobile": [
                "Áreas clicáveis mínimas: 48x48px",
                "Use bottom-navigation para navegação principal",
                "Evite hover states (não funciona em touch)",
                "Teste com polegares - elementos importantes devem estar acessíveis",
                "Use v-bottom-sheet para ações contextuais"
            ],
            "formulario": [
                "Agrupe campos relacionados",
                "Use apenas 1 coluna em mobile",
                "Valide em tempo real com feedback claro",
                "Desabilite submit até formulário válido",
                "Use autocomplete nativo do navegador"
            ],
            "dashboard": [
                "Métricas importantes no topo",
                "Use skeleton-loaders durante carregamento",
                "Limite cards visíveis (máx 6-8)",
                "Gráficos antes de tabelas",
                "Ações rápidas sempre visíveis"
            ],
            "tabela": [
                "Máximo 7 colunas visíveis",
                "Use paginação server-side para +100 registros",
                "Ações na última coluna",
                "Busca e filtros sempre disponíveis",
                "Loading states claros"
            ],
            "cor": [
                "Use paleta de no máximo 3 cores principais",
                "Cinza para textos secundários",
                "Verde para sucesso, vermelho para erro, amarelo para aviso",
                "Teste contraste (mínimo 4.5:1)",
                "Use cores semânticas do Vuetify"
            ]
        }

        context_lower = context.lower()
        tips = None

        for key, tip_list in tips_db.items():
            if key in context_lower or context_lower in key:
                tips = tip_list
                break

        if not tips:
            return json.dumps({
                "success": False,
                "error": f"Contexto '{context}' não encontrado. Disponíveis: {list(tips_db.keys())}"
            }, ensure_ascii=False, indent=2)

        return json.dumps({
            "success": True,
            "context": context,
            "tips": tips,
            "count": len(tips)
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
