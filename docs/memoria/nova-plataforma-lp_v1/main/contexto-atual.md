# Contexto Atual - nova-plataforma-lp_v1/main

**Última atualização:** 2026-01-26 (16:00)

---


## Runtime Rules - Chave

**Status:** completed

## Fluxo /chave com runtime_rules

### Pré-requisitos
1. `evento_chave = true` nos controles (evento.campo_tipo_5.controles)
2. Parâmetro `/chave` na URL
3. `runtime_rule` configurada no admin para `funcao_chave = 'nao_encontrada'`

### Fluxo
1. Usuario acessa `/chave`
2. VerificaURL verifica `evento_chave` nos controles
   - Se `false`: não mostra nada (nem mensagem, nem card)
3. Se `true`, seta `runtime.funcao_chave = 'nao_encontrada'`
4. FlowResolver verifica `runtime_rules` do admin:
   - Se existe rule com `chave='funcao_chave'` e `valor='nao_encontrada'`:
     - `pesquisa_cpf_email`: abre formComponenteChave (3 tentativas, fallback para `acao.form_id`)
     - `chave_unica`: abre FormularioChaveUnica (busca direta, executa `acao` configurada)
   - Se NÃO existe rule: mostra mensagem de erro amigável

### Configuração Admin (runtime_rules)
```json
// Para pesquisa_cpf_email
{
  "chave": "funcao_chave",
  "valor": "nao_encontrada",
  "acao": {
    "tipo": "pesquisa_cpf_email",
    "form_id": "form_xxx"  // formulario que abre APOS 3 tentativas falharem
  }
}

// Para chave_unica
{
  "chave": "funcao_chave",
  "valor": "nao_encontrada",
  "acao": {
    "tipo": "chave_unica",
    "form_id": "form_xxx",  // formulario que abre se encontrar
    "tipo_chave": "email",
    "mensagem_nao_encontrado": {...}  // se não encontrar
  }
}
```

### Arquivos envolvidos
- VerificaURL.js: detecta /chave e seta runtime
- FlowResolver.js: verifica runtime_rules e decide ação
- ActionExecutor.js: executa ação (abre componente)
- formComponenteChave.vue: componente de pesquisa (3 tentativas)
- FormularioChaveUnica.vue: componente de chave única

## Runtime Rules - Chave (CORRIGIDO)

**Status:** completed

## Fluxo /chave com runtime_rules - CORRIGIDO

### Pré-requisitos
1. `evento_chave = true` nos controles
2. Parâmetro `/chave` na URL
3. `runtime_rule` configurada para `funcao_chave = 'nao_encontrada'`

### Componentes de Chave

#### pesquisa_cpf_email (formComponenteChave.vue)
- Faz 3 tentativas de busca (celular, email, CPF)
- Se NÃO ENCONTRAR → abre formulário `acao.form_id` (via `pesquisaCpfEmailConfig.form_id_fallback`)
- Config salva em `mainStore.pesquisaCpfEmailConfig`

#### chave_unica (FormularioChaveUnica.vue)
- Faz busca direta pelo tipo configurado
- Se ENCONTRAR → abre formulário `acao.form_id` (via `chaveUnicaConfig.form_id_encontrado`)
- Se NÃO ENCONTRAR → mostra `acao.mensagem_nao_encontrado`
- Config salva em `mainStore.chaveUnicaConfig`

### Arquivos Alterados

1. **ActionExecutor.js**
   - `abrirPesquisa`: Salva `pesquisaCpfEmailConfig.form_id_fallback`
   - `abrirChaveUnica`: Renomeado para `form_id_encontrado`

2. **formComponenteChave.vue**
   - `prosseguirSemCadastro`: Usa `form_id_fallback` direto (sem reprocessar flow)

3. **ModuloFormulario.vue**
   - `handleChaveUnicaSubmit`: Usa `form_id_encontrado` quando PAX encontrado

4. **mainStore.pinia.js**
   - Adicionado `pesquisaCpfEmailConfig`
   - Renomeado `form_id_fallback` → `form_id_encontrado` em chaveUnicaConfig

### Configuração Admin (runtime_rules)

