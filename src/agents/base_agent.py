"""
Base Agent class for the email automation system.
All specific agents should inherit from this class.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""
    
    def __init__(self, name: str):
        """
        Initialize the agent.
        
        Args:
            name: Name of the agent
        """
        self.name = name
        self.status = "initialized"
        self.output = None
    
    @abstractmethod
    def execute(self, input_data: Any = None) -> Any:
        """
        Execute the agent's main functionality.
        
        Args:
            input_data: Input data for the agent to process
            
        Returns:
            Processed output data
        """
        pass
    
    def get_config_schema(self) -> Dict[str, Any]:
        """
        Return the configuration schema for this agent.
        
        Returns:
            Dictionary describing required configuration parameters
        """
        return {}
    
    def get_status(self) -> str:
        """Get the current status of the agent."""
        return self.status
    
    def get_output(self) -> Any:
        """Get the output from the last execution."""
        return self.output
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', status='{self.status}')"
