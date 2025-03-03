"""
Unit tests for Gmail Service Client module.
"""

import pytest
from unittest.mock import Mock, patch

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from google_workspace_agent.gmail_client import GmailClient

class TestGmailClient:
    @pytest.fixture
    def mock_credentials(self):
        """Create a mock Credentials object."""
        return Mock(spec=Credentials)
    
    @pytest.fixture
    def gmail_client(self, mock_credentials):
        """Create a GmailClient instance for testing."""
        with patch('googleapiclient.discovery.build') as mock_build:
            mock_service = Mock()
            mock_build.return_value = mock_service
            
            client = GmailClient(mock_credentials)
            client._service = mock_service
            return client
    
    def test_list_emails(self, gmail_client):
        """Test listing emails."""
        # Mock the list method response
        mock_list_response = {
            'messages': [
                {'id': 'email1', 'threadId': 'thread1'},
                {'id': 'email2', 'threadId': 'thread2'}
            ]
        }
        
        # Set up mock service method
        gmail_client._service.users().messages().list.return_value.execute.return_value = mock_list_response
        
        # Call list_items method
        emails = gmail_client.list_items(max_results=2)
        
        # Verify results
        assert len(emails) == 2
        assert emails[0]['id'] == 'email1'
        assert emails[1]['id'] == 'email2'
        
        # Verify service method was called with correct parameters
        gmail_client._service.users().messages().list.assert_called_once_with(
            userId='me', 
            maxResults=2
        )
    
    def test_get_email(self, gmail_client):
        """Test retrieving a specific email."""
        # Mock the get method response
        mock_email_response = {
            'id': 'email1',
            'threadId': 'thread1',
            'payload': {
                'headers': [
                    {'name': 'Subject', 'value': 'Test Email'},
                    {'name': 'From', 'value': 'sender@example.com'}
                ]
            }
        }
        
        # Set up mock service method
        gmail_client._service.users().messages().get.return_value.execute.return_value = mock_email_response
        
        # Call get_item method
        email = gmail_client.get_item('email1')
        
        # Verify results
        assert email['id'] == 'email1'
        
        # Verify service method was called with correct parameters
        gmail_client._service.users().messages().get.assert_called_once_with(
            userId='me', 
            id='email1', 
            format='full'
        )
    
    def test_send_email(self, gmail_client):
        """Test sending an email."""
        # Mock the send method response
        mock_send_response = {
            'id': 'sent_email1',
            'threadId': 'thread_sent1'
        }
        
        # Set up mock service method
        gmail_client._service.users().messages().send.return_value.execute.return_value = mock_send_response
        
        # Call create_item method
        sent_email = gmail_client.create_item(
            to='recipient@example.com', 
            subject='Test Subject', 
            body='Test email body'
        )
        
        # Verify results
        assert sent_email['id'] == 'sent_email1'
        
        # Verify service method was called
        gmail_client._service.users().messages().send.assert_called_once()
    
    def test_update_email_labels(self, gmail_client):
        """Test updating email labels."""
        # Mock the modify method response
        mock_modify_response = {
            'id': 'email1',
            'threadId': 'thread1',
            'labelIds': ['INBOX', 'IMPORTANT']
        }
        
        # Set up mock service method
        gmail_client._service.users().messages().modify.return_value.execute.return_value = mock_modify_response
        
        # Call update_item method
        updated_email = gmail_client.update_item(
            message_id='email1', 
            add_labels=['IMPORTANT'], 
            remove_labels=['UNREAD']
        )
        
        # Verify results
        assert updated_email['id'] == 'email1'
        
        # Verify service method was called with correct parameters
        gmail_client._service.users().messages().modify.assert_called_once_with(
            userId='me', 
            id='email1', 
            body={
                'addLabelIds': ['IMPORTANT'], 
                'removeLabelIds': ['UNREAD']
            }
        )
    
    def test_delete_email(self, gmail_client):
        """Test deleting an email."""
        # Set up mock service method
        gmail_client._service.users().messages().delete.return_value.execute.return_value = None
        
        # Call delete_item method
        result = gmail_client.delete_item('email1')
        
        # Verify results
        assert result is True
        
        # Verify service method was called with correct parameters
        gmail_client._service.users().messages().delete.assert_called_once_with(
            userId='me', 
            id='email1'
        )
    
    def test_api_error_handling(self, gmail_client):
        """Test error handling for API errors."""
        # Create a mock HTTP error
        mock_error = HttpError(
            resp=Mock(status=403, reason='Forbidden'), 
            content=b'Permission denied'
        )
        
        # Set up mock service method to raise HttpError
        gmail_client._service.users().messages().list.return_value.execute.side_effect = mock_error
        
        # Verify that handle_api_error is called and re-raises the error
        with pytest.raises(HttpError):
            gmail_client.list_items()
