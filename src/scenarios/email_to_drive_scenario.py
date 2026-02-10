"""
Email to Drive Scenario - Exports emails to Google Drive.
"""
from typing import Dict, Any
from ..agents import EmailReaderAgent, EmailFilterAgent, ExcelWriterAgent, GoogleDriveAgent
from ..orchestrator import Orchestrator


class EmailToDriveScenario:
    """Scenario for reading emails and uploading to Google Drive."""
    
    def __init__(self):
        self.name = "Email to Google Drive"
        self.description = "Lee correos, los filtra y sube el Excel a Google Drive"
        self.orchestrator = Orchestrator(self.name)
        
        # Initialize agents
        self.email_reader = EmailReaderAgent()
        self.email_filter = EmailFilterAgent()
        self.excel_writer = ExcelWriterAgent()
        self.drive_agent = GoogleDriveAgent()
    
    def configure(self, config: Dict[str, Any]):
        """Configure the scenario."""
        # Configure email reader
        self.email_reader.configure(
            email_address=config.get('email_address'),
            password=config.get('email_password'),
            imap_server=config.get('imap_server', 'imap.gmail.com'),
            imap_port=config.get('imap_port', 993)
        )
        
        # Configure email filter
        filter_criteria = config.get('filter_criteria', {})
        self.email_filter.configure(filter_criteria)
        
        # Configure excel writer
        self.excel_writer.configure(
            output_folder=config.get('output_folder', 'output')
        )
        
        # Configure Google Drive
        self.drive_agent.configure(
            credentials_file=config.get('drive_credentials'),
            token=config.get('drive_token'),
            folder_id=config.get('drive_folder_id')
        )
        
        # Add agents to orchestrator
        self.orchestrator.clear_agents()
        self.orchestrator.add_agent(self.email_reader)
        self.orchestrator.add_agent(self.email_filter)
        self.orchestrator.add_agent(self.excel_writer)
        self.orchestrator.add_agent(self.drive_agent)
    
    def execute(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the scenario."""
        input_params = params or {}
        result = self.orchestrator.execute(input_params)
        return result
    
    def get_info(self) -> Dict[str, Any]:
        """Get scenario information."""
        return {
            'name': self.name,
            'description': self.description,
            'agents': self.orchestrator.get_agents_info()
        }
