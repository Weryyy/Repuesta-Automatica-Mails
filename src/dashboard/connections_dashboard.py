"""
Connections Dashboard - Interface for managing connections to external services.
"""
import panel as pn
from typing import Dict, Any
from ..utils.connection_manager import ConnectionManager


class ConnectionsDashboard:
    """Dashboard for managing connections to external services."""
    
    def __init__(self, connection_manager: ConnectionManager):
        """Initialize the connections dashboard."""
        self.connection_manager = connection_manager
        
        # Service type selector
        self.service_type = pn.widgets.Select(
            name='Tipo de Servicio',
            options=[
                'Email (IMAP)',
                'Google Drive',
                'Webhook',
                'OpenAI',
                'Anthropic (Claude)',
                'Google Gemini',
                'Modelo Local'
            ],
            value='Email (IMAP)'
        )
        
        # Connection name
        self.connection_name = pn.widgets.TextInput(
            name='Nombre de la Conexión',
            placeholder='Mi conexión de Gmail'
        )
        
        # Dynamic credential fields
        self.credential_inputs = pn.Column()
        
        # Buttons
        self.save_button = pn.widgets.Button(
            name='Guardar Conexión',
            button_type='primary'
        )
        self.test_button = pn.widgets.Button(
            name='Probar Conexión',
            button_type='success'
        )
        self.delete_button = pn.widgets.Button(
            name='Eliminar Conexión',
            button_type='danger'
        )
        
        # Connection list
        self.connections_list = pn.widgets.Select(
            name='Conexiones Existentes',
            options=[],
            size=10
        )
        
        # Status messages
        self.status_message = pn.pane.Markdown("### Estado\nSelecciona un tipo de servicio y completa los campos.")
        
        # Setup callbacks
        self.service_type.param.watch(self._update_credential_fields, 'value')
        self.connections_list.param.watch(self._load_connection, 'value')
        self.save_button.on_click(self._save_connection)
        self.test_button.on_click(self._test_connection)
        self.delete_button.on_click(self._delete_connection)
        
        # Initialize
        self._update_credential_fields(None)
        self._refresh_connections_list()
    
    def _get_service_type_key(self, display_name: str) -> str:
        """Convert display name to service type key."""
        mapping = {
            'Email (IMAP)': 'email',
            'Google Drive': 'google_drive',
            'Webhook': 'webhook',
            'OpenAI': 'openai',
            'Anthropic (Claude)': 'anthropic',
            'Google Gemini': 'gemini',
            'Modelo Local': 'local_model'
        }
        return mapping.get(display_name, 'email')
    
    def _update_credential_fields(self, event):
        """Update credential input fields based on service type."""
        service_type = self._get_service_type_key(self.service_type.value)
        
        self.credential_inputs.clear()
        
        if service_type == 'email':
            self.credential_inputs.extend([
                pn.widgets.TextInput(name='Email', placeholder='usuario@gmail.com'),
                pn.widgets.PasswordInput(name='Contraseña', placeholder='Contraseña o contraseña de aplicación'),
                pn.widgets.TextInput(name='Servidor IMAP', value='imap.gmail.com'),
                pn.widgets.IntInput(name='Puerto IMAP', value=993)
            ])
        
        elif service_type == 'google_drive':
            self.credential_inputs.extend([
                pn.pane.Markdown("""
                ### Configuración de Google Drive
                1. Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com)
                2. Habilita Google Drive API
                3. Crea credenciales OAuth 2.0
                4. Descarga el archivo JSON de credenciales
                """),
                pn.widgets.TextInput(name='Archivo de Credenciales', placeholder='ruta/a/credentials.json'),
                pn.widgets.TextInput(name='Folder ID (opcional)', placeholder='ID de carpeta en Drive')
            ])
        
        elif service_type == 'webhook':
            self.credential_inputs.extend([
                pn.widgets.TextInput(name='URL del Webhook', placeholder='https://ejemplo.com/webhook'),
                pn.widgets.Select(name='Método HTTP', options=['POST', 'GET', 'PUT'], value='POST'),
                pn.widgets.TextAreaInput(name='Headers personalizados (JSON, opcional)', placeholder='{"Authorization": "Bearer token"}')
            ])
        
        elif service_type in ['openai', 'anthropic', 'gemini']:
            provider_info = {
                'openai': ('OpenAI', 'https://platform.openai.com/api-keys', 'gpt-3.5-turbo, gpt-4'),
                'anthropic': ('Anthropic (Claude)', 'https://console.anthropic.com/', 'claude-3-sonnet, claude-3-opus'),
                'gemini': ('Google Gemini', 'https://makersuite.google.com/app/apikey', 'gemini-pro')
            }
            name, url, models = provider_info[service_type]
            
            self.credential_inputs.extend([
                pn.pane.Markdown(f"""
                ### Configuración de {name}
                Obtén tu API key en: [{url}]({url})
                
                **Modelos disponibles:** {models}
                """),
                pn.widgets.PasswordInput(name='API Key', placeholder='sk-...'),
                pn.widgets.TextInput(name='Modelo (opcional)', placeholder='Dejar vacío para usar el predeterminado')
            ])
        
        elif service_type == 'local_model':
            self.credential_inputs.extend([
                pn.pane.Markdown("""
                ### Modelo Local
                Configura un modelo local para procesamiento de IA sin APIs externas.
                
                **Opciones futuras:**
                - Ollama
                - LM Studio
                - Transformers (Hugging Face)
                """),
                pn.widgets.TextInput(name='Ruta del Modelo', placeholder='/ruta/al/modelo'),
                pn.widgets.TextInput(name='Tipo de Modelo', placeholder='ollama, transformers, etc.')
            ])
    
    def _get_credentials_from_inputs(self) -> Dict[str, Any]:
        """Extract credentials from input widgets."""
        credentials = {}
        service_type = self._get_service_type_key(self.service_type.value)
        
        for widget in self.credential_inputs:
            if hasattr(widget, 'name') and hasattr(widget, 'value') and widget.name:
                key = widget.name.lower().replace(' ', '_').replace('(', '').replace(')', '')
                credentials[key] = widget.value
        
        # Map to expected keys
        if service_type == 'email':
            return {
                'email_address': credentials.get('email', ''),
                'password': credentials.get('contraseña', ''),
                'imap_server': credentials.get('servidor_imap', 'imap.gmail.com'),
                'imap_port': credentials.get('puerto_imap', 993)
            }
        elif service_type == 'google_drive':
            return {
                'credentials_file': credentials.get('archivo_de_credenciales', ''),
                'folder_id': credentials.get('folder_id_opcional', '')
            }
        elif service_type == 'webhook':
            return {
                'url': credentials.get('url_del_webhook', ''),
                'method': credentials.get('método_http', 'POST'),
                'headers': credentials.get('headers_personalizados_json,_opcional', '')
            }
        elif service_type in ['openai', 'anthropic', 'gemini']:
            return {
                'api_key': credentials.get('api_key', ''),
                'model': credentials.get('modelo_opcional', '')
            }
        elif service_type == 'local_model':
            return {
                'model_path': credentials.get('ruta_del_modelo', ''),
                'model_type': credentials.get('tipo_de_modelo', '')
            }
        
        return credentials
    
    def _save_connection(self, event):
        """Save a new connection."""
        name = self.connection_name.value
        if not name:
            self.status_message.object = "### Estado\n❌ Por favor ingresa un nombre para la conexión."
            return
        
        service_type = self._get_service_type_key(self.service_type.value)
        credentials = self._get_credentials_from_inputs()
        
        self.connection_manager.add_connection(name, service_type, credentials)
        self.status_message.object = f"### Estado\n✅ Conexión '{name}' guardada exitosamente."
        
        self._refresh_connections_list()
        self.connection_name.value = ''
    
    def _test_connection(self, event):
        """Test the selected connection."""
        selected = self.connections_list.value
        if not selected:
            self.status_message.object = "### Estado\n❌ Selecciona una conexión para probar."
            return
        
        result = self.connection_manager.test_connection(selected)
        
        if result['success']:
            self.status_message.object = f"### Estado\n✅ {result['message']}"
        else:
            self.status_message.object = f"### Estado\n❌ Error: {result['error']}"
    
    def _delete_connection(self, event):
        """Delete the selected connection."""
        selected = self.connections_list.value
        if not selected:
            self.status_message.object = "### Estado\n❌ Selecciona una conexión para eliminar."
            return
        
        if self.connection_manager.remove_connection(selected):
            self.status_message.object = f"### Estado\n✅ Conexión '{selected}' eliminada."
            self._refresh_connections_list()
        else:
            self.status_message.object = f"### Estado\n❌ Error al eliminar la conexión."
    
    def _load_connection(self, event):
        """Load a connection's details."""
        selected = self.connections_list.value
        if not selected:
            return
        
        connection = self.connection_manager.get_connection(selected)
        if connection:
            self.status_message.object = f"### Estado\n📋 Conexión '{selected}' cargada.\nTipo: {connection['service_type']}"
    
    def _refresh_connections_list(self):
        """Refresh the connections list."""
        connections = self.connection_manager.list_connections()
        self.connections_list.options = [f"{c['name']} ({c['service_type']})" 
                                        for c in connections]
        if not connections:
            self.connections_list.options = ['No hay conexiones']
    
    def create_layout(self):
        """Create the connections dashboard layout."""
        header = pn.pane.Markdown("""
        # 🔌 Gestor de Conexiones
        
        Gestiona las conexiones a servicios externos (Email, Google Drive, Webhooks, APIs de IA, etc.)
        """, styles={'background-color': '#f0f0f0', 'padding': '20px', 'border-radius': '5px'})
        
        # Left panel - Create new connection
        create_panel = pn.Column(
            "## Nueva Conexión",
            self.service_type,
            self.connection_name,
            self.credential_inputs,
            pn.Row(self.save_button),
            styles={'background-color': '#ffffff', 'padding': '20px', 'border-radius': '5px'}
        )
        
        # Right panel - Manage existing connections
        manage_panel = pn.Column(
            "## Gestionar Conexiones",
            self.connections_list,
            pn.Row(self.test_button, self.delete_button),
            self.status_message,
            styles={'background-color': '#ffffff', 'padding': '20px', 'border-radius': '5px'}
        )
        
        layout = pn.Column(
            header,
            pn.Row(create_panel, manage_panel)
        )
        
        return layout
