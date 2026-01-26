# MCP Vuetify UI/UX Assistant

## Visao Geral

O MCP Vuetify UI/UX Assistant e um servidor MCP que atua como um consultor de design web, fornecendo:

- Sugestoes de componentes Vuetify 3
- Padroes de layout prontos para uso
- Esquemas de cores profissionais
- Guias de acessibilidade
- Analise de codigo
- Dicas de design

---

## Instalacao

### 1. Configuracao

O servidor ja esta configurado no arquivo `.mcp.json`:

```json
{
  "mcpServers": {
    "vuetify-uiux": {
      "type": "stdio",
      "command": "python3",
      "args": [
        "/Users/rafamacpro/Projetos/NOVA-PLATAFORMA-GIT/sigaevento/mcp-uiux/server.py"
      ],
      "env": {}
    }
  }
}
```

### 2. Reiniciar Claude Code

Apos configurar, reinicie o Claude Code para carregar o MCP.

---

## Ferramentas Disponiveis

### suggest_component

Sugere componentes Vuetify para um caso de uso especifico.

**Parametros:**
| Nome | Tipo | Obrigatorio | Descricao |
|------|------|-------------|-----------|
| use_case | string | Sim | Descricao do caso de uso |

**Casos de uso suportados:**
- formulario / form
- tabela / table
- lista / list
- card
- navegacao / navigation / menu
- modal / dialog
- alerta / notification
- loading / carregamento
- upload
- imagem / image
- busca / search
- filtro / filter
- status
- perfil / profile
- dashboard
- login
- configuracao / settings

**Exemplo:**
```
"Preciso criar um formulario de cadastro de usuario"
-> Sugere: v-text-field, v-select, v-checkbox, v-btn, v-form
```

---

### component_info

Retorna informacoes detalhadas de um componente Vuetify.

**Parametros:**
| Nome | Tipo | Obrigatorio | Descricao |
|------|------|-------------|-----------|
| component | string | Sim | Nome do componente |

**Retorno:**
- description: Descricao do componente
- props: Propriedades principais
- best_practices: Boas praticas de uso
- example: Codigo de exemplo

**Exemplo:**
```
component: "v-data-table"
```

---

### layout_pattern

Retorna um padrao de layout completo com codigo.

**Parametros:**
| Nome | Tipo | Obrigatorio | Descricao |
|------|------|-------------|-----------|
| pattern | string | Sim | Nome do padrao |

**Padroes disponiveis:**
| Padrao | Descricao |
|--------|-----------|
| dashboard | Layout para paineis administrativos |
| form_page | Pagina de formulario (criar/editar) |
| list_page | Pagina de listagem (tabela/grid) |
| detail_page | Pagina de detalhes/visualizacao |
| login_page | Pagina de login/autenticacao |
| empty_state | Estado vazio (sem dados) |
| error_page | Pagina de erro (404, 500) |

**Retorno:**
- description: Descricao do padrao
- structure: Estrutura de componentes
- best_practices: Boas praticas
- example: Codigo Vue completo

---

### color_scheme

Retorna esquemas de cores profissionais.

**Parametros:**
| Nome | Tipo | Obrigatorio | Descricao |
|------|------|-------------|-----------|
| scheme | string | Nao | Nome do esquema (opcional) |

**Esquemas disponiveis:**
| Nome | Uso |
|------|-----|
| professional_blue | Sistemas corporativos, dashboards |
| modern_purple | Startups, apps criativos |
| dark_mode | Apps noturnos, ferramentas dev |
| nature_green | Apps de saude, sustentabilidade |
| warm_orange | E-commerce, food delivery |
| minimal_gray | Portfolios, blogs, apps minimalistas |

**Retorno por esquema:**
```json
{
  "name": "Profissional Azul",
  "description": "Esquema classico corporativo",
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
  "usage": "Sistemas corporativos, dashboards, aplicacoes financeiras"
}
```

---

### accessibility_guide

Retorna guia de acessibilidade.

**Parametros:**
| Nome | Tipo | Obrigatorio | Descricao |
|------|------|-------------|-----------|
| topic | string | Nao | Topico especifico (opcional) |

**Topicos disponiveis:**
- color_contrast: Regras de contraste de cores
- keyboard_navigation: Navegacao por teclado
- screen_readers: Suporte a leitores de tela
- forms: Formularios acessiveis
- motion: Movimento e animacao

---

### spacing_guide

Retorna guia completo de espacamento do Vuetify.

**Sem parametros**

