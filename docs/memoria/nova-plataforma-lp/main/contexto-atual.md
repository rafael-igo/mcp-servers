# Contexto Atual - nova-plataforma-lp/main

**Última atualização:** 2026-01-27 (20:48)

---


## Mensagens de Status - Manual Admin

**Status:** completed

# MANUAL: Personalização de Mensagens de Status - SigaEventos Admin

## Visão Geral

O sistema de Landing Page permite personalizar as mensagens exibidas para cada status de presença do participante (CONFIRMADO, CANCELADO, EM ANÁLISE, PENDENTE, etc.).

---

## ONDE CONFIGURAR

### Local no Admin Editor
```
lp_conteudo → [idioma ativo] → modulos → tipo: "formulario" → conteudo → titulo_card → presets
```

### Estrutura JSON Completa
```json
{
  "idioma": "pt-br",
  "ativo": true,
  "modulos": [
    {
      "tipo": "formulario",
      "ativo": true,
      "conteudo": {
        "titulo_card": {
          "presets": {
            "confirmado": {
              "texto": "Sua presença está confirmada! Obrigado, <<pax_nome>>!"
            },
            "cancelado": {
              "texto": "Participação cancelada. Em caso de dúvidas, entre em contato."
            },
            "analisar_inscricao": {
              "texto": "Sua inscrição está em análise. Aguarde nosso retorno."
            },
            "entrada_pendente": {
              "texto": "Confirme sua presença no evento!"
            }
          }
        }
      }
    }
  ]
}
```

---

## PRESETS DISPONÍVEIS

| Preset | Status que Ativa | Descrição |
|--------|------------------|-----------|
| `confirmado` | CONFIRMADO, CONFIRMADO CONVIDADO | PAX confirmou presença |
| `cancelado` | CANCELADO | PAX cancelou participação |
| `analisar_inscricao` | EM ANÁLISE | Cadastro aguardando aprovação |
| `entrada_pendente` | PENDENTE, PENDENTE CONVIDADO | PAX ainda não confirmou |

---

## PLACEHOLDERS DISPONÍVEIS

### Sintaxe: `<<tabela_campo>>`

| Placeholder | Descrição | Exemplo |
|-------------|-----------|---------|
| `<<pax_nome>>` | Nome do participante | "Rafael" |
| `<<pax_email>>` | E-mail do participante | "rafael@email.com" |
| `<<pax_status_presenca>>` | Status atual | "CONFIRMADO" |
| `<<evento_nome>>` | Nome do evento | "Convenção 2026" |
| `<<evento_data_evento>>` | Data do evento | "15/03/2026" |

### Com Valor Padrão: `<<tabela_campo|default:valor>>`

```
Olá <<pax_nome|default:Convidado>>, seja bem-vindo!
```
→ Se `pax.nome` estiver vazio, exibe "Convidado"

---

## CONDICIONAIS (Avançado)

### Sintaxe Mustache: `{{#if condição}}texto{{/if}}`

#### Operadores Suportados:
- `==` - Igual (case-insensitive)
- `!=` - Diferente
- `~=` - Contém
- `!~` - Não contém
- `!!` - Existe/não vazio
- `??` - Não existe/vazio
- `>`, `<`, `>=`, `<=` - Comparação numérica

#### Exemplos:

**Texto condicional por status:**
```
{{#if pax.status_presenca ~= "CONFIRMADO"}}
Sua presença está confirmada!
{{else}}
Aguardando confirmação.
{{/if}}
```

**Verificar se campo existe:**
```
{{#if pax.empresa !!}}
Empresa: <<pax_empresa>>
{{/if}}
```

**Combinando condições (AND/OR):**
```
{{#if pax.status_presenca == "CONFIRMADO" AND pax.acompanhante == "SIM"}}
Você pode adicionar acompanhantes!
{{/if}}
```

---

## COMPORTAMENTO DO DIALOG

### Status CONFIRMADO
- **Dialog Universal:** NÃO aparece (desabilitado automaticamente)
- **Card Inline:** APARECE com a mensagem personalizada
- **Motivo:** Evitar pop-up para quem já está confirmado

### Outros Status (CANCELADO, EM ANÁLISE, PRAZO VENCIDO)
- **Dialog Universal:** APARECE como pop-up
- **Card Inline:** Também disponível

---

## EXEMPLOS COMPLETOS

