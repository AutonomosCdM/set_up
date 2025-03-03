"""
Unit tests for Workspace Integration module.
"""

import pytest
from unittest.mock import Mock, patch
import json

from google.oauth2.credentials import Credentials

from google_workspace_agent.integration import WorkspaceIntegration
from google_workspace_agent.auth import GoogleWorkspaceAuth
from google_workspace_agent.llm_client import GroqLLMClient

class TestWorkspaceIntegration:
    @pytest.fixture
    def mock_credentials(self):
        """Create a mock GoogleWorkspaceAuth object."""
        mock_auth = Mock(spec=GoogleWorkspaceAuth)
        mock_credentials = Mock(spec=Credentials)
        mock_auth.get_credentials.return_value = mock_credentials
        return mock_auth
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create a mock GroqLLMClient."""
        return Mock(spec=GroqLLMClient)
    
    @pytest.fixture
    def workspace_integration(self, mock_credentials, mock_llm_client):
        """Create a WorkspaceIntegration instance for testing."""
        with patch('googleapiclient.discovery.build'):
            integration = WorkspaceIntegration(
                credentials=mock_credentials, 
                llm_client=mock_llm_client
            )
            return integration
    
    def test_initialization(self, workspace_integration):
        """Test WorkspaceIntegration initialization."""
        assert hasattr(workspace_integration, 'gmail_client')
        assert hasattr(workspace_integration, 'calendar_client')
        assert hasattr(workspace_integration, 'drive_client')
        assert hasattr(workspace_integration, 'sheets_client')
        assert hasattr(workspace_integration, 'docs_client')
        assert hasattr(workspace_integration, 'llm_client')
    
    def test_extract_intent_success(self, workspace_integration, mock_llm_client):
        """Test intent extraction with successful LLM response."""
        # Mock LLM response
        mock_llm_client.generate_response.return_value = json.dumps({
            'service': 'email',
            'action': 'send',
            'details': {
                'to': 'test@example.com',
                'subject': 'Test Subject',
                'body': 'Test Body'
            }
        })
        
        # Call method
        intent = workspace_integration._extract_intent("Send an email to test@example.com")
        
        # Verify results
        assert intent['service'] == 'email'
        assert intent['action'] == 'send'
        assert intent['details']['to'] == 'test@example.com'
    
    def test_extract_intent_parsing_failure(self, workspace_integration, mock_llm_client):
        """Test intent extraction with invalid JSON response."""
        # Mock LLM response with invalid JSON
        mock_llm_client.generate_response.return_value = "Invalid JSON"
        
        # Call method
        intent = workspace_integration._extract_intent("Complex request")
        
        # Verify fallback intent
        assert intent['service'] == 'multi'
        assert intent['action'] == 'interpret'
        assert intent['details'] == 'Complex request'
    
    def test_handle_email_request(self, workspace_integration, mock_llm_client):
        """Test handling an email request."""
        # Prepare mock intent
        intent = {
            'service': 'email',
            'action': 'send',
            'details': {
                'to': 'test@example.com',
                'subject': 'Test Subject',
                'body': 'Test Body'
            }
        }
        
        # Mock Gmail client
        mock_send_result = {'id': 'sent_email_id'}
        workspace_integration.gmail_client.create_item.return_value = mock_send_result
        
        # Call method
        result = workspace_integration._handle_email_request(intent)
        
        # Verify results
        assert result['status'] == 'success'
        assert result['result'] == mock_send_result
        
        # Verify service method was called
        workspace_integration.gmail_client.create_item.assert_called_once_with(
            to='test@example.com',
            subject='Test Subject',
            body='Test Body'
        )
    
    def test_handle_multi_service_request(self, workspace_integration, mock_llm_client):
        """Test handling a multi-service request."""
        # Mock LLM breakdown response
        mock_llm_client.generate_response.return_value = json.dumps({
            'email': {
                'action': 'send',
                'details': {
                    'to': 'test@example.com',
                    'subject': 'Test Subject',
                    'body': 'Test Body'
                }
            },
            'calendar': {
                'action': 'create',
                'details': {
                    'summary': 'Team Meeting',
                    'start_time': '2025-03-15T10:00:00Z',
                    'end_time': '2025-03-15T11:00:00Z'
                }
            }
        })
        
        # Mock service clients
        mock_email_result = {'id': 'sent_email_id'}
        mock_calendar_result = {'id': 'created_event_id'}
        workspace_integration.gmail_client.create_item.return_value = mock_email_result
        workspace_integration.calendar_client.create_item.return_value = mock_calendar_result
        
        # Prepare intent
        intent = {
            'service': 'multi',
            'details': 'Send an email and create a calendar event'
        }
        
        # Call method
        result = workspace_integration._handle_multi_service_request(intent)
        
        # Verify results
        assert result['status'] == 'success'
        assert 'results' in result
        assert 'email' in result['results']
        assert 'calendar' in result['results']
        assert result['results']['email']['result'] == mock_email_result
        assert result['results']['calendar']['result'] == mock_calendar_result
    
    def test_process_natural_language_request(self, workspace_integration, mock_llm_client):
        """Test processing a complete natural language request."""
        # Mock intent extraction
        mock_llm_client.generate_response.return_value = json.dumps({
            'service': 'email',
            'action': 'send',
            'details': {
                'to': 'test@example.com',
                'subject': 'Test Subject',
                'body': 'Test Body'
            }
        })
        
        # Mock Gmail client
        mock_send_result = {'id': 'sent_email_id'}
        workspace_integration.gmail_client.create_item.return_value = mock_send_result
        
        # Call method
        result = workspace_integration.process_natural_language_request(
            "Send an email to test@example.com with subject 'Test Subject'"
        )
        
        # Verify results
        assert result['status'] == 'success'
        assert result['result'] == mock_send_result
