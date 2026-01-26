# Vuetify UI/UX Assistant MCP

MCP consultor de design web para Vuetify 3, fornecendo sugestões de componentes, padrões de layout, esquemas de cores e guias de acessibilidade.

## 🎯 Funcionalidades

- ✅ Sugestão de componentes Vuetify para casos de uso específicos
- ✅ Informações detalhadas de componentes
- ✅ Padrões de layout prontos (dashboard, form_page, list_page, etc)
- ✅ Esquemas de cores profissionais
- ✅ Guias de acessibilidade (WCAG)
- ✅ Guias de espaçamento, tipografia e breakpoints
- ✅ Análise de código Vue/Vuetify
- ✅ Dicas de design contextual

## 🔧 Ferramentas Disponíveis

### 1. `suggest_component`

Sugere componentes Vuetify para um caso de uso específico.

**Parâmetros:**
- `use_case` (str): Descrição do caso de uso

**Casos de uso suportados:**
- formulário, form
- tabela, table
- lista, list
- card
- navegação, navigation, menu
- modal, dialog
- alerta, notification
- loading, carregamento
- upload
- imagem, image
- busca, search
- filtro, filter
- status
- perfil, profile
- dashboard
- login
- configuração, settings

**Exemplo:**
```python
mcp__vuetify-uiux__suggest_component(
    use_case="formulário de cadastro de usuário"
)
```

### 2. `component_info`

Retorna informações detalhadas de um componente Vuetify.

**Parâmetros:**
- `component` (str): Nome do componente (ex: v-data-table, v-btn)

**Retorno:**
- description: Descrição do componente
- props: Propriedades principais
- best_practices: Boas práticas de uso
- example: Código de exemplo

**Exemplo:**
```python
mcp__vuetify-uiux__component_info(
    component="v-data-table"
)
```

### 3. `layout_pattern`

Retorna um padrão de layout completo com código.

**Parâmetros:**
- `pattern` (str): Nome do padrão

**Padrões disponíveis:**
- **dashboard**: Layout para painéis administrativos com sidebar e cards
- **form_page**: Página de formulário (criar/editar)
- **list_page**: Página de listagem (tabela/grid)
- **detail_page**: Página de detalhes/visualização
- **login_page**: Página de login/autenticação
- **empty_state**: Estado vazio (sem dados)
- **error_page**: Página de erro (404, 500)

**Exemplo:**
```python
mcp__vuetify-uiux__layout_pattern(
    pattern="dashboard"
)
```

### 4. `color_scheme`

Retorna esquemas de cores profissionais.

**Parâmetros:**
- `scheme` (str, opcional): Nome do esquema

**Esquemas disponíveis:**
- **professional_blue**: Sistemas corporativos, dashboards
- **modern_purple**: Startups, apps criativos
- **dark_mode**: Apps noturnos, ferramentas dev
- **nature_green**: Apps de saúde, sustentabilidade
- **warm_orange**: E-commerce, food delivery
- **minimal_gray**: Portfolios, blogs, apps minimalistas

**Exemplo:**
```python
# Listar todos os esquemas
mcp__vuetify-uiux__color_scheme()

# Obter esquema específico
mcp__vuetify-uiux__color_scheme(scheme="professional_blue")
```

### 5. `accessibility_guide`

Retorna guia de acessibilidade WCAG.

**Parâmetros:**
- `topic` (str, opcional): Tópico específico

**Tópicos disponíveis:**
- **color_contrast**: Regras de contraste de cores
- **keyboard_navigation**: Navegação por teclado
- **screen_readers**: Suporte a leitores de tela
- **forms**: Formulários acessíveis
- **motion**: Movimento e animação

**Exemplo:**
```python
# Guia completo
mcp__vuetify-uiux__accessibility_guide()

# Tópico específico
mcp__vuetify-uiux__accessibility_guide(topic="forms")
```

### 6. `spacing_guide`

Retorna guia completo de espaçamento do Vuetify.

**Retorno:**
- Escala de espaçamento (0-16, baseada em 4px)
- Classes de margin (ma-*, mt-*, etc.)
- Classes de padding (pa-*, pt-*, etc.)
- Boas práticas de espaçamento

**Exemplo:**
```python
mcp__vuetify-uiux__spacing_guide()
```

### 7. `typography_guide`

Retorna guia de tipografia do Vuetify.

**Retorno:**
- Classes de texto (text-h1 a text-overline)
- Tamanhos e pesos
- Boas práticas de uso

**Exemplo:**
```python
mcp__vuetify-uiux__typography_guide()
```

### 8. `breakpoints_guide`

Retorna guia de breakpoints responsivos.

**Retorno:**
- Valores dos breakpoints (xs, sm, md, lg, xl, xxl)
- Classes de display (d-none, d-sm-none, etc.)
- Boas práticas de responsividade

**Exemplo:**
```python
mcp__vuetify-uiux__breakpoints_guide()
```

### 9. `review_code`

Analisa código Vue/Vuetify e sugere melhorias.

