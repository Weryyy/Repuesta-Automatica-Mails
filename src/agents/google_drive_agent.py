"""
Google Drive Agent - Uploads files to Google Drive.
"""
import os
from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent


class GoogleDriveAgent(BaseAgent):
    """Agent for uploading files to Google Drive."""
    
    def __init__(self, name: str = "GoogleDrive"):
        super().__init__(name)
        self.credentials = None
        self.service = None
        self.folder_id = None
    
    def configure(self, credentials_file: Optional[str] = None, 
                  token: Optional[Dict] = None,
                  folder_id: Optional[str] = None):
        """
        Configure Google Drive access.
        
        Args:
            credentials_file: Path to credentials JSON file
            token: OAuth2 token dictionary
            folder_id: Optional folder ID to upload to
        """
        self.credentials_file = credentials_file
        self.token = token
        self.folder_id = folder_id
        
        if credentials_file or token:
            self._initialize_service()
    
    def _initialize_service(self):
        """Initialize the Google Drive service."""
        try:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import Request
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/drive.file']
            
            creds = None
            
            # Load from token if available
            if self.token:
                creds = Credentials.from_authorized_user_info(self.token, SCOPES)
            
            # Load from credentials file
            elif self.credentials_file and os.path.exists(self.credentials_file):
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Refresh if needed
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            if creds:
                self.service = build('drive', 'v3', credentials=creds)
                self.status = "connected"
            else:
                self.status = "error: No valid credentials"
                
        except Exception as e:
            self.status = f"error: {str(e)}"
            self.service = None
    
    def execute(self, input_data: Any = None) -> Dict[str, Any]:
        """
        Upload a file to Google Drive.
        
        Args:
            input_data: Dictionary with:
                - file_path: Path to the file to upload
                - file_name: Optional custom name for the file
                - mime_type: Optional MIME type
        
        Returns:
            Dictionary with upload results
        """
        self.status = "executing"
        
        if not self.service:
            self.status = "error: Google Drive service not initialized"
            self.output = {'success': False, 'error': 'Service not initialized'}
            return self.output
        
        # Parse input
        if isinstance(input_data, str):
            # Assume it's a file path
            file_path = input_data
            file_name = os.path.basename(file_path)
        elif isinstance(input_data, dict):
            file_path = input_data.get('file_path')
            file_name = input_data.get('file_name', os.path.basename(file_path) if file_path else None)
        else:
            self.status = "error: Invalid input data"
            self.output = {'success': False, 'error': 'Invalid input'}
            return self.output
        
        if not file_path or not os.path.exists(file_path):
            self.status = "error: File not found"
            self.output = {'success': False, 'error': 'File not found'}
            return self.output
        
        try:
            from googleapiclient.http import MediaFileUpload
            
            # Prepare file metadata
            file_metadata = {'name': file_name}
            if self.folder_id:
                file_metadata['parents'] = [self.folder_id]
            
            # Upload file
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()
            
            self.output = {
                'success': True,
                'file_id': file.get('id'),
                'file_name': file.get('name'),
                'web_link': file.get('webViewLink')
            }
            self.status = f"completed: Uploaded {file_name}"
            
        except Exception as e:
            self.status = f"error: {str(e)}"
            self.output = {'success': False, 'error': str(e)}
        
        return self.output
    
    def list_files(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        List files in Google Drive.
        
        Args:
            max_results: Maximum number of files to return
        
        Returns:
            List of file dictionaries
        """
        if not self.service:
            return []
        
        try:
            results = self.service.files().list(
                pageSize=max_results,
                fields="files(id, name, mimeType, modifiedTime)"
            ).execute()
            
            return results.get('files', [])
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Return configuration schema."""
        return {
            'credentials_file': 'string (optional) - Path to Google credentials JSON',
            'token': 'dict (optional) - OAuth2 token dictionary',
            'folder_id': 'string (optional) - Google Drive folder ID to upload to'
        }
