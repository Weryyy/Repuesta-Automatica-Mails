# 📚 Guía de Plantillas

## ¿Qué son las Plantillas?

Las plantillas son flujos de trabajo predefinidos y listos para usar que combinan múltiples agentes para automatizar tareas comunes. Están inspiradas en las plantillas de Make.com y te permiten empezar rápidamente sin necesidad de configurar cada agente individualmente.

## 🎯 Plantillas Disponibles

### 📊 Categoría: Email

#### 1. Email to Excel
**Descripción:** Lee correos de tu buzón, los filtra según criterios y los exporta a un archivo Excel.

**Flujo:**
```
📧 EmailReader → 🔍 EmailFilter → 📊 ExcelWriter
```

**Casos de uso:**
- Exportar facturas recibidas por email
- Crear reportes de comunicaciones con clientes
- Archivar correos importantes en Excel
- Analizar patrones de correos recibidos

**Conexiones requeridas:**
- Email (IMAP)

**Configuración:**
- Email y contraseña
- Filtros opcionales (asunto, remitente)
- Número máximo de correos

---

### ☁️ Categoría: Integration

#### 2. Email to Google Drive
**Descripción:** Exporta correos filtrados a Google Drive automáticamente.

**Flujo:**
```
📧 EmailReader → 🔍 EmailFilter → 📊 ExcelWriter → ☁️ GoogleDrive
```

**Casos de uso:**
- Backup automático de correos importantes
- Compartir reportes de email con el equipo
- Almacenamiento centralizado de comunicaciones
- Integración con Google Workspace

**Conexiones requeridas:**
- Email (IMAP)
- Google Drive

**Configuración:**
- Credenciales de email
- Credenciales de Google Drive
- Filtros de correo
- Carpeta de destino en Drive

---

#### 3. Email to Webhook
**Descripción:** Envía correos filtrados a un webhook para integrar con otros sistemas.

**Flujo:**
```
📧 EmailReader → 🔍 EmailFilter → 🔗 Webhook
```

**Casos de uso:**
- Notificar a Slack cuando llegan ciertos correos
- Integrar con sistemas CRM
- Activar flujos de trabajo en otras plataformas
- Enviar datos a bases de datos externas

**Conexiones requeridas:**
- Email (IMAP)
- Webhook

**Configuración:**
- Credenciales de email
- URL del webhook
- Método HTTP (POST, GET, PUT)
- Headers personalizados

