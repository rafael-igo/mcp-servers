# Base de Conhecimento - Agente Transfer Logística

## 📁 Estrutura de Código

### Arquivo Principal
**[src/views/TransferLogistics.vue](../../../src/views/TransferLogistics.vue)**

Componente principal que orquestra todo o módulo:
- Upload de Excel
- Configurações de agrupamento
- Visualização de grupos
- Exportação

### Composables

#### 1. [src/composables/useExcelProcessor.js](../../../src/composables/useExcelProcessor.js)

**Funções principais:**
```javascript
// Processa arquivo Excel
processExcelFile(file)
  → Encontra cabeçalho "ID SISTEMA"
  → Mapeia todas as 185+ colunas
  → Valida dados obrigatórios
  → Retorna array de passageiros

// Busca linha do cabeçalho
findHeaderRow(sheet)
  → Procura "ID SISTEMA" em cols A-G, linhas 1-40
  → Retorna linha encontrada ou null

// Extrai dados de um passageiro
extractPassengerData(row)
  → Mapeia cada coluna do Excel
  → Normaliza valores
  → Retorna objeto com todos os campos
```

**Campos processados:**
- Dados pessoais: nome, CPF, categoria, contato
- Voos IDA: origem, destino, chegada, partida, voo
- Voos VOLTA: origem, destino, chegada, partida, voo
- Status: RSVP, aéreo
- Patrocínios: geral, inscrição, participação, hospedagem, aéreo
- Hospedagem: hotel, tipo apto, check-in/out

#### 2. [src/composables/useTransferGrouping.js](../../../src/composables/useTransferGrouping.js)

**Funções principais:**
```javascript
// Agrupa passageiros por tempo
groupPassengersByTime(passengers, type, marginMinutes)
  → type: 'in' ou 'out'
  → marginMinutes: 15, 30, 45, 60
  → Separa por categoria (Palestrante vs Convidado)
  → Retorna grupos com horário base

// Aloca veículos para um grupo
allocateVehicles(group)
  → Palestrantes: sempre carro individual
  → Convidados:
    - 1-2: Carro
    - 3-10: Van
    - 11-18: Micro-ônibus
    - 19+: Ônibus
  → Retorna lista de veículos

// Calcula horário Transfer OUT
calculateTransferOut(flightTime, aeroporto, config)
  → flightTime: horário do voo
  → aeroporto: código do aeroporto
  → config: {horasAntes: 2, tempoBase: 60, temposEspecificos: {}}
  → Retorna horário calculado
  → Fórmula: voo - (horasAntes * 60) - tempo do aeroporto

// Extrai horários de conexões
extractConnectionTimes(cellValue, useFirst = false)
  → Normaliza quebras de linha (\r\n, \r, \n)
  → Separa por linhas
  → Extrai todos os horários (hh:mm, hhHmm, h:mm, hHmm)
  → useFirst: true → primeiro horário, false → último horário
  → Retorna horário formatado hh:mm

// Extrai aeroportos de conexões
extractConnectionAirports(cellValue, useFirst = false)
  → Processa múltiplas linhas
  → useFirst: true → primeira origem, false → último destino
  → Retorna código do aeroporto
```

#### 3. [src/composables/useFilters.js](../../../src/composables/useFilters.js)

**Funções principais:**
```javascript
// Filtra passageiros
applyFilters(passengers)
  → STATUS RSVP: "CONFIRMADO" ou "CARTA INFORMATIVA ENVIADA"
  → STATUS AÉREO: "EMITIDO" ou "REEMITIDO"
  → Verifica patrocínios
  → Retorna passageiros válidos

// Busca por nome
filterByName(passengers, searchTerm)
  → Case-insensitive
  → Busca em nome completo
  → Retorna array filtrado
```

#### 4. [src/composables/useExcelExport.js](../../../src/composables/useExcelExport.js)

**Planilhas geradas:**
1. **Resumo**: Total de passageiros, veículos, configurações
2. **Grupos de Transfer**: Data, horário, range, quantidade por tipo
3. **Alocação de Veículos**: Tipo, quantidade de passageiros, nomes
4. **Detalhes dos Passageiros**: Todos os dados de cada passageiro
5. **Configurações**: Margem, horas antes, tempos por aeroporto

### Store Pinia

#### [src/stores/transferStore.js](../../../src/stores/transferStore.js)

**Estado:**
```javascript
state: {
  passengers: [],           // Todos os passageiros processados
  filteredPassengers: [],   // Após filtros
  transferInGroups: [],     // Grupos de Transfer IN
  transferOutGroups: [],    // Grupos de Transfer OUT
  config: {
    marginMinutes: 30,
    transferOutHoursBeforeFlight: 2,
    transferOutBaseTime: 60,
    airportSpecificTimes: {}
  },
  selectedVehicleType: null,
  searchQuery: ''
}
```

**Getters:**
```javascript
totalPassengers          // Total de passageiros
validPassengersCount     // Após filtros
totalVehicles            // Total de veículos alocados
vehiclesByType           // Contagem por tipo (Carro, Van, etc)
groupedByDate            // Grupos agrupados por data
```

**Actions:**
```javascript
loadPassengers(data)            // Carrega dados do Excel
applyFilters()                  // Aplica filtros de status
groupTransfers(type)            // Agrupa por tipo (in/out)
updateConfig(newConfig)         // Atualiza configurações
filterByVehicleType(type)       // Filtra por tipo de veículo
searchPassengers(query)         // Busca por nome
```

### Componentes

#### 1. [src/components/Upload/UploadArea.vue](../../../src/components/Upload/UploadArea.vue)

