"""
Dashboard - Web interface for the email automation system using Panel (holoviz).
"""
import panel as pn
from typing import Dict, Any
from ..scenarios import EmailToExcelScenario
from ..scenarios.email_to_drive_scenario import EmailToDriveScenario
from ..scenarios.email_ai_analysis_scenario import EmailAIAnalysisScenario
from ..utils.connection_manager import ConnectionManager
from .connections_dashboard import ConnectionsDashboard
from .templates_dashboard import TemplatesDashboard


class Dashboard:
    """Main dashboard for the email automation system."""
    
    def __init__(self):
        """Initialize the dashboard."""
        pn.extension()
        
        # Initialize connection manager
        self.connection_manager = ConnectionManager()
        
        # Initialize sub-dashboards
        self.connections_dashboard = ConnectionsDashboard(self.connection_manager)
        self.templates_dashboard = TemplatesDashboard(self.connection_manager)
        
        self.scenario = None
        self.execution_result = None
        
        # Widgets for user input
        self.scenario_select = pn.widgets.Select(
            name='Escenario',
            options=[
                'Email a Excel',
                'Email a Google Drive',
                'Email con Análisis IA'
            ],
            value='Email a Excel'
        )
        
        # Connection selector
        self.connection_select = pn.widgets.Select(
            name='Seleccionar Conexión de Email',
            options=self._get_email_connections(),
            value=None
        )
        
        self.email_input = pn.widgets.TextInput(
            name='Correo Electrónico (o usa una conexión)',
            placeholder='tu_email@ejemplo.com'
        )
        
        self.password_input = pn.widgets.PasswordInput(
            name='Contraseña',
            placeholder='Contraseña o contraseña de aplicación'
        )
        
        self.imap_server_input = pn.widgets.TextInput(
            name='Servidor IMAP',
            value='imap.gmail.com'
        )
        
        self.max_emails_input = pn.widgets.IntInput(
            name='Máximo de correos',
            value=10,
            start=1,
            end=100
        )
        
        self.filter_subject_input = pn.widgets.TextInput(
            name='Filtrar por asunto (palabras clave, separadas por coma)',
            placeholder='ejemplo: factura, pedido'
        )
        
        self.filter_from_input = pn.widgets.TextInput(
            name='Filtrar por remitente (palabras clave, separadas por coma)',
            placeholder='ejemplo: cliente@ejemplo.com'
        )
        
        # AI configuration (shown conditionally)
        self.ai_provider_select = pn.widgets.Select(
            name='Proveedor de IA',
            options=['Modelo Local', 'OpenAI', 'Anthropic', 'Gemini'],
            value='Modelo Local',
            visible=False
        )
        
        self.ai_connection_select = pn.widgets.Select(
            name='Conexión de IA',
            options=self._get_ai_connections(),
            visible=False
        )
        
        # Google Drive configuration (shown conditionally)
        self.drive_connection_select = pn.widgets.Select(
            name='Conexión de Google Drive',
            options=self._get_drive_connections(),
            visible=False
        )
        
        self.execute_button = pn.widgets.Button(
            name='Ejecutar Escenario',
            button_type='primary'
        )
        self.execute_button.on_click(self._execute_scenario)
        
        self.refresh_button = pn.widgets.Button(
            name='🔄 Actualizar Conexiones',
            button_type='default'
        )
        self.refresh_button.on_click(self._refresh_connections)
        
        # Output displays
        self.status_pane = pn.pane.Markdown("### Estado\nListo para ejecutar.")
        self.log_pane = pn.pane.JSON({}, name='Registro de Ejecución', depth=2)
        self.result_pane = pn.pane.Markdown("### Resultado\nNo se ha ejecutado ningún escenario aún.")
        
        # Watch for scenario changes
        self.scenario_select.param.watch(self._update_scenario_fields, 'value')
        self.connection_select.param.watch(self._load_connection_credentials, 'value')
    
    def _get_email_connections(self):
        """Get list of email connections."""
        connections = self.connection_manager.list_connections('email')
        options = ['[Manual]'] + [c['name'] for c in connections]
        return options
    
    def _get_ai_connections(self):
        """Get list of AI connections."""
        connections = self.connection_manager.list_connections()
        ai_connections = [c for c in connections if c['service_type'] in ['openai', 'anthropic', 'gemini', 'local_model']]
        options = ['[Manual]'] + [c['name'] for c in ai_connections]
        return options
    
    def _get_drive_connections(self):
        """Get list of Google Drive connections."""
        connections = self.connection_manager.list_connections('google_drive')
        options = ['[Manual]'] + [c['name'] for c in connections]
        return options
    
    def _refresh_connections(self, event=None):
        """Refresh connection lists."""
        self.connection_select.options = self._get_email_connections()
        self.ai_connection_select.options = self._get_ai_connections()
        self.drive_connection_select.options = self._get_drive_connections()
        self.status_pane.object = "### Estado\n✅ Conexiones actualizadas."
    
    def _update_scenario_fields(self, event):
        """Update visible fields based on selected scenario."""
        scenario = self.scenario_select.value
        
        # Show/hide AI fields
        if scenario == 'Email con Análisis IA':
            self.ai_provider_select.visible = True
            self.ai_connection_select.visible = True
        else:
            self.ai_provider_select.visible = False
            self.ai_connection_select.visible = False
        
        # Show/hide Drive fields
        if scenario == 'Email a Google Drive':
            self.drive_connection_select.visible = True
        else:
            self.drive_connection_select.visible = False
    
    def _load_connection_credentials(self, event):
        """Load credentials from selected connection."""
        selected = self.connection_select.value
        if not selected or selected == '[Manual]':
            return
        
        credentials = self.connection_manager.get_credentials(selected)
        if credentials:
            self.email_input.value = credentials.get('email_address', '')
            self.password_input.value = credentials.get('password', '')
            self.imap_server_input.value = credentials.get('imap_server', 'imap.gmail.com')
            self.status_pane.object = f"### Estado\n✅ Credenciales cargadas desde '{selected}'"
    
    def _execute_scenario(self, event):
        """Execute the selected scenario."""
        try:
            # Update status
            self.status_pane.object = "### Estado\n⏳ Ejecutando..."
            
            # Get user inputs
            email = self.email_input.value
            password = self.password_input.value
            
            if not email or not password:
                self.status_pane.object = "### Estado\n❌ Error: Por favor ingresa email y contraseña."
                return
            
            # Parse filter criteria
            filter_criteria = {}
            if self.filter_subject_input.value:
                filter_criteria['subject_contains'] = [
                    s.strip() for s in self.filter_subject_input.value.split(',')
                ]
            if self.filter_from_input.value:
                filter_criteria['from_contains'] = [
                    s.strip() for s in self.filter_from_input.value.split(',')
                ]
            
            # Create and configure scenario based on selection
            scenario_name = self.scenario_select.value
            
            if scenario_name == 'Email a Excel':
                self.scenario = EmailToExcelScenario()
                self.scenario.configure({
                    'email_address': email,
                    'email_password': password,
                    'imap_server': self.imap_server_input.value,
                    'filter_criteria': filter_criteria,
                    'output_folder': 'output'
                })
            
            elif scenario_name == 'Email a Google Drive':
                # Get Drive connection
                drive_conn_name = self.drive_connection_select.value
                drive_creds = None
                if drive_conn_name and drive_conn_name != '[Manual]':
                    drive_creds = self.connection_manager.get_credentials(drive_conn_name)
                
                self.scenario = EmailToDriveScenario()
                self.scenario.configure({
                    'email_address': email,
                    'email_password': password,
                    'imap_server': self.imap_server_input.value,
                    'filter_criteria': filter_criteria,
                    'output_folder': 'output',
                    'drive_credentials': drive_creds.get('credentials_file') if drive_creds else None,
                    'drive_folder_id': drive_creds.get('folder_id') if drive_creds else None
                })
            
            elif scenario_name == 'Email con Análisis IA':
                # Get AI connection
                ai_conn_name = self.ai_connection_select.value
                ai_creds = None
                ai_provider = 'local'
                
                if ai_conn_name and ai_conn_name != '[Manual]':
                    ai_connection = self.connection_manager.get_connection(ai_conn_name)
                    if ai_connection:
                        ai_provider = ai_connection['service_type']
                        ai_creds = ai_connection['credentials']
                
                self.scenario = EmailAIAnalysisScenario()
                self.scenario.configure({
                    'email_address': email,
                    'email_password': password,
                    'imap_server': self.imap_server_input.value,
                    'filter_criteria': filter_criteria,
                    'output_folder': 'output',
                    'ai_provider': ai_provider,
                    'ai_api_key': ai_creds.get('api_key') if ai_creds else None,
                    'ai_model': ai_creds.get('model') if ai_creds else None
                })
            
            # Execute scenario
            self.execution_result = self.scenario.execute({
                'max_emails': self.max_emails_input.value
            })
            
            # Update displays
            if self.execution_result['status'] == 'completed':
                self.status_pane.object = "### Estado\n✅ Escenario completado exitosamente!"
                
                # Show result
                output_file = self.execution_result.get('output', 'N/A')
                self.result_pane.object = f"""### Resultado
                
**Archivo generado:** `{output_file}`

**Resumen de ejecución:**
- Total de pasos: {len(self.execution_result['logs'])}
- Estado final: {self.execution_result['status']}
"""
            else:
                self.status_pane.object = f"### Estado\n❌ Error: {self.execution_result['status']}"
            
            # Update log
            self.log_pane.object = self.execution_result['logs']
            
        except Exception as e:
            self.status_pane.object = f"### Estado\n❌ Error: {str(e)}"
            self.result_pane.object = f"### Resultado\nError durante la ejecución: {str(e)}"
    
    def create_layout(self):
        """Create the dashboard layout."""
        # Header
        header = pn.pane.Markdown("""
        # 📧 Sistema de Automatización de Correos
        ## Aplicación estilo Make.com
        
        Esta aplicación te permite automatizar la lectura, filtrado y procesamiento de correos electrónicos con integración de IA, webhooks y servicios externos.
        """, styles={'background-color': '#f0f0f0', 'padding': '20px', 'border-radius': '5px'})
        
        # Instructions
        instructions = pn.pane.Markdown("""
        ### Instrucciones:
        1. **Gestiona tus conexiones** en la pestaña "Conexiones"
        2. Selecciona un escenario de automatización
        3. Configura los parámetros requeridos o selecciona una conexión existente
        4. Haz clic en "Ejecutar Escenario"
        5. Revisa los resultados y archivos generados
        
        **Escenarios disponibles:**
        - 📊 **Email a Excel**: Lee, filtra y exporta correos a Excel
        - ☁️ **Email a Google Drive**: Exporta correos a Google Drive
        - 🤖 **Email con Análisis IA**: Analiza correos con IA (OpenAI, Claude, Gemini)
        """)
        
        # Configuration panel
        config_panel = pn.Column(
            "## Configuración del Escenario",
            self.scenario_select,
            pn.pane.Markdown("### Conexión de Email"),
            self.connection_select,
            self.refresh_button,
            self.email_input,
            self.password_input,
            self.imap_server_input,
            self.max_emails_input,
            pn.pane.Markdown("### Filtros (opcional)"),
            self.filter_subject_input,
            self.filter_from_input,
            pn.pane.Markdown("### Configuración Adicional"),
            self.ai_provider_select,
            self.ai_connection_select,
            self.drive_connection_select,
            self.execute_button,
            styles={'background-color': '#ffffff', 'padding': '20px', 'border-radius': '5px'},
            scroll=True,
            height=600
        )
        
        # Results panel
        results_panel = pn.Column(
            self.status_pane,
            self.result_pane,
            "## Registro de Ejecución",
            self.log_pane,
            styles={'background-color': '#ffffff', 'padding': '20px', 'border-radius': '5px'},
            scroll=True,
            height=600
        )
        
        # Create scenarios tab
        scenarios_tab = pn.Column(
            instructions,
            pn.Row(
                config_panel,
                results_panel
            )
        )
        
        # Create connections tab
        connections_tab = self.connections_dashboard.create_layout()
        
        # Create templates tab
        templates_tab = self.templates_dashboard.create_layout()
        
        # Create tabs
        tabs = pn.Tabs(
            ('📚 Plantillas', templates_tab),
            ('🎬 Escenarios', scenarios_tab),
            ('🔌 Conexiones', connections_tab)
        )
        
        # Main layout
        layout = pn.Column(
            header,
            tabs
        )
        
        return layout
    
    def serve(self, port: int = 5006, show: bool = True):
        """
        Start the dashboard server.
        
        Args:
            port: Port number to serve on
            show: Whether to open browser automatically
        """
        layout = self.create_layout()
        pn.serve(layout, port=port, show=show, title='Email Automation System')
