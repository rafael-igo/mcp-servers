# Base de Conhecimento - Agente Check-in e NFC

## 📁 Estrutura Planejada

```
src/
├── views/
│   └── CheckInView.vue          - View principal do check-in
│
├── components/
│   └── CheckIn/
│       ├── ServiceSelector.vue   - Seletor de serviços
│       ├── NFCReader.vue         - Leitor NFC
│       ├── GuestList.vue         - Lista de convidados
│       ├── GuestDetails.vue      - Modal de detalhes
│       ├── StatusBadge.vue       - Badge de status
│       └── PresenceDashboard.vue - Dashboard
│
├── composables/
│   ├── useNFC.js                - Lógica Web NFC API
│   ├── useCheckIn.js            - Lógica de check-in
│   └── useOfflineSync.js        - Sincronização offline
│
└── stores/
    ├── checkInStore.js          - Estado de check-ins
    └── offlineStore.js          - Gerenciamento offline
```

## 🔧 Web NFC API

### Verificar Suporte
```javascript
if ('NDEFReader' in window) {
  // NFC suportado
} else {
  // Fallback para busca manual
}
```

### Ler Tag NFC
```javascript
const reader = new NDEFReader()
await reader.scan()

reader.onreading = (event) => {
  const { serialNumber } = event
  // Buscar guest vinculado a serialNumber
  // Marcar presença
}
```

### Gravar Tag NFC
```javascript
const writer = new NDEFReader()
await writer.write({
  records: [{
    recordType: "text",
    data: guestId
  }]
})
```

## 💾 Offline Mode (Dexie.js)

### Definir Schema
```javascript
const db = new Dexie('CheckInDB')
db.version(1).stores({
  checkIns: '++id, guestId, serviceId, timestamp, synced',
  guests: 'id, name, nfcTag'
})
```

### Salvar Check-in Offline
```javascript
await db.checkIns.add({
  guestId: '123',
  serviceId: 'transfer-in',
  timestamp: Date.now(),
  synced: false
})
```

### Sincronizar ao Reconectar
```javascript
const pending = await db.checkIns
  .where('synced').equals(false)
  .toArray()

for (const checkIn of pending) {
  await api.post('/api/checkin', checkIn)
  await db.checkIns.update(checkIn.id, { synced: true })
}
```

## 📡 SignalR Real-time

### Conectar ao Hub
```javascript
const connection = new signalR.HubConnectionBuilder()
  .withUrl('/hubs/checkin')
  .build()

await connection.start()
```

### Escutar Atualizações
```javascript
connection.on('CheckInUpdated', (data) => {
  // Atualizar lista de presença
  checkInStore.updateGuestStatus(data.guestId, data.status)
})
```

### Enviar Check-in
```javascript
await connection.invoke('MarkPresence', {
  eventId, serviceId, guestId
})
```

## 🎨 Estados de Presença

```javascript
const presenceStates = {
  PENDING: {
    icon: '⚠️',
    color: '#f59e0b',
    label: 'Não está presente'
  },
  PRESENT: {
    icon: '✅',
    color: '#22c55e',
    label: 'Presente'
  },
  NO_SHOW: {
    icon: '❌',
    color: '#ef4444',
    label: 'No-Show'
  }
}
```

## 📋 Store de Check-in

```javascript
// checkInStore.js
export const useCheckInStore = defineStore('checkIn', {
  state: () => ({
    currentService: null,
    guests: [],
    checkIns: {},
    offlineQueue: []
  }),

  getters: {
    presentCount: (state) =>
      Object.values(state.checkIns)
        .filter(c => c.status === 'PRESENT').length,

    absentCount: (state) =>
      state.guests.length - presentCount,

    presenceRate: (state) =>
      (presentCount / state.guests.length) * 100
  },

  actions: {
    async markPresence(guestId) {
      const checkIn = {
        guestId,
        serviceId: this.currentService.id,
        timestamp: Date.now(),
        status: 'PRESENT'
      }

      if (navigator.onLine) {
        await api.post('/api/checkin', checkIn)
      } else {
        this.offlineQueue.push(checkIn)
        await offlineDb.save(checkIn)
      }

      this.checkIns[guestId] = checkIn
    }
  }
})
```

## 🔌 APIs Backend

### POST /api/checkin
```json
{
  "eventoId": "uuid",
  "servicoTipo": "transfer_in",
  "guestId": "uuid",
  "metodo": "nfc",
  "nfcTagId": "04:A3:2B:F2",
  "timestamp": "2026-02-15T10:30:00Z",
  "coordenadorId": "uuid"
}
```

### GET /api/dashboard/{eventoId}?servico=transfer_in
```json
{
  "total": 45,
  "presente": 42,
  "ausente": 3,
  "noShow": 0,
  "taxa": 93.3,
  "checkIns": [
    {
      "guestId": "uuid",
      "nome": "ANGELA ANTONACCI",
      "status": "PRESENT",
      "timestamp": "2026-02-15T10:30:00Z",
      "coordenador": "João Silva"
    }
  ]
}
```

## 🎯 Fluxogramas

### Gravação de NFC
```
START
  ↓
Coordenador busca nome
  ↓
Sistema exibe convidado
  ↓
Aproxima pulseira NFC
  ↓
Sistema lê serialNumber
  ↓
POST /api/nfc/write {guestId, nfcTag}
  ↓
Confirmação visual ✅
  ↓
END
```

### Check-in via NFC
```
START
  ↓
Coordenador seleciona serviço
  ↓
Aproxima pulseira
  ↓
Sistema lê NFC tag
  ↓
Busca guest vinculado
  ↓
POST /api/checkin
  ↓
Marca PRESENT
  ↓
SignalR notifica todos
  ↓
Dashboard atualiza
  ↓
END
```

## 🐛 Tratamento de Erros

```javascript
// NFC não disponível
if (!('NDEFReader' in window)) {
  showMessage('NFC não suportado. Use busca manual.')
  showSearchInput()
}

// Tag NFC não vinculada
if (!guest) {
  showError('Pulseira não vinculada. Grave primeiro.')
}

// Offline
if (!navigator.onLine) {
  showWarning('Modo offline. Check-in será sincronizado.')
  saveToOfflineQueue(checkIn)
}

// Conflito de sincronização
if (checkIn.exists) {
  if (checkIn.timestamp > local.timestamp) {
    useServerVersion()
  } else {
    useLocalVersion()
  }
}
```

## 📱 PWA Configuration

```javascript
// vite.config.js
import { VitePWA } from 'vite-plugin-pwa'

export default {
  plugins: [
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'I GO Check-in',
        short_name: 'IGO',
        theme_color: '#3b82f6',
        icons: [...]
      },
      workbox: {
        runtimeCaching: [{
          urlPattern: /^https:\/\/api\.*/i,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            expiration: {
              maxEntries: 100,
              maxAgeSeconds: 60 * 60 // 1 hour
            }
          }
        }]
      }
    })
  ]
}
```

---

**Este conhecimento permite planejar e implementar o módulo de Check-in com máxima eficiência!**
