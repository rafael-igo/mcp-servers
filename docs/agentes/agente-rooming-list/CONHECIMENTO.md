# Base de Conhecimento - Agente Rooming List / Hospedagem

## 📁 Estrutura de Código

### Arquivo Principal
**[src/views/HospedagemView.vue](../../../src/views/HospedagemView.vue)**

Componente principal do módulo:
- Upload de Excel (reutiliza componente de Transfer)
- Visualização de estatísticas
- Cards expandidos por hotel
- Tabela de passageiros com filtros
- Detalhes financeiros expansíveis

### Composables

#### 1. [src/composables/useRoomingList.js](../../../src/composables/useRoomingList.js)

**Função principal de processamento:**
```javascript
processHospedagemData(passengers) {
  const filtered = passengers.filter(p => {
    // REGRA 1: Verificar patrocínio de HOSPEDAGEM = "SIM"
    const hasHospedagem = (p.patrocinios?.hospedagem || '')
      .toUpperCase()
      .trim() === 'SIM'

    // REGRA 2: Verificar status de presença
    const validStatus = ['CONFIRMADO', 'CARTA INFORMATIVA ENVIADA']
    const hasValidStatus = validStatus.includes(
      (p.statusRSVP || '').toUpperCase().trim()
    )

    return hasHospedagem && hasValidStatus
  })

  // REGRA 3: Marcar passageiros com aéreo pendente
  return filtered.map(p => {
    const isPending =
      p.statusRSVP?.toUpperCase() === 'CONFIRMADO' &&
      (p.statusAereo || '').toUpperCase().includes('PENDENTE')

    return {
      ...p,
      isPendingFlight: isPending,
      warningMessage: isPending
        ? 'Aéreo pendente - Confirmação sujeita a alterações'
        : null
    }
  })
}
```

**Agrupamento por hotel:**
```javascript
groupByHotelAndDate(hospedagemData) {
  const groups = {}

  hospedagemData.forEach(passenger => {
    const hotel = passenger.hospedagem.hotel || 'Sem Hotel'
    const date = passenger.hospedagem.checkIn?.split(' ')[0] || 'Sem Data'

    if (!groups[hotel]) groups[hotel] = {}
    if (!groups[hotel][date]) groups[hotel][date] = []

    groups[hotel][date].push(passenger)
  })

  return groups
}
```

**Validação de conflitos:**
```javascript
validateDateConflicts(data) {
  const conflicts = []

  data.forEach(p => {
    const checkIn = new Date(p.hospedagem.checkIn)
    const checkOut = new Date(p.hospedagem.checkOut)

    if (checkOut < checkIn) {
      conflicts.push({
        passenger: p.nome,
        error: 'Check-out antes de check-in',
        checkIn: p.hospedagem.checkIn,
        checkOut: p.hospedagem.checkOut
      })
    }
  })

  return conflicts
}
```

**Estatísticas por hotel:**
```javascript
calculateHotelStats(hotelGroups) {
  const stats = {}

  Object.entries(hotelGroups).forEach(([hotel, dates]) => {
    const allPassengers = Object.values(dates).flat()

    stats[hotel] = {
      totalGuests: allPassengers.length,
      totalRooms: allPassengers.reduce((sum, p) =>
        sum + (p.hospedagem.quantidadeApartamentos || 1), 0),
      checkIns: new Set(allPassengers.map(p =>
        p.hospedagem.checkIn?.split(' ')[0])).size,
      checkOuts: new Set(allPassengers.map(p =>
        p.hospedagem.checkOut?.split(' ')[0])).size,
      pendingFlights: allPassengers.filter(p =>
        p.isPendingFlight).length,
      earlyCheckIns: allPassengers.filter(p =>
        p.hospedagem.earlyCheckIn === 'SIM').length,
      lateCheckOuts: allPassengers.filter(p =>
        p.hospedagem.lateCheckOut === 'SIM').length
    }
  })

  return stats
}
```

#### 2. [src/composables/useExcelProcessor.js](../../../src/composables/useExcelProcessor.js)

