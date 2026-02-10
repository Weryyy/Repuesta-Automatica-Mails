"""
Base Agent class for the email automation system.
All specific agents should inherit from this class.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


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
        self.skills = []  # List of skills assigned to this agent
        self.skill_manager = None  # Will be set by skill manager
    
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
    
    def add_skill(self, skill):
        """
        Add a skill to this agent.
        
        Args:
            skill: Skill instance to add
        """
        if skill not in self.skills:
            self.skills.append(skill)
    
    def get_skills(self) -> List:
        """Get all skills assigned to this agent."""
        return self.skills
    
    def execute_skill(self, skill_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a specific skill.
        
        Args:
            skill_name: Name of the skill to execute
            context: Execution context
            
        Returns:
            Skill execution result
        """
        for skill in self.skills:
            if skill.name == skill_name:
                return skill.execute(context)
        
        return {'success': False, 'error': f'Skill {skill_name} not found'}
    
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
        skills_info = f", skills={len(self.skills)}" if self.skills else ""
        return f"{self.__class__.__name__}(name='{self.name}', status='{self.status}'{skills_info})"
