"""
Email to Excel Scenario - Reads emails, filters them, and exports to Excel.
"""
from typing import Dict, Any
from ..agents import EmailReaderAgent, EmailFilterAgent, ExcelWriterAgent
from ..orchestrator import Orchestrator


class EmailToExcelScenario:
    """Scenario for reading emails, filtering them, and exporting to Excel."""
    
    def __init__(self):
        self.name = "Email to Excel"
        self.description = "Lee correos electrónicos, los filtra y los exporta a Excel"
        self.orchestrator = Orchestrator(self.name)
        
        # Initialize agents
        self.email_reader = EmailReaderAgent()
        self.email_filter = EmailFilterAgent()
        self.excel_writer = ExcelWriterAgent()
    
    def configure(self, config: Dict[str, Any]):
        """
        Configure the scenario with user inputs.
        
        Args:
            config: Configuration dictionary with keys:
                - email_address: Email address
                - email_password: Email password
                - imap_server: IMAP server (optional)
                - imap_port: IMAP port (optional)
                - filter_criteria: Filter criteria (optional)
                - output_folder: Output folder (optional)
                - max_emails: Max emails to read (optional)
        """
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
        
        # Add agents to orchestrator
        self.orchestrator.clear_agents()
        self.orchestrator.add_agent(self.email_reader)
        self.orchestrator.add_agent(self.email_filter)
        self.orchestrator.add_agent(self.excel_writer)
    
    def execute(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute the scenario.
        
        Args:
            params: Execution parameters (e.g., max_emails, folder)
        
        Returns:
            Execution results
        """
        # Prepare input for email reader
        input_params = params or {}
        
        # Execute the orchestrator
        result = self.orchestrator.execute(input_params)
        
        return result
    
    def get_info(self) -> Dict[str, Any]:
        """Get scenario information."""
        return {
            'name': self.name,
            'description': self.description,
            'agents': self.orchestrator.get_agents_info()
        }
