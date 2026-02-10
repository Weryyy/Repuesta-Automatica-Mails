"""
Dashboard - Web interface for the email automation system using Panel (holoviz).
"""
import panel as pn
from typing import Dict, Any
from ..scenarios import EmailToExcelScenario


class Dashboard:
    """Main dashboard for the email automation system."""
    
    def __init__(self):
        """Initialize the dashboard."""
        pn.extension()
        
        self.scenario = None
        self.execution_result = None
        
        # Widgets for user input
        self.scenario_select = pn.widgets.Select(
            name='Escenario',
            options=['Email a Excel'],
            value='Email a Excel'
        )
        
        self.email_input = pn.widgets.TextInput(
            name='Correo Electrónico',
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
        
        self.execute_button = pn.widgets.Button(
            name='Ejecutar Escenario',
            button_type='primary'
        )
        self.execute_button.on_click(self._execute_scenario)
        
        # Output displays
        self.status_pane = pn.pane.Markdown("### Estado\nListo para ejecutar.")
        self.log_pane = pn.pane.JSON({}, name='Registro de Ejecución', depth=2)
        self.result_pane = pn.pane.Markdown("### Resultado\nNo se ha ejecutado ningún escenario aún.")
    
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
            
            # Create and configure scenario
            self.scenario = EmailToExcelScenario()
            self.scenario.configure({
                'email_address': email,
                'email_password': password,
                'imap_server': self.imap_server_input.value,
                'filter_criteria': filter_criteria,
                'output_folder': 'output'
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
        
        Esta aplicación te permite automatizar la lectura, filtrado y procesamiento de correos electrónicos.
        """, styles={'background-color': '#f0f0f0', 'padding': '20px', 'border-radius': '5px'})
        
        # Instructions
        instructions = pn.pane.Markdown("""
        ### Instrucciones:
        1. Selecciona un escenario de automatización
        2. Configura los parámetros requeridos
        3. Haz clic en "Ejecutar Escenario"
        4. Revisa los resultados y el archivo Excel generado
        
        **Nota:** Para Gmail, necesitarás usar una contraseña de aplicación en lugar de tu contraseña regular.
        """)
        
        # Configuration panel
        config_panel = pn.Column(
            "## Configuración del Escenario",
            self.scenario_select,
            self.email_input,
            self.password_input,
            self.imap_server_input,
            self.max_emails_input,
            pn.pane.Markdown("### Filtros (opcional)"),
            self.filter_subject_input,
            self.filter_from_input,
            self.execute_button,
            styles={'background-color': '#ffffff', 'padding': '20px', 'border-radius': '5px'}
        )
        
        # Results panel
        results_panel = pn.Column(
            self.status_pane,
            self.result_pane,
            "## Registro de Ejecución",
            self.log_pane,
            styles={'background-color': '#ffffff', 'padding': '20px', 'border-radius': '5px'}
        )
        
        # Main layout
        layout = pn.Column(
            header,
            instructions,
            pn.Row(
                config_panel,
                results_panel
            )
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
