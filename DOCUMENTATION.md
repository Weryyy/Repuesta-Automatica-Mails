# 📘 Documentación Técnica

## Arquitectura del Sistema

### Visión General

El sistema de automatización de correos está basado en una arquitectura modular de agentes que pueden ser orquestados para crear flujos de trabajo complejos. Esta arquitectura está inspirada en plataformas como Make.com.

```
┌─────────────────────────────────────────────────────────┐
│                    Dashboard (Panel)                     │
│              Interfaz Web del Usuario                    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator                          │
│          Gestiona la ejecución de agentes                │
└──────────┬────────────┬────────────┬────────────────────┘
           │            │            │
           ▼            ▼            ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │  Agent 1 │ │  Agent 2 │ │  Agent 3 │
    │  (Read)  │ │ (Filter) │ │ (Export) │
    └──────────┘ └──────────┘ └──────────┘
```

### Componentes Principales

#### 1. Agentes (Agents)

Los agentes son componentes modulares e independientes que realizan tareas específicas.

**BaseAgent**: Clase abstracta base
- Define la interfaz común para todos los agentes
- Métodos principales: `execute()`, `get_status()`, `get_output()`

**EmailReaderAgent**: Lee correos electrónicos
- Conecta a servidores IMAP (Gmail, Outlook, etc.)
- Lee correos de carpetas específicas
- Soporta filtrado por estado (leído/no leído)
- Retorna lista de correos con metadata

**EmailFilterAgent**: Filtra correos
- Filtra por palabras clave en asunto
- Filtra por remitente
- Filtra por contenido del cuerpo
- Soporta múltiples criterios simultáneos

**ExcelWriterAgent**: Exporta a Excel
- Convierte datos de correos a formato Excel
- Genera nombres de archivo automáticos
- Configurable folder de salida

#### 2. Orquestador (Orchestrator)

El orquestador gestiona la ejecución secuencial de múltiples agentes:

```python
orchestrator = Orchestrator("Mi Escenario")
orchestrator.add_agent(agent1)
orchestrator.add_agent(agent2)
orchestrator.add_agent(agent3)
result = orchestrator.execute(initial_input)
```

**Características:**
- Ejecución secuencial: La salida de cada agente se pasa como entrada al siguiente
- Logging automático: Registra cada paso de la ejecución
- Manejo de errores: Detiene la ejecución si un agente falla
- Estado centralizado: Mantiene el estado de toda la pipeline

#### 3. Escenarios (Scenarios)

Los escenarios son configuraciones predefinidas de agentes y orquestadores:

**EmailToExcelScenario**: Escenario de ejemplo
- Combina EmailReader → EmailFilter → ExcelWriter
- Configuración simplificada para el usuario
- Parámetros personalizables

#### 4. Dashboard (Web Interface)

Interfaz web construida con Panel (Holoviz):
- Selección de escenarios
- Formularios de configuración
- Visualización de resultados
- Logs de ejecución en tiempo real

## Flujo de Datos

### Ejemplo: Email a Excel

1. **Usuario configura en Dashboard:**
   ```
   Email: usuario@gmail.com
   Password: ****
   Filtro: "factura"
   ```

2. **Dashboard crea y configura el escenario:**
   ```python
   scenario = EmailToExcelScenario()
   scenario.configure(config)
   ```

3. **Escenario prepara el orquestador:**
   ```python
   orchestrator.add_agent(email_reader)
   orchestrator.add_agent(email_filter)
   orchestrator.add_agent(excel_writer)
   ```

4. **Ejecución del orquestador:**
   ```
   Input: {'max_emails': 10}
   ↓
   EmailReader → Lista de 10 correos
   ↓
   EmailFilter → Lista de 2 correos (con "factura")
   ↓
   ExcelWriter → Archivo Excel generado
   ↓
   Output: "output/emails_20250210_153000.xlsx"
   ```

## Extendiendo el Sistema

### Añadir un Nuevo Agente

```python
from src.agents.base_agent import BaseAgent

class MiNuevoAgente(BaseAgent):
    def __init__(self, name: str = "MiAgente"):
        super().__init__(name)
        self.config = {}
    
    def configure(self, **kwargs):
        """Configurar el agente"""
        self.config = kwargs
    
    def execute(self, input_data):
        """Lógica principal del agente"""
        self.status = "executing"
        
        try:
            # Tu lógica aquí
            result = self._procesar(input_data)
            
            self.status = "completed"
            self.output = result
            return result
            
        except Exception as e:
            self.status = f"error: {str(e)}"
            return None
    
    def get_config_schema(self):
        """Describir la configuración necesaria"""
        return {
            'param1': 'descripción del parámetro 1',
            'param2': 'descripción del parámetro 2'
        }
```