**Campos de hospedagem processados:**
```javascript
// Campos principais
'HOSPEDAGEM\nNOME' → hospedagem.hotel
'HOSPEDAGEM\nENDEREÇO' → hospedagem.endereco
'HOSPEDAGEM\nTIPO' → hospedagem.tipoApartamento
'HOSPEDAGEM\nQTDE APTOS' → hospedagem.quantidadeApartamentos
'HOSPEDAGEM\nCHECK-IN' → hospedagem.checkIn
'HOSPEDAGEM\nCHECK-OUT' → hospedagem.checkOut

// Campos financeiros
'HOSPEDAGEM\nVALOR DIÁRIA' → hospedagem.valorDiaria
'HOSPEDAGEM\nTAXA ISS' → hospedagem.taxaISS
'HOSPEDAGEM\nVALOR TOTAL' → hospedagem.valorTotal
'HOSPEDAGEM\nNº DIÁRIAS' → hospedagem.numeroDiarias

// Campos adicionais
'HOSPEDAGEM\nEARLY' → hospedagem.earlyCheckIn
'HOSPEDAGEM\nLATE' → hospedagem.lateCheckOut
'HOSPEDAGEM\nOBS' → hospedagem.observacoes

// Pernoites (1-6)
'PERNOITE 1\nNOME' → pernoites[0].hotel
'PERNOITE 1\nCHECK-IN' → pernoites[0].checkIn
// ... até pernoite 6
```

### Stores

#### 1. [src/stores/hospedagemStore.js](../../../src/stores/hospedagemStore.js)

**Estado:**
```javascript
state: {
  hospedagemData: [],        // Dados processados de hospedagem
  hotelGroups: {},           // Agrupado por hotel e data
  stats: {},                 // Estatísticas por hotel
  conflicts: [],             // Conflitos detectados
  selectedHotel: null,       // Filtro por hotel
  dateRange: null            // Filtro por período
}
```

**Getters:**
```javascript
totalHotels               // Total de hotéis únicos
totalGuestsWithHospedagem // Total de hóspedes
totalRooms                // Total de quartos
totalPendingFlights       // Total com aéreo pendente
hotelsList                // Array de nomes de hotéis
statsForHotel(hotel)      // Stats de hotel específico
```

**Actions:**
```javascript
processHospedagem(passengers)   // Processa dados
groupByHotel()                  // Agrupa por hotel
calculateAllStats()             // Calcula todas as stats
validateConflicts()             // Valida conflitos
filterByHotel(hotel)            // Filtra por hotel
filterByDateRange(start, end)   // Filtra por período
```

#### 2. [src/stores/adminStore.js](../../../src/stores/adminStore.js)

**Dados compartilhados:**
```javascript
state: {
  passengers: [],    // Passageiros processados do Excel
  currentEvent: null // Evento atual
}
```

Usado por Transfer e Hospedagem para compartilhar dados.

## 🎨 Interface Visual

### Cards de Resumo (HospedagemView.vue, linhas 42-75)
```vue
<div class="summary-cards">
  <!-- Total de Hotéis -->
  <div class="stat-card">
    <div class="stat-value">{{ totalHotels }}</div>
    <div class="stat-label">Hotéis</div>
  </div>

  <!-- Total de Hóspedes -->
  <div class="stat-card">
    <div class="stat-value">{{ totalGuests }}</div>
    <div class="stat-label">Hóspedes</div>
  </div>

  <!-- Total de Quartos -->
  <div class="stat-card">
    <div class="stat-value">{{ totalRooms }}</div>
    <div class="stat-label">Quartos</div>
  </div>

  <!-- Aéreo Pendente (destaque laranja) -->
  <div class="stat-card warning">
    <div class="stat-value">{{ totalPendingFlights }}</div>
    <div class="stat-label">Aéreo Pendente</div>
  </div>

  <!-- Conflitos (se houver) -->
  <div v-if="conflicts.length" class="stat-card error">
    <div class="stat-value">{{ conflicts.length }}</div>
    <div class="stat-label">Conflitos</div>
  </div>
</div>
```

### Info Box de Filtros (linhas 51-60)
```vue
<div class="filter-info-box">
  <h4>🔍 Critérios Aplicados</h4>
  <ul>
    <li>✅ HOSPEDAGEM = "SIM"</li>
    <li>✅ Status: CONFIRMADO ou CARTA INFORMATIVA ENVIADA</li>
    <li>⚠️ Sinaliza aéreos pendentes com destaque</li>
  </ul>
</div>
```

