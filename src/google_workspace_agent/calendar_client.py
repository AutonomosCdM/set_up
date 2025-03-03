"""
Calendar Service Client for Google Workspace Intelligent Agent.

Provides methods for interacting with Google Calendar API, including 
creating, reading, updating, and deleting calendar events.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from .service_client import BaseServiceClient

class CalendarClient(BaseServiceClient):
    """
    Client for interacting with Google Calendar API.
    
    Provides methods for calendar and event-related operations.
    """
    
    def __init__(self, credentials: Credentials):
        """
        Initialize Calendar service client.
        
        Args:
            credentials: Google OAuth 2.0 credentials
        """
        super().__init__(
            credentials=credentials, 
            service_name='calendar',
            service_version='v3'
        )
    
    def list_items(self, 
                   max_results: Optional[int] = 10, 
                   time_min: Optional[str] = None,
                   time_max: Optional[str] = None,
                   single_events: bool = True) -> List[Dict[str, Any]]:
        """
        List calendar events.
        
        Args:
            max_results: Maximum number of events to return
            time_min: Lower bound for event start time (ISO 8601 format)
            time_max: Upper bound for event start time (ISO 8601 format)
            single_events: Whether to expand recurring events
        
        Returns:
            List of calendar events
        """
        try:
            # Prepare request parameters
            list_params = {
                'calendarId': 'primary',
                'maxResults': max_results,
                'singleEvents': single_events
            }
            
            # Add optional time filters
            if time_min:
                list_params['timeMin'] = time_min
            
            if time_max:
                list_params['timeMax'] = time_max
            
            # Execute list request
            results = self._service.events().list(**list_params).execute()
            
            # Extract and return events
            return results.get('items', [])
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def get_item(self, event_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific calendar event.
        
        Args:
            event_id: Unique identifier for the event
        
        Returns:
            Detailed event information
        """
        try:
            event = self._service.events().get(
                calendarId='primary', 
                eventId=event_id
            ).execute()
            
            return event
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def create_item(self, 
                    summary: str, 
                    start_time: Optional[str] = None, 
                    end_time: Optional[str] = None,
                    description: Optional[str] = None,
                    attendees: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Create a new calendar event.
        
        Args:
            summary: Event title
            start_time: Event start time (ISO 8601 format)
            end_time: Event end time (ISO 8601 format)
            description: Event description
            attendees: List of email addresses to invite
        
        Returns:
            Created event details
        """
        try:
            # Prepare event data
            event_data = {
                'summary': summary,
                'start': {'dateTime': start_time} if start_time else {'date': datetime.now().date().isoformat()},
                'end': {'dateTime': end_time} if end_time else {'date': (datetime.now() + timedelta(hours=1)).date().isoformat()}
            }
            
            # Add optional fields
            if description:
                event_data['description'] = description
            
            if attendees:
                event_data['attendees'] = [{'email': email} for email in attendees]
            
            # Create event
            event = self._service.events().insert(
                calendarId='primary', 
                body=event_data
            ).execute()
            
            return event
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def update_item(self, 
                    event_id: str, 
                    update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing calendar event.
        
        Args:
            event_id: Unique identifier for the event
            update_data: Dictionary of event fields to update
        
        Returns:
            Updated event details
        """
        try:
            # Update event
            updated_event = self._service.events().update(
                calendarId='primary', 
                eventId=event_id, 
                body=update_data
            ).execute()
            
            return updated_event
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def delete_item(self, event_id: str) -> bool:
        """
        Delete a calendar event.
        
        Args:
            event_id: Unique identifier for the event
        
        Returns:
            True if deletion was successful
        """
        try:
            self._service.events().delete(
                calendarId='primary', 
                eventId=event_id
            ).execute()
            
            return True
        
        except HttpError as error:
            self.handle_api_error(error)
