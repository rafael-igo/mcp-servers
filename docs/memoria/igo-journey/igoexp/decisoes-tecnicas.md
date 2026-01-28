# Decisões Técnicas - ADRs - igo-journey/igoexp

Registro de decisões arquiteturais importantes.

---

## Redesign UI/UX - Cards de Ve\u00edculos e Fluxo de Check-in

**Data:** 2026-01-26
**Projeto/Branch:** igo-journey/igoexp

### Contexto
P\u00e1gina Transfer tinha cards com emojis infantis e cores confusas. P\u00e1gina Hospedagem tinha tooltips com baixo contraste e check-in sem confirma\u00e7\u00e3o, sem possibilidade de desfazer.

### Alternativas Consideradas
1) Manter emojis e cores atuais; 2) Usar \u00edcones MDI profissionais com design minimalista; 3) Migrar para tabela pura sem cards

### Decisão
Op\u00e7\u00e3o 2 - \u00cdcones MDI profissionais com design corporativo minimalista + sistema de confirma\u00e7\u00e3o e undo para a\u00e7\u00f5es cr\u00edticas

### Razão
Visual profissional adequado para sistema corporativo de log\u00edstica de eventos. Sistema de confirma\u00e7\u00e3o e undo previne erros acidentais e permite rastreabilidade com logs de auditoria.

---

## Desabilitar HTTPS no frontend para desenvolvimento

**Data:** 2026-01-26
**Projeto/Branch:** igo-journey/igoexp

### Contexto
Frontend rodava em HTTPS (porta 5179) mas API roda em HTTP (porta 3000), causando erro de Mixed Content que bloqueava login

### Alternativas Consideradas
1) Frontend HTTP + API HTTP, 2) Frontend HTTPS + API HTTPS, 3) Proxy reverso

### Decisão
Frontend HTTP + API HTTP

### Razão
Solução mais simples para ambiente de desenvolvimento. Em produção será necessário configurar ambos com HTTPS ou usar proxy reverso

---

## Status padrão de eventos alterado para 'active'

**Data:** 2026-01-26
**Projeto/Branch:** igo-journey/igoexp

### Contexto
Eventos criados não apareciam nas listagens (Hospedagem, Dashboard, Transfer) porque eram criados com status 'draft' por padrão, enquanto as views filtravam por status='active'.

### Alternativas Consideradas
1) Alterar o status padrão no controller para 'active'; 2) Remover o filtro de status nas views; 3) Adicionar UI para ativar eventos manualmente.

### Decisão
Alterar o status padrão no controller para 'active'

### Razão
A maioria dos eventos criados deve estar ativa imediatamente. O fluxo draft->active seria útil apenas para eventos em planejamento, que é um caso de uso minoritário. A solução mantém a simplicidade do fluxo atual.

---

## Implementação de Edição de Nome dos Grupos de Transfer

**Data:** 2026-01-26
**Projeto/Branch:** igo-journey/igoexp

### Contexto
O consultor precisava identificar grupos de transfer facilmente. O nome padrão gerado automaticamente "{IN|OUT} {Veículo} {dd/mm HH:mm}" ajuda, mas permitir edição dá flexibilidade para nomes como "Transfer VIP Jantar" ou "Grupo Palestrantes Manhã".

### Alternativas Consideradas
1. Apenas nome fixo gerado automaticamente - sem flexibilidade
2. Campo name obrigatório - mais trabalho para o consultor
3. Nome opcional com fallback para padrão gerado - escolhido

### Decisão
Nome opcional com fallback para padrão gerado automaticamente

### Razão
Permite flexibilidade quando necessário, mas não exige trabalho extra quando o nome padrão é suficiente. O campo name é NULL por padrão e o display_name é calculado em tempo de execução.

---
