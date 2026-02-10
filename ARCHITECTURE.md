# 🏗️ Arquitectura del Sistema

## Visión General

```
┌─────────────────────────────────────────────────────────────────┐
│                     DASHBOARD WEB (Panel/Holoviz)               │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  📚 Plantillas│  │ 🎬 Escenarios│  │ 🔌 Conexiones│          │
│  │   (Templates)│  │  (Scenarios) │  │  (Connections)│          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  CAPA DE LÓGICA DE NEGOCIO                       │
│                                                                   │
│  ┌──────────────────────────────────────────────────┐           │
│  │            ORCHESTRATOR (Orquestador)            │           │
│  │  - Gestiona flujo de ejecución                   │           │
│  │  - Coordina agentes                               │           │
│  │  - Logging y monitoreo                            │           │
│  └────────────┬─────────────────────────┬───────────┘           │
│               │                         │                        │
│               ▼                         ▼                        │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │  Template Library   │  │  Connection Manager │              │
│  │  - 5+ Plantillas    │  │  - Gestión de       │              │
│  │  - Categorías       │  │    credenciales     │              │
│  │  - Configuraciones  │  │  - Múltiples        │              │
│  │                     │  │    servicios        │              │
│  └─────────────────────┘  └─────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      CAPA DE AGENTES                             │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │📧 Email  │  │🔍 Filter │  │📊 Excel  │  │☁️  Drive │       │
│  │ Reader   │  │          │  │ Writer   │  │          │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│  │🤖 AI     │  │🔗 Webhook│  │➕ Custom │                      │
│  │ Agent    │  │          │  │ Agents   │                      │
│  └──────────┘  └──────────┘  └──────────┘                      │
└───────┬───────────┬──────────────┬────────────┬─────────────────┘
        │           │              │            │
        ▼           ▼              ▼            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  SERVICIOS EXTERNOS                              │
│                                                                   │
│  📧 Gmail/Outlook  ☁️  Google Drive  🤖 OpenAI/Claude/Gemini   │
│  🔗 Webhooks      🌐 HTTP APIs      💾 Local Storage            │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Datos

### Ejemplo 1: Email to Excel

```
1. Usuario → Dashboard → Selecciona "Email to Excel"
                    ↓
2. Dashboard → Template Library → Obtiene plantilla
                    ↓
3. Template → Orchestrator → Configura agentes
                    ↓
4. Orchestrator → EmailReader → Lee correos de IMAP
                    ↓
5. EmailReader → EmailFilter → Filtra según criterios
                    ↓
6. EmailFilter → ExcelWriter → Genera archivo Excel
                    ↓
7. ExcelWriter → Dashboard → Muestra resultado
                    ↓
8. Dashboard → Usuario → ✅ "emails_20250210.xlsx creado"
```

### Ejemplo 2: Email + IA + Google Drive

```
1. Usuario → Dashboard → "Email AI Summary"
                    ↓
2. Dashboard → Connection Manager → Obtiene credenciales
                    ↓
3. Orchestrator → [EmailReader → EmailFilter → AIAgent → ExcelWriter → GoogleDrive]
                    ↓                ↓           ↓           ↓              ↓
                  Gmail          Filtra      OpenAI      Excel.xlsx    Upload
                    ↓                ↓           ↓           ↓              ↓
4. Usuario ← Dashboard ← Resultado ← ← ← ← ← ← ← ← ← ← ← ← ←
   "✅ Archivo subido a Google Drive"
```

## Componentes Detallados

### 1. Dashboard (Interfaz Web)

```
┌─────────────────────────────────────┐
│         Dashboard Principal          │
├─────────────────────────────────────┤
│                                      │
│  TAB 1: 📚 Plantillas                │
│  ┌────────────────────────────────┐ │
│  │ - Explorar por categoría       │ │
│  │ - Tarjetas de plantillas       │ │
│  │ - Configuración rápida         │ │
│  │ - Ejecutar con un clic         │ │
│  └────────────────────────────────┘ │
│                                      │
│  TAB 2: 🎬 Escenarios                │
│  ┌────────────────────────────────┐ │
│  │ - Escenarios personalizados    │ │
│  │ - Configuración avanzada       │ │
│  │ - Múltiples agentes            │ │
│  │ - Control granular             │ │
│  └────────────────────────────────┘ │
│                                      │
│  TAB 3: 🔌 Conexiones                │
│  ┌────────────────────────────────┐ │
│  │ - Gestión de credenciales      │ │
│  │ - Múltiples servicios          │ │
│  │ - Probar conexiones            │ │
│  │ - Reutilización                │ │
│  └────────────────────────────────┘ │
└─────────────────────────────────────┘
```

### 2. Agentes (Modular)

Cada agente implementa la interfaz `BaseAgent`:

```python
BaseAgent
├── execute(input_data) → output_data
├── configure(**kwargs)
├── get_status() → string
└── get_config_schema() → dict

Agentes Específicos:
├── EmailReaderAgent      📧 Lee correos via IMAP
├── EmailFilterAgent      🔍 Filtra correos
├── ExcelWriterAgent      📊 Exporta a Excel
├── GoogleDriveAgent      ☁️  Sube a Drive
├── WebhookAgent          🔗 Llama webhooks
└── AIAgent               🤖 Procesa con IA
```

### 3. Orchestrator (Coordinador)

```
Orchestrator
│
├── add_agent(agent)         # Añade agente al pipeline
├── execute(input)           # Ejecuta todos los agentes
├── get_status()             # Estado actual
└── get_execution_log()      # Log detallado