### 1. Mensagem de Confirmado Simples
```json
{
  "confirmado": {
    "texto": "Olá <<pax_nome>>, sua presença no <<evento_nome>> está confirmada!"
  }
}
```

### 2. Mensagem de Confirmado com Condicionais
```json
{
  "confirmado": {
    "texto": "{{#if pax.status_presenca ~= \"CONFIRMADO\"}}Presença confirmada! {{#if pax.acompanhante == \"SIM\"}}Você pode adicionar até <<pax_generico1>> acompanhante(s).{{/if}}{{/if}}"
  }
}
```

### 3. Mensagem de Cancelado
```json
{
  "cancelado": {
    "texto": "Olá <<pax_nome|default:Participante>>, sua participação foi cancelada. Entre em contato conosco para mais informações."
  }
}
```

### 4. Mensagem de Análise
```json
{
  "analisar_inscricao": {
    "texto": "Sua inscrição está em análise. Você receberá um e-mail em <<pax_email>> com a confirmação."
  }
}
```

---

## HIERARQUIA DE PRIORIDADE

Se a mensagem não for encontrada em um nível, o sistema busca no próximo:

1. **lp_conteudo.modulo_formulario.titulo_card.presets** (Admin Editor) ← MAIOR PRIORIDADE
2. **mainStore.runtime.mensagens_status** (Configuração runtime)
3. **campo_tipo_5.controles.mensagens_status** (Controles do evento)
4. **Fallback hardcoded** (Mensagens padrão do sistema)

---

## ARQUIVOS RELACIONADOS (Desenvolvedores)

- `src/Funcoes/verificaPresencaFn.js` - Função `getMensagemDoFlow()`
- `src/Formularios/FormularioSistemaPadrao.vue` - Computed `mensagemStatusFinal`
- `src/components/ModulosDinamicos/utils/mescla-condicional.js` - Função de mescla
- `src/flow/core/ActionExecutor.js` - Exibição de mensagens
- `src/flow/core/FlowResolver.js` - Decisão de ações por status

## Mensagens de Status - Controle Dialog

**Status:** completed

# Controle de Dialog (Pop-up) nas Mensagens de Status

## Propriedade `dialog`

Cada preset pode controlar se o dialog (pop-up) será exibido através da propriedade `dialog`.

### Valores
- `true` (PADRÃO) - Exibe o dialog pop-up ao carregar a página
- `false` - NÃO exibe dialog, apenas o card inline no formulário

### Exemplo de Configuração

```json
{
  "confirmado": {
    "texto": "Sua presença está confirmada!",
    "dialog": false
  },
  "cancelado": {
    "texto": "Participação cancelada.",
    "dialog": true
  },
  "analisar_inscricao": {
    "texto": "Inscrição em análise.",
    "dialog": true
  }
}
```

### Comportamento Padrão por Status

| Status | Dialog Padrão | Motivo |
|--------|---------------|--------|
| CONFIRMADO | false | Evitar interrupção para quem já está confirmado |
| CANCELADO | true | Informar claramente sobre o cancelamento |
| EM ANÁLISE | true | Informar que está aguardando aprovação |
| PRAZO VENCIDO | true | Informar que as inscrições encerraram |
| PENDENTE | false | Deixar o usuário preencher o formulário |

### Onde é Processado

1. **FlowResolver** cria a ação de mensagem
2. **VerifcaStatusPadrao** verifica se status é CONFIRMADO e seta `action.dialog = false`
3. **ActionExecutor.exibirMensagem()** respeita a flag `dialog` da ação
4. Se `dialog: false`, apenas seta as propriedades no `universalMsg` sem abrir o pop-up

### Arquivos Relacionados

- `src/Funcoes/verificaPresencaFn.js` - Linha ~292: seta `action.dialog = false` para CONFIRMADO
- `src/flow/core/ActionExecutor.js` - `exibirMensagem()` respeita flag dialog
- `src/stores/mainStore.pinia.js` - `universalMsg.dialog` controla visibilidade

## Mensagens de Status - Controle Dialog

**Status:** completed

Implementado sistema completo de controle de dialog para mensagens de status:

## Arquivos Modificados
- src/flow/core/ActionExecutor.js - Respeita flag dialog da ação
- src/Funcoes/verificaPresencaFn.js - Define dialog=false para CONFIRMADO
- docs/MANUAL-MENSAGENS-STATUS-ADMIN.md - Manual completo para admin

