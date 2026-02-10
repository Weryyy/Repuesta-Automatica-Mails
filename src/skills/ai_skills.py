"""
AI-related skills for AI agents.
"""
from typing import Dict, Any, List
from .base_skill import Skill


class TextSummarizationSkill(Skill):
    """Skill for summarizing text content."""
    
    def __init__(self):
        super().__init__(
            name="Text Summarization",
            description="Summarize long texts into concise summaries"
        )
        self.max_summary_ratio = 0.3  # Summary should be 30% of original
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize text.
        
        Args:
            context: Dictionary with 'text' and optional 'ai_client'
            
        Returns:
            Summarization result
        """
        text = context.get('text', '')
        ai_client = context.get('ai_client')
        
        if not text:
            return {'success': False, 'error': 'No text provided'}
        
        # Simple summarization (can be enhanced with AI)
        sentences = text.split('.')
        max_sentences = max(1, int(len(sentences) * self.max_summary_ratio))
        summary = '. '.join(sentences[:max_sentences]) + '.'
        
        self.record_usage(success=True)
        
        return {
            'success': True,
            'summary': summary,
            'original_length': len(text),
            'summary_length': len(summary),
            'compression_ratio': len(summary) / len(text) if text else 0,
            'skill_level': self.level
        }


class DataExtractionSkill(Skill):
    """Skill for extracting structured data from unstructured text."""
    
    def __init__(self):
        super().__init__(
            name="Data Extraction",
            description="Extract structured information from unstructured text"
        )
        self.extraction_patterns = {}
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract structured data.
        
        Args:
            context: Dictionary with 'text' and 'fields' to extract
            
        Returns:
            Extracted data
        """
        text = context.get('text', '')
        fields = context.get('fields', [])
        
        extracted = {}
        for field in fields:
            # Simple keyword-based extraction
            # In production, would use NER or AI
            extracted[field] = self._extract_field(text, field)
        
        self.record_usage(success=bool(extracted))
        
        return {
            'success': True,
            'extracted': extracted,
            'skill_level': self.level
        }
    
    def _extract_field(self, text: str, field: str) -> str:
        """Extract a specific field from text."""
        # Placeholder - would use NLP/AI in production
        lines = text.split('\n')
        for line in lines:
            if field.lower() in line.lower():
                return line.strip()
        return ''


class PromptOptimizationSkill(Skill):
    """Skill for optimizing prompts for AI models."""
    
    def __init__(self):
        super().__init__(
            name="Prompt Optimization",
            description="Optimize prompts for better AI responses"
        )
        self.optimization_techniques = [
            'add_context',
            'specify_format',
            'add_examples',
            'clarify_instructions'
        ]
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize a prompt.
        
        Args:
            context: Dictionary with 'prompt' and optional 'task_type'
            
        Returns:
            Optimized prompt
        """
        prompt = context.get('prompt', '')
        task_type = context.get('task_type', 'general')
        
        optimized = self._optimize_prompt(prompt, task_type)
        
        self.record_usage(success=True)
        
        return {
            'success': True,
            'original_prompt': prompt,
            'optimized_prompt': optimized,
            'improvements': self._get_improvements(prompt, optimized),
            'skill_level': self.level
        }
    
    def _optimize_prompt(self, prompt: str, task_type: str) -> str:
        """Optimize a prompt based on best practices."""
        optimized = prompt
        
        # Add clarity
        if not prompt.endswith('?') and not prompt.endswith('.'):
            optimized += '.'
        
        # Add context based on task type
        if task_type == 'summarization':
            optimized = f"Summarize the following text concisely:\n\n{optimized}"
        elif task_type == 'classification':
            optimized = f"Classify the following text:\n\n{optimized}\n\nProvide the category."
        elif task_type == 'extraction':
            optimized = f"Extract key information from:\n\n{optimized}"
        
        return optimized
    
    def _get_improvements(self, original: str, optimized: str) -> List[str]:
        """List improvements made to the prompt."""
        improvements = []
        
        if len(optimized) > len(original):
            improvements.append('Added context and structure')
        if ':\n\n' in optimized and ':\n\n' not in original:
            improvements.append('Improved formatting')
        
        return improvements if improvements else ['Prompt already optimal']
