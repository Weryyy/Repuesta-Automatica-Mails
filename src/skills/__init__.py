"""
Skills package - Agent skills and capabilities.
"""
from .base_skill import Skill
from .skill_manager import SkillManager
from .email_skills import EmailParsingSkill, EmailClassificationSkill, EmailSentimentSkill
from .ai_skills import TextSummarizationSkill, DataExtractionSkill, PromptOptimizationSkill

__all__ = [
    'Skill',
    'SkillManager',
    'EmailParsingSkill',
    'EmailClassificationSkill',
    'EmailSentimentSkill',
    'TextSummarizationSkill',
    'DataExtractionSkill',
    'PromptOptimizationSkill'
]
