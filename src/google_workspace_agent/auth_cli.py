"""
Authentication CLI for Google Workspace Intelligent Agent.

Provides an interactive command-line interface for OAuth 2.0 authentication
and token management.
"""

import os
import sys
import webbrowser
from typing import Optional
import json
import logging

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class GoogleWorkspaceAuthCLI:
    """
    Command-line interface for Google Workspace authentication.
    Handles OAuth 2.0 flow, token management, and credential storage.
    """
    
    # Comprehensive OAuth scopes for all integrated services
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
        Initialize authentication CLI.
        
        Args:
            credentials_path: Path to OAuth 2.0 client credentials
            token_path: Path to store access tokens
        """
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Set paths
        self.credentials_path = credentials_path or self._default_credentials_path()
        self.token_path = token_path or self._default_token_path()
    
    @staticmethod
    def _default_credentials_path() -> str:
        """
        Get default path for OAuth 2.0 client credentials.
        
        Returns:
            Path to credentials file
        """
        return os.path.expanduser('~/.google/workspace_agent_credentials.json')
    
    @staticmethod
    def _default_token_path() -> str:
        """
        Get default path for storing access tokens.
        
        Returns:
            Path to token file
        """
        return os.path.expanduser('~/.google/workspace_agent_token.json')
    
    def authenticate(self) -> Credentials:
        """
        Perform OAuth 2.0 authentication flow.
        
        Returns:
            Authenticated Google API credentials
        """
        credentials = None
        
        # Try to load existing credentials
        if os.path.exists(self.token_path):
            try:
                credentials = Credentials.from_authorized_user_file(
                    self.token_path, self.SCOPES
                )
            except Exception as e:
                self.logger.warning(f"Failed to load existing credentials: {e}")
        
        # Refresh if credentials are invalid or expired
        if credentials and credentials.valid:
            if credentials.expired and credentials.refresh_token:
                try:
                    credentials.refresh(Request())
                except Exception as e:
                    self.logger.warning(f"Failed to refresh credentials: {e}")
                    credentials = None
        
        # Initiate new authentication flow if no valid credentials
        if not credentials:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES
                )
                credentials = flow.run_local_server(port=0)
            except Exception as e:
                self.logger.error(f"Authentication failed: {e}")
                sys.exit(1)
        
        # Ensure token directory exists
        os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
        
        # Save the credentials for the next run
        with open(self.token_path, 'w') as token:
            token.write(credentials.to_json())
        
        self.logger.info("Authentication successful!")
        return credentials
    
    def revoke_credentials(self) -> None:
        """
        Revoke and remove stored credentials.
        """
        try:
            if os.path.exists(self.token_path):
                os.unlink(self.token_path)
                self.logger.info("Credentials revoked and token file removed.")
        except Exception as e:
            self.logger.error(f"Error revoking credentials: {e}")
    
    def interactive_setup(self) -> None:
        """
        Interactive authentication setup with user guidance.
        """
        print("Google Workspace Authentication Setup")
        print("--------------------------------------")
        
        # Check for existing credentials file
        if not os.path.exists(self.credentials_path):
            print("\nCredentials file not found.")
            print("Please follow these steps:")
            print("1. Go to https://console.cloud.google.com/")
            print("2. Create a new project or select an existing one")
            print("3. Enable the following APIs:")
            for scope in self.SCOPES:
                print(f"   - {scope.split('/')[-1]}")
            print("4. Create OAuth 2.0 credentials")
            print("5. Download the credentials JSON file")
            print(f"6. Save the file at: {self.credentials_path}")
            
            input("\nPress Enter after downloading and saving the credentials file...")
        
        # Perform authentication
        try:
            credentials = self.authenticate()
            print("\nAuthentication successful!")
            print(f"Credentials saved to: {self.token_path}")
        except Exception as e:
            print(f"Authentication failed: {e}")
            sys.exit(1)

def main():
    """
    Main entry point for authentication CLI.
    """
    auth_cli = GoogleWorkspaceAuthCLI()
    auth_cli.interactive_setup()

if __name__ == '__main__':
    main()
