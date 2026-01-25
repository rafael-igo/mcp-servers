# Checklist Detalhado - Módulo Check-in NFC

**Última atualização:** 2026-01-25
**Progresso:** 0% ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜

---

## 🎯 Fase 1: MVP Sem NFC (Prioridade Crítica)

### Backend APIs
- [ ] POST /api/checkin - Endpoint de marcação de presença
- [ ] GET /api/eventos/{id}/guests - Listar convidados do evento
- [ ] GET /api/servicos/{id} - Listar serviços configurados
- [ ] GET /api/dashboard/{eventoId} - Dashboard de presença
- [ ] Models: CheckIn, Guest, Servico
- [ ] Validações e autorizações

### Frontend - Componentes Base
- [ ] CheckInView.vue - View principal
- [ ] ServiceSelector.vue - Seletor de serviços (cards)
- [ ] ServiceList.vue - Lista de serviços específicos
- [ ] GuestList.vue - Lista de convidados
- [ ] GuestCard.vue - Card de convidado individual
- [ ] StatusBadge.vue - Badge de status (Presente/Ausente/No-Show)
- [ ] SearchBar.vue - Busca de convidados

### Frontend - Composables
- [ ] useCheckIn.js - Lógica de check-in
- [ ] useServices.js - Gerenciamento de serviços
- [ ] useGuests.js - Gerenciamento de convidados
- [ ] usePresence.js - Estados de presença

### Frontend - Store
- [ ] checkInStore.js - Estado de check-ins
  - [ ] State: currentService, guests, checkIns
  - [ ] Getters: presentCount, absentCount, presenceRate
  - [ ] Actions: selectService, markPresence, loadGuests

### Check-in Manual
- [ ] Campo de busca em tempo real
- [ ] Autocomplete de nomes
- [ ] Botão de marcar presença
- [ ] Confirmação visual
- [ ] Feedback de sucesso/erro

### Estados de Presença
- [ ] ⚠️ Não está presente (amarelo)
- [ ] ✅ Presente (verde)
- [ ] ❌ No-Show (vermelho)
- [ ] Transições de estado
- [ ] Validações de mudança

### Dashboard Básico
- [ ] Quadro de resumo (total, presentes, ausentes, %)
- [ ] Lista de convidados com status
- [ ] Filtros por status
- [ ] Horário do último check-in
- [ ] Coordenador responsável

**Progresso Fase 1:** ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%

---

## 🔖 Fase 2: Gravação de Pulseiras NFC

### Backend
- [ ] POST /api/nfc/write - Endpoint de vinculação
- [ ] Model: NFCTag (id, guestId, tagId, timestamp)
- [ ] Validação de tag única
- [ ] Histórico de vinculações

### Frontend - Componente
- [ ] NFCRegistration.vue - Tela de gravação
- [ ] NFCWriter.vue - Componente de escrita
- [ ] GuestSearchModal.vue - Busca de convidado
- [ ] SuccessAnimation.vue - Animação de sucesso

### Frontend - Composable
- [ ] useNFC.js - Lógica Web NFC API
  - [ ] checkNFCSupport()
  - [ ] writeNFC(guestId)
  - [ ] handleNFCError()
  - [ ] iOS fallback

### Fluxo de Gravação
- [ ] Coordenador busca nome
- [ ] Sistema exibe dados do convidado
- [ ] Botão "Aproximar Pulseira"
- [ ] Leitura de serialNumber
- [ ] POST /api/nfc/write
- [ ] Confirmação visual ✅
- [ ] Adicionar à lista de gravados

### Validações
- [ ] Verificar se pulseira já vinculada
- [ ] Permitir re-vinculação (com confirmação)
- [ ] Alertar sobre pulseira duplicada
- [ ] Log de todas as vinculações

**Progresso Fase 2:** ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%

---

## 📡 Fase 3: Check-in via NFC

### Frontend - Componente
- [ ] NFCScanner.vue - Scanner NFC ativo
- [ ] ScanFeedback.vue - Feedback visual de scan
- [ ] QuickCheckIn.vue - Check-in rápido

### Frontend - useNFC.js (Atualizado)
- [ ] readNFC() - Ler tag NFC
- [ ] onNFCRead(callback) - Event listener
- [ ] parseNFCData(data) - Parser de dados
- [ ] Auto-retry em caso de erro

### Fluxo de Check-in NFC
- [ ] Coordenador seleciona serviço
- [ ] Ativa modo de scan
- [ ] Aproxima pulseira
- [ ] Sistema lê NFC tag
- [ ] Busca guest vinculado
- [ ] POST /api/checkin automaticamente
- [ ] Marca como PRESENTE
- [ ] Feedback visual instantâneo

### Tratamento de Erros
- [ ] Tag não vinculada → Sugerir gravação
- [ ] Erro de leitura → Retry automático
- [ ] NFC não suportado → Fallback busca manual
- [ ] Guest já tem check-in → Confirmar ou atualizar

### iOS Fallback
- [ ] Detectar iOS
- [ ] Exibir alternativa de busca manual
- [ ] Sugestão de app nativo (futuro)

**Progresso Fase 3:** ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%

---

## 👤 Fase 4: Detalhes do Convidado

### Frontend - Componente
- [ ] GuestDetailsModal.vue - Modal completo
- [ ] GuestInfoSection.vue - Seção de informações
- [ ] EmergencyContact.vue - Contato de emergência
- [ ] HealthInfo.vue - Informações de saúde