## Comportamento por Status
| Status | Dialog Padrão | Motivo |
|--------|---------------|--------|
| CONFIRMADO | false | Evitar interrupção para quem já está confirmado |
| CANCELADO | true | Informar claramente sobre o cancelamento |
| EM ANÁLISE | true | Informar que está aguardando aprovação |
| PRAZO VENCIDO | true | Informar que as inscrições encerraram |
| PENDENTE | false | Deixar o usuário preencher o formulário |

## Configuração no Admin (lp_conteudo)
```json
{
  "confirmado": {
    "texto": "Sua presença está confirmada!",
    "dialog": false
  }
}
```

## Funcionalidades
- Placeholders: <<pax_nome>>, <<evento_nome|default:valor>>
- Condicionais: {{#if pax.status == "CONFIRMADO"}}...{{/if}}
- Operadores: ==, !=, ~=, !~, !!, ??, >, <, >=, <=, AND, OR

## Dialog Universal Dinâmico

**Status:** completed

## Implementação Completa - Dialog Universal Dinâmico

### Arquivos Modificados

1. **src/components/dialogs/DialogoUniversal.vue**
   - Reescrito com Composition API
   - Suporte completo a `dialog_config` com todas as configurações visuais
   - Configurações: card, header, content, texto2, imagem, mostra_conteudo, botao_fechar
   - Responsivo (detecta mobile vs desktop)
   - Imagem posicionada entre texto e texto2

2. **src/Funcoes/verificaPresencaFn.js**
   - `getMensagemDoFlow()` retorna `dialogmsg` e `dialog_config`
   - Defaults por status: CONFIRMADO=false, CANCELADO=true, etc.
   - `aplicarRegrasConfirmado()` usa dialogmsg do preset
   - `aplicarRegrasCancelado()` usa dialogmsg do preset
   - `aplicarRegrasPrazoVencido()` usa dialogmsg do preset

3. **src/stores/mainStore.pinia.js**
   - `universalMsg` agora tem `dialog_config` e `imagem`
   - `hideUniversalMsg()` reseta os novos campos

4. **docs/MANUAL-MENSAGENS-STATUS-ADMIN.md**
   - Documentação completa da estrutura `dialog_config`
   - Todas as propriedades documentadas com tipos e valores padrão
   - Exemplos práticos de uso

### Estrutura do dialog_config

```json
{
  "dialogmsg": true,
  "dialog_config": {
    "max_width": "600px",
    "max_width_mobile": "95%",
    "persistent": true,
    "card": { elevation, rounded, color, min_width, min_height, max_width, border, shadow },
    "header": { background_color, color, font_size, font_weight, min_height, text_align, padding },
    "content": { text_align, font_size, padding, color, line_height },
    "texto2": { text_align, font_size, padding, color, line_height },
    "imagem": { ativo, url, width, max_width, height, max_height, border_radius, margin, object_fit, aspect_ratio, cover, contain, justify, alt },
    "mostra_conteudo": { cabecalho, texto, texto2, qrcode, imagem, botao_fechar },
    "botao_fechar": { texto, color, variant, size, actions_class }
  }
}
```

### Comportamento Padrão por Status

| Status | dialogmsg | Motivo |
|--------|-----------|--------|
| CONFIRMADO | false | Evitar interrupção |
| CANCELADO | true | Informar cancelamento |
| EM ANÁLISE | true | Informar aguardando |
| PRAZO VENCIDO | true | Informar encerrado |
| PENDENTE | false | Deixar preencher |

## Sistema de Presets Dinamicos v2.0

**Status:** completed

Implementado sistema completo de presets dinamicos com: 1) Criado preset-helpers.js com funcoes auxiliares (getPresetComFallback, renderizarCampoPreset, renderizarIconePreset, detectarTipoPreset). 2) Refatorado FormularioSistemaPadrao.vue para usar presets com estilos dinamicos (titulo_card, subtitulo_card, icone, mensagem_final). 3) Template usa component dinamico para tags (h2, h3, p, etc). 4) Atualizado MANUAL-MENSAGENS-STATUS-ADMIN.md com documentacao completa. 5) Verificado que DialogoUniversal.vue implementa todas as configs do manual (dialog_config, header, content, imagem, botao_fechar, etc). 6) Sistema de Card Inline agora totalmente configuravel via Admin Editor.
