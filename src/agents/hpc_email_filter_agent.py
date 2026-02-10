"""
HPC-Optimized Email Filter Agent - High-performance email filtering with GPU support.
"""
from typing import List, Dict, Any
from .base_agent import BaseAgent


class HPCEmailFilterAgent(BaseAgent):
    """HPC-optimized agent for filtering large volumes of emails."""
    
    def __init__(self, name: str = "HPC EmailFilter"):
        super().__init__(name)
        self.filter_criteria = {}
        self.hpc_config = None
        self.parallel_processor = None
        self.use_gpu = False
    
    def configure(self, criteria: Dict[str, Any], use_hpc: bool = True):
        """
        Configure the filter with HPC optimizations.
        
        Args:
            criteria: Filter criteria
            use_hpc: Whether to use HPC optimizations
        """
        self.filter_criteria = criteria
        
        if use_hpc:
            try:
                from ..hpc import get_hpc_config, ParallelProcessor
                self.hpc_config = get_hpc_config()
                self.parallel_processor = ParallelProcessor(self.hpc_config)
                self.use_gpu = self.hpc_config.has_cuda or self.hpc_config.has_rapids
                
                print(f"✅ HPC enabled for {self.name}")
                print(f"   Backend: {self.hpc_config.backend}")
                print(f"   GPU: {'Yes' if self.use_gpu else 'No'}")
            except ImportError:
                print(f"⚠️  HPC components not available, using standard processing")
                self.parallel_processor = None
    
    def execute(self, input_data: Any = None) -> List[Dict[str, Any]]:
        """
        Filter emails with HPC optimizations.
        
        Args:
            input_data: List of email dictionaries
            
        Returns:
            Filtered list of emails
        """
        self.status = "executing"
        
        if not input_data or not isinstance(input_data, list):
            self.status = "error: No email data provided"
            self.output = []
            return self.output
        
        emails = input_data
        
        try:
            # Use parallel processing if available and data is large enough
            if self.parallel_processor and len(emails) > 100:
                filtered_emails = self._filter_parallel(emails)
            else:
                filtered_emails = self._filter_sequential(emails)
            
            self.output = filtered_emails
            self.status = f"completed: {len(filtered_emails)}/{len(emails)} emails matched (HPC: {bool(self.parallel_processor)})"
            
        except Exception as e:
            self.status = f"error: {str(e)}"
            self.output = []
        
        return self.output
    
    def _filter_parallel(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter emails in parallel."""
        # Process in parallel
        results = self.parallel_processor.map_parallel(
            self._matches_criteria,
            emails,
            use_processes=False  # Use threads for I/O-bound filtering
        )
        
        # Return only matched emails
        return [email for email, matches in zip(emails, results) if matches]
    
    def _filter_sequential(self, emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter emails sequentially."""
        return [email for email in emails if self._matches_criteria(email)]
    
    def _matches_criteria(self, email_data: Dict[str, Any]) -> bool:
        """Check if an email matches filter criteria."""
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
            'body_contains': 'list of strings (optional)',
            'use_hpc': 'boolean (optional, default: True) - Enable HPC optimizations'
        }