**Ejemplo de webhook (Slack):**
```json
{
  "url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

---

### 🤖 Categoría: AI

#### 4. Email AI Summary
**Descripción:** Resume correos usando inteligencia artificial.

**Flujo:**
```
📧 EmailReader → 🔍 EmailFilter → 🤖 AI Agent → 📊 ExcelWriter
```

**Casos de uso:**
- Resumir correos largos automáticamente
- Extraer puntos clave de comunicaciones
- Procesar grandes volúmenes de correos
- Crear reportes ejecutivos de emails

**Conexiones requeridas:**
- Email (IMAP)
- AI (OpenAI, Claude, Gemini o Local)

**Configuración:**
- Credenciales de email
- Proveedor de IA y API key
- Modelo de IA (opcional)
- Filtros de correo

**Proveedores de IA soportados:**
- **OpenAI**: GPT-3.5-turbo, GPT-4
- **Anthropic**: Claude 3 Sonnet, Claude 3 Opus
- **Google**: Gemini Pro
- **Local**: Modelos locales (próximamente)

---

#### 5. AI Email Classification
**Descripción:** Clasifica correos automáticamente usando IA.

**Flujo:**
```
📧 EmailReader → 🤖 AI Classification → 📊 ExcelWriter
```

**Casos de uso:**
- Clasificar correos por prioridad
- Categorizar automáticamente comunicaciones
- Identificar tipos de solicitudes
- Organizar correos por departamento

**Conexiones requeridas:**
- Email (IMAP)
- AI (OpenAI, Claude, Gemini o Local)

**Configuración:**
- Credenciales de email
- Proveedor de IA
- Categorías de clasificación (configurables)

**Ejemplo de categorías:**
- Urgente / Normal / Bajo
- Ventas / Soporte / General
- Cliente / Proveedor / Interno

---

## 🔧 Cómo Usar una Plantilla

### Paso 1: Seleccionar Plantilla

1. Abre el dashboard (`python main.py`)
2. Ve a la pestaña **"📚 Plantillas"**
3. Navega por categorías o explora todas
4. Haz clic en **"Usar esta plantilla"**

### Paso 2: Configurar Conexiones

Tienes dos opciones:

**Opción A: Usar Conexiones Guardadas (Recomendado)**
1. Ve a la pestaña **"🔌 Conexiones"**
2. Crea conexiones para los servicios que necesitas
3. Vuelve a "Plantillas" y selecciónalas del menú desplegable

**Opción B: Ingresar Manualmente**
1. Selecciona **[Manual]** en el selector de conexiones
2. Ingresa las credenciales directamente en los campos

### Paso 3: Configurar Parámetros

- **Filtros**: Define criterios de filtrado (opcional)
- **Límites**: Establece máximo de correos a procesar
- **Opciones específicas**: Según la plantilla seleccionada

### Paso 4: Ejecutar

1. Haz clic en **"Ejecutar Plantilla"**
2. Observa el progreso en tiempo real
3. Revisa los resultados y logs

### Paso 5: Revisar Resultados

- **Estado**: Muestra si la ejecución fue exitosa
- **Resultado**: Información sobre archivos generados
- **Registro**: Detalles de cada paso ejecutado

---

## 💡 Tips y Mejores Prácticas

### 🔐 Seguridad

- **Usa conexiones guardadas** en lugar de ingresar credenciales manualmente cada vez
- **Para Gmail**: Usa contraseñas de aplicación, no tu contraseña principal
- **API Keys**: Nunca compartas tus API keys públicamente
- El archivo `connections.json` está en `.gitignore` por defecto

### ⚡ Rendimiento

- **Empieza con pocos correos** (10-20) para pruebas
- **Usa filtros** para procesar solo los correos relevantes
- **Para IA**: Modelos más grandes son más precisos pero más lentos
- **Webhooks**: Configura timeouts apropiados

### 🎯 Casos de Uso Reales

#### Caso 1: Facturación Automática
```
Plantilla: Email to Excel
Filtro por asunto: factura, invoice
Resultado: Excel con todas las facturas recibidas
```

#### Caso 2: Soporte al Cliente
```
Plantilla: AI Email Classification
Clasificar por: Urgente/Normal/Bajo
Resultado: Correos clasificados para priorizar
```

#### Caso 3: Integración con Slack
```
Plantilla: Email to Webhook
Webhook: Slack Incoming Webhook
Resultado: Notificaciones en Slack de correos importantes
```

#### Caso 4: Backup en Drive
```
Plantilla: Email to Google Drive
Frecuencia: Diaria
Resultado: Backup automático en Google Drive
```

---

## 🆕 Próximas Plantillas

Estamos trabajando en más plantillas:

- 📨 **Auto-responder**: Respuestas automáticas con IA
- 📊 **Email Analytics**: Dashboard de estadísticas de correos
- 🔄 **Email Sync**: Sincronización entre múltiples cuentas
- 📅 **Calendar Integration**: Crear eventos desde correos
- 💬 **Sentiment Analysis**: Análisis de sentimiento en correos
- 🌍 **Multi-language**: Traducción automática de correos

---

## 🤝 Crear Tus Propias Plantillas

¿Tienes una idea para una plantilla? Puedes:

1. **Crear un escenario personalizado** en la pestaña "🎬 Escenarios"
2. **Contribuir al proyecto** con tu plantilla
3. **Solicitar una plantilla** en los Issues de GitHub

### Estructura de una Plantilla

```python
from src.templates.template_library import Template

class MiPlantilla(Template):
    def __init__(self):
        super().__init__(
            name="Mi Plantilla",
            description="Descripción de lo que hace",
            category="Categoría"
        )
        self.icon = "🎯"
        self.required_connections = ['email', 'otro']
        
        # Inicializar agentes
        self.agent1 = Agent1()
        self.agent2 = Agent2()
    
    def configure(self, config):
        # Configurar agentes
        self.agent1.configure(**config)
        
        # Añadir al orquestador
        self.orchestrator.add_agent(self.agent1)
        self.orchestrator.add_agent(self.agent2)
```

---

## ❓ FAQ

### ¿Puedo modificar una plantilla?

Sí, las plantillas son un punto de partida. Puedes crear escenarios personalizados basados en ellas.

### ¿Las plantillas funcionan con cualquier proveedor de email?

Sí, siempre que soporten IMAP (Gmail, Outlook, etc.).

### ¿Necesito pagar por usar IA?

Depende del proveedor:
- **Modelo Local**: Gratis (próximamente)
- **OpenAI**: Requiere API key de pago
- **Claude**: Requiere API key de pago
- **Gemini**: Requiere API key (tiene tier gratuito)

### ¿Puedo ejecutar plantillas automáticamente?

Por ahora es manual. Estamos trabajando en scheduling automático.

### ¿Las conexiones son seguras?

Las conexiones se guardan localmente en tu máquina en `connections.json`. El archivo está excluido de git por seguridad.

---

## 📞 Soporte

- **Documentación**: Ver `DOCUMENTATION.md`
- **Inicio Rápido**: Ver `QUICKSTART.md`
- **Issues**: [GitHub Issues](https://github.com/Weryyy/Repuesta-Automatica-Mails/issues)
- **Demo**: Ejecuta `python demo.py` para una demostración sin credenciales
