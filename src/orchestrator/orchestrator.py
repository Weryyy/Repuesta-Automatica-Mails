"""
Orchestrator - Manages the execution of multiple agents in a scenario.
"""
from typing import List, Dict, Any, Optional
from ..agents.base_agent import BaseAgent


class Orchestrator:
    """Orchestrates the execution of multiple agents in sequence."""
    
    def __init__(self, name: str):
        """
        Initialize the orchestrator.
        
        Args:
            name: Name of the orchestrator/scenario
        """
        self.name = name
        self.agents: List[BaseAgent] = []
        self.execution_log: List[Dict[str, Any]] = []
        self.status = "initialized"
    
    def add_agent(self, agent: BaseAgent):
        """
        Add an agent to the orchestration pipeline.
        
        Args:
            agent: Agent instance to add
        """
        self.agents.append(agent)
    
    def clear_agents(self):
        """Clear all agents from the pipeline."""
        self.agents = []
        self.execution_log = []
    
    def execute(self, initial_input: Any = None) -> Dict[str, Any]:
        """
        Execute all agents in sequence.
        
        Args:
            initial_input: Initial input for the first agent
        
        Returns:
            Dictionary with execution results and logs
        """
        self.status = "executing"
        self.execution_log = []
        
        current_data = initial_input
        
        for i, agent in enumerate(self.agents):
            try:
                # Execute the agent
                result = agent.execute(current_data)
                
                # Log the execution
                log_entry = {
                    'step': i + 1,
                    'agent': agent.name,
                    'status': agent.get_status(),
                    'output_type': type(result).__name__,
                    'output_length': len(result) if isinstance(result, (list, dict, str)) else None
                }
                self.execution_log.append(log_entry)
                
                # Pass output to next agent
                current_data = result
                
            except Exception as e:
                # Log the error
                log_entry = {
                    'step': i + 1,
                    'agent': agent.name,
                    'status': 'error',
                    'error': str(e)
                }
                self.execution_log.append(log_entry)
                self.status = f"failed at step {i + 1}"
                return {
                    'status': self.status,
                    'logs': self.execution_log,
                    'output': None
                }
        
        self.status = "completed"
        return {
            'status': self.status,
            'logs': self.execution_log,
            'output': current_data
        }
    
    def get_status(self) -> str:
        """Get the current status of the orchestrator."""
        return self.status
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Get the execution log."""
        return self.execution_log
    
    def get_agents_info(self) -> List[Dict[str, str]]:
        """Get information about all agents in the pipeline."""
        return [
            {
                'name': agent.name,
                'type': type(agent).__name__,
                'status': agent.get_status()
            }
            for agent in self.agents
        ]
    
    def __repr__(self) -> str:
        return f"Orchestrator(name='{self.name}', agents={len(self.agents)}, status='{self.status}')"
