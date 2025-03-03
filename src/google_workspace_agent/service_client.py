"""
Base Service Client for Google Workspace Agent.

Provides a common interface and utility methods for different 
Google Workspace service clients.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class BaseServiceClient(ABC):
    """
    Abstract base class for Google Workspace service clients.
    
    Provides common functionality and interface for service-specific clients.
    """
    
    def __init__(self, 
                 credentials: Credentials, 
                 service_name: str, 
                 service_version: str):
        """
        Initialize the base service client.
        
        Args:
            credentials: Google OAuth 2.0 credentials
            service_name: Name of the Google Workspace service
            service_version: Version of the service API
        """
        self._credentials = credentials
        self._service_name = service_name
        self._service_version = service_version
        
        # Configure logging
        self._logger = logging.getLogger(f'{self.__class__.__name__}')
        
        # Build service client
        try:
            self._service = build(
                serviceName=service_name, 
                version=service_version, 
                credentials=credentials
            )
        except Exception as e:
            self._logger.error(f"Failed to build {service_name} service: {e}")
            raise
    
    @abstractmethod
    def list_items(self, 
                   max_results: Optional[int] = None, 
                   **kwargs) -> List[Dict[str, Any]]:
        """
        List items in the service.
        
        Args:
            max_results: Maximum number of results to return
            **kwargs: Additional filtering or search parameters
        
        Returns:
            List of items
        """
        pass
    
    @abstractmethod
    def create_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new item in the service.
        
        Args:
            item_data: Data for the new item
        
        Returns:
            Created item details
        """
        pass
    
    @abstractmethod
    def get_item(self, item_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific item by ID.
        
        Args:
            item_id: Unique identifier for the item
        
        Returns:
            Item details
        """
        pass
    
    @abstractmethod
    def update_item(self, 
                    item_id: str, 
                    item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing item.
        
        Args:
            item_id: Unique identifier for the item
            item_data: Updated item data
        
        Returns:
            Updated item details
        """
        pass
    
    @abstractmethod
    def delete_item(self, item_id: str) -> bool:
        """
        Delete an item.
        
        Args:
            item_id: Unique identifier for the item
        
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    def handle_api_error(self, error: HttpError) -> None:
        """
        Handle and log Google API errors.
        
        Args:
            error: HttpError from Google API
        
        Raises:
            The original error after logging
        """
        error_details = {
            'status': error.resp.status,
            'reason': error.resp.reason,
            'error_details': error.error_details if hasattr(error, 'error_details') else None
        }
        
        self._logger.error(f"Google API Error: {error_details}")
        
        # Optionally add more specific error handling based on error type
        if error.resp.status == 403:
            self._logger.warning("Permission denied. Check OAuth scopes.")
        elif error.resp.status == 404:
            self._logger.warning("Resource not found.")
        
        # Re-raise the original error
        raise
    
    def __repr__(self) -> str:
        """
        String representation of the service client.
        
        Returns:
            Descriptive string about the service client
        """
        return (f"{self.__class__.__name__}("
                f"service={self._service_name}, "
                f"version={self._service_version})")
