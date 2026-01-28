# Contexto Atual - igo-journey/igoexp

**Última atualização:** 2026-01-26 (11:14)

---


## API Backend

**Status:** in_progress

API Node.js/Express com PostgreSQL. Migracoes: init.sql (base), 002_complete_schema.sql (novas tabelas), 003_ai_first_schema.sql (IA-first). Runner criado em migrations/run.js. Comandos: npm run migrate, npm run migrate:status.

## UI/UX - Sidebar

**Status:** completed

Corrigido bug do botão hamburger no header (agora aparece quando sidebar collapsed). Corrigido ícones do menu lateral que não renderizavam: mdi-car-estate → mdi-bus, mdi-bed → mdi-home-city

## Database - IA First

**Status:** completed

Migration 003_ai_first_schema.sql atualizada para tornar pgvector opcional. Tabelas AI criadas: ai_api_keys, ai_conversations, ai_suggestions, ai_analytics. Tabela ai_embeddings só é criada se pgvector estiver disponível.

## UI/UX - Sidebar v2

**Status:** completed

Correções aplicadas: 1) Botão expandir adicionado quando sidebar colapsada (seta para direita), 2) Logo trocado de SVG customizado para mdi-airplane (ícone de viagem), 3) Hospedagem: mdi-home-city → mdi-domain. Sidebar header agora muda para layout vertical quando colapsada.

## Sidebar Navigation

**Status:** completed

Implementado botão toggle FIXO na borda da sidebar. Usa v-icon mdi-chevron-left/right. Posição absoluta com right: -12px para ficar na borda. Ícone muda direção conforme estado collapsed. Logo clicável como backup. Estilos antigos removidos.

## AdminLayout Navigation

**Status:** completed

Corrigido AdminLayout.vue: 1) Logo mdi-pulse -> mdi-airplane, 2) Hospedagem mdi-hotel -> mdi-domain, 3) Botão toggle movido para FORA do v-navigation-drawer com position:fixed, transiciona left baseado no estado rail (242px expandido, 58px colapsado)

## Sidebar Toggle Button

**Status:** completed

Botão toggle movido para FOOTER do v-navigation-drawer (slot append). Sempre visível em desktop. Quando expandido mostra 'Recolher' + ícone chevron-left. Quando colapsado (rail) mostra apenas ícone chevron-right centralizado. Ícones: Logo=mdi-airplane, Hospedagem=mdi-domain, Transfer=mdi-bus

## AdminLayout Final

**Status:** completed

Revisão completa do AdminLayout.vue: 1) Dois botões separados para toggle (icon quando rail, texto quando expandido), 2) Memory leak corrigido (timeInterval limpo no onUnmounted), 3) aria-label em ambos botões, 4) CSS limpo sem overflow:visible, 5) Botões usam variant=tonal color=primary para melhor visibilidade

## AdminLayout Sidebar Toggle

**Status:** completed

Corrigido botão toggle da sidebar. Agora usa DOIS botões separados: 1) Quando rail=true (colapsado): v-btn icon com mdi-chevron-right 2) Quando rail=false (expandido): v-btn block com texto 'Recolher'. Ambos usam variant=tonal color=primary. CSS simplificado. Aria-labels adicionados.

## Sidebar Toggle Final

**Status:** completed

Botão toggle movido para o CABEÇALHO (v-list-item slot:append). Um único botão com ícone chevron-left/right. Footer agora só mostra versão quando expandido. Padrão correto do Vuetify Navigation Drawer.

## Database

**Status:** completed

{
  "resumo_banco": {
    "total_eventos": 2,
    "total_pax": 10,
    "total_usuarios": 7,
    "total_empresas": 2,
    "total_hospedagens": 0,
    "total_transfers": 0,
    "total_hoteis": 1
  },
  "credenciais": {
    "super_admin": "admin@igopulse.com / admin123",
    "usuarios_teste": "*/teste123"
  },
  "conexao_postgresql": "postgresql://igo_pulse_user:igo_pulse_secret_password@localhost:5432/igo_pulse",
  "docker_container": "igo-pulse-postgres",
  "migrations_executadas": ["001_init.sql", "002_complete_schema.sql", "003_ai_first_schema.sql"],
  "eventos": [
    {"nome": "Imuno teste", "status": "draft", "datas": "2026-01-28 a 2026-01-30"},
    {"nome": "Evento Teste I Go Journey", "status": "active", "cidade": "São Paulo", "datas": "2025-12-01 a 2025-12-05"}
  ]
}

