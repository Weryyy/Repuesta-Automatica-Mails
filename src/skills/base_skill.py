"""
Base Skill class - Defines capabilities that agents can have and improve over time.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime


class Skill(ABC):
    """Abstract base class for agent skills."""
    
    def __init__(self, name: str, description: str):
        """
        Initialize a skill.
        
        Args:
            name: Skill name
            description: Skill description
        """
        self.name = name
        self.description = description
        self.level = 1  # Skill level (1-10)
        self.experience = 0  # Experience points
        self.usage_count = 0  # Times this skill has been used
        self.success_count = 0  # Successful executions
        self.last_used = None  # Last usage timestamp
        self.metadata = {}  # Additional metadata
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the skill.
        
        Args:
            context: Execution context with input data
            
        Returns:
            Result dictionary with output and success status
        """
        pass
    
    def train(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train the skill with examples.
        
        Args:
            training_data: List of training examples
            
        Returns:
            Training results
        """
        results = {
            'skill': self.name,
            'examples_trained': len(training_data),
            'success': True
        }
        
        # Update experience based on training
        self.experience += len(training_data) * 10
        self._update_level()
        
        return results
    
    def record_usage(self, success: bool = True):
        """
        Record skill usage and update statistics.
        
        Args:
            success: Whether the execution was successful
        """
        self.usage_count += 1
        if success:
            self.success_count += 1
            self.experience += 5
        self.last_used = datetime.now().isoformat()
        self._update_level()
    
    def _update_level(self):
        """Update skill level based on experience."""
        # Level up every 100 experience points
        new_level = min(10, 1 + (self.experience // 100))
        if new_level > self.level:
            self.level = new_level
    
    def get_proficiency(self) -> float:
        """
        Get skill proficiency (0.0 to 1.0).
        
        Returns:
            Proficiency score
        """
        if self.usage_count == 0:
            return 0.0
        return min(1.0, self.success_count / self.usage_count)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get skill statistics.
        
        Returns:
            Statistics dictionary
        """
        return {
            'name': self.name,
            'description': self.description,
            'level': self.level,
            'experience': self.experience,
            'usage_count': self.usage_count,
            'success_count': self.success_count,
            'proficiency': self.get_proficiency(),
            'last_used': self.last_used,
            'metadata': self.metadata
        }
    
    def save(self, filepath: str):
        """
        Save skill state to file.
        
        Args:
            filepath: Path to save file
        """
        with open(filepath, 'w') as f:
            json.dump(self.get_stats(), f, indent=2)
    
    def load(self, filepath: str):
        """
        Load skill state from file.
        
        Args:
            filepath: Path to load file
        """
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.level = data.get('level', 1)
                self.experience = data.get('experience', 0)
                self.usage_count = data.get('usage_count', 0)
                self.success_count = data.get('success_count', 0)
                self.last_used = data.get('last_used')
                self.metadata = data.get('metadata', {})
    
    def __repr__(self) -> str:
        return f"Skill(name='{self.name}', level={self.level}, proficiency={self.get_proficiency():.2f})"
