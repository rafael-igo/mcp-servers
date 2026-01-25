# Próximos Passos Planejados

## Imediato (Esta Semana)

### 1. Completar Rooming List ✅ CONCLUÍDO
- [x] Adicionar coluna "Nº Total de diárias" ✅ (já existia como "Noites")
- [x] Adicionar coluna "Forma de pagamento" ✅
- [x] Adicionar coluna "Observações" ✅
- [x] Implementar Modal de Edição ✅
- [x] Implementar Modal de Detalhes ✅
- [x] Exportação Excel com 3 abas ✅

### 2. Backend API - Iniciar (Nova Prioridade)
- [ ] Criar projeto .NET 8 WebAPI
  - `dotnet new webapi -n IGOExperienceAPI`
  - Estrutura: Controllers, Services, Models

- [ ] Configurar PostgreSQL
  - Docker Compose com PostgreSQL 16
  - Connection string em appsettings

- [ ] EF Core 8 Code-First
  - Models: Evento, Guest, Accommodation, Hotel, User
  - Migrations iniciais

## Próxima Semana

### 3. Setup Backend API
- [ ] Criar projeto .NET 8 WebAPI
  - `dotnet new webapi -n IGOExperienceAPI`
  - Estrutura: Controllers, Services, Models

- [ ] Configurar PostgreSQL
  - Docker Compose com PostgreSQL 16
  - Connection string em appsettings

- [ ] EF Core 8 Code-First
  - Models: Evento, Guest, CheckIn, User, NFCTag
  - Migrations iniciais

- [ ] JWT Authentication
  - Microsoft.AspNetCore.Authentication.JwtBearer
  - Roles: Admin, Coordenador, Líder

## Próximas 2-3 Semanas

### 4. Endpoints Essenciais
- [ ] `/api/eventos` (POST, GET, PUT, DELETE)
- [ ] `/api/eventos/{id}/upload` (POST Excel)
- [ ] `/api/auth/login` (POST)
- [ ] `/api/checkin` (POST)
- [ ] `/api/dashboard/{id}` (GET)

### 5. Iniciar Check-in Frontend
- [ ] `CheckInView.vue` base
- [ ] Login com JWT
- [ ] Seleção de evento
- [ ] Cards de serviços
- [ ] Check-in manual (lista)

## Mês Seguinte

### 6. Dashboard de Presença
- [ ] SignalR Hub
- [ ] Atualização em tempo real
- [ ] Estatísticas consolidadas

### 7. Web NFC API
- [ ] Componente `NFCReader.vue`
- [ ] Gravação de pulseiras
- [ ] Leitura para check-in

---

**Atualizado em:** 2026-01-25 (15:30)
**Próxima revisão:** Após setup do Backend API

## Resumo de Progresso

- ✅ Rooming List: 100% completo
- ⚠️ Transfer: 90% completo
- 🔴 Backend API: Próximo passo crítico
- 🔴 Check-in: Aguardando backend