### Card de Hotel (linhas 108-239)
```vue
<div v-for="(hotel, hotelName) in hotelGroups" class="hotel-card">
  <!-- Cabeçalho -->
  <div class="hotel-header">
    <h3>🏨 {{ hotelName }}</h3>
    <div class="hotel-badges">
      <span class="badge">{{ stats.totalGuests }} Hóspedes</span>
      <span class="badge">{{ stats.totalRooms }} Quartos</span>
      <span v-if="stats.pendingFlights" class="badge warning">
        {{ stats.pendingFlights }} Aéreo Pendente
      </span>
    </div>
  </div>

  <!-- Tabela de Passageiros -->
  <div class="passengers-table-grid">
    <!-- Cabeçalhos -->
    <div class="table-header">Hóspede</div>
    <div class="table-header">Tipo Apto</div>
    <div class="table-header">Check-in</div>
    <div class="table-header">Check-out</div>
    <div class="table-header">Diárias</div>
    <div class="table-header">Status</div>

    <!-- Linhas de passageiros -->
    <div v-for="passenger in hotelPassengers"
         :class="{'pending-flight-row': passenger.isPendingFlight}">

      <!-- Nome + Categoria -->
      <div class="passenger-name">
        {{ passenger.nome }}
        <span class="category-badge">{{ passenger.categoria }}</span>
      </div>

      <!-- Tipo de Apartamento -->
      <div>{{ passenger.hospedagem.tipoApartamento }}</div>

      <!-- Check-in -->
      <div>
        {{ formatDate(passenger.hospedagem.checkIn) }}
        <span v-if="passenger.hospedagem.earlyCheckIn === 'SIM'"
              class="badge small">⚡ Early</span>
      </div>

      <!-- Check-out -->
      <div>
        {{ formatDate(passenger.hospedagem.checkOut) }}
        <span v-if="passenger.hospedagem.lateCheckOut === 'SIM'"
              class="badge small">🌙 Late</span>
      </div>

      <!-- Diárias -->
      <div>{{ passenger.hospedagem.numeroDiarias }}</div>

      <!-- Status -->
      <div>
        <span v-if="passenger.isPendingFlight" class="status-badge warning">
          ⚠️ Aéreo Pendente
        </span>
        <span v-else class="status-badge success">
          ✅ Confirmado
        </span>
      </div>
    </div>
  </div>

  <!-- Detalhes Financeiros (expansível) -->
  <details class="financial-details">
    <summary>💰 Detalhes Financeiros</summary>
    <div class="financial-grid">
      <div>
        <strong>Valor da Diária:</strong>
        {{ formatCurrency(passenger.hospedagem.valorDiaria) }}
      </div>
      <div>
        <strong>Taxa ISS:</strong>
        {{ formatCurrency(passenger.hospedagem.taxaISS) }}
      </div>
      <div>
        <strong>Valor Total:</strong>
        <span class="total-value">
          {{ formatCurrency(passenger.hospedagem.valorTotal) }}
        </span>
      </div>
      <div class="full-width">
        <strong>Observações:</strong>
        {{ passenger.hospedagem.observacoes || 'Nenhuma' }}
      </div>
    </div>
  </details>
</div>
```

### Sistema de Cores (CSS)
```css
/* Linha de passageiro com aéreo pendente */
.pending-flight-row {
  border-left: 4px solid var(--warning-500);
  background-color: #fff6e0;
}

/* Badge de status */
.status-badge.warning {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
}

.status-badge.success {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
}

/* Badges de Early/Late */
.badge.small {
  font-size: 0.75rem;
  padding: 2px 6px;
}
```

## 📊 Dados de Exemplo

### Passageiro com Hospedagem
```javascript
{
  nome: "ANGELA OLIVEIRA ANTONACCI",
  categoria: "PALESTRANTE",
  statusRSVP: "CONFIRMADO",
  statusAereo: "PENDENTE*", // ⚠️ Aéreo pendente
  patrocinios: {
    hospedagem: "SIM"
  },
  hospedagem: {
    hotel: "Copacabana Palace",
    endereco: "Av Atlântica, 1702 - Copacabana",
    tipoApartamento: "Single Deluxe",
    quantidadeApartamentos: 1,
    checkIn: "2026-02-10 14:00",
    checkOut: "2026-02-15 12:00",
    numeroDiarias: 5,
    earlyCheckIn: "SIM",
    lateCheckOut: "NÃO",
    valorDiaria: 850.00,
    taxaISS: 42.50,
    valorTotal: 4292.50,
    observacoes: "Quarto com vista para o mar"
  },
  isPendingFlight: true, // ✅ Flag aplicada
  warningMessage: "Aéreo pendente - Confirmação sujeita a alterações"
}
```