## Queries Depuração

**Status:** completed

{
  "conexao": {
    "docker_exec": "docker exec igo-pulse-postgres psql -U igo_pulse_user -d igo_pulse -c \"QUERY\"",
    "connection_string": "postgresql://igo_pulse_user:igo_pulse_secret_password@localhost:5432/igo_pulse"
  },
  "queries_uteis": {
    "resumo_banco": "SELECT (SELECT COUNT(*) FROM events) as eventos, (SELECT COUNT(*) FROM guests) as pax, (SELECT COUNT(*) FROM users) as usuarios;",
    "listar_eventos": "SELECT id, name, status, start_date, end_date, city FROM events ORDER BY created_at DESC;",
    "buscar_evento_nome": "SELECT * FROM events WHERE name ILIKE '%TERMO%';",
    "buscar_pax_nome": "SELECT g.*, e.name as evento FROM guests g JOIN events e ON g.event_id = e.id WHERE g.name ILIKE '%TERMO%';",
    "listar_usuarios": "SELECT id, name, email, role FROM users;",
    "pax_por_evento": "SELECT g.name, g.email, g.category, g.rsvp_status FROM guests g WHERE g.event_id = 'UUID';",
    "listar_tabelas": "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';"
  },
  "total_tabelas": 31,
  "tabelas_principais": ["events", "guests", "users", "companies", "accommodations", "transfer_groups", "event_hotels", "ai_conversations", "ai_suggestions"]
}

## Transfer

**Status:** completed

Implementado funcionalidade Editar Passageiro (INS-0003): API transfer com controller/routes, EditPassengerModal com trocar veículo, marcar no-show, observações, editar contato. Frontend integrado com indicadores visuais de no-show.

## Transfer Logístico

**Status:** in_progress

Implementado dropdown dinâmico de seleção de eventos no TransferLogistics.vue. Alterações: 1) Import de eventsService e transferService; 2) Estado de seleção de evento (selectedEventId, events, eventsLoading); 3) Funções loadEvents(), onEventChange(), loadEventData(), loadTransferGroups(); 4) UI com v-select para seleção de evento e cards explicativos; 5) Dialog de upload quando já tem dados. O frontend agora pode selecionar eventos da API ou fazer upload de planilha.

## Sistema completo

**Status:** completed

Correção completa do problema de eventos não aparecendo nas listagens. Alterações realizadas:

1. **API (events.controller.js)**: Status padrão de eventos alterado de 'draft' para 'active'. O INSERT agora inclui o campo status com valor padrão 'active'.

2. **Banco de dados**: Eventos existentes atualizados de 'draft' para 'active'.

3. **TransferLogistics.vue**: Implementado dropdown dinâmico de seleção de eventos:
   - Import de eventsService e transferService
   - Seletor de eventos com v-select que carrega da API
   - Função loadEvents() que busca eventos ativos
   - Função onEventChange() e loadEventData() para carregar convidados do evento
   - UI melhorada com header, cards explicativos e dialog de upload

4. **EventsView.vue**: Status padrão alterado de 'draft' para 'active' no formulário de criação.

O sistema agora:
- Mostra eventos nas listagens (Hospedagem, Transfer, EventsView)
- Permite selecionar eventos via dropdown no Transfer
- Mantém a funcionalidade de upload de Excel como alternativa
- Cria novos eventos com status 'active' por padrão

## Transfer Logistico

**Status:** completed

Corrigido regex para quebras de linha do Excel (\\n, \\r, \\r\\n, \\n\\r). Criado plano de testes em docs/PLANO_TESTES_TRANSFER.md com queries SQL, testes de API e checklist. API retornando flightData corretamente para 977 convidados do evento Imuno teste.

## Transfer Logistics - ControlPanel

**Status:** completed

