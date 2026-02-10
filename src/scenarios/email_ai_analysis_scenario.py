"""
Email AI Analysis Scenario - Analyzes emails with AI and exports results.
"""
from typing import Dict, Any
from ..agents import EmailReaderAgent, EmailFilterAgent, AIAgent, ExcelWriterAgent
from ..orchestrator import Orchestrator


class EmailAIAnalysisScenario:
    """Scenario for reading emails, analyzing them with AI, and exporting results."""
    
    def __init__(self):
        self.name = "Email AI Analysis"
        self.description = "Lee correos, los analiza con IA y exporta los resultados"
        self.orchestrator = Orchestrator(self.name)
        
        # Initialize agents
        self.email_reader = EmailReaderAgent()
        self.email_filter = EmailFilterAgent()
        self.ai_agent = AIAgent()
        self.excel_writer = ExcelWriterAgent()
    
    def configure(self, config: Dict[str, Any]):
        """
        Configure the scenario.
        
        Args:
            config: Configuration dictionary with keys:
                - email_address, email_password, imap_server
                - filter_criteria (optional)
                - ai_provider: AI provider (openai, anthropic, gemini, local)
                - ai_api_key: API key for AI
                - ai_task: Task for AI (summarize, classify, extract)
                - output_folder (optional)
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
        
        # Configure AI agent
        self.ai_agent.configure(
            provider=config.get('ai_provider', 'local'),
            api_key=config.get('ai_api_key'),
            model=config.get('ai_model')
        )
        
        # Configure excel writer
        self.excel_writer.configure(
            output_folder=config.get('output_folder', 'output')
        )
        
        # Add agents to orchestrator
        self.orchestrator.clear_agents()
        self.orchestrator.add_agent(self.email_reader)
        self.orchestrator.add_agent(self.email_filter)
        # AI agent would process emails here
        self.orchestrator.add_agent(self.excel_writer)
    
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