### Crear un Nuevo Escenario

```python
from src.orchestrator import Orchestrator

class MiNuevoEscenario:
    def __init__(self):
        self.name = "Mi Nuevo Escenario"
        self.description = "Descripción del escenario"
        self.orchestrator = Orchestrator(self.name)
        
        # Inicializar agentes
        self.agent1 = Agent1()
        self.agent2 = Agent2()
    
    def configure(self, config):
        """Configurar el escenario"""
        self.agent1.configure(**config['agent1'])
        self.agent2.configure(**config['agent2'])
        
        # Añadir al orquestador
        self.orchestrator.clear_agents()
        self.orchestrator.add_agent(self.agent1)
        self.orchestrator.add_agent(self.agent2)
    
    def execute(self, params=None):
        """Ejecutar el escenario"""
        return self.orchestrator.execute(params)
```

## Mejores Prácticas

### Diseño de Agentes

1. **Un Agente = Una Responsabilidad**
   - Cada agente debe hacer una sola cosa bien
   - No mezclar múltiples funcionalidades en un agente

2. **Entrada y Salida Clara**
   - Documentar qué tipo de datos espera el agente
   - Documentar qué tipo de datos produce

3. **Manejo de Errores**
   - Siempre usar try/except en execute()
   - Actualizar self.status con información del error
   - No propagar excepciones, retornar None o lista vacía

4. **Estado Observable**
   - Mantener self.status actualizado
   - Guardar self.output para inspección posterior

### Diseño de Escenarios

1. **Reutilización de Agentes**
   - Usar agentes existentes cuando sea posible
   - Solo crear nuevos agentes cuando sea necesario

2. **Configuración Flexible**
   - Permitir parámetros opcionales con valores por defecto
   - Validar configuración antes de ejecutar

3. **Documentación Clara**
   - Describir qué hace el escenario
   - Listar parámetros requeridos y opcionales

## Seguridad

### Credenciales

- **NUNCA** hardcodear credenciales en el código
- Usar variables de entorno o .env
- .env debe estar en .gitignore

### Gmail

Para Gmail se requiere:
1. Activar verificación en 2 pasos
2. Generar contraseña de aplicación
3. Usar la contraseña de aplicación, no la contraseña normal

### Permisos IMAP

Asegurarse de que IMAP está habilitado en la cuenta de correo:
- Gmail: Configuración → Ver toda la configuración → Reenvío y correo POP/IMAP
- Outlook: Similar en configuración de la cuenta

## Troubleshooting

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Authentication failed"
- Verificar credenciales
- Para Gmail, usar contraseña de aplicación
- Verificar que IMAP está habilitado

### Error: "Connection refused"
- Verificar servidor IMAP y puerto
- Gmail: imap.gmail.com:993
- Outlook: outlook.office365.com:993

### Dashboard no se abre
```bash
# Verificar que el puerto 5006 está libre
lsof -i :5006

# Si está ocupado, usar otro puerto
python -c "from src.dashboard import Dashboard; Dashboard().serve(port=5007)"
```

## Performance

### Optimizaciones

1. **Limitar cantidad de correos**
   - Usar max_emails para limitar correos leídos
   - Filtrar en el servidor cuando sea posible

2. **Batch Processing**
   - Procesar correos en lotes si hay muchos
   - Usar chunks en pandas para Excel grandes

3. **Cache**
   - Considerar cachear resultados de lectura
   - Evitar releer los mismos correos múltiples veces

## Testing

### Demo Script

El proyecto incluye `demo.py` para testing sin credenciales reales:

```bash
python demo.py
```

Este script:
- Crea datos de correos ficticios
- Ejecuta el pipeline completo
- Genera un archivo Excel de prueba

### Testing Manual

1. Configurar .env con credenciales de test
2. Ejecutar main.py
3. Usar el dashboard para probar escenarios
4. Verificar archivos Excel generados

## Roadmap Futuro

### Funcionalidades Planeadas

- [ ] Más agentes: Respuesta automática, Clasificación con IA
- [ ] Más escenarios: Respuestas automáticas, Análisis de sentimiento
- [ ] Base de datos: Almacenar historial de ejecuciones
- [ ] Scheduler: Ejecutar escenarios automáticamente
- [ ] API REST: Integración con otros sistemas
- [ ] Webhooks: Notificaciones en tiempo real
- [ ] Multi-idioma: Soporte para más idiomas

### Integraciones Futuras

- Microsoft 365
- Slack
- Google Sheets
- APIs de terceros
- Bases de datos SQL/NoSQL
