# Contexto Atual - igo-journey/main

**Última atualização:** 2026-01-26 (05:20)

---


## Fase 1: Multi-Projeto

**Status:** in_progress

Sistema multi-projeto/branch implementado com contexto híbrido

## Database Schema

**Status:** completed

# Esquema do Banco PostgreSQL - I Go Journey

## Arquivos de Migration
- 001_init.sql: Tabelas base (companies, users, events, guests, accommodations, transfers, services, checkins)
- 002_complete_schema.sql: Extensões (import_jobs, guest_documents, guest_flights, flight_legs, guest_tracking, drivers, vehicles, global_hotels)
- 003_ai_first_schema.sql: Tabelas IA (ai_api_keys, ai_conversations, ai_suggestions, ai_analytics, ai_embeddings)

## Domínios e Tabelas (26 tabelas)

### Organizacional (3)
- companies: Empresas/Agências/Clientes
- users: Usuários com roles hierárquicos (7 níveis)
- refresh_tokens: Tokens JWT

### Eventos (2)
- events: Eventos com settings JSONB
- event_users: Vínculo usuário-evento com papel

### Convidados (3)
- guests: Dados principais + raw_data JSONB
- guest_documents: Documentos normalizados (CPF/RG/PASSAPORTE/CNH/VISTO)
- guest_tracking: Timeline completa da jornada

### Hospedagem (4)
- event_hotels: Hotéis do evento
- accommodations: Reservas/Rooming list
- accommodation_logs: Auditoria
- accommodation_checkins: Check-ins
- global_hotels: Catálogo global reutilizável

### Aéreo (2)
- guest_flights: Voos (IDA/VOLTA/INTERNO) com financeiro
- flight_legs: Trechos normalizados (N trechos por voo)

### Transfer (5)
- event_airports: Aeroportos do evento
- transfer_groups: Grupos de transfer
- transfer_passengers: Passageiros
- drivers: Motoristas cadastrados
- vehicles: Veículos cadastrados

### Serviços (3)
- event_services: Passeios/Atividades
- service_guests: Inscritos
- service_checkins: Presenças

### Check-in Geral (1)
- event_checkins: Check-ins com geolocalização

### Importação (1)
- import_jobs: Jobs de importação Excel com mapping JSONB

### IA (5)
- ai_api_keys: Chaves por empresa/evento
- ai_conversations: Histórico de chat
- ai_suggestions: Sugestões com workflow aprovação
- ai_analytics: Métricas agregadas
- ai_embeddings: Vetores pgvector (opcional)

## Padrões de Design
- Multi-tenant via company_id
- Escopo por evento via event_id
- JSONB para flexibilidade (settings, raw_data, mapping_config, metadata)
- Triggers updated_at em todas tabelas
- Índices em todas FKs
- UUID como PK
- Auditoria em accommodation_logs
