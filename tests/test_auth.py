"""
Unit tests for Google Workspace authentication module.
"""

import os
import tempfile
import pytest
from google_workspace_agent.auth import GoogleWorkspaceAuth

class TestGoogleWorkspaceAuth:
    @pytest.fixture
    def temp_credentials_file(self):
        """Create a temporary credentials file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_cred:
            temp_cred.write('''{
                "installed": {
                    "client_id": "test_client_id",
                    "client_secret": "test_client_secret",
                    "redirect_uris": ["http://localhost"]
                }
            }''')
            temp_cred_path = temp_cred.name
        
        yield temp_cred_path
        
        # Cleanup
        if os.path.exists(temp_cred_path):
            os.unlink(temp_cred_path)
    
    @pytest.fixture
    def temp_token_file(self):
        """Create a temporary token file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_token:
            temp_token_path = temp_token.name
        
        yield temp_token_path
        
        # Cleanup
        if os.path.exists(temp_token_path):
            os.unlink(temp_token_path)
    
    def test_initialization(self, temp_credentials_file):
        """Test authentication class initialization."""
        auth = GoogleWorkspaceAuth(
            credentials_path=temp_credentials_file
        )
        
        assert auth.credentials_path == temp_credentials_file
        assert auth.credentials is None
    
    def test_default_paths(self):
        """Test default path generation for credentials and tokens."""
        auth = GoogleWorkspaceAuth()
        
        assert auth.credentials_path.endswith('workspace_agent_credentials.json')
        assert auth.token_path.endswith('workspace_agent_token.json')
    
    def test_revoke_credentials(self, temp_credentials_file, temp_token_file):
        """Test credential revocation."""
        auth = GoogleWorkspaceAuth(
            credentials_path=temp_credentials_file,
            token_path=temp_token_file
        )
        
        # Create a dummy token file
        with open(temp_token_file, 'w') as f:
            f.write('dummy_token')
        
        assert os.path.exists(temp_token_file)
        
        auth.revoke_credentials()
        
        assert not os.path.exists(temp_token_file)
        assert auth.credentials is None
