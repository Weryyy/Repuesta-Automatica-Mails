"""
Templates Dashboard - Browse and use predefined templates like Make.com
"""
import panel as pn
from typing import Dict, Any
from ..templates import TemplateLibrary
from ..utils.connection_manager import ConnectionManager


class TemplatesDashboard:
    """Dashboard for browsing and using templates."""
    
    def __init__(self, connection_manager: ConnectionManager):
        """Initialize the templates dashboard."""
        self.connection_manager = connection_manager
        self.template_library = TemplateLibrary()
        self.selected_template = None
        self.execution_result = None
        
        # Category filter
        categories = ['Todas'] + self.template_library.get_categories()
        self.category_filter = pn.widgets.Select(
            name='Categoría',
            options=categories,
            value='Todas'
        )
        self.category_filter.param.watch(self._update_templates_grid, 'value')
        
        # Templates grid
        self.templates_grid = pn.GridBox(ncols=3)
        self._update_templates_grid(None)
        
        # Configuration panel
        self.config_panel = pn.Column(
            pn.pane.Markdown("### Configuración\nSelecciona una plantilla para comenzar."),
            visible=False
        )
        
        # Execution panel
        self.execute_button = pn.widgets.Button(
            name='Ejecutar Plantilla',
            button_type='primary',
            visible=False
        )
        self.execute_button.on_click(self._execute_template)
        
        self.status_pane = pn.pane.Markdown("### Estado\nListo.")
        self.result_pane = pn.pane.Markdown("### Resultado\nNo se ha ejecutado ninguna plantilla.")
        self.log_pane = pn.pane.JSON({}, depth=2)
    
    def _update_templates_grid(self, event):
        """Update the templates grid based on category filter."""
        category = self.category_filter.value
        category = None if category == 'Todas' else category
        
        templates = self.template_library.list_templates(category)
        
        self.templates_grid.clear()
        
        for template_info in templates:
            card = self._create_template_card(template_info)
            self.templates_grid.append(card)
    
    def _create_template_card(self, template_info: Dict[str, Any]):
        """Create a card for a template."""
        card_content = f"""
### {template_info['icon']} {template_info['name']}

{template_info['description']}

**Categoría:** {template_info['category']}  
**Conexiones requeridas:** {', '.join(template_info['required_connections'])}
"""
        
        select_button = pn.widgets.Button(
            name='Usar esta plantilla',
            button_type='success',
            width=200
        )
        
        # Store template_id in the button
        template_id = template_info['id']
        select_button.on_click(lambda event: self._select_template(template_id))
        
        card = pn.Card(
            pn.pane.Markdown(card_content),
            select_button,
            title=f"{template_info['icon']} {template_info['name']}",
            collapsed=False,
            styles={
                'background': '#ffffff',
                'border': '1px solid #ddd',
                'border-radius': '8px',
                'padding': '15px'
            }
        )
        
        return card
    
    def _select_template(self, template_id: str):
        """Select a template and show its configuration."""
        self.selected_template = self.template_library.get_template(template_id)
        
        if not self.selected_template:
            return
        
        # Show configuration panel
        self.config_panel.clear()
        self.config_panel.visible = True
        self.execute_button.visible = True
        
        # Add configuration fields based on template requirements
        self.config_panel.append(
            pn.pane.Markdown(f"## Configurar: {self.selected_template.name}")
        )
        
        # Email connection (most templates need this)
        if 'email' in self.selected_template.required_connections:
            email_connections = self.connection_manager.list_connections('email')
            connection_options = ['[Manual]'] + [c['name'] for c in email_connections]
            
            self.config_panel.extend([
                pn.pane.Markdown("### Conexión de Email"),
                pn.widgets.Select(
                    name='Conexión',
                    options=connection_options,
                    value='[Manual]'
                ),
                pn.widgets.TextInput(name='Email', placeholder='tu_email@gmail.com'),
                pn.widgets.PasswordInput(name='Contraseña'),
                pn.widgets.TextInput(name='Servidor IMAP', value='imap.gmail.com'),
                pn.widgets.IntInput(name='Máximo de correos', value=10, start=1, end=100)
            ])
        
        # Google Drive connection
        if 'google_drive' in self.selected_template.required_connections:
            drive_connections = self.connection_manager.list_connections('google_drive')
            drive_options = ['[Manual]'] + [c['name'] for c in drive_connections]
            
            self.config_panel.extend([
                pn.pane.Markdown("### Google Drive"),
                pn.widgets.Select(
                    name='Conexión Drive',
                    options=drive_options,
                    value='[Manual]'
                )
            ])
        
        # AI connection
        if 'ai' in self.selected_template.required_connections:
            ai_connections = self.connection_manager.list_connections()
            ai_conns = [c for c in ai_connections if c['service_type'] in ['openai', 'anthropic', 'gemini', 'local_model']]
            ai_options = ['Modelo Local'] + [c['name'] for c in ai_conns]
            
            self.config_panel.extend([
                pn.pane.Markdown("### Inteligencia Artificial"),
                pn.widgets.Select(
                    name='Proveedor IA',
                    options=ai_options,
                    value='Modelo Local'
                )
            ])
        
        # Webhook connection
        if 'webhook' in self.selected_template.required_connections:
            webhook_connections = self.connection_manager.list_connections('webhook')
            webhook_options = ['[Manual]'] + [c['name'] for c in webhook_connections]
            
            self.config_panel.extend([
                pn.pane.Markdown("### Webhook"),
                pn.widgets.Select(
                    name='Conexión Webhook',
                    options=webhook_options,
                    value='[Manual]'
                ),
                pn.widgets.TextInput(name='URL Webhook', placeholder='https://ejemplo.com/webhook')
            ])
        
        # Filters (common for most templates)
        self.config_panel.extend([
            pn.pane.Markdown("### Filtros (opcional)"),
            pn.widgets.TextInput(
                name='Filtrar por asunto',
                placeholder='palabra1, palabra2'
            ),
            pn.widgets.TextInput(
                name='Filtrar por remitente',
                placeholder='email@ejemplo.com'
            )
        ])
        
        self.status_pane.object = f"### Estado\n✅ Plantilla '{self.selected_template.name}' seleccionada. Configura los parámetros y ejecuta."
    
    def _get_config_from_inputs(self) -> Dict[str, Any]:
        """Extract configuration from input widgets."""
        config = {}
        
        for widget in self.config_panel:
            if hasattr(widget, 'name') and hasattr(widget, 'value') and widget.name:
                key = widget.name.lower().replace(' ', '_')
                config[key] = widget.value
        
        # Map to expected keys
        return {
            'email_address': config.get('email', ''),
            'email_password': config.get('contraseña', ''),
            'imap_server': config.get('servidor_imap', 'imap.gmail.com'),
            'output_folder': 'output',
            'filter_criteria': {
                'subject_contains': [s.strip() for s in config.get('filtrar_por_asunto', '').split(',') if s.strip()],
                'from_contains': [s.strip() for s in config.get('filtrar_por_remitente', '').split(',') if s.strip()]
            },
            'webhook_url': config.get('url_webhook', ''),
            'ai_provider': 'local',  # Default
            'max_emails': config.get('máximo_de_correos', 10)
        }
    
    def _execute_template(self, event):
        """Execute the selected template."""
        if not self.selected_template:
            self.status_pane.object = "### Estado\n❌ No hay plantilla seleccionada."
            return
        
        try:
            self.status_pane.object = "### Estado\n⏳ Ejecutando plantilla..."
            
            # Get configuration
            config = self._get_config_from_inputs()
            
            # Validate email credentials
            if not config['email_address'] or not config['email_password']:
                self.status_pane.object = "### Estado\n❌ Falta email o contraseña."
                return
            
            # Configure and execute template
            self.selected_template.configure(config)
            self.execution_result = self.selected_template.execute({
                'max_emails': config['max_emails']
            })
            
            # Show results
            if self.execution_result['status'] == 'completed':
                self.status_pane.object = "### Estado\n✅ Plantilla ejecutada exitosamente!"
                
                output = self.execution_result.get('output', 'N/A')
                self.result_pane.object = f"""### Resultado
                
**Salida:** `{output}`

**Pasos completados:** {len(self.execution_result['logs'])}
"""
            else:
                self.status_pane.object = f"### Estado\n❌ Error: {self.execution_result['status']}"
            
            self.log_pane.object = self.execution_result['logs']
            
        except Exception as e:
            self.status_pane.object = f"### Estado\n❌ Error: {str(e)}"
            import traceback
            self.result_pane.object = f"### Resultado\nError: {traceback.format_exc()}"
    
    def create_layout(self):
        """Create the templates dashboard layout."""
        header = pn.pane.Markdown("""
        # 📚 Plantillas de Automatización
        ## Inspiradas en Make.com
        
        Explora y usa plantillas predefinidas para automatizar tus flujos de trabajo.
        """, styles={'background-color': '#f0f0f0', 'padding': '20px', 'border-radius': '5px'})
        
        instructions = pn.pane.Markdown("""
        ### Cómo usar las plantillas:
        1. 🔍 **Explora** las plantillas disponibles por categoría
        2. ✅ **Selecciona** la plantilla que necesites
        3. ⚙️ **Configura** las conexiones y parámetros
        4. ▶️ **Ejecuta** y revisa los resultados
        
        **Tip:** Configura tus conexiones en la pestaña "Conexiones" para reutilizarlas en múltiples plantillas.
        """)
        
        # Left panel - Template browser
        browser_panel = pn.Column(
            "## Explorar Plantillas",
            self.category_filter,
            self.templates_grid,
            styles={'background-color': '#ffffff', 'padding': '20px', 'border-radius': '5px'},
            scroll=True,
            height=700
        )
        
        # Right panel - Configuration and execution
        config_execution_panel = pn.Column(
            self.config_panel,
            self.execute_button,
            self.status_pane,
            self.result_pane,
            pn.pane.Markdown("## Registro de Ejecución"),
            self.log_pane,
            styles={'background-color': '#ffffff', 'padding': '20px', 'border-radius': '5px'},
            scroll=True,
            height=700
        )
        
        layout = pn.Column(
            header,
            instructions,
            pn.Row(
                browser_panel,
                config_execution_panel
            )
        )
        
        return layout
