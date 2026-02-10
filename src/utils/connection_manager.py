"""
Connection Manager - Manages credentials and connections for external services.
"""
import os
import json
from typing import Dict, Any, Optional, List
from pathlib import Path


class ConnectionManager:
    """Manages connections and credentials for external services."""
    
    def __init__(self, storage_path: str = "connections.json"):
        """
        Initialize the connection manager.
        
        Args:
            storage_path: Path to store connection data
        """
        self.storage_path = storage_path
        self.connections: Dict[str, Dict[str, Any]] = {}
        self.load_connections()
    
    def load_connections(self):
        """Load connections from storage file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    self.connections = json.load(f)
            except Exception as e:
                print(f"Error loading connections: {e}")
                self.connections = {}
        else:
            self.connections = {}
    
    def save_connections(self):
        """Save connections to storage file."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.connections, f, indent=2)
        except Exception as e:
            print(f"Error saving connections: {e}")
    
    def add_connection(self, name: str, service_type: str, credentials: Dict[str, Any]):
        """
        Add a new connection.
        
        Args:
            name: Name of the connection
            service_type: Type of service (email, google_drive, webhook, openai, etc.)
            credentials: Credentials dictionary
        """
        self.connections[name] = {
            'service_type': service_type,
            'credentials': credentials,
            'created_at': str(Path(self.storage_path).stat().st_mtime if os.path.exists(self.storage_path) else 0)
        }
        self.save_connections()
    
    def remove_connection(self, name: str) -> bool:
        """
        Remove a connection.
        
        Args:
            name: Name of the connection to remove
            
        Returns:
            True if removed, False if not found
        """
        if name in self.connections:
            del self.connections[name]
            self.save_connections()
            return True
        return False
    
    def get_connection(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a connection by name.
        
        Args:
            name: Name of the connection
            
        Returns:
            Connection dictionary or None if not found
        """
        return self.connections.get(name)
    
    def list_connections(self, service_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all connections, optionally filtered by service type.
        
        Args:
            service_type: Optional service type to filter by
            
        Returns:
            List of connection dictionaries
        """
        connections_list = []
        for name, data in self.connections.items():
            if service_type is None or data['service_type'] == service_type:
                # Don't include full credentials in list
                connections_list.append({
                    'name': name,
                    'service_type': data['service_type'],
                    'created_at': data.get('created_at', 'unknown')
                })
        return connections_list
    
    def get_credentials(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get credentials for a connection.
        
        Args:
            name: Name of the connection
            
        Returns:
            Credentials dictionary or None if not found
        """
        connection = self.get_connection(name)
        if connection:
            return connection.get('credentials')
        return None
    
    def test_connection(self, name: str) -> Dict[str, Any]:
        """
        Test a connection.
        
        Args:
            name: Name of the connection to test
            
        Returns:
            Dictionary with test results
        """
        connection = self.get_connection(name)
        if not connection:
            return {'success': False, 'error': 'Connection not found'}
        
        service_type = connection['service_type']
        
        # Basic validation - actual testing would be done by agents
        if service_type == 'email':
            required = ['email_address', 'password', 'imap_server']
            credentials = connection['credentials']
            missing = [k for k in required if k not in credentials or not credentials[k]]
            if missing:
                return {'success': False, 'error': f'Missing credentials: {", ".join(missing)}'}
            return {'success': True, 'message': 'Email connection configured (test by using EmailReader agent)'}
        
        elif service_type == 'google_drive':
            credentials = connection['credentials']
            if 'token' not in credentials and 'credentials_file' not in credentials:
                return {'success': False, 'error': 'Missing Google Drive credentials'}
            return {'success': True, 'message': 'Google Drive connection configured'}
        
        elif service_type == 'webhook':
            credentials = connection['credentials']
            if 'url' not in credentials:
                return {'success': False, 'error': 'Missing webhook URL'}
            return {'success': True, 'message': 'Webhook configured'}
        
        elif service_type in ['openai', 'anthropic', 'gemini']:
            credentials = connection['credentials']
            if 'api_key' not in credentials:
                return {'success': False, 'error': 'Missing API key'}
            return {'success': True, 'message': f'{service_type.title()} API key configured'}
        
        elif service_type == 'local_model':
            return {'success': True, 'message': 'Local model configured'}
        
        return {'success': False, 'error': f'Unknown service type: {service_type}'}
