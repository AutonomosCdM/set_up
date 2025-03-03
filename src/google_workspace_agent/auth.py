"""
Authentication module for Google Workspace Agent.

Handles OAuth 2.0 authentication and token management for Google Workspace services.
"""

from typing import Dict, Any, Optional
import os
from pathlib import Path
import json

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleWorkspaceAuth:
    """
    Manages authentication for Google Workspace services.
    
    Handles OAuth 2.0 flow, token storage, and refresh.
    """
    
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/documents'
    ]
    
    def __init__(self, 
                 credentials_path: Optional[str] = None, 
                 token_path: Optional[str] = None):
        """
        Initialize Google Workspace authentication.
        
        Args:
            credentials_path: Path to OAuth 2.0 client credentials JSON file
            token_path: Path to store/load access tokens
        """
        self.credentials_path = credentials_path or self._default_credentials_path()
        self.token_path = token_path or self._default_token_path()
        self.credentials = None
    
    @staticmethod
    def _default_credentials_path() -> str:
        """
        Get default path for OAuth 2.0 client credentials.
        
        Returns:
            Path to credentials file in user's home directory
        """
        return str(Path.home() / '.google' / 'workspace_agent_credentials.json')
    
    @staticmethod
    def _default_token_path() -> str:
        """
        Get default path for storing access tokens.
        
        Returns:
            Path to token file in user's home directory
        """
        return str(Path.home() / '.google' / 'workspace_agent_token.json')
    
    def authenticate(self) -> Credentials:
        """
        Perform OAuth 2.0 authentication flow.
        
        Returns:
            Authenticated Google API credentials
        """
        credentials = None
        
        # Try to load existing credentials
        if os.path.exists(self.token_path):
            credentials = Credentials.from_authorized_user_file(
                self.token_path, self.SCOPES
            )
        
        # Refresh if credentials are invalid or expired
        if credentials and credentials.valid:
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
        else:
            # Initiate new authentication flow
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, self.SCOPES
            )
            credentials = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(self.token_path, 'w') as token:
            token.write(credentials.to_json())
        
        self.credentials = credentials
        return credentials
    
    def get_credentials(self) -> Credentials:
        """
        Get current credentials, authenticating if necessary.
        
        Returns:
            Authenticated Google API credentials
        """
        if not self.credentials:
            self.authenticate()
        return self.credentials
    
    def revoke_credentials(self) -> None:
        """
        Revoke and remove stored credentials.
        """
        if os.path.exists(self.token_path):
            os.unlink(self.token_path)
        self.credentials = None
