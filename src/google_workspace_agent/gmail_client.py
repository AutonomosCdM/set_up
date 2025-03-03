"""
Gmail Service Client for Google Workspace Intelligent Agent.

Provides methods for interacting with Gmail API, including 
reading, sending, and managing emails.
"""

from typing import List, Dict, Any, Optional
import base64
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

from .service_client import BaseServiceClient

class GmailClient(BaseServiceClient):
    """
    Client for interacting with Gmail API.
    
    Provides methods for email-related operations.
    """
    
    def __init__(self, credentials: Credentials):
        """
        Initialize Gmail service client.
        
        Args:
            credentials: Google OAuth 2.0 credentials
        """
        super().__init__(
            credentials=credentials, 
            service_name='gmail',
            service_version='v1'
        )
    
    def list_items(self, 
                   max_results: Optional[int] = 10, 
                   label_ids: Optional[List[str]] = None,
                   query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List emails in the user's mailbox.
        
        Args:
            max_results: Maximum number of emails to return
            label_ids: List of label IDs to filter emails
            query: Search query to filter emails
        
        Returns:
            List of email metadata
        """
        try:
            # Prepare request parameters
            list_params = {'userId': 'me', 'maxResults': max_results}
            
            if label_ids:
                list_params['labelIds'] = label_ids
            
            if query:
                list_params['q'] = query
            
            # Execute list request
            results = self._service.users().messages().list(**list_params).execute()
            
            # Extract and return email metadata
            return results.get('messages', [])
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def get_item(self, message_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific email by ID.
        
        Args:
            message_id: Unique identifier for the email
        
        Returns:
            Detailed email information
        """
        try:
            message = self._service.users().messages().get(
                userId='me', 
                id=message_id, 
                format='full'
            ).execute()
            
            return message
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def create_item(self, 
                    to: str, 
                    subject: str, 
                    body: str, 
                    html_body: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a new email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Plain text email body
            html_body: Optional HTML email body
        
        Returns:
            Sent email details
        """
        try:
            # Create email message
            message = MIMEText(body, 'plain')
            message['to'] = to
            message['subject'] = subject
            
            # Add HTML body if provided
            if html_body:
                message.attach(MIMEText(html_body, 'html'))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send email
            sent_message = self._service.users().messages().send(
                userId='me', 
                body={'raw': raw_message}
            ).execute()
            
            return sent_message
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def update_item(self, 
                    message_id: str, 
                    add_labels: Optional[List[str]] = None, 
                    remove_labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Update email labels.
        
        Args:
            message_id: Unique identifier for the email
            add_labels: Labels to add to the email
            remove_labels: Labels to remove from the email
        
        Returns:
            Updated email details
        """
        try:
            # Prepare label modification request
            modify_request = {
                'userId': 'me',
                'id': message_id,
                'body': {}
            }
            
            if add_labels:
                modify_request['body']['addLabelIds'] = add_labels
            
            if remove_labels:
                modify_request['body']['removeLabelIds'] = remove_labels
            
            # Execute label modification
            updated_message = self._service.users().messages().modify(
                **modify_request
            ).execute()
            
            return updated_message
        
        except HttpError as error:
            self.handle_api_error(error)
    
    def delete_item(self, message_id: str) -> bool:
        """
        Permanently delete an email.
        
        Args:
            message_id: Unique identifier for the email
        
        Returns:
            True if deletion was successful
        """
        try:
            self._service.users().messages().delete(
                userId='me', 
                id=message_id
            ).execute()
            
            return True
        
        except HttpError as error:
            self.handle_api_error(error)
