"""
Email-related skills for email processing agents.
"""
import re
from typing import Dict, Any, List
from .base_skill import Skill


class EmailParsingSkill(Skill):
    """Skill for parsing and extracting information from emails."""
    
    def __init__(self):
        super().__init__(
            name="Email Parsing",
            description="Parse and extract structured information from emails"
        )
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'url': r'https?://[^\s]+',
            'amount': r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?'
        }
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract structured information from email.
        
        Args:
            context: Dictionary with 'email_text' key
            
        Returns:
            Extracted information
        """
        email_text = context.get('email_text', '')
        
        extracted = {}
        for key, pattern in self.patterns.items():
            matches = re.findall(pattern, email_text)
            extracted[key] = matches
        
        self.record_usage(success=bool(extracted))
        
        return {
            'success': True,
            'extracted': extracted,
            'skill_level': self.level
        }
    
    def train(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train the skill with example emails.
        
        Args:
            training_data: List of {'email_text': str, 'expected': dict}
            
        Returns:
            Training results
        """
        correct = 0
        for example in training_data:
            result = self.execute({'email_text': example['email_text']})
            expected = example.get('expected', {})
            
            # Check if extracted matches expected
            if self._matches_expected(result['extracted'], expected):
                correct += 1
        
        accuracy = correct / len(training_data) if training_data else 0
        self.metadata['training_accuracy'] = accuracy
        
        return super().train(training_data)
    
    def _matches_expected(self, extracted: Dict, expected: Dict) -> bool:
        """Check if extracted data matches expected."""
        for key, values in expected.items():
            if key not in extracted:
                return False
            if not all(v in extracted[key] for v in values):
                return False
        return True


class EmailClassificationSkill(Skill):
    """Skill for classifying emails into categories."""
    
    def __init__(self):
        super().__init__(
            name="Email Classification",
            description="Classify emails into predefined categories"
        )
        self.categories = {
            'urgent': ['urgent', 'asap', 'immediately', 'critical'],
            'invoice': ['invoice', 'factura', 'bill', 'payment'],
            'support': ['help', 'issue', 'problem', 'support', 'error'],
            'sales': ['offer', 'discount', 'sale', 'promotion'],
            'spam': ['click here', 'winner', 'claim', 'free money']
        }
        self.learned_patterns = {}
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Classify an email.
        
        Args:
            context: Dictionary with 'subject' and 'body' keys
            
        Returns:
            Classification result
        """
        subject = context.get('subject', '').lower()
        body = context.get('body', '').lower()
        text = f"{subject} {body}"
        
        scores = {}
        for category, keywords in self.categories.items():
            score = sum(1 for keyword in keywords if keyword in text)
            scores[category] = score
        
        # Get category with highest score
        if max(scores.values()) > 0:
            category = max(scores, key=scores.get)
            confidence = scores[category] / sum(scores.values())
        else:
            category = 'general'
            confidence = 0.5
        
        self.record_usage(success=True)
        
        return {
            'success': True,
            'category': category,
            'confidence': confidence,
            'scores': scores,
            'skill_level': self.level
        }
    
    def train(self, training_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train classification with labeled examples.
        
        Args:
            training_data: List of {'subject': str, 'body': str, 'category': str}
            
        Returns:
            Training results
        """
        # Learn new patterns from training data
        for example in training_data:
            category = example.get('category')
            text = f"{example.get('subject', '')} {example.get('body', '')}".lower()
            
            if category not in self.learned_patterns:
                self.learned_patterns[category] = set()
            
            # Extract frequent words
            words = re.findall(r'\b\w{4,}\b', text)
            self.learned_patterns[category].update(words[:5])
        
        # Update categories with learned patterns
        for category, patterns in self.learned_patterns.items():
            if category in self.categories:
                self.categories[category].extend(list(patterns)[:3])
        
        self.metadata['learned_categories'] = len(self.learned_patterns)
        
        return super().train(training_data)


class EmailSentimentSkill(Skill):
    """Skill for analyzing sentiment in emails."""
    
    def __init__(self):
        super().__init__(
            name="Email Sentiment Analysis",
            description="Analyze the sentiment and tone of emails"
        )
        self.positive_words = ['great', 'excellent', 'thanks', 'appreciate', 'love', 'perfect']
        self.negative_words = ['bad', 'terrible', 'hate', 'disappointed', 'angry', 'worst']
        self.urgent_words = ['urgent', 'asap', 'immediately', 'critical', 'emergency']
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze email sentiment.
        
        Args:
            context: Dictionary with 'text' key
            
        Returns:
            Sentiment analysis result
        """
        text = context.get('text', '').lower()
        
        positive_count = sum(1 for word in self.positive_words if word in text)
        negative_count = sum(1 for word in self.negative_words if word in text)
        urgent_count = sum(1 for word in self.urgent_words if word in text)
        
        # Calculate sentiment score (-1 to 1)
        total = positive_count + negative_count
        if total > 0:
            sentiment_score = (positive_count - negative_count) / total
        else:
            sentiment_score = 0
        
        # Determine sentiment label
        if sentiment_score > 0.3:
            sentiment = 'positive'
        elif sentiment_score < -0.3:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        is_urgent = urgent_count > 0
        
        self.record_usage(success=True)
        
        return {
            'success': True,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'is_urgent': is_urgent,
            'metrics': {
                'positive_words': positive_count,
                'negative_words': negative_count,
                'urgent_words': urgent_count
            },
            'skill_level': self.level
        }