**Retorno:**
- Escala de espacamento (0-16, baseada em 4px)
- Classes de margin (ma-*, mt-*, etc.)
- Classes de padding (pa-*, pt-*, etc.)
- Boas praticas de espacamento

---

### typography_guide

Retorna guia de tipografia do Vuetify.

**Sem parametros**

**Retorno:**
- Classes de texto (text-h1 a text-overline)
- Tamanhos e pesos
- Boas praticas de uso

---

### breakpoints_guide

Retorna guia de breakpoints responsivos.

**Sem parametros**

**Retorno:**
- Valores dos breakpoints (xs, sm, md, lg, xl, xxl)
- Classes de display (d-none, d-sm-none, etc.)
- Boas praticas de responsividade

---

### review_code

Analisa codigo Vue/Vuetify e sugere melhorias.

**Parametros:**
| Nome | Tipo | Obrigatorio | Descricao |
|------|------|-------------|-----------|
| code | string | Sim | Codigo Vue para analisar |

**Verificacoes realizadas:**
- v-for sem :key
- Campos sem label/placeholder
- Botoes icon sem aria-label
- Colunas sem breakpoints responsivos
- Dialogs sem max-width
- Elementos clicaveis nao acessiveis
- Uso de position absolute/fixed
- Uso de !important
- Inline styles

---

### design_tips

Retorna dicas de design para um contexto.

**Parametros:**
| Nome | Tipo | Obrigatorio | Descricao |
|------|------|-------------|-----------|
| context | string | Sim | Contexto para as dicas |

**Contextos suportados:**
- mobile: Dicas para design mobile
- form / formulario: Dicas para formularios
- dashboard: Dicas para dashboards
- table / tabela: Dicas para tabelas
- color / cor: Dicas sobre cores

---

## Exemplos de Uso

### 1. Criar um formulario de cadastro

```
Use suggest_component com "formulario de cadastro de usuario"
```

Retorno: Lista de componentes recomendados com exemplos.

### 2. Montar um dashboard

```
Use layout_pattern com "dashboard"
```

Retorno: Codigo completo de um layout de dashboard com sidebar, header e cards.

### 3. Escolher cores para o projeto

```
Use color_scheme sem parametro para ver todos
Use color_scheme com "professional_blue" para detalhes
```

### 4. Verificar acessibilidade do codigo

```
Use review_code com o codigo Vue do componente
```

### 5. Aprender sobre um componente

```
Use component_info com "v-data-table"
```

---

## Componentes Documentados

### Layout
- v-container
- v-row
- v-col

### Navegacao
- v-app-bar
- v-navigation-drawer
- v-bottom-navigation
- v-tabs

### Inputs
- v-text-field
- v-select
- v-autocomplete
- v-checkbox
- v-switch
- v-radio-group
- v-slider
- v-file-input
- v-textarea

### Botoes
- v-btn
- v-btn-group
- v-fab

### Dados
- v-card
- v-data-table
- v-list
- v-chip
- v-avatar
- v-badge
- v-tooltip

### Feedback
- v-dialog
- v-snackbar
- v-alert
- v-progress-linear
- v-progress-circular
- v-skeleton-loader

### Midia
- v-img
- v-carousel

### Utilitarios
- v-divider
- v-spacer
- v-expand-transition
- v-expansion-panels

---

## Boas Praticas Integradas

O MCP ja inclui boas praticas de:

1. **UX/UI**: Hierarquia visual, espacamento, consistencia
2. **Acessibilidade**: WCAG, teclado, leitores de tela
3. **Responsividade**: Mobile-first, breakpoints
4. **Performance**: Lazy loading, skeleton loaders
5. **Vuetify 3**: Uso correto de props e slots

---

## Arquivo Principal

`sigaevento/mcp-uiux/server.py`

---

## Troubleshooting

### MCP nao aparece no Claude Code

1. Verificar se o arquivo `.mcp.json` esta correto
2. Reiniciar o Claude Code completamente

### Erro de execucao

- Verificar se Python 3 esta instalado
- Verificar caminho do arquivo no .mcp.json

---

## Integracao com o Projeto

Este MCP e util para:

1. **Desenvolvimento de novas telas**: Obter padroes de layout prontos
2. **Revisao de codigo**: Verificar acessibilidade e boas praticas
3. **Design system**: Manter consistencia visual
4. **Onboarding**: Aprender Vuetify rapidamente

Ver tambem:
- [MCP-EXCEL-READER.md](./MCP-EXCEL-READER.md)
- [EXCEL-AEREO-MALHA-ABERTA.md](./EXCEL-AEREO-MALHA-ABERTA.md)
