"""
Sheets Service Client for Google Workspace Intelligent Agent.

Provides methods for interacting with Google Sheets API, including 
spreadsheet and worksheet management operations.
"""

from typing import List, Dict, Any, Optional, Union
import os

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from .service_client import BaseServiceClient

class SheetsClient(BaseServiceClient):
    """
    Client for interacting with Google Sheets API.
    
    Provides methods for spreadsheet and worksheet-related operations.
    """
    
    def __init__(self, credentials: Credentials):
        """
        Initialize Sheets service client.
        
        Args:
            credentials: Google OAuth 2.0 credentials
        """
        super().__init__(
            credentials=credentials, 
            service_name='sheets',
            service_version='v4'
        )
    
    def list_items(self, 
                   max_results: Optional[int] = 10) -> List[Dict[str, Any]]:
        """
        List spreadsheets in the user's Google Drive.
        
        Args:
            max_results: Maximum number of spreadsheets to return
        
        Returns:
            List of spreadsheet metadata
        """
        try:
            # Create a separate Drive service
            from googleapiclient.discovery import build
            drive_service = build('drive', 'v3', credentials=self._credentials)
            
            results = drive_service.files().list(
                pageSize=max_results,
                q="mimeType='application/vnd.google-apps.spreadsheet'"
            ).execute()
            
            return results.get('files', [])
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def get_item(self, spreadsheet_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific spreadsheet metadata.
        
        Args:
            spreadsheet_id: Unique identifier for the spreadsheet
        
        Returns:
            Detailed spreadsheet information
        """
        try:
            spreadsheet = self._service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            
            return spreadsheet
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def create_item(self, 
                    title: str, 
                    sheets: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Create a new spreadsheet.
        
        Args:
            title: Title of the spreadsheet
            sheets: Optional list of sheet configurations
        
        Returns:
            Created spreadsheet metadata
        """
        try:
            # Prepare spreadsheet creation request
            spreadsheet_body = {
                'properties': {
                    'title': title
                }
            }
            
            # Add sheet configurations if provided
            if sheets:
                spreadsheet_body['sheets'] = [
                    {'properties': sheet} for sheet in sheets
                ]
            
            # Create spreadsheet
            spreadsheet = self._service.spreadsheets().create(
                body=spreadsheet_body
            ).execute()
            
            return spreadsheet
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def update_item(self, 
                    spreadsheet_id: str, 
                    update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update spreadsheet metadata.
        
        Args:
            spreadsheet_id: Unique identifier for the spreadsheet
            update_data: Dictionary of metadata to update
        
        Returns:
            Updated spreadsheet metadata
        """
        try:
            # Prepare batch update request
            batch_update_request = {
                'requests': [
                    {
                        'updateSpreadsheetProperties': {
                            'properties': update_data,
                            'fields': ','.join(update_data.keys())
                        }
                    }
                ]
            }
            
            # Execute batch update
            response = self._service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=batch_update_request
            ).execute()
            
            return response
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def delete_item(self, spreadsheet_id: str) -> bool:
        """
        Delete a spreadsheet.
        
        Args:
            spreadsheet_id: Unique identifier for the spreadsheet
        
        Returns:
            True if deletion was successful
        """
        try:
            # Use Drive API to delete spreadsheet
            drive_service = self._service.service_resources['drive']
            drive_service.files().delete(fileId=spreadsheet_id).execute()
            
            return True
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def read_values(self, 
                    spreadsheet_id: str, 
                    range_name: str) -> List[List[Any]]:
        """
        Read values from a specific range in a spreadsheet.
        
        Args:
            spreadsheet_id: Unique identifier for the spreadsheet
            range_name: A1 notation range to read (e.g., 'Sheet1!A1:D10')
        
        Returns:
            2D list of cell values
        """
        try:
            result = self._service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            return result.get('values', [])
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def write_values(self, 
                     spreadsheet_id: str, 
                     range_name: str, 
                     values: List[List[Any]]) -> Dict[str, Any]:
        """
        Write values to a specific range in a spreadsheet.
        
        Args:
            spreadsheet_id: Unique identifier for the spreadsheet
            range_name: A1 notation range to write (e.g., 'Sheet1!A1:D10')
            values: 2D list of values to write
        
        Returns:
            Update result metadata
        """
        try:
            body = {
                'values': values
            }
            
            result = self._service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, 
                range=range_name,
                valueInputOption='RAW'
            ).execute()
            
            return result
        
        except HttpError as error:
            self.handle_api_error(error)
