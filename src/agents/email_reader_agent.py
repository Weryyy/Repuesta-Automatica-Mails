"""
Email Reader Agent - Reads emails from an IMAP server.
"""
import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Any
from .base_agent import BaseAgent


class EmailReaderAgent(BaseAgent):
    """Agent for reading emails from an IMAP server."""
    
    def __init__(self, name: str = "EmailReader"):
        super().__init__(name)
        self.server = None
        self.config = {}
    
    def configure(self, email_address: str, password: str, 
                  imap_server: str = "imap.gmail.com", 
                  imap_port: int = 993):
        """
        Configure the email reader.
        
        Args:
            email_address: Email address to connect to
            password: Email password or app password
            imap_server: IMAP server address
            imap_port: IMAP server port
        """
        self.config = {
            'email_address': email_address,
            'password': password,
            'imap_server': imap_server,
            'imap_port': imap_port
        }
    
    def connect(self) -> bool:
        """
        Connect to the IMAP server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.server = imaplib.IMAP4_SSL(
                self.config['imap_server'], 
                self.config['imap_port']
            )
            self.server.login(
                self.config['email_address'], 
                self.config['password']
            )
            self.status = "connected"
            return True
        except Exception as e:
            self.status = f"connection_failed: {str(e)}"
            return False
    
    def execute(self, input_data: Any = None) -> List[Dict[str, Any]]:
        """
        Read emails from the inbox.
        
        Args:
            input_data: Dictionary with optional parameters:
                - folder: Email folder to read from (default: "INBOX")
                - max_emails: Maximum number of emails to read (default: 10)
                - unread_only: Only read unread emails (default: False)
        
        Returns:
            List of email dictionaries with keys: subject, from, date, body
        """
        self.status = "executing"
        emails_list = []
        
        # Parse input parameters
        params = input_data or {}
        folder = params.get('folder', 'INBOX')
        max_emails = params.get('max_emails', 10)
        unread_only = params.get('unread_only', False)
        
        try:
            # Connect if not already connected
            if not self.server:
                if not self.connect():
                    return emails_list
            
            # Select the folder
            self.server.select(folder)
            
            # Search for emails
            search_criteria = 'UNSEEN' if unread_only else 'ALL'
            _, message_numbers = self.server.search(None, search_criteria)
            
            # Get the list of email IDs
            email_ids = message_numbers[0].split()
            
            # Limit the number of emails
            email_ids = email_ids[-max_emails:] if len(email_ids) > max_emails else email_ids
            
            # Fetch each email
            for email_id in email_ids:
                _, msg_data = self.server.fetch(email_id, '(RFC822)')
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)
                
                # Decode email subject
                subject = decode_header(email_message["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                
                # Get email from
                from_addr = email_message.get("From")
                
                # Get email date
                date = email_message.get("Date")
                
                # Get email body
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = email_message.get_payload(decode=True).decode()
                
                emails_list.append({
                    'id': email_id.decode(),
                    'subject': subject,
                    'from': from_addr,
                    'date': date,
                    'body': body[:500]  # Limit body to 500 chars
                })
            
            self.output = emails_list
            self.status = "completed"
            
        except Exception as e:
            self.status = f"error: {str(e)}"
            self.output = []
        
        return self.output
    
    def disconnect(self):
        """Disconnect from the IMAP server."""
        if self.server:
            try:
                self.server.close()
                self.server.logout()
            except:
                pass
            self.server = None
            self.status = "disconnected"
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Return configuration schema."""
        return {
            'email_address': 'string (required)',
            'password': 'string (required)',
            'imap_server': 'string (optional, default: imap.gmail.com)',
            'imap_port': 'integer (optional, default: 993)'
        }