### Grupo por Hotel
```javascript
{
  "Copacabana Palace": {
    "2026-02-10": [
      { nome: "ANGELA...", ... },
      { nome: "BRUNA...", ... },
      // ... mais hóspedes
    ],
    "2026-02-11": [
      // Hóspedes com check-in em 11/02
    ]
  },
  "Fasano Rio": {
    "2026-02-10": [
      // Hóspedes do Fasano
    ]
  }
}
```

### Estatísticas por Hotel
```javascript
{
  "Copacabana Palace": {
    totalGuests: 45,
    totalRooms: 30,
    checkIns: 2,        // 2 datas únicas de check-in
    checkOuts: 2,       // 2 datas únicas de check-out
    pendingFlights: 5,  // 5 passageiros com aéreo pendente
    earlyCheckIns: 12,
    lateCheckOuts: 8
  }
}
```

## 🔍 Casos de Uso Detalhados

### 1. Detectar e Sinalizar Aéreo Pendente
```javascript
// Entrada
const passenger = {
  statusRSVP: "CONFIRMADO",
  statusAereo: "PENDENTE*"
}

// Processamento (useRoomingList.js:61-66)
const isPending =
  passenger.statusRSVP?.toUpperCase() === 'CONFIRMADO' &&
  (passenger.statusAereo || '').toUpperCase().includes('PENDENTE')

// Saída
{
  ...passenger,
  isPendingFlight: true,
  warningMessage: "Aéreo pendente - Confirmação sujeita a alterações"
}

// Impacto visual
- Border laranja na linha
- Badge "⚠️ Aéreo Pendente"
- Contador no card de resumo
- Estatística por hotel
```

### 2. Validar Conflito de Datas
```javascript
// Entrada
const passenger = {
  hospedagem: {
    checkIn: "2026-02-15 14:00",
    checkOut: "2026-02-10 12:00" // ❌ Antes do check-in!
  }
}

// Validação
const checkInDate = new Date("2026-02-15")
const checkOutDate = new Date("2026-02-10")

if (checkOutDate < checkInDate) {
  conflicts.push({
    passenger: passenger.nome,
    error: "Check-out antes de check-in",
    checkIn: "2026-02-15 14:00",
    checkOut: "2026-02-10 12:00"
  })
}

// Resultado
- Card vermelho de alerta
- Contador de conflitos
- Detalhes do erro
```

### 3. Calcular Estatísticas Globais
```javascript
// Processamento
const allHotels = Object.keys(hotelGroups) // ["Copacabana", "Fasano"]
const totalGuests = hospedagemData.length  // 85
const totalPending = hospedagemData.filter(p => p.isPendingFlight).length // 12

const totalRooms = hospedagemData.reduce((sum, p) =>
  sum + (p.hospedagem.quantidadeApartamentos || 1), 0) // 65

// Cards de resumo atualizados
- 2 Hotéis
- 85 Hóspedes
- 65 Quartos
- 12 Aéreo Pendente (14.1%)
```

## 🐛 Problemas Conhecidos e Soluções

### Problema: Passageiros não aparecem
**Causa:** Não atende REGRA 1 ou 2
**Solução:** Verificar HOSPEDAGEM=SIM e status válido

### Problema: Aéreo pendente não sinalizado
**Causa:** Campo statusAereo vazio ou formato diferente
**Solução:** Verificar se contém "PENDENTE" (case-insensitive)

### Problema: Conflitos não detectados
**Causa:** Datas em formato inválido
**Solução:** Normalizar formato de data antes de validar

## 🚀 Melhorias Futuras

- [ ] Auto-correção de conflitos sugerida
- [ ] Integração com sistema do hotel (UH automático)
- [ ] Notificações de mudanças de aéreo
- [ ] Dashboard de ocupação em tempo real
- [ ] Exportação multi-formato (PDF, Excel, CSV)

---

**Este conhecimento permite atuação precisa e eficiente no módulo de Hospedagem!**
