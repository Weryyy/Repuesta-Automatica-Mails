"""
Email Filter Agent - Filters emails based on criteria.
"""
from typing import List, Dict, Any
from .base_agent import BaseAgent


class EmailFilterAgent(BaseAgent):
    """Agent for filtering emails based on various criteria."""
    
    def __init__(self, name: str = "EmailFilter"):
        super().__init__(name)
        self.filter_criteria = {}
    
    def configure(self, criteria: Dict[str, Any]):
        """
        Configure the filter criteria.
        
        Args:
            criteria: Dictionary with filter criteria:
                - subject_contains: List of strings that should be in subject
                - from_contains: List of strings that should be in from address
                - body_contains: List of strings that should be in body
        """
        self.filter_criteria = criteria
    
    def execute(self, input_data: Any = None) -> List[Dict[str, Any]]:
        """
        Filter emails based on configured criteria.
        
        Args:
            input_data: List of email dictionaries to filter
        
        Returns:
            Filtered list of emails
        """
        self.status = "executing"
        
        if not input_data or not isinstance(input_data, list):
            self.status = "error: No email data provided"
            self.output = []
            return self.output
        
        emails = input_data
        filtered_emails = []
        
        try:
            for email_data in emails:
                if self._matches_criteria(email_data):
                    filtered_emails.append(email_data)
            
            self.output = filtered_emails
            self.status = f"completed: {len(filtered_emails)}/{len(emails)} emails matched"
            
        except Exception as e:
            self.status = f"error: {str(e)}"
            self.output = []
        
        return self.output
    
    def _matches_criteria(self, email_data: Dict[str, Any]) -> bool:
        """
        Check if an email matches the filter criteria.
        
        Args:
            email_data: Email dictionary to check
        
        Returns:
            True if email matches criteria, False otherwise
        """
        # If no criteria set, return all emails
        if not self.filter_criteria:
            return True
        
        # Check subject contains
        if 'subject_contains' in self.filter_criteria:
            subject = email_data.get('subject', '').lower()
            subject_keywords = self.filter_criteria['subject_contains']
            if not any(keyword.lower() in subject for keyword in subject_keywords):
                return False
        
        # Check from contains
        if 'from_contains' in self.filter_criteria:
            from_addr = email_data.get('from', '').lower()
            from_keywords = self.filter_criteria['from_contains']
            if not any(keyword.lower() in from_addr for keyword in from_keywords):
                return False
        
        # Check body contains
        if 'body_contains' in self.filter_criteria:
            body = email_data.get('body', '').lower()
            body_keywords = self.filter_criteria['body_contains']
            if not any(keyword.lower() in body for keyword in body_keywords):
                return False
        
        return True
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Return configuration schema."""
        return {
            'subject_contains': 'list of strings (optional)',
            'from_contains': 'list of strings (optional)',
            'body_contains': 'list of strings (optional)'
        }