**Parâmetros:**
- `code` (str): Código Vue para analisar

**Verificações realizadas:**
- v-for sem :key
- Campos sem label/placeholder
- Botões icon sem aria-label
- Colunas sem breakpoints responsivos
- Dialogs sem max-width
- Elementos clicáveis não acessíveis
- Uso de position absolute/fixed
- Uso de !important
- Inline styles

**Exemplo:**
```python
code = '''
<template>
  <v-row>
    <v-col>
      <v-text-field />
    </v-col>
  </v-row>
</template>
'''

mcp__vuetify-uiux__review_code(code=code)
```

### 10. `design_tips`

Retorna dicas de design para um contexto.

**Parâmetros:**
- `context` (str): Contexto para as dicas

**Contextos suportados:**
- **mobile**: Dicas para design mobile
- **form/formulário**: Dicas para formulários
- **dashboard**: Dicas para dashboards
- **table/tabela**: Dicas para tabelas
- **color/cor**: Dicas sobre cores

**Exemplo:**
```python
mcp__vuetify-uiux__design_tips(context="mobile")
```

## 💡 Exemplos de Uso

### Cenário 1: Criar formulário de cadastro

```python
# 1. Sugerir componentes
mcp__vuetify-uiux__suggest_component(
    use_case="formulário de cadastro de usuário"
)

# 2. Obter padrão de layout
mcp__vuetify-uiux__layout_pattern(pattern="form_page")

# 3. Escolher esquema de cores
mcp__vuetify-uiux__color_scheme(scheme="professional_blue")

# 4. Verificar acessibilidade
mcp__vuetify-uiux__accessibility_guide(topic="forms")
```

### Cenário 2: Montar dashboard administrativo

```python
# 1. Obter layout completo
mcp__vuetify-uiux__layout_pattern(pattern="dashboard")

# 2. Dicas de design
mcp__vuetify-uiux__design_tips(context="dashboard")

# 3. Guia de espaçamento
mcp__vuetify-uiux__spacing_guide()
```

### Cenário 3: Revisar código existente

```python
# Analisar código Vue/Vuetify
code = open('MyComponent.vue').read()
mcp__vuetify-uiux__review_code(code=code)
```

## 📦 Instalação

### Dependências

```bash
cd vuetify-uiux
pip install --user -r requirements.txt
```

### Registro no Claude Code

Já está registrado em:
- `.mcp.json` (local)
- `docs/mcp.json` (remoto via SSH)
- `agente-orchestrator/server.py` (lista de MCPs)
- `.claude/settings.local.json` (permissões)

## 🚀 Como Usar

### Direto via Python (Windows)

```bash
python c:/GIT-RAFAEL/mcp-servers/vuetify-uiux/server.py
```

### Via Claude Code

As ferramentas estarão disponíveis automaticamente com prefixo `mcp__vuetify-uiux__`.

### Via Orchestrator

```python
mcp__agente-orchestrator__list_agents()
# Verá vuetify-uiux na lista de MCPs
```

## 🎨 Componentes Documentados

### Layout
- v-container, v-row, v-col

### Navegação
- v-app-bar, v-navigation-drawer, v-bottom-navigation, v-tabs

### Inputs
- v-text-field, v-select, v-autocomplete, v-checkbox, v-switch, v-radio-group, v-slider, v-file-input, v-textarea

### Botões
- v-btn, v-btn-group, v-fab

### Dados
- v-card, v-data-table, v-list, v-chip, v-avatar, v-badge, v-tooltip

### Feedback
- v-dialog, v-snackbar, v-alert, v-progress-linear, v-progress-circular, v-skeleton-loader

### Mídia
- v-img, v-carousel

### Utilitários
- v-divider, v-spacer, v-expand-transition, v-expansion-panels

## 🔍 Boas Práticas Integradas

1. **UX/UI**: Hierarquia visual, espaçamento, consistência
2. **Acessibilidade**: WCAG, teclado, leitores de tela
3. **Responsividade**: Mobile-first, breakpoints
4. **Performance**: Lazy loading, skeleton loaders
5. **Vuetify 3**: Uso correto de props e slots

## ⚠️ Notas Importantes

### Sem Docker
Este MCP roda **sem Docker**, diretamente no Windows via Python. Ideal para ambientes onde Docker não é necessário.

### Integração com GPT
Pode ser usado em conjunto com o `igo-openai-gateway` para análises de código aprofundadas.

### Agente Especialista
Use como consultor durante desenvolvimento de interfaces com Vuetify 3.

## 🔄 Atualização

Para atualizar o código:
```bash
# Editar server.py
# Nenhum rebuild necessário (sem Docker)
# Basta reiniciar o processo Python
```

## 📝 Logs

Como roda localmente, os logs aparecem no terminal onde o Python foi executado.

---

**Criado em:** 2026-01-26
**Última atualização:** 2026-01-26
**Status:** ✅ Produção
**Docker:** ❌ Não necessário (roda nativamente no Windows)