```json
// pesquisa_cpf_email
{
  "chave": "funcao_chave",
  "valor": "nao_encontrada",
  "acao": {
    "tipo": "pesquisa_cpf_email",
    "form_id": "form_xxx"  // abre quando NÃO encontrar
  }
}

// chave_unica
{
  "chave": "funcao_chave",
  "valor": "nao_encontrada",
  "acao": {
    "tipo": "chave_unica",
    "form_id": "form_xxx",  // abre quando ENCONTRAR
    "tipo_chave": "email",
    "mensagem_nao_encontrado": {...}  // mostra quando NÃO encontrar
  }
}
```

## acao_submit - Transicoes e Comparadores

**Status:** completed

## Implementação de acao_submit

### Funcionalidade
Quando `pesquisa_cpf_email` não encontra o PAX, abre um formulário (form_id) que ao ser submetido:
1. Valida `comparadores` antes do submit
2. Aplica `transicoes` ao payload (ex: status_presenca = "EM ANALISE")
3. Envia para API

### Arquivos Alterados

1. **ActionExecutor.js** - `abrirPesquisa`
   - Adicionado `acao_submit` na config do mainStore

2. **formularioStore.js** - `submit`
   - Processa `acao_submit.comparadores` (validação)
   - Processa `acao_submit.transicoes` (sobrescreve campos do pax)
   - Limpa `pesquisaCpfEmailConfig` após sucesso

### Estrutura JSON (Admin)
```json
{
  "runtime_rules": [{
    "chave": "funcao_chave",
    "valor": "nao_encontrada",
    "acao": {
      "tipo": "pesquisa_cpf_email",
      "form_id": "optin",
      "acao_submit": {
        "herdar_regra_status": "Regra Em Analise",
        "transicoes": [
          { "tabela": "pax", "campo": "status_presenca", "valor": "EM ANALISE" }
        ],
        "comparadores": [
          { "tabela": "pax", "campo": "status_presenca", "operador": "contem", "valores": ["PENDENTE"] }
        ]
      }
    }
  }]
}
```

### Operadores de Comparadores
- `igual` - Valor exato
- `contem` - Contém substring (case insensitive)
- `em` - Valor está na lista
- `vazio` - Campo vazio/null
- `preenchido` - Campo tem valor

## Dialog Universal Messages

**Status:** completed

Corrigido problema onde mensagens do dialog universal (confirmado, cancelado, prazo_vencido) usavam valores hardcoded ao invés das configurações do lp_flow.

PROBLEMA IDENTIFICADO:
- As funções aplicarRegrasConfirmado(), aplicarRegrasCancelado(), aplicarRegrasPrazoVencido() em verificaPresencaFn.js tinham mensagens hardcoded
- O lp_flow suporta configuração via flow.mensagens.{confirmado,cancelado,pendente,analise,prazo_vencido}
- Mas o código nunca foi implementado para usar essas configurações

SOLUÇÃO IMPLEMENTADA:
1. Criada função helper getMensagemDoFlow(tipo, pax, mainStore) que:
   - Verifica se existe configuração em mainStore.lpFlow.mensagens[tipo]
   - Se existir string simples, usa como texto
   - Se existir objeto, usa {titulo, texto, texto2, classe, qrcode}
   - Se não existir, usa fallback hardcoded

2. Atualizado aplicarRegrasConfirmado() para usar getMensagemDoFlow('confirmado')
3. Atualizado aplicarRegrasCancelado() para usar getMensagemDoFlow('cancelado')
4. Atualizado aplicarRegrasPrazoVencido() para usar getMensagemDoFlow('prazo_vencido')
5. Exportada função getMensagemDoFlow para uso externo

ESTRUTURA DE CONFIGURAÇÃO NO LP_FLOW:
{
  "mensagens": {
    "confirmado": { "titulo": "...", "texto": "...", "texto2": "...", "classe": "...", "qrcode": "" },
    "cancelado": { "titulo": "...", "texto": "...", "classe": "cabecalho_universal_alerta" },
    "pendente": "Texto simples também funciona",
    "analise": { "titulo": "...", "texto": "..." },
    "prazo_vencido": { "titulo": "...", "texto": "..." }
  }
}