### Dados Exibidos
- [ ] 👤 Nome Completo
- [ ] 📄 CPF/RG
- [ ] 🎭 Categoria
- [ ] 📱 Celular (com botão de ligar)
- [ ] 📧 E-mail
- [ ] 🏥 Problemas de Saúde
- [ ] 🍽️ Restrição Alimentar
- [ ] 🚨 Contato de Emergência (nome + telefone)
- [ ] ✈️ Dados de Voo (se aplicável)
- [ ] 🏨 Dados de Hospedagem

### Ações no Modal
- [ ] Botão "Ligar" para celular
- [ ] Botão "Ligar para Emergência"
- [ ] Botão "Ver Histórico de Check-ins"
- [ ] Botão "Editar Observações"

**Progresso Fase 4:** ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%

---

## 📊 Fase 5: Dashboard Avançado

### Frontend - Componentes
- [ ] PresenceDashboard.vue - Dashboard completo
- [ ] ServiceFilter.vue - Filtro de serviços
- [ ] SummaryCards.vue - Cards de resumo
- [ ] PresenceChart.vue - Gráfico de presença
- [ ] GuestTable.vue - Tabela de convidados

### Visualizações
- [ ] Gráfico de pizza (presentes/ausentes/no-show)
- [ ] Barra de progresso visual
- [ ] Timeline de check-ins
- [ ] Heat map por horário

### Filtros
- [ ] Por serviço específico
- [ ] Por status (Todos/Presentes/Ausentes/No-Shows)
- [ ] Por categoria de convidado
- [ ] Por coordenador responsável
- [ ] Por período (últimas 6h, hoje, semana)

### Exportação
- [ ] Exportar para Excel
- [ ] Exportar para PDF
- [ ] Enviar relatório por e-mail
- [ ] Imprimir lista de presença

**Progresso Fase 5:** ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%

---

## 🔄 Fase 6: Real-time com SignalR

### Backend
- [ ] CheckInHub.cs - Hub SignalR
- [ ] Configurar CORS para WebSockets
- [ ] Métodos: JoinEventoGroup, MarkPresence
- [ ] Broadcast de atualizações

### Frontend - Composable
- [ ] useSignalR.js - Integração SignalR
  - [ ] connect(eventoId)
  - [ ] disconnect()
  - [ ] onCheckInUpdated(callback)
  - [ ] sendCheckIn(data)

### Notificações Real-time
- [ ] Atualização de lista de presença
- [ ] Notificação de novo check-in
- [ ] Atualização de contadores
- [ ] Sincronização entre múltiplos coordenadores

### Tratamento de Conexão
- [ ] Reconexão automática
- [ ] Fallback para polling
- [ ] Indicador de conexão
- [ ] Queue de mensagens offline

**Progresso Fase 6:** ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%

---

## 💾 Fase 7: Modo Offline (PWA)

### Service Workers
- [ ] Configurar Vite PWA
- [ ] Cache de assets estáticos
- [ ] Cache de API responses
- [ ] Estratégia Network-First

### Dexie.js (IndexedDB)
- [ ] Schema: checkIns, guests, services
- [ ] Salvar check-ins offline
- [ ] Sincronizar ao reconectar
- [ ] Resolver conflitos

### Frontend - Composable
- [ ] useOfflineSync.js
  - [ ] saveOffline(checkIn)
  - [ ] syncPending()
  - [ ] resolveConflicts()
  - [ ] getOfflineQueue()

### UX Offline
- [ ] Indicador "Modo Offline"
- [ ] Badge de itens pendentes
- [ ] Botão "Sincronizar Agora"
- [ ] Notificação de sucesso de sync

### Conflitos
- [ ] Detectar check-in duplicado
- [ ] Resolver por timestamp (mais recente ganha)
- [ ] Permitir resolução manual
- [ ] Log de conflitos resolvidos

**Progresso Fase 7:** ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%

---

## 🧪 Fase 8: Testes e Validação

### Testes de NFC
- [ ] Testar em dispositivos Android (Chrome)
- [ ] Testar fallback em iOS
- [ ] Testar múltiplas pulseiras
- [ ] Testar re-gravação
- [ ] Testar pulseiras corrompidas

### Testes de Check-in
- [ ] Check-in via NFC
- [ ] Check-in manual
- [ ] Múltiplos coordenadores simultâneos
- [ ] 100+ check-ins em 10 minutos
- [ ] Mudança de estados

### Testes de Offline
- [ ] Check-in sem internet
- [ ] Sincronização ao reconectar
- [ ] Resolução de conflitos
- [ ] Cache de dados

### Testes de Real-time
- [ ] Notificações instantâneas
- [ ] Múltiplos browsers/devices
- [ ] Reconexão automática
- [ ] Escalabilidade (50+ coordenadores)

### Testes de Usabilidade
- [ ] Coordenador leigo consegue usar
- [ ] Tempo médio de check-in < 5 segundos
- [ ] Interface clara em sol forte
- [ ] Feedback adequado de ações

**Progresso Fase 8:** ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜ 0%

---

## 📋 Resumo por Prioridade

### 🔴 Crítico (MVP)
- [ ] Fase 1: MVP Sem NFC (check-in manual)
- [ ] Fase 4: Detalhes do Convidado
- [ ] Fase 5: Dashboard Básico

### ⚠️ Alto (Pós-MVP)
- [ ] Fase 2: Gravação de Pulseiras
- [ ] Fase 3: Check-in via NFC
- [ ] Fase 6: Real-time básico

### 🟡 Médio (Futuro)
- [ ] Fase 5: Dashboard Avançado
- [ ] Fase 7: Modo Offline

### 🟢 Baixo (Melhorias)
- [ ] Fase 8: Testes Completos
- [ ] Exportações avançadas
- [ ] Analytics e métricas

---

**Progresso Global:** 0% ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜
**Próximo Milestone:** Fase 1 MVP Sem NFC
**Estimativa Total:** 6-8 semanas
