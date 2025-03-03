"""
Drive Service Client for Google Workspace Intelligent Agent.

Provides methods for interacting with Google Drive API, including 
file and folder management operations.
"""

from typing import List, Dict, Any, Optional
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from .service_client import BaseServiceClient

class DriveClient(BaseServiceClient):
    """
    Client for interacting with Google Drive API.
    
    Provides methods for file and folder-related operations.
    """
    
    def __init__(self, credentials: Credentials):
        """
        Initialize Drive service client.
        
        Args:
            credentials: Google OAuth 2.0 credentials
        """
        super().__init__(
            credentials=credentials, 
            service_name='drive',
            service_version='v3'
        )
    
    def list_items(self, 
                   max_results: Optional[int] = 10, 
                   query: Optional[str] = None,
                   order_by: Optional[str] = 'modifiedTime desc') -> List[Dict[str, Any]]:
        """
        List files and folders in Google Drive.
        
        Args:
            max_results: Maximum number of items to return
            query: Optional search query to filter files
            order_by: Optional sorting parameter
        
        Returns:
            List of files and folders
        """
        try:
            # Prepare request parameters
            list_params = {
                'pageSize': max_results,
                'orderBy': order_by,
                'fields': 'files(id, name, mimeType, modifiedTime, owners, size)'
            }
            
            # Add optional query
            if query:
                list_params['q'] = query
            
            # Execute list request
            results = self._service.files().list(**list_params).execute()
            
            # Extract and return files
            return results.get('files', [])
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def get_item(self, file_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific file or folder metadata.
        
        Args:
            file_id: Unique identifier for the file or folder
        
        Returns:
            Detailed file or folder information
        """
        try:
            file_metadata = self._service.files().get(
                fileId=file_id,
                fields='id, name, mimeType, modifiedTime, owners, size, webViewLink'
            ).execute()
            
            return file_metadata
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def create_item(self, 
                    name: str, 
                    mime_type: str = 'application/vnd.google-apps.document',
                    parent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new file or folder in Google Drive.
        
        Args:
            name: Name of the file or folder
            mime_type: MIME type of the item (default: Google Docs)
            parent_id: Optional parent folder ID
        
        Returns:
            Created file or folder metadata
        """
        try:
            # Prepare file metadata
            file_metadata = {
                'name': name,
                'mimeType': mime_type
            }
            
            # Add parent folder if specified
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            # Create file or folder
            created_file = self._service.files().create(
                body=file_metadata,
                fields='id, name, mimeType, webViewLink'
            ).execute()
            
            return created_file
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def update_item(self, 
                    file_id: str, 
                    update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update file or folder metadata.
        
        Args:
            file_id: Unique identifier for the file or folder
            update_data: Dictionary of metadata to update
        
        Returns:
            Updated file or folder metadata
        """
        try:
            # Update file metadata
            updated_file = self._service.files().update(
                fileId=file_id,
                body=update_data,
                fields='id, name, mimeType'
            ).execute()
            
            return updated_file
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def delete_item(self, file_id: str) -> bool:
        """
        Permanently delete a file or folder.
        
        Args:
            file_id: Unique identifier for the file or folder
        
        Returns:
            True if deletion was successful
        """
        try:
            self._service.files().delete(fileId=file_id).execute()
            return True
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def download_file(self, 
                      file_id: str, 
                      local_path: Optional[str] = None) -> Optional[bytes]:
        """
        Download a file from Google Drive.
        
        Args:
            file_id: Unique identifier for the file
            local_path: Optional local file path to save the downloaded file
        
        Returns:
            File content as bytes if no local path provided, otherwise None
        """
        try:
            # Request file download
            request = self._service.files().get_media(fileId=file_id)
            
            # Prepare download destination
            if local_path:
                # Download to local file
                with open(local_path, 'wb') as file:
                    downloader = MediaIoBaseDownload(file, request)
                    done = False
                    while not done:
                        _, done = downloader.next_chunk()
                return None
            else:
                # Return file content as bytes
                file_content = io.BytesIO()
                downloader = MediaIoBaseDownload(file_content, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
                return file_content.getvalue()
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def upload_file(self, 
                    local_path: str, 
                    name: Optional[str] = None,
                    mime_type: Optional[str] = None,
                    parent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file to Google Drive.
        
        Args:
            local_path: Path to the local file to upload
            name: Optional custom name for the uploaded file
            mime_type: Optional MIME type for the file
            parent_id: Optional parent folder ID
        
        Returns:
            Uploaded file metadata
        """
        try:
            # Prepare file metadata
            file_metadata = {
                'name': name or os.path.basename(local_path)
            }
            
            # Add parent folder if specified
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            # Prepare media upload
            media = MediaFileUpload(
                local_path, 
                resumable=True, 
                mimetype=mime_type
            )
            
            # Upload file
            uploaded_file = self._service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, mimeType, webViewLink'
            ).execute()
            
            return uploaded_file
        
        except HttpError as error:
            self.handle_api_error(error)
