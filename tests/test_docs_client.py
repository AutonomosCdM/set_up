"""
Unit tests for Docs Service Client module.
"""

import pytest
from unittest.mock import Mock, patch

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from google_workspace_agent.docs_client import DocsClient

class TestDocsClient:
    @pytest.fixture
    def mock_credentials(self):
        """Create a mock Credentials object."""
        return Mock(spec=Credentials)
    
    @pytest.fixture
    def docs_client(self, mock_credentials):
        """Create a DocsClient instance for testing."""
        with patch('googleapiclient.discovery.build') as mock_build:
            mock_service = Mock()
            mock_build.return_value = mock_service
            
            # Add mock drive service to service resources
            mock_service.service_resources = {
                'drive': Mock()
            }
            
            client = DocsClient(mock_credentials)
            client._service = mock_service
            return client
    
    def test_list_documents(self, docs_client):
        """Test listing documents."""
        # Mock the list method response
        mock_list_response = {
            'files': [
                {'id': 'doc1', 'name': 'Project Proposal'},
                {'id': 'doc2', 'name': 'Meeting Notes'}
            ]
        }
        
        # Set up mock service method
        docs_client._service.service_resources['drive'].files().list.return_value.execute.return_value = mock_list_response
        
        # Call list_items method
        documents = docs_client.list_items(max_results=2)
        
        # Verify results
        assert len(documents) == 2
        assert documents[0]['id'] == 'doc1'
        assert documents[1]['name'] == 'Meeting Notes'
        
        # Verify service method was called with correct parameters
        docs_client._service.service_resources['drive'].files().list.assert_called_once_with(
            pageSize=2,
            q="mimeType='application/vnd.google-apps.document'"
        )
    
    def test_get_document(self, docs_client):
        """Test retrieving a specific document metadata."""
        # Mock the get method response
        mock_document_response = {
            'documentId': 'doc1',
            'title': 'Project Proposal',
            'body': {
                'content': [
                    {'paragraph': {'elements': [{'textRun': {'content': 'Introduction'}}]}}
                ]
            }
        }
        
        # Set up mock service method
        docs_client._service.documents().get.return_value.execute.return_value = mock_document_response
        
        # Call get_item method
        document = docs_client.get_item('doc1')
        
        # Verify results
        assert document['documentId'] == 'doc1'
        assert document['title'] == 'Project Proposal'
        
        # Verify service method was called with correct parameters
        docs_client._service.documents().get.assert_called_once_with(
            documentId='doc1'
        )
    
    def test_create_document(self, docs_client):
        """Test creating a new document."""
        # Mock the create method response
        mock_create_response = {
            'documentId': 'new_doc1',
            'title': 'New Document'
        }
        
        # Set up mock service method
        docs_client._service.documents().create.return_value.execute.return_value = mock_create_response
        
        # Call create_item method
        new_document = docs_client.create_item(
            title='New Document', 
            content=[{'text': 'Initial content'}]
        )
        
        # Verify results
        assert new_document['documentId'] == 'new_doc1'
        assert new_document['title'] == 'New Document'
        
        # Verify service methods were called
        docs_client._service.documents().create.assert_called_once()
        docs_client._service.documents().batchUpdate.assert_called_once()
    
    def test_update_document(self, docs_client):
        """Test updating a document."""
        # Mock the batchUpdate method response
        mock_update_response = {
            'documentId': 'doc1',
            'replies': [{'updateTextStyle': {}}]
        }
        
        # Set up mock service method
        docs_client._service.documents().batchUpdate.return_value.execute.return_value = mock_update_response
        
        # Prepare update requests
        updates = [{
            'updateTextStyle': {
                'range': {'startIndex': 1, 'endIndex': 10},
                'textStyle': {'bold': True}
            }
        }]
        
        # Call update_item method
        updated_document = docs_client.update_item('doc1', updates)
        
        # Verify results
        assert updated_document['documentId'] == 'doc1'
        
        # Verify service method was called with correct parameters
        docs_client._service.documents().batchUpdate.assert_called_once_with(
            documentId='doc1',
            body={'requests': updates}
        )
    
    def test_delete_document(self, docs_client):
        """Test deleting a document."""
        # Set up mock service method
        docs_client._service.service_resources['drive'].files().delete.return_value.execute.return_value = None
        
        # Call delete_item method
        result = docs_client.delete_item('doc1')
        
        # Verify results
        assert result is True
        
        # Verify service method was called with correct parameters
        docs_client._service.service_resources['drive'].files().delete.assert_called_once_with(
            fileId='doc1'
        )
    
    def test_append_text(self, docs_client):
        """Test appending text to a document."""
        # Mock the get_item method to return document length
        docs_client._get_document_length = Mock(return_value=10)
        
        # Mock the batchUpdate method response
        mock_append_response = {
            'documentId': 'doc1',
            'replies': [{'insertText': {}}]
        }
        
        # Set up mock service method
        docs_client._service.documents().batchUpdate.return_value.execute.return_value = mock_append_response
        
        # Call append_text method
        result = docs_client.append_text('doc1', 'New text to append')
        
        # Verify results
        assert result['documentId'] == 'doc1'
        
        # Verify service method was called with correct parameters
        docs_client._service.documents().batchUpdate.assert_called_once_with(
            documentId='doc1',
            body={'requests': [{
                'insertText': {
                    'location': {'index': 10},
                    'text': 'New text to append'
                }
            }]}
        )
    
    def test_api_error_handling(self, docs_client):
        """Test error handling for API errors."""
        # Create a mock HTTP error
        mock_error = HttpError(
            resp=Mock(status=403, reason='Forbidden'), 
            content=b'Permission denied'
        )
        
        # Set up mock service method to raise HttpError
        docs_client._service.service_resources['drive'].files().list.return_value.execute.side_effect = mock_error
        
        # Verify that handle_api_error is called and re-raises the error
        with pytest.raises(HttpError):
            docs_client.list_items()