- Drag & drop de arquivo Excel
- Preview de arquivo selecionado
- Botão de remoção
- Feedback visual moderno

#### 2. [src/components/Dashboard/SummaryCards.vue](../../../src/components/Dashboard/SummaryCards.vue)

- Cards clicáveis por tipo de veículo
- Badges coloridos (VIP, STD, VAN, BUS)
- Ícones SVG customizados
- Estados hover e active

#### 3. [src/components/Transfer/TransferGroups.vue](../../../src/components/Transfer/TransferGroups.vue)

- Lista de grupos de transfer
- Range de horários (início - fim)
- Alocação de veículos por grupo
- Detalhes de passageiros
- Modais de edição

#### 4. [src/components/Filters/ConfigPanel.vue](../../../src/components/Filters/ConfigPanel.vue)

- Seletor de margem (15/30/45/60 min)
- Configuração de Transfer OUT (1-4 horas antes)
- Tempo base até aeroporto
- Tempos específicos por aeroporto
- Busca por nome de passageiro

## 🎨 Design System

### Paleta de Cores
```css
--primary-500: #3b82f6;      /* Azul principal */
--secondary-800: #1e293b;    /* Cinza escuro */
--success-500: #22c55e;      /* Verde */
--warning-500: #f59e0b;      /* Âmbar */
--error-500: #ef4444;        /* Vermelho */
```

### Badges de Veículos
- **VIP** (Carro): Gradiente dourado
- **STD** (Van): Azul
- **BUS** (Micro/Ônibus): Verde

### Responsividade
- Mobile-first approach
- Grid responsivo (4→2→1 colunas)
- Touch-friendly (hover: none)

## 📊 Dados de Exemplo

### Passageiro Processado
```javascript
{
  id: "12345",
  nome: "ANGELA OLIVEIRA ANTONACCI",
  categoria: "PALESTRANTE",
  statusRSVP: "CONFIRMADO",
  statusAereo: "EMITIDO",
  vooIda: {
    origem: "GRU",
    destino: "GIG",
    chegada: "14:30",
    partida: "12:15",
    voo: "G31234\nG31456" // múltiplas conexões
  },
  vooVolta: {
    origem: "GIG",
    destino: "GRU",
    chegada: "22:00",
    partida: "20:15"
  },
  patrocinios: {
    geral: "SIM",
    hospedagem: "SIM",
    aereo: "SIM"
  }
}
```

### Grupo de Transfer
```javascript
{
  baseTime: "14:30",
  timeRange: "14:15 - 14:45",
  passengers: [
    { nome: "ANGELA...", categoria: "PALESTRANTE" },
    { nome: "BRUNA...", categoria: "CONVIDADO" }
  ],
  vehicles: [
    { type: "Carro Executivo", count: 1, passengers: ["ANGELA..."] },
    { type: "Van", count: 1, passengers: ["BRUNA...", "..."] }
  ],
  date: "2026-02-15"
}
```

## 🔍 Casos de Uso Comuns

### 1. Processar Nova Planilha
```
1. Upload do arquivo Excel
2. Sistema busca cabeçalho "ID SISTEMA"
3. Mapeia todas as colunas
4. Extrai dados de cada passageiro
5. Aplica filtros (RSVP + Aéreo)
6. Armazena em transferStore.passengers
```

### 2. Agrupar Transfer IN
```
1. Filtrar passageiros válidos
2. Extrair último horário de chegada (IDA\nCHEGADA)
3. Extrair último destino (IDA\nDESTINO)
4. Separar palestrantes de convidados
5. Agrupar por horário com margem de 30min
6. Alocar veículos por grupo
7. Exibir grupos com range de horários
```

### 3. Configurar Transfer OUT por Aeroporto
```
1. Processar planilha
2. Identificar aeroportos únicos em VOLTA\nORIGEM
3. Exibir campo de configuração para cada aeroporto
4. Usuário define tempo específico (ex: GRU = 90min)
5. Ao agrupar Transfer OUT, aplicar tempo específico
6. Fórmula: voo_partida - 2h - 90min = 10:15
```

## 📈 Métricas e Performance

### Processamento
- Planilhas: Até 500 passageiros testadas
- Tempo: < 2 segundos para processar e agrupar
- Memória: ~10MB para 500 passageiros

### Exportação
- 5 planilhas geradas
- Tempo: < 1 segundo
- Formato: .xlsx (SheetJS)

## 🐛 Problemas Conhecidos e Soluções

### Problema: Passageiros não aparecem
**Causa:** Status RSVP ou Aéreo inválido
**Solução:** Verificar filtros em `useFilters.js`

### Problema: Horários errados em conexões
**Causa:** Quebras de linha não normalizadas
**Solução:** `extractConnectionTimes()` normaliza `\r\n` → `\n`

### Problema: Transfer OUT não agrupa corretamente
**Causa:** Tempo do aeroporto não configurado
**Solução:** Configurar tempo específico no painel

## 🚀 Roadmap Futuro

### Curto Prazo
- [ ] Integração com backend API
- [ ] Persistência de configurações
- [ ] Histórico de processamentos

### Médio Prazo
- [ ] Otimizador automático de agrupamentos
- [ ] Machine learning para sugerir margens
- [ ] Integração com Google Maps (tempo real)

### Longo Prazo
- [ ] App mobile nativo
- [ ] Tracking em tempo real
- [ ] Notificações push para coordenadores

---

**Este conhecimento permite que você atue com máxima precisão e eficiência no módulo Transfer!**
