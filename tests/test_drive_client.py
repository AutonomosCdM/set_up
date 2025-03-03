"""
Unit tests for Drive Service Client module.
"""

import pytest
import os
from unittest.mock import Mock, patch, mock_open
from io import BytesIO

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from google_workspace_agent.drive_client import DriveClient

class TestDriveClient:
    @pytest.fixture
    def mock_credentials(self):
        """Create a mock Credentials object."""
        return Mock(spec=Credentials)
    
    @pytest.fixture
    def drive_client(self, mock_credentials):
        """Create a DriveClient instance for testing."""
        with patch('googleapiclient.discovery.build') as mock_build:
            mock_service = Mock()
            mock_build.return_value = mock_service
            
            client = DriveClient(mock_credentials)
            client._service = mock_service
            return client
    
    def test_list_files(self, drive_client):
        """Test listing files in Google Drive."""
        # Mock the list method response
        mock_list_response = {
            'files': [
                {'id': 'file1', 'name': 'Document 1', 'mimeType': 'application/vnd.google-apps.document'},
                {'id': 'file2', 'name': 'Spreadsheet 1', 'mimeType': 'application/vnd.google-apps.spreadsheet'}
            ]
        }
        
        # Set up mock service method
        drive_client._service.files().list.return_value.execute.return_value = mock_list_response
        
        # Call list_items method
        files = drive_client.list_items(max_results=2)
        
        # Verify results
        assert len(files) == 2
        assert files[0]['id'] == 'file1'
        assert files[1]['name'] == 'Spreadsheet 1'
        
        # Verify service method was called with correct parameters
        drive_client._service.files().list.assert_called_once_with(
            pageSize=2,
            orderBy='modifiedTime desc',
            fields='files(id, name, mimeType, modifiedTime, owners, size)'
        )
    
    def test_get_file(self, drive_client):
        """Test retrieving a specific file metadata."""
        # Mock the get method response
        mock_file_response = {
            'id': 'file1',
            'name': 'Test Document',
            'mimeType': 'application/vnd.google-apps.document',
            'webViewLink': 'https://docs.google.com/document/d/file1'
        }
        
        # Set up mock service method
        drive_client._service.files().get.return_value.execute.return_value = mock_file_response
        
        # Call get_item method
        file_metadata = drive_client.get_item('file1')
        
        # Verify results
        assert file_metadata['id'] == 'file1'
        assert file_metadata['name'] == 'Test Document'
        
        # Verify service method was called with correct parameters
        drive_client._service.files().get.assert_called_once_with(
            fileId='file1',
            fields='id, name, mimeType, modifiedTime, owners, size, webViewLink'
        )
    
    def test_create_file(self, drive_client):
        """Test creating a new file in Google Drive."""
        # Mock the create method response
        mock_create_response = {
            'id': 'new_file1',
            'name': 'New Document',
            'mimeType': 'application/vnd.google-apps.document',
            'webViewLink': 'https://docs.google.com/document/d/new_file1'
        }
        
        # Set up mock service method
        drive_client._service.files().create.return_value.execute.return_value = mock_create_response
        
        # Call create_item method
        new_file = drive_client.create_item(
            name='New Document', 
            parent_id='folder1'
        )
        
        # Verify results
        assert new_file['id'] == 'new_file1'
        assert new_file['name'] == 'New Document'
        
        # Verify service method was called with correct parameters
        drive_client._service.files().create.assert_called_once_with(
            body={
                'name': 'New Document', 
                'mimeType': 'application/vnd.google-apps.document',
                'parents': ['folder1']
            },
            fields='id, name, mimeType, webViewLink'
        )
    
    def test_update_file(self, drive_client):
        """Test updating file metadata."""
        # Mock the update method response
        mock_update_response = {
            'id': 'file1',
            'name': 'Updated Document',
            'mimeType': 'application/vnd.google-apps.document'
        }
        
        # Set up mock service method
        drive_client._service.files().update.return_value.execute.return_value = mock_update_response
        
        # Call update_item method
        update_data = {'name': 'Updated Document'}
        updated_file = drive_client.update_item('file1', update_data)
        
        # Verify results
        assert updated_file['id'] == 'file1'
        assert updated_file['name'] == 'Updated Document'
        
        # Verify service method was called with correct parameters
        drive_client._service.files().update.assert_called_once_with(
            fileId='file1',
            body=update_data,
            fields='id, name, mimeType'
        )
    
    def test_delete_file(self, drive_client):
        """Test deleting a file."""
        # Set up mock service method
        drive_client._service.files().delete.return_value.execute.return_value = None
        
        # Call delete_item method
        result = drive_client.delete_item('file1')
        
        # Verify results
        assert result is True
        
        # Verify service method was called with correct parameters
        drive_client._service.files().delete.assert_called_once_with(fileId='file1')
    
    def test_download_file(self, drive_client):
        """Test downloading a file from Google Drive."""
        # Prepare mock download data
        mock_file_content = b'Test file content'
        
        # Mock the download process
        mock_downloader = Mock()
        mock_downloader.next_chunk.side_effect = [
            (Mock(), False),  # First chunk
            (Mock(), True)   # Last chunk
        ]
        
        # Patch MediaIoBaseDownload to return our mock
        with patch('googleapiclient.http.MediaIoBaseDownload', return_value=mock_downloader):
            # Mock get_media method
            drive_client._service.files().get_media.return_value = Mock()
            
            # Call download_file method with BytesIO
            file_content = drive_client.download_file('file1')
            
            # Verify results
            assert file_content == mock_file_content
    
    def test_upload_file(self, drive_client):
        """Test uploading a file to Google Drive."""
        # Mock the upload method response
        mock_upload_response = {
            'id': 'uploaded_file1',
            'name': 'test_upload.txt',
            'mimeType': 'text/plain',
            'webViewLink': 'https://drive.google.com/file/d/uploaded_file1'
        }
        
        # Patch MediaFileUpload
        with patch('googleapiclient.http.MediaFileUpload') as mock_media_upload:
            # Set up mock service method
            drive_client._service.files().create.return_value.execute.return_value = mock_upload_response
            
            # Call upload_file method
            uploaded_file = drive_client.upload_file(
                local_path='/path/to/test_upload.txt', 
                parent_id='folder1'
            )
            
            # Verify results
            assert uploaded_file['id'] == 'uploaded_file1'
            assert uploaded_file['name'] == 'test_upload.txt'
    
    def test_api_error_handling(self, drive_client):
        """Test error handling for API errors."""
        # Create a mock HTTP error
        mock_error = HttpError(
            resp=Mock(status=403, reason='Forbidden'), 
            content=b'Permission denied'
        )
        
        # Set up mock service method to raise HttpError
        drive_client._service.files().list.return_value.execute.side_effect = mock_error
        
        # Verify that handle_api_error is called and re-raises the error
        with pytest.raises(HttpError):
            drive_client.list_items()
