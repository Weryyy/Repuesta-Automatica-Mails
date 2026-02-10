"""
Skill Manager - Manages skills for agents, including training and persistence.
"""
import os
import json
from typing import Dict, Any, List, Optional
from .base_skill import Skill
from .email_skills import EmailParsingSkill, EmailClassificationSkill, EmailSentimentSkill
from .ai_skills import TextSummarizationSkill, DataExtractionSkill, PromptOptimizationSkill


class SkillManager:
    """Manages skills for agents."""
    
    def __init__(self, skills_dir: str = "skills_data"):
        """
        Initialize skill manager.
        
        Args:
            skills_dir: Directory to store skill data
        """
        self.skills_dir = skills_dir
        self.skills: Dict[str, Skill] = {}
        self.agent_skills: Dict[str, List[str]] = {}  # Agent -> Skills mapping
        
        # Create skills directory
        os.makedirs(skills_dir, exist_ok=True)
        
        # Register available skills
        self._register_default_skills()
    
    def _register_default_skills(self):
        """Register default skills."""
        # Email skills
        self.register_skill('email_parsing', EmailParsingSkill())
        self.register_skill('email_classification', EmailClassificationSkill())
        self.register_skill('email_sentiment', EmailSentimentSkill())
        
        # AI skills
        self.register_skill('text_summarization', TextSummarizationSkill())
        self.register_skill('data_extraction', DataExtractionSkill())
        self.register_skill('prompt_optimization', PromptOptimizationSkill())
    
    def register_skill(self, skill_id: str, skill: Skill):
        """
        Register a skill.
        
        Args:
            skill_id: Unique skill identifier
            skill: Skill instance
        """
        self.skills[skill_id] = skill
        
        # Try to load saved state
        skill_file = os.path.join(self.skills_dir, f"{skill_id}.json")
        if os.path.exists(skill_file):
            skill.load(skill_file)
    
    def assign_skill_to_agent(self, agent_name: str, skill_id: str) -> bool:
        """
        Assign a skill to an agent.
        
        Args:
            agent_name: Name of the agent
            skill_id: ID of the skill to assign
            
        Returns:
            True if successful, False otherwise
        """
        if skill_id not in self.skills:
            return False
        
        if agent_name not in self.agent_skills:
            self.agent_skills[agent_name] = []
        
        if skill_id not in self.agent_skills[agent_name]:
            self.agent_skills[agent_name].append(skill_id)
        
        return True
    
    def get_agent_skills(self, agent_name: str) -> List[Skill]:
        """
        Get all skills assigned to an agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            List of skill instances
        """
        skill_ids = self.agent_skills.get(agent_name, [])
        return [self.skills[sid] for sid in skill_ids if sid in self.skills]
    
    def execute_skill(self, skill_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a skill.
        
        Args:
            skill_id: ID of the skill to execute
            context: Execution context
            
        Returns:
            Execution result
        """
        if skill_id not in self.skills:
            return {'success': False, 'error': f'Skill {skill_id} not found'}
        
        skill = self.skills[skill_id]
        result = skill.execute(context)
        
        # Save updated skill state
        self.save_skill(skill_id)
        
        return result
    
    def train_skill(self, skill_id: str, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train a skill with examples.
        
        Args:
            skill_id: ID of the skill to train
            training_data: Training examples
            
        Returns:
            Training results
        """
        if skill_id not in self.skills:
            return {'success': False, 'error': f'Skill {skill_id} not found'}
        
        skill = self.skills[skill_id]
        result = skill.train(training_data)
        
        # Save updated skill state
        self.save_skill(skill_id)
        
        return result
    
    def save_skill(self, skill_id: str):
        """
        Save skill state to disk.
        
        Args:
            skill_id: ID of the skill to save
        """
        if skill_id in self.skills:
            skill_file = os.path.join(self.skills_dir, f"{skill_id}.json")
            self.skills[skill_id].save(skill_file)
    
    def save_all_skills(self):
        """Save all skills to disk."""
        for skill_id in self.skills:
            self.save_skill(skill_id)
    
    def get_skill_stats(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """
        Get statistics for a skill.
        
        Args:
            skill_id: ID of the skill
            
        Returns:
            Skill statistics or None if not found
        """
        if skill_id in self.skills:
            return self.skills[skill_id].get_stats()
        return None
    
    def list_skills(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all available skills.
        
        Args:
            category: Optional category filter
            
        Returns:
            List of skill information dictionaries
        """
        skills_info = []
        for skill_id, skill in self.skills.items():
            stats = skill.get_stats()
            stats['skill_id'] = skill_id
            skills_info.append(stats)
        
        return skills_info
    
    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """
        Get skill leaderboard sorted by proficiency.
        
        Returns:
            List of skills sorted by performance
        """
        leaderboard = []
        for skill_id, skill in self.skills.items():
            leaderboard.append({
                'skill_id': skill_id,
                'name': skill.name,
                'level': skill.level,
                'proficiency': skill.get_proficiency(),
                'usage_count': skill.usage_count
            })
        
        # Sort by proficiency and level
        leaderboard.sort(key=lambda x: (x['proficiency'], x['level']), reverse=True)
        
        return leaderboard
    
    def reset_skill(self, skill_id: str) -> bool:
        """
        Reset a skill to initial state.
        
        Args:
            skill_id: ID of the skill to reset
            
        Returns:
            True if successful, False otherwise
        """
        if skill_id not in self.skills:
            return False
        
        skill = self.skills[skill_id]
        skill.level = 1
        skill.experience = 0
        skill.usage_count = 0
        skill.success_count = 0
        skill.last_used = None
        
        self.save_skill(skill_id)
        
        return True
    
    def export_skills_report(self, filepath: str):
        """
        Export skills report to file.
        
        Args:
            filepath: Path to save report
        """
        report = {
            'total_skills': len(self.skills),
            'agent_assignments': self.agent_skills,
            'skills': self.list_skills(),
            'leaderboard': self.get_leaderboard()
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
