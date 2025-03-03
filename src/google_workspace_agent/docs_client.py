"""
Docs Service Client for Google Workspace Intelligent Agent.

Provides methods for interacting with Google Docs API, including 
document management and manipulation operations.
"""

from typing import List, Dict, Any, Optional
import os

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from .service_client import BaseServiceClient

class DocsClient(BaseServiceClient):
    """
    Client for interacting with Google Docs API.
    
    Provides methods for document-related operations.
    """
    
    def __init__(self, credentials: Credentials):
        """
        Initialize Docs service client.
        
        Args:
            credentials: Google OAuth 2.0 credentials
        """
        super().__init__(
            credentials=credentials, 
            service_name='docs',
            service_version='v1'
        )
    
    def list_items(self, 
                   max_results: Optional[int] = 10) -> List[Dict[str, Any]]:
        """
        List documents in the user's Google Drive.
        
        Args:
            max_results: Maximum number of documents to return
        
        Returns:
            List of document metadata
        """
        try:
            # Create a separate Drive service
            from googleapiclient.discovery import build
            drive_service = build('drive', 'v3', credentials=self._credentials)
            
            results = drive_service.files().list(
                pageSize=max_results,
                q="mimeType='application/vnd.google-apps.document'"
            ).execute()
            
            return results.get('files', [])
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def get_item(self, document_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific document metadata.
        
        Args:
            document_id: Unique identifier for the document
        
        Returns:
            Detailed document information
        """
        try:
            document = self._service.documents().get(
                documentId=document_id
            ).execute()
            
            return document
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def create_item(self, 
                    title: str, 
                    content: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Create a new document.
        
        Args:
            title: Title of the document
            content: Optional initial document content
        
        Returns:
            Created document metadata
        """
        try:
            # Prepare document creation request
            document_body = {
                'title': title
            }
            
            # Create document
            document = self._service.documents().create(
                body=document_body
            ).execute()
            
            # Add initial content if provided
            if content:
                requests = []
                for item in content:
                    requests.append({
                        'insertText': {
                            'location': {
                                'index': 1
                            },
                            'text': item.get('text', '')
                        }
                    })
                
                # Batch update document with content
                self._service.documents().batchUpdate(
                    documentId=document['documentId'],
                    body={'requests': requests}
                ).execute()
            
            return document
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def update_item(self, 
                    document_id: str, 
                    updates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Update a document.
        
        Args:
            document_id: Unique identifier for the document
            updates: List of update requests
        
        Returns:
            Updated document metadata
        """
        try:
            # Prepare batch update request
            batch_update_request = {
                'requests': updates
            }
            
            # Execute batch update
            response = self._service.documents().batchUpdate(
                documentId=document_id,
                body=batch_update_request
            ).execute()
            
            return response
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def delete_item(self, document_id: str) -> bool:
        """
        Delete a document.
        
        Args:
            document_id: Unique identifier for the document
        
        Returns:
            True if deletion was successful
        """
        try:
            # Use Drive API to delete document
            drive_service = self._service.service_resources['drive']
            drive_service.files().delete(fileId=document_id).execute()
            
            return True
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def append_text(self, 
                    document_id: str, 
                    text: str, 
                    index: Optional[int] = None) -> Dict[str, Any]:
        """
        Append text to a document.
        
        Args:
            document_id: Unique identifier for the document
            text: Text to append
            index: Optional index to insert text (default: end of document)
        
        Returns:
            Batch update response
        """
        try:
            # Prepare insert text request
            request = {
                'insertText': {
                    'location': {
                        'index': index or self._get_document_length(document_id)
                    },
                    'text': text
                }
            }
            
            # Execute text insertion
            response = self._service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': [request]}
            ).execute()
            
            return response
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def _get_document_length(self, document_id: str) -> int:
        """
        Get the total length of a document.
        
        Args:
            document_id: Unique identifier for the document
        
        Returns:
            Total number of characters in the document
        """
        try:
            document = self.get_item(document_id)
            return document.get('body', {}).get('content', [])[-1].get('endIndex', 1)
        
        except Exception:
            return 1
