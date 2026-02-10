"""
Utility functions for the email automation system.
"""
import os
from typing import Dict, Any


def load_env_config() -> Dict[str, str]:
    """
    Load configuration from environment variables or .env file.
    
    Returns:
        Dictionary with configuration values
    """
    from dotenv import load_dotenv
    
    # Load .env file if it exists
    load_dotenv()
    
    return {
        'email_address': os.getenv('EMAIL_ADDRESS', ''),
        'email_password': os.getenv('EMAIL_PASSWORD', ''),
        'imap_server': os.getenv('IMAP_SERVER', 'imap.gmail.com'),
        'imap_port': int(os.getenv('IMAP_PORT', '993')),
        'output_folder': os.getenv('OUTPUT_FOLDER', 'output')
    }


def validate_email_config(config: Dict[str, Any]) -> bool:
    """
    Validate email configuration.
    
    Args:
        config: Configuration dictionary
    
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['email_address', 'email_password']
    return all(config.get(field) for field in required_fields)
