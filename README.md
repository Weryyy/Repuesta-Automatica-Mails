# 📧 Sistema de Automatización de Correos

App basada en el concepto de make.com para automatizar la lectura, filtrado y procesamiento de correos electrónicos con integración de IA, webhooks y múltiples servicios.

## 🎯 Características

- **Dashboard Web Interactivo**: Interfaz gráfica usando Panel (Holoviz) accesible desde el navegador
- **Sistema de Plantillas**: Plantillas predefinidas estilo Make.com listas para usar
- **Arquitectura de Agentes**: Sistema modular con múltiples agentes especializados
- **Skills (Habilidades)**: Agentes con habilidades entreñables y mejorables
- **Orquestador por Escenario**: Gestión inteligente de flujos de trabajo
- **Gestor de Conexiones**: Gestiona credenciales para múltiples servicios de forma segura
- **Webhooks**: Comunica con sistemas externos mediante HTTP
- **Integraciones IA**: OpenAI, Anthropic Claude, Google Gemini y modelos locales
- **Google Drive**: Sube archivos directamente a Drive
- **⚡ HPC (High-Performance Computing)**: Optimizaciones con RAPIDS, CUDA, XGBoost, xarray
- **Procesamiento Paralelo**: Multi-threading y multi-processing automático
- **Escenarios Configurables**: Flujos de automatización personalizables según tus necesidades

## 📚 Plantillas Disponibles

### 📊 Email
- **Email to Excel**: Lee y filtra correos, exporta a Excel
- **Email to Webhook**: Envía correos filtrados a un webhook

### ☁️ Integración
- **Email to Google Drive**: Exporta correos a Google Drive
- **Email to Webhook**: Notifica sistemas externos

### 🤖 IA
- **Email AI Summary**: Resumen inteligente de correos con IA
- **AI Email Classification**: Clasifica correos automáticamente con IA

## 🔌 Conexiones Soportadas

- **Email (IMAP)**: Gmail, Outlook, y otros servidores IMAP
- **Google Drive**: Almacenamiento en la nube
- **Webhooks**: Integración con cualquier API HTTP
- **OpenAI**: GPT-3.5, GPT-4
- **Anthropic**: Claude 3 (Sonnet, Opus)
- **Google Gemini**: Gemini Pro
- **Modelos Locales**: Ollama, LM Studio (próximamente)

## 🚀 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- (Opcional) NVIDIA GPU con CUDA para aceleración HPC

### Pasos de Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/Weryyy/Repuesta-Automatica-Mails.git
cd Repuesta-Automatica-Mails
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. (Opcional) Verifica configuración HPC:
```bash
python hpc_info.py
```

4. (Opcional) Configura tus credenciales:
```bash
cp .env.example .env
# Edita .env con tus credenciales
```

## 💻 Uso

### Iniciar la Aplicación

Para iniciar el dashboard web:

```bash
python main.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:5006`

### Configuración para Gmail

Si usas Gmail, necesitarás:
1. Activar la verificación en dos pasos en tu cuenta de Google
2. Generar una "contraseña de aplicación" específica
3. Usar esta contraseña de aplicación en lugar de tu contraseña regular

[Instrucciones para generar contraseña de aplicación](https://support.google.com/accounts/answer/185833)

## 🏗️ Arquitectura

### Componentes Principales

```
src/
├── agents/               # Agentes especializados
│   ├── base_agent.py    # Clase base para agentes
│   ├── email_reader_agent.py    # Lee correos del servidor IMAP
│   ├── email_filter_agent.py    # Filtra correos según criterios
│   └── excel_writer_agent.py    # Exporta datos a Excel
├── orchestrator/         # Orquestador de flujos
│   └── orchestrator.py  # Gestiona la ejecución de agentes
├── scenarios/            # Escenarios predefinidos
│   └── email_to_excel_scenario.py
└── dashboard/            # Interfaz web
    └── dashboard.py     # Dashboard con Panel
```

### Agentes Disponibles

1. **EmailReaderAgent**: Lee correos electrónicos de un servidor IMAP
2. **EmailFilterAgent**: Filtra correos según criterios (asunto, remitente, contenido)
3. **ExcelWriterAgent**: Exporta los correos filtrados a un archivo Excel

### Escenarios

#### Email a Excel (Implementado)
Este escenario:
1. Lee correos electrónicos de tu cuenta
2. Filtra los correos según criterios opcionales
3. Exporta los correos filtrados a un archivo Excel

## 📝 Ejemplo de Uso

### Opción 1: Usar Plantillas (Recomendado)

1. Abre el dashboard (`python main.py`)
2. Ve a la pestaña "📚 Plantillas"
3. Explora las plantillas disponibles
4. Haz clic en "Usar esta plantilla"
5. Configura las conexiones necesarias
6. Haz clic en "Ejecutar Plantilla"

### Opción 2: Escenarios Personalizados

1. Ve a la pestaña "🔌 Conexiones"
2. Crea conexiones para los servicios que usarás
3. Ve a la pestaña "🎬 Escenarios"
4. Selecciona un escenario y configura
5. Ejecuta el escenario

### Ejemplo: Exportar Facturas a Excel

1. **Plantilla**: Email to Excel
2. **Configuración**:
   - Conexión de email o ingresa credenciales
   - Filtrar por asunto: "factura, invoice"
   - Máximo de correos: 50
3. **Resultado**: Archivo Excel con facturas en `output/`

## 🔧 Desarrollo

### Añadir Nuevos Agentes

Para crear un nuevo agente:

```python
from src.agents.base_agent import BaseAgent

class MiNuevoAgente(BaseAgent):
    def __init__(self, name: str = "MiAgente"):
        super().__init__(name)
    
    def execute(self, input_data):
        # Tu lógica aquí
        return resultado
```

### Crear Nuevos Escenarios

Para crear un nuevo escenario:

```python
from src.scenarios import EmailToExcelScenario

class MiNuevoEscenario:
    def __init__(self):
        self.name = "Mi Escenario"
        self.orchestrator = Orchestrator(self.name)
        # Configura tus agentes
```

## 🛡️ Seguridad

- **Nunca** commitas credenciales en el repositorio
- Usa el archivo `.env` para configuración local
- Para Gmail, usa contraseñas de aplicación en lugar de tu contraseña real
- Los archivos de salida están en `.gitignore` por defecto

## 📋 Dependencias Principales

- **panel**: Framework para crear dashboards web interactivos
- **holoviews**: Visualización de datos
- **openpyxl**: Manejo de archivos Excel
- **pandas**: Análisis y manipulación de datos

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT.

## 🙏 Agradecimientos

- Inspirado en Make.com
- Construido con Holoviz/Panel
- Comunidad de Python
