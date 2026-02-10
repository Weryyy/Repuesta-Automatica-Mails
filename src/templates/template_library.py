"""
Template System - Predefined workflow templates inspired by Make.com
"""
from typing import Dict, Any, List
from ..agents import (EmailReaderAgent, EmailFilterAgent, ExcelWriterAgent, 
                      WebhookAgent, GoogleDriveAgent, AIAgent)
from ..orchestrator import Orchestrator


class Template:
    """Base class for workflow templates."""
    
    def __init__(self, name: str, description: str, category: str):
        """
        Initialize template.
        
        Args:
            name: Template name
            description: Template description
            category: Template category (Email, AI, Integration, etc.)
        """
        self.name = name
        self.description = description
        self.category = category
        self.icon = "🔄"
        self.required_connections = []
        self.orchestrator = Orchestrator(name)
    
    def configure(self, config: Dict[str, Any]):
        """Configure the template with user settings."""
        raise NotImplementedError
    
    def execute(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the template workflow."""
        return self.orchestrator.execute(params)
    
    def get_info(self) -> Dict[str, Any]:
        """Get template information."""
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'icon': self.icon,
            'required_connections': self.required_connections,
            'agents': self.orchestrator.get_agents_info()
        }


class EmailToExcelTemplate(Template):
    """Template: Email → Filter → Excel"""
    
    def __init__(self):
        super().__init__(
            name="Email to Excel",
            description="Lee correos, filtra y exporta a Excel",
            category="Email"
        )
        self.icon = "📊"
        self.required_connections = ['email']
        
        self.email_reader = EmailReaderAgent()
        self.email_filter = EmailFilterAgent()
        self.excel_writer = ExcelWriterAgent()
    
    def configure(self, config: Dict[str, Any]):
        self.email_reader.configure(
            email_address=config['email_address'],
            password=config['email_password'],
            imap_server=config.get('imap_server', 'imap.gmail.com')
        )
        self.email_filter.configure(config.get('filter_criteria', {}))
        self.excel_writer.configure(output_folder=config.get('output_folder', 'output'))
        
        self.orchestrator.clear_agents()
        self.orchestrator.add_agent(self.email_reader)
        self.orchestrator.add_agent(self.email_filter)
        self.orchestrator.add_agent(self.excel_writer)


class EmailToGoogleDriveTemplate(Template):
    """Template: Email → Filter → Excel → Google Drive"""
    
    def __init__(self):
        super().__init__(
            name="Email to Google Drive",
            description="Exporta correos filtrados a Google Drive",
            category="Integration"
        )
        self.icon = "☁️"
        self.required_connections = ['email', 'google_drive']
        
        self.email_reader = EmailReaderAgent()
        self.email_filter = EmailFilterAgent()
        self.excel_writer = ExcelWriterAgent()
        self.drive_agent = GoogleDriveAgent()
    
    def configure(self, config: Dict[str, Any]):
        self.email_reader.configure(
            email_address=config['email_address'],
            password=config['email_password'],
            imap_server=config.get('imap_server', 'imap.gmail.com')
        )
        self.email_filter.configure(config.get('filter_criteria', {}))
        self.excel_writer.configure(output_folder=config.get('output_folder', 'output'))
        self.drive_agent.configure(
            credentials_file=config.get('drive_credentials'),
            token=config.get('drive_token'),
            folder_id=config.get('drive_folder_id')
        )
        
        self.orchestrator.clear_agents()
        self.orchestrator.add_agent(self.email_reader)
        self.orchestrator.add_agent(self.email_filter)
        self.orchestrator.add_agent(self.excel_writer)
        self.orchestrator.add_agent(self.drive_agent)


class EmailAISummaryTemplate(Template):
    """Template: Email → Filter → AI Summary → Excel"""
    
    def __init__(self):
        super().__init__(
            name="Email AI Summary",
            description="Resumen de correos con IA",
            category="AI"
        )
        self.icon = "🤖"
        self.required_connections = ['email', 'ai']
        
        self.email_reader = EmailReaderAgent()
        self.email_filter = EmailFilterAgent()
        self.ai_agent = AIAgent()
        self.excel_writer = ExcelWriterAgent()
    
    def configure(self, config: Dict[str, Any]):
        self.email_reader.configure(
            email_address=config['email_address'],
            password=config['email_password'],
            imap_server=config.get('imap_server', 'imap.gmail.com')
        )
        self.email_filter.configure(config.get('filter_criteria', {}))
        self.ai_agent.configure(
            provider=config.get('ai_provider', 'local'),
            api_key=config.get('ai_api_key'),
            model=config.get('ai_model')
        )
        self.excel_writer.configure(output_folder=config.get('output_folder', 'output'))
        
        self.orchestrator.clear_agents()
        self.orchestrator.add_agent(self.email_reader)
        self.orchestrator.add_agent(self.email_filter)
        # Note: AI processing would be integrated here
        self.orchestrator.add_agent(self.excel_writer)


class EmailToWebhookTemplate(Template):
    """Template: Email → Filter → Webhook"""
    
    def __init__(self):
        super().__init__(
            name="Email to Webhook",
            description="Envía correos filtrados a un webhook",
            category="Integration"
        )
        self.icon = "🔗"
        self.required_connections = ['email', 'webhook']
        
        self.email_reader = EmailReaderAgent()
        self.email_filter = EmailFilterAgent()
        self.webhook_agent = WebhookAgent()
    
    def configure(self, config: Dict[str, Any]):
        self.email_reader.configure(
            email_address=config['email_address'],
            password=config['email_password'],
            imap_server=config.get('imap_server', 'imap.gmail.com')
        )
        self.email_filter.configure(config.get('filter_criteria', {}))
        self.webhook_agent.configure(
            webhook_url=config['webhook_url'],
            method=config.get('webhook_method', 'POST')
        )
        
        self.orchestrator.clear_agents()
        self.orchestrator.add_agent(self.email_reader)
        self.orchestrator.add_agent(self.email_filter)
        self.orchestrator.add_agent(self.webhook_agent)


class AIClassificationTemplate(Template):
    """Template: Email → AI Classification → Multiple outputs"""
    
    def __init__(self):
        super().__init__(
            name="AI Email Classification",
            description="Clasifica correos con IA y los organiza",
            category="AI"
        )
        self.icon = "🎯"
        self.required_connections = ['email', 'ai']
        
        self.email_reader = EmailReaderAgent()
        self.ai_agent = AIAgent()
        self.excel_writer = ExcelWriterAgent()
    
    def configure(self, config: Dict[str, Any]):
        self.email_reader.configure(
            email_address=config['email_address'],
            password=config['email_password'],
            imap_server=config.get('imap_server', 'imap.gmail.com')
        )
        self.ai_agent.configure(
            provider=config.get('ai_provider', 'local'),
            api_key=config.get('ai_api_key'),
            model=config.get('ai_model')
        )
        self.excel_writer.configure(output_folder=config.get('output_folder', 'output'))
        
        self.orchestrator.clear_agents()
        self.orchestrator.add_agent(self.email_reader)
        self.orchestrator.add_agent(self.ai_agent)
        self.orchestrator.add_agent(self.excel_writer)


class TemplateLibrary:
    """Library of available templates."""
    
    def __init__(self):
        """Initialize template library."""
        self.templates = {
            'email_to_excel': EmailToExcelTemplate(),
            'email_to_drive': EmailToGoogleDriveTemplate(),
            'email_ai_summary': EmailAISummaryTemplate(),
            'email_to_webhook': EmailToWebhookTemplate(),
            'ai_classification': AIClassificationTemplate()
        }
    
    def get_template(self, template_id: str) -> Template:
        """Get a template by ID."""
        return self.templates.get(template_id)
    
    def list_templates(self, category: str = None) -> List[Dict[str, Any]]:
        """
        List all templates, optionally filtered by category.
        
        Args:
            category: Optional category to filter by
            
        Returns:
            List of template information dictionaries
        """
        templates_list = []
        for template_id, template in self.templates.items():
            if category is None or template.category == category:
                info = template.get_info()
                info['id'] = template_id
                templates_list.append(info)
        return templates_list
    
    def get_categories(self) -> List[str]:
        """Get all template categories."""
        categories = set()
        for template in self.templates.values():
            categories.add(template.category)
        return sorted(list(categories))