Pipeline:
Input → Agent1 → Agent2 → Agent3 → Output
  ↓       ↓        ↓        ↓        ↓
 Log     Log      Log      Log    Result
```

### 4. Connection Manager (Seguridad)

```
ConnectionManager
│
├── add_connection(name, type, credentials)
├── get_connection(name) → connection
├── list_connections(type) → [connections]
├── remove_connection(name)
└── test_connection(name) → result

Conexiones:
├── Email (IMAP)
│   ├── email_address
│   ├── password
│   ├── imap_server
│   └── imap_port
│
├── Google Drive
│   ├── credentials_file
│   └── folder_id
│
├── AI Services
│   ├── provider (openai/claude/gemini)
│   ├── api_key
│   └── model
│
└── Webhook
    ├── url
    ├── method
    └── headers
```

## Patrones de Diseño

### 1. Strategy Pattern (Agentes)

Cada agente es una estrategia intercambiable:

```
Context (Orchestrator)
    ↓
Strategy Interface (BaseAgent)
    ↓
Concrete Strategies (EmailReader, AIAgent, etc.)
```

### 2. Template Method (Plantillas)

Las plantillas definen el esqueleto del algoritmo:

```
Template (abstract)
    ↓
configure() → Implementado por subclases
execute() → Heredado
get_info() → Heredado
```

### 3. Facade Pattern (Dashboard)

El dashboard ofrece una interfaz simplificada:

```
Dashboard (Facade)
    ↓
├── TemplateLibrary
├── ConnectionManager
├── Orchestrator
└── Agents
```

## Escalabilidad

### Horizontal

```
Actual:
[Dashboard] → [Orchestrator] → [Agents]

Futuro:
[Dashboard] → [Load Balancer] → [Orchestrator 1] → [Agents]
                              → [Orchestrator 2] → [Agents]
                              → [Orchestrator N] → [Agents]
```

### Vertical

```
Añadir más agentes:
├── SlackAgent
├── DatabaseAgent
├── PDFAgent
├── ImageProcessingAgent
└── [Your Custom Agent]

Añadir más plantillas:
├── Slack Notifications
├── Database Sync
├── PDF Processing
└── [Your Custom Template]
```

## Seguridad

```
┌─────────────────────────────────────┐
│         Capas de Seguridad           │
├─────────────────────────────────────┤
│                                      │
│ 1. Credenciales Locales              │
│    └─ connections.json (local only) │
│                                      │
│ 2. Variables de Entorno              │
│    └─ .env (gitignored)             │
│                                      │
│ 3. Contraseñas de Aplicación         │
│    └─ Gmail App Passwords           │
│                                      │
│ 4. OAuth2 (Google Drive)             │
│    └─ Token refresh automático      │
│                                      │
│ 5. HTTPS para Webhooks               │
│    └─ Conexiones seguras            │
└─────────────────────────────────────┘
```

## Performance

### Optimizaciones Implementadas

1. **Lazy Loading**: Agentes se inicializan solo cuando se usan
2. **Streaming**: Procesamiento por lotes para emails grandes
3. **Caching**: ConnectionManager cachea conexiones
4. **Async Ready**: Diseño preparado para async/await

### Métricas Típicas

```
Operación               Tiempo    Throughput
─────────────────────────────────────────────
Leer 10 emails          2-5s      2-5 emails/s
Filtrar 100 emails      <1s       100+ emails/s
Escribir Excel          1-2s      500+ rows/s
Subir a Drive          2-10s      Depende de tamaño
Llamar Webhook         0.5-2s     Depende de API
Procesar con IA        5-30s      Depende de modelo
```

## Futuras Mejoras

### Corto Plazo
- [ ] Visual Workflow Builder (drag & drop)
- [ ] Scheduler (ejecutar automáticamente)
- [ ] Más plantillas (10+)
- [ ] Modo batch para grandes volúmenes

### Mediano Plazo
- [ ] API REST
- [ ] Webhooks entrantes
- [ ] Base de datos para historial
- [ ] Multi-usuario

### Largo Plazo
- [ ] IA para crear plantillas automáticamente
- [ ] Marketplace de plantillas
- [ ] Versión cloud/SaaS
- [ ] Mobile app

## Comparación con Make.com

| Característica          | Make.com | Esta App |
|------------------------|----------|----------|
| Interfaz visual        | ✅       | 🔄 Próx. |
| Plantillas            | ✅       | ✅       |
| Integraciones (100+)  | ✅       | 🔄 6+    |
| Webhooks              | ✅       | ✅       |
| IA Integration        | ✅       | ✅       |
| Scheduler             | ✅       | 🔄 Próx. |
| Cloud-based           | ✅       | ❌ Local |
| Open Source           | ❌       | ✅       |
| Costo                 | 💰       | 🆓 Free  |
| Personalizable        | ⚠️       | ✅       |

## Conclusión

Este sistema está diseñado para ser:
- **Modular**: Fácil añadir nuevos agentes y plantillas
- **Escalable**: Puede crecer horizontalmente y verticalmente
- **Seguro**: Credenciales locales, no en la nube
- **Flexible**: Plantillas predefinidas + escenarios custom
- **Open Source**: Código abierto, 100% personalizable
