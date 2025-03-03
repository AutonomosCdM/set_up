"""
Unit tests for Calendar Service Client module.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from google_workspace_agent.calendar_client import CalendarClient

class TestCalendarClient:
    @pytest.fixture
    def mock_credentials(self):
        """Create a mock Credentials object."""
        return Mock(spec=Credentials)
    
    @pytest.fixture
    def calendar_client(self, mock_credentials):
        """Create a CalendarClient instance for testing."""
        with patch('googleapiclient.discovery.build') as mock_build:
            mock_service = Mock()
            mock_build.return_value = mock_service
            
            client = CalendarClient(mock_credentials)
            client._service = mock_service
            return client
    
    def test_list_events(self, calendar_client):
        """Test listing calendar events."""
        # Mock the list method response
        mock_list_response = {
            'items': [
                {'id': 'event1', 'summary': 'Meeting 1'},
                {'id': 'event2', 'summary': 'Meeting 2'}
            ]
        }
        
        # Set up mock service method
        calendar_client._service.events().list.return_value.execute.return_value = mock_list_response
        
        # Call list_items method
        events = calendar_client.list_items(max_results=2)
        
        # Verify results
        assert len(events) == 2
        assert events[0]['id'] == 'event1'
        assert events[1]['summary'] == 'Meeting 2'
        
        # Verify service method was called with correct parameters
        calendar_client._service.events().list.assert_called_once_with(
            calendarId='primary', 
            maxResults=2,
            singleEvents=True
        )
    
    def test_get_event(self, calendar_client):
        """Test retrieving a specific calendar event."""
        # Mock the get method response
        mock_event_response = {
            'id': 'event1',
            'summary': 'Team Meeting',
            'start': {'dateTime': '2025-03-15T10:00:00Z'},
            'end': {'dateTime': '2025-03-15T11:00:00Z'}
        }
        
        # Set up mock service method
        calendar_client._service.events().get.return_value.execute.return_value = mock_event_response
        
        # Call get_item method
        event = calendar_client.get_item('event1')
        
        # Verify results
        assert event['id'] == 'event1'
        assert event['summary'] == 'Team Meeting'
        
        # Verify service method was called with correct parameters
        calendar_client._service.events().get.assert_called_once_with(
            calendarId='primary', 
            eventId='event1'
        )
    
    def test_create_event(self, calendar_client):
        """Test creating a new calendar event."""
        # Mock the insert method response
        mock_create_response = {
            'id': 'new_event1',
            'summary': 'New Team Meeting',
            'start': {'dateTime': '2025-03-20T14:00:00Z'},
            'end': {'dateTime': '2025-03-20T15:00:00Z'}
        }
        
        # Set up mock service method
        calendar_client._service.events().insert.return_value.execute.return_value = mock_create_response
        
        # Call create_item method
        new_event = calendar_client.create_item(
            summary='New Team Meeting', 
            start_time='2025-03-20T14:00:00Z',
            end_time='2025-03-20T15:00:00Z',
            description='Quarterly planning',
            attendees=['team@example.com', 'manager@example.com']
        )
        
        # Verify results
        assert new_event['id'] == 'new_event1'
        assert new_event['summary'] == 'New Team Meeting'
        
        # Verify service method was called
        calendar_client._service.events().insert.assert_called_once()
    
    def test_update_event(self, calendar_client):
        """Test updating an existing calendar event."""
        # Mock the update method response
        mock_update_response = {
            'id': 'event1',
            'summary': 'Updated Team Meeting',
            'description': 'Updated description'
        }
        
        # Set up mock service method
        calendar_client._service.events().update.return_value.execute.return_value = mock_update_response
        
        # Call update_item method
        update_data = {
            'summary': 'Updated Team Meeting',
            'description': 'Updated description'
        }
        updated_event = calendar_client.update_item('event1', update_data)
        
        # Verify results
        assert updated_event['id'] == 'event1'
        assert updated_event['summary'] == 'Updated Team Meeting'
        
        # Verify service method was called with correct parameters
        calendar_client._service.events().update.assert_called_once_with(
            calendarId='primary', 
            eventId='event1', 
            body=update_data
        )
    
    def test_delete_event(self, calendar_client):
        """Test deleting a calendar event."""
        # Set up mock service method
        calendar_client._service.events().delete.return_value.execute.return_value = None
        
        # Call delete_item method
        result = calendar_client.delete_item('event1')
        
        # Verify results
        assert result is True
        
        # Verify service method was called with correct parameters
        calendar_client._service.events().delete.assert_called_once_with(
            calendarId='primary', 
            eventId='event1'
        )
    
    def test_api_error_handling(self, calendar_client):
        """Test error handling for API errors."""
        # Create a mock HTTP error
        mock_error = HttpError(
            resp=Mock(status=403, reason='Forbidden'), 
            content=b'Permission denied'
        )
        
        # Set up mock service method to raise HttpError
        calendar_client._service.events().list.return_value.execute.side_effect = mock_error
        
        # Verify that handle_api_error is called and re-raises the error
        with pytest.raises(HttpError):
            calendar_client.list_items()
