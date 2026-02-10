"""
Webhook Agent - Sends data to external webhooks.
"""
import requests
from typing import Dict, Any, Optional
from .base_agent import BaseAgent


class WebhookAgent(BaseAgent):
    """Agent for sending data to external webhooks."""
    
    def __init__(self, name: str = "Webhook"):
        super().__init__(name)
        self.webhook_url = None
        self.method = "POST"
        self.headers = {}
    
    def configure(self, webhook_url: str, method: str = "POST", 
                  headers: Optional[Dict[str, str]] = None):
        """
        Configure the webhook.
        
        Args:
            webhook_url: URL to send the webhook to
            method: HTTP method (POST, GET, PUT, etc.)
            headers: Optional custom headers
        """
        self.webhook_url = webhook_url
        self.method = method.upper()
        self.headers = headers or {'Content-Type': 'application/json'}
    
    def execute(self, input_data: Any = None) -> Dict[str, Any]:
        """
        Send data to the webhook.
        
        Args:
            input_data: Data to send to the webhook
        
        Returns:
            Dictionary with response information
        """
        self.status = "executing"
        
        if not self.webhook_url:
            self.status = "error: Webhook URL not configured"
            self.output = {'success': False, 'error': 'URL not configured'}
            return self.output
        
        try:
            # Prepare the data
            if isinstance(input_data, (dict, list)):
                import json
                data = json.dumps(input_data)
            else:
                data = str(input_data)
            
            # Send the request
            if self.method == "POST":
                response = requests.post(self.webhook_url, data=data, 
                                       headers=self.headers, timeout=30)
            elif self.method == "GET":
                response = requests.get(self.webhook_url, headers=self.headers, 
                                      timeout=30)
            elif self.method == "PUT":
                response = requests.put(self.webhook_url, data=data, 
                                      headers=self.headers, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {self.method}")
            
            # Process response
            self.output = {
                'success': response.status_code < 400,
                'status_code': response.status_code,
                'response_text': response.text[:500],  # Limit response size
                'headers': dict(response.headers)
            }
            
            if response.status_code < 400:
                self.status = f"completed: {response.status_code}"
            else:
                self.status = f"warning: HTTP {response.status_code}"
            
        except Exception as e:
            self.status = f"error: {str(e)}"
            self.output = {'success': False, 'error': str(e)}
        
        return self.output
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Return configuration schema."""
        return {
            'webhook_url': 'string (required) - URL to send webhook to',
            'method': 'string (optional, default: POST) - HTTP method',
            'headers': 'dict (optional) - Custom HTTP headers'
        }
