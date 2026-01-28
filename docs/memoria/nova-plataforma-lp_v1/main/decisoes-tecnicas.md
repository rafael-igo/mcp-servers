# Decisões Técnicas - ADRs - nova-plataforma-lp_v1/main

Registro de decisões arquiteturais importantes.

---

## Corrigir fluxo /chave para abrir formComponenteChave antes de fallback optin

**Data:** 2026-01-26
**Projeto/Branch:** nova-plataforma-lp_v1/main

### Contexto
Quando usuario acessava /chave com flow ativo, o codigo setava runtime.funcao_chave='nao_encontrada' ANTES de mostrar o componente de chave, fazendo o sistema abrir optin diretamente sem dar chance ao usuario de tentar buscar por celular/email/CPF.

### Alternativas Consideradas
1. Setar funcao_chave='nao_encontrada' imediatamente (comportamento antigo - bug). 2. Setar apenas modo_entrada='chave' e deixar FlowResolver decidir abrir pesquisa_cpf_email primeiro.

### Decisão
Opcao 2 - Setar apenas modo_entrada='chave' e adicionar regra especial no FlowResolver para abrir pesquisa_cpf_email

### Razão
Permite que usuario tente buscar primeiro, e somente apos falhar (quando prosseguirSemCadastro seta funcao_chave='nao_encontrada') o sistema abre optin. Isso segue a documentacao de runtime_rules que especifica que funcao_chave='nao_encontrada' deve ser setado APOS a pesquisa falhar.

---

## Fluxo correto para /chave com runtime_rules

**Data:** 2026-01-26
**Projeto/Branch:** nova-plataforma-lp_v1/main

### Contexto
O fluxo de /chave deve respeitar as runtime_rules configuradas no admin. Os componentes de chave (pesquisa_cpf_email e chave_unica) sao acionados quando existe uma runtime_rule para funcao_chave='nao_encontrada'. Cada componente tem seu comportamento: pesquisa_cpf_email faz 3 tentativas e abre form_id se falhar; chave_unica faz busca direta e executa acao configurada.

### Alternativas Consideradas
1. Regra hardcoded no FlowResolver que ignora admin (incorreto). 2. Verificar runtime_rules do admin e usar acao configurada (correto). 3. Se nao existir runtime_rule configurada, mostrar mensagem de erro amigavel.

### Decisão
Opcao 2 e 3 - Respeitar runtime_rules do admin e mostrar erro amigavel se nao configurado

### Razão
O admin configura no lp_flow.runtime_rules qual componente usar (pesquisa_cpf_email ou chave_unica) e qual formulario abrir em caso de fallback (acao.form_id). Se evento_chave=false, nao mostra nada. Se evento_chave=true mas runtime_rule nao existe, mostra mensagem de erro amigavel.

---

## Estratégia de exibição de mensagens de status (Dialog vs Card)

**Data:** 2026-01-26
**Projeto/Branch:** nova-plataforma-lp_v1/main

### Contexto
O sistema atualmente exibe mensagens de status em dois lugares quando o PAX está confirmado: 1) Dialog universal (popup) com título, texto e texto2; 2) Card de status final (inline) com título, texto, ícone e cor. Isso causa redundância visual. O admin já tem presets configuráveis em lp_conteudo.modulo_formulario.conteudo.titulo_card.presets

### Alternativas Consideradas
1. Manter ambos (dialog + card) com mensagens diferentes; 2. Manter apenas o card (mais limpo); 3. Manter apenas o dialog (mais visível); 4. Dialog para confirmação inicial + card para visualização posterior

### Decisão
Opção 4 - Dialog mostra mensagem resumida na confirmação inicial, Card mostra mensagem detalhada disponível para consulta posterior

### Razão
Melhor UX: usuário recebe feedback imediato (dialog) e pode consultar informações depois (card). Evita redundância ao diferenciar o conteúdo de cada um.

---
