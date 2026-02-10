"""
AI Agent - Processes text using AI models (OpenAI, Anthropic, Gemini, or local).
"""
from typing import Dict, Any, Optional
from .base_agent import BaseAgent


class AIAgent(BaseAgent):
    """Agent for processing text with AI models."""
    
    def __init__(self, name: str = "AI"):
        super().__init__(name)
        self.provider = None
        self.api_key = None
        self.model = None
        self.client = None
    
    def configure(self, provider: str = "openai", api_key: Optional[str] = None,
                  model: Optional[str] = None):
        """
        Configure the AI agent.
        
        Args:
            provider: AI provider (openai, anthropic, gemini, local)
            api_key: API key for the provider (not needed for local)
            model: Model name (e.g., gpt-4, claude-3, gemini-pro)
        """
        self.provider = provider.lower()
        self.api_key = api_key
        
        # Set default models
        if not model:
            if self.provider == "openai":
                self.model = "gpt-3.5-turbo"
            elif self.provider == "anthropic":
                self.model = "claude-3-sonnet-20240229"
            elif self.provider == "gemini":
                self.model = "gemini-pro"
            else:
                self.model = "local"
        else:
            self.model = model
        
        # Initialize client
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the AI client based on provider."""
        try:
            if self.provider == "openai":
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
                self.status = "connected"
                
            elif self.provider == "anthropic":
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
                self.status = "connected"
                
            elif self.provider == "gemini":
                # Google Generative AI
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=self.api_key)
                    self.client = genai.GenerativeModel(self.model)
                    self.status = "connected"
                except ImportError:
                    self.status = "error: google-generativeai not installed"
                    self.client = None
                    
            elif self.provider == "local":
                # Local model - would need additional setup
                self.status = "initialized (local model)"
                self.client = "local"
            else:
                self.status = f"error: Unknown provider {self.provider}"
                self.client = None
                
        except Exception as e:
            self.status = f"error: {str(e)}"
            self.client = None
    
    def execute(self, input_data: Any = None) -> str:
        """
        Process text with AI.
        
        Args:
            input_data: Can be:
                - string: Direct prompt
                - dict with 'prompt' and optional 'system_message'
        
        Returns:
            AI-generated text response
        """
        self.status = "executing"
        
        if not self.client:
            self.status = "error: AI client not initialized"
            self.output = "Error: AI client not initialized"
            return self.output
        
        # Parse input
        if isinstance(input_data, str):
            prompt = input_data
            system_message = None
        elif isinstance(input_data, dict):
            prompt = input_data.get('prompt', '')
            system_message = input_data.get('system_message')
        else:
            prompt = str(input_data)
            system_message = None
        
        if not prompt:
            self.status = "error: No prompt provided"
            self.output = "Error: No prompt provided"
            return self.output
        
        try:
            response_text = self._generate_response(prompt, system_message)
            self.output = response_text
            self.status = "completed"
            
        except Exception as e:
            self.status = f"error: {str(e)}"
            self.output = f"Error: {str(e)}"
        
        return self.output
    
    def _generate_response(self, prompt: str, system_message: Optional[str] = None) -> str:
        """Generate response using the configured provider."""
        
        if self.provider == "openai":
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000
            )
            return response.choices[0].message.content
        
        elif self.provider == "anthropic":
            system_param = system_message if system_message else "You are a helpful assistant."
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                system=system_param,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        
        elif self.provider == "gemini":
            full_prompt = f"{system_message}\n\n{prompt}" if system_message else prompt
            response = self.client.generate_content(full_prompt)
            return response.text
        
        elif self.provider == "local":
            # Placeholder for local model
            return f"[Local Model Response] Processed prompt: {prompt[:100]}..."
        
        return "Error: Unknown provider"
    
    def summarize(self, text: str) -> str:
        """
        Summarize text using AI.
        
        Args:
            text: Text to summarize
        
        Returns:
            Summary text
        """
        prompt = f"Summarize the following text concisely:\n\n{text}"
        return self.execute(prompt)
    
    def classify(self, text: str, categories: list) -> str:
        """
        Classify text into categories.
        
        Args:
            text: Text to classify
            categories: List of possible categories
        
        Returns:
            Classification result
        """
        cats = ", ".join(categories)
        prompt = f"Classify the following text into one of these categories: {cats}\n\nText: {text}\n\nCategory:"
        return self.execute(prompt)
    
    def extract_info(self, text: str, fields: list) -> Dict[str, str]:
        """
        Extract specific information from text.
        
        Args:
            text: Text to extract from
            fields: List of fields to extract
        
        Returns:
            Dictionary with extracted information
        """
        fields_str = ", ".join(fields)
        prompt = f"Extract the following information from the text: {fields_str}\n\nText: {text}\n\nProvide the response as a JSON object."
        
        response = self.execute(prompt)
        
        # Try to parse JSON response
        try:
            import json
            return json.loads(response)
        except:
            return {'raw_response': response}
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Return configuration schema."""
        return {
            'provider': 'string (required) - AI provider: openai, anthropic, gemini, local',
            'api_key': 'string (required for cloud providers) - API key',
            'model': 'string (optional) - Model name, defaults per provider'
        }
