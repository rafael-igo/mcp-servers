# Base de Conhecimento - Agente Backend

## 📁 Estrutura Backend

```
backend/
├── Controllers/
│   ├── AuthController.cs
│   ├── EventosController.cs
│   ├── CheckInController.cs
│   └── UsuariosController.cs
│
├── Models/
│   ├── Usuario.cs
│   ├── Evento.cs
│   ├── Guest.cs
│   ├── CheckIn.cs
│   └── NFCTag.cs
│
├── Services/
│   ├── AuthService.cs
│   ├── EventoService.cs
│   └── CheckInService.cs
│
├── Data/
│   ├── AppDbContext.cs
│   └── Migrations/
│
└── Hubs/
    └── CheckInHub.cs (SignalR)
```

## 💾 Modelos de Dados

### Usuario
```csharp
public class Usuario {
  public Guid Id { get; set; }
  public string Nome { get; set; }
  public string Email { get; set; }
  public string PasswordHash { get; set; }
  public UserRole Role { get; set; } // Admin, Coordenador, Líder
  public Guid? EventoId { get; set; }
}
```

### Evento
```csharp
public class Evento {
  public Guid Id { get; set; }
  public string Nome { get; set; }
  public DateTime DataInicio { get; set; }
  public DateTime DataFim { get; set; }
  public List<Guest> Guests { get; set; }
  public List<Servico> Servicos { get; set; }
}
```

### CheckIn
```csharp
public class CheckIn {
  public Guid Id { get; set; }
  public Guid EventoId { get; set; }
  public Guid GuestId { get; set; }
  public Guid ServicoId { get; set; }
  public CheckInStatus Status { get; set; } // Presente, Ausente, NoShow
  public DateTime Timestamp { get; set; }
  public Guid CoordenadorId { get; set; }
  public string Metodo { get; set; } // nfc, manual
}
```

## 🔌 Endpoints Detalhados

### POST /api/auth/login
```csharp
[HttpPost("login")]
public async Task<IActionResult> Login([FromBody] LoginRequest request) {
  var user = await _authService.ValidateCredentials(request.Email, request.Password);
  if (user == null) return Unauthorized();

  var token = _authService.GenerateJWT(user);
  return Ok(new { token, user });
}
```

### POST /api/checkin
```csharp
[HttpPost]
[Authorize(Roles = "Coordenador,Líder")]
public async Task<IActionResult> MarcarPresenca([FromBody] CheckInRequest request) {
  var checkIn = new CheckIn {
    EventoId = request.EventoId,
    GuestId = request.GuestId,
    ServicoId = request.ServicoId,
    Status = CheckInStatus.Presente,
    Timestamp = DateTime.UtcNow,
    CoordenadorId = User.GetId(),
    Metodo = request.Metodo
  };

  await _context.CheckIns.AddAsync(checkIn);
  await _context.SaveChangesAsync();

  // SignalR notification
  await _hubContext.Clients.Group($"evento-{request.EventoId}")
    .SendAsync("CheckInUpdated", checkIn);

  return Ok(checkIn);
}
```

## 📡 SignalR Hub

```csharp
public class CheckInHub : Hub {
  public async Task JoinEventoGroup(string eventoId) {
    await Groups.AddToGroupAsync(Context.ConnectionId, $"evento-{eventoId}");
  }

  public async Task MarkPresence(CheckInRequest request) {
    // Salvar no banco
    // Notificar grupo
    await Clients.Group($"evento-{request.EventoId}")
      .SendAsync("CheckInUpdated", result);
  }
}
```

## 🔐 Segurança

### JWT Configuration
```csharp
services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
  .AddJwtBearer(options => {
    options.TokenValidationParameters = new TokenValidationParameters {
      ValidateIssuer = true,
      ValidateAudience = true,
      ValidateLifetime = true,
      ValidateIssuerSigningKey = true,
      ValidIssuer = configuration["Jwt:Issuer"],
      ValidAudience = configuration["Jwt:Audience"],
      IssuerSigningKey = new SymmetricSecurityKey(
        Encoding.UTF8.GetBytes(configuration["Jwt:Key"]))
    };
  });
```

---

**Conhecimento para construir backend robusto e escalável!**