Reescrito ControlPanel.vue com layout compacto Vuetify:
- Layout em única linha: Direção, Margem, Data, Busca, Botões
- Margem padrão alterada para 0 (sem margem) - cliente não quer espera
- Opções de margem agora de 0 a 120 minutos (1 em 1) usando TIME_MARGIN_OPTIONS
- Configurações OUT aparecem em sheet expansível apenas quando direção=OUT
- Select de direção simplificado: "Chegada (IN)" e "Partida (OUT)"
- Todos os campos usando density="compact" para altura mínima

## Transfer Groups - Edição de Nome

**Status:** completed

Implementação completa da edição de nome dos grupos de transfer:

**Backend (API):**
- Migration 004_transfer_group_name.sql: adiciona campo 'name' à tabela transfer_groups
- Controller updateTransferGroup: permite editar nome, veículo, motorista
- Função generateGroupName: gera nome padrão "{IN|OUT} {Veículo} {dd/mm HH:mm}"
- Nova rota PATCH /api/transfer/groups/:groupId

**Frontend:**
- transferService.updateGroup: método para atualizar grupo via API
- EditGroupModal: campo editável para nome do grupo com botão "Usar Padrão"
- TransferGroups.vue: exibe display_name no header dos cards
- transferStore: gera display_name automaticamente para cada grupo

**Formato do nome padrão:**
- IN Van 25/01 14:30
- OUT Micro 26/01 08:00

## Transfer Module - Fluxo Completo

**Status:** completed

## Fluxo de Edição de Grupo de Transfer

### 1. Visualização (TransferGroups.vue)
- Grupos exibem `display_name` no header do card
- Nome aparece acima de data/hora
- Estilo: branco, bold, 14px

### 2. Edição (EditGroupModal.vue)
- Campo de texto para nome personalizado
- Placeholder mostra nome padrão gerado
- Botão "Usar Padrão" reseta para vazio
- Chip mostra direção (IN/OUT)

### 3. API (transfer.controller.js)
- GET /transfer/:eventId/groups - lista com display_name
- GET /transfer/groups/:groupId - detalhes com display_name
- PATCH /transfer/groups/:groupId - atualiza nome e outros campos

### 4. Banco (004_transfer_group_name.sql)
- Campo `name` VARCHAR(255) NULL
- Função `generate_transfer_group_name()` no PostgreSQL
- View `transfer_groups_with_name`

### 5. Frontend Store (transferStore.js)
- Função `generateGroupDisplayName()` gera nome localmente
- Cada grupo tem: direction, display_name, localId

## Formato do Nome Padrão
`{IN|OUT} {Veículo} {dd/mm} {HH:mm}`
Exemplos:
- IN Van 25/01 14:30
- OUT Executivo 26/01 08:00
- IN Micro 27/01 10:15

## ControlPanel - Layout Compacto

**Status:** completed

## Alterações no ControlPanel

### Layout
- Tudo em uma única linha usando v-row dense
- Campos: Direção, Margem, Data, Busca, Botões
- density="compact" em todos os campos

### Margem de Agrupamento
- Padrão alterado para 0 (sem margem)
- Cliente não quer que convidados esperem
- Opções: 0 a 120 minutos (1 em 1)
- Usa constante TIME_MARGIN_OPTIONS do constants.js

### Configurações OUT
- Aparecem apenas quando direção = OUT
- Sheet expansível (amber) com v-expand-transition
- Inclui: Antecedência, Tempo base, Tempos por aeroporto

### Select de Direção
- Labels: "Chegada (IN)" e "Partida (OUT)"
- Select padrão Vuetify com variant="outlined"

## Transfer Module - Editar Passageiro (INS-0003)

**Status:** completed

## Funcionalidades Implementadas

### 1. Trocar Veículo/Grupo
- Select com todos os grupos disponíveis
- API: PATCH /transfer/passengers/:id com group_id

### 2. Marcar No-Show
- Toggle switch no modal
- Visual: card vermelho, nome riscado, avatar vermelho
- API: POST /transfer/passengers/:id/no-show

### 3. Observações
- Textarea no modal
- Salvo em _NOTES_TRANSFER no rawData local

### 4. Editar Contato
- Campos: telefone e email
- Atualiza tanto no transfer_passengers quanto no guests

## Arquivos
- EditPassengerModal.vue (novo)
- TransferGroups.vue (estilos no-show)
- transfer.controller.js (API)
- api.js (transferService)
