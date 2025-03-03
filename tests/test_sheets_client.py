"""
Unit tests for Sheets Service Client module.
"""

import pytest
from unittest.mock import Mock, patch

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from google_workspace_agent.sheets_client import SheetsClient

class TestSheetsClient:
    @pytest.fixture
    def mock_credentials(self):
        """Create a mock Credentials object."""
        return Mock(spec=Credentials)
    
    @pytest.fixture
    def sheets_client(self, mock_credentials):
        """Create a SheetsClient instance for testing."""
        with patch('googleapiclient.discovery.build') as mock_build:
            mock_service = Mock()
            mock_build.return_value = mock_service
            
            # Add mock drive service to service resources
            mock_service.service_resources = {
                'drive': Mock()
            }
            
            client = SheetsClient(mock_credentials)
            client._service = mock_service
            return client
    
    def test_list_spreadsheets(self, sheets_client):
        """Test listing spreadsheets."""
        # Mock the list method response
        mock_list_response = {
            'files': [
                {'id': 'sheet1', 'name': 'Quarterly Report'},
                {'id': 'sheet2', 'name': 'Budget Tracker'}
            ]
        }
        
        # Set up mock service method
        sheets_client._service.service_resources['drive'].files().list.return_value.execute.return_value = mock_list_response
        
        # Call list_items method
        spreadsheets = sheets_client.list_items(max_results=2)
        
        # Verify results
        assert len(spreadsheets) == 2
        assert spreadsheets[0]['id'] == 'sheet1'
        assert spreadsheets[1]['name'] == 'Budget Tracker'
        
        # Verify service method was called with correct parameters
        sheets_client._service.service_resources['drive'].files().list.assert_called_once_with(
            pageSize=2,
            q="mimeType='application/vnd.google-apps.spreadsheet'"
        )
    
    def test_get_spreadsheet(self, sheets_client):
        """Test retrieving a specific spreadsheet metadata."""
        # Mock the get method response
        mock_spreadsheet_response = {
            'spreadsheetId': 'sheet1',
            'properties': {
                'title': 'Quarterly Report',
                'locale': 'en_US'
            },
            'sheets': [
                {'properties': {'title': 'Q1 2025'}}
            ]
        }
        
        # Set up mock service method
        sheets_client._service.spreadsheets().get.return_value.execute.return_value = mock_spreadsheet_response
        
        # Call get_item method
        spreadsheet = sheets_client.get_item('sheet1')
        
        # Verify results
        assert spreadsheet['spreadsheetId'] == 'sheet1'
        assert spreadsheet['properties']['title'] == 'Quarterly Report'
        
        # Verify service method was called with correct parameters
        sheets_client._service.spreadsheets().get.assert_called_once_with(
            spreadsheetId='sheet1'
        )
    
    def test_create_spreadsheet(self, sheets_client):
        """Test creating a new spreadsheet."""
        # Mock the create method response
        mock_create_response = {
            'spreadsheetId': 'new_sheet1',
            'properties': {
                'title': 'New Spreadsheet',
                'locale': 'en_US'
            }
        }
        
        # Set up mock service method
        sheets_client._service.spreadsheets().create.return_value.execute.return_value = mock_create_response
        
        # Call create_item method
        new_spreadsheet = sheets_client.create_item(
            title='New Spreadsheet', 
            sheets=[{'title': 'Sheet1'}, {'title': 'Sheet2'}]
        )
        
        # Verify results
        assert new_spreadsheet['spreadsheetId'] == 'new_sheet1'
        assert new_spreadsheet['properties']['title'] == 'New Spreadsheet'
        
        # Verify service method was called with correct parameters
        sheets_client._service.spreadsheets().create.assert_called_once_with(
            body={
                'properties': {'title': 'New Spreadsheet'},
                'sheets': [
                    {'properties': {'title': 'Sheet1'}},
                    {'properties': {'title': 'Sheet2'}}
                ]
            }
        )
    
    def test_update_spreadsheet(self, sheets_client):
        """Test updating spreadsheet metadata."""
        # Mock the batchUpdate method response
        mock_update_response = {
            'spreadsheetId': 'sheet1',
            'replies': [{'updateSpreadsheetProperties': {}}]
        }
        
        # Set up mock service method
        sheets_client._service.spreadsheets().batchUpdate.return_value.execute.return_value = mock_update_response
        
        # Call update_item method
        update_data = {'title': 'Updated Spreadsheet Title'}
        updated_spreadsheet = sheets_client.update_item('sheet1', update_data)
        
        # Verify results
        assert updated_spreadsheet['spreadsheetId'] == 'sheet1'
        
        # Verify service method was called with correct parameters
        sheets_client._service.spreadsheets().batchUpdate.assert_called_once_with(
            spreadsheetId='sheet1',
            body={
                'requests': [{
                    'updateSpreadsheetProperties': {
                        'properties': update_data,
                        'fields': 'title'
                    }
                }]
            }
        )
    
    def test_delete_spreadsheet(self, sheets_client):
        """Test deleting a spreadsheet."""
        # Set up mock service method
        sheets_client._service.service_resources['drive'].files().delete.return_value.execute.return_value = None
        
        # Call delete_item method
        result = sheets_client.delete_item('sheet1')
        
        # Verify results
        assert result is True
        
        # Verify service method was called with correct parameters
        sheets_client._service.service_resources['drive'].files().delete.assert_called_once_with(
            fileId='sheet1'
        )
    
    def test_read_values(self, sheets_client):
        """Test reading values from a spreadsheet range."""
        # Mock the values().get method response
        mock_values_response = {
            'values': [
                ['Name', 'Age', 'City'],
                ['Alice', '30', 'New York'],
                ['Bob', '25', 'San Francisco']
            ]
        }
        
        # Set up mock service method
        sheets_client._service.spreadsheets().values().get.return_value.execute.return_value = mock_values_response
        
        # Call read_values method
        values = sheets_client.read_values('sheet1', 'Sheet1!A1:C3')
        
        # Verify results
        assert len(values) == 3
        assert values[0] == ['Name', 'Age', 'City']
        assert values[2] == ['Bob', '25', 'San Francisco']
        
        # Verify service method was called with correct parameters
        sheets_client._service.spreadsheets().values().get.assert_called_once_with(
            spreadsheetId='sheet1',
            range='Sheet1!A1:C3'
        )
    
    def test_write_values(self, sheets_client):
        """Test writing values to a spreadsheet range."""
        # Mock the values().update method response
        mock_update_response = {
            'spreadsheetId': 'sheet1',
            'updatedRange': 'Sheet1!A1:C3',
            'updatedRows': 3
        }
        
        # Set up mock service method
        sheets_client._service.spreadsheets().values().update.return_value.execute.return_value = mock_update_response
        
        # Call write_values method
        values = [
            ['Name', 'Age', 'City'],
            ['Alice', '30', 'New York'],
            ['Bob', '25', 'San Francisco']
        ]
        result = sheets_client.write_values('sheet1', 'Sheet1!A1:C3', values)
        
        # Verify results
        assert result['spreadsheetId'] == 'sheet1'
        assert result['updatedRange'] == 'Sheet1!A1:C3'
        
        # Verify service method was called with correct parameters
        sheets_client._service.spreadsheets().values().update.assert_called_once_with(
            spreadsheetId='sheet1', 
            range='Sheet1!A1:C3',
            valueInputOption='RAW'
        )
    
    def test_api_error_handling(self, sheets_client):
        """Test error handling for API errors."""
        # Create a mock HTTP error
        mock_error = HttpError(
            resp=Mock(status=403, reason='Forbidden'), 
            content=b'Permission denied'
        )
        
        # Set up mock service method to raise HttpError
        sheets_client._service.service_resources['drive'].files().list.return_value.execute.side_effect = mock_error
        
        # Verify that handle_api_error is called and re-raises the error
        with pytest.raises(HttpError):
            sheets_client.list_items()
