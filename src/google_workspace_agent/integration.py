"""
Integration Module for Google Workspace Intelligent Agent.

Provides coordination and workflow management across different 
Google Workspace service clients using Groq LLM.
"""

from typing import List, Dict, Any, Optional
import logging
import json

from .auth import GoogleWorkspaceAuth
from .llm_client import GroqLLMClient
from .gmail_client import GmailClient
from .calendar_client import CalendarClient
from .drive_client import DriveClient
from .sheets_client import SheetsClient
from .docs_client import DocsClient

class WorkspaceIntegration:
    """
    Manages interactions between Google Workspace services 
    using natural language processing.
    """
    
    def __init__(self, 
                 credentials: GoogleWorkspaceAuth, 
                 llm_client: Optional[GroqLLMClient] = None):
        """
        Initialize Workspace Integration.
        
        Args:
            credentials: Authenticated Google Workspace credentials
            llm_client: Optional Groq LLM client for natural language processing
        """
        self._credentials = credentials
        
        # Initialize service clients
        self.gmail_client = GmailClient(credentials.get_credentials())
        self.calendar_client = CalendarClient(credentials.get_credentials())
        self.drive_client = DriveClient(credentials.get_credentials())
        self.sheets_client = SheetsClient(credentials.get_credentials())
        self.docs_client = DocsClient(credentials.get_credentials())
        
        # Initialize LLM client
        self.llm_client = llm_client or GroqLLMClient()
        
        # Configure logging
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def process_natural_language_request(self, request: str) -> Dict[str, Any]:
        """
        Process a natural language request across multiple services.
        
        Args:
            request: Natural language request from the user
        
        Returns:
            Processed request result with action details
        """
        try:
            # Use LLM to interpret the request
            intent = self._extract_intent(request)
            
            # Route request to appropriate service(s)
            if intent['service'] == 'email':
                return self._handle_email_request(intent)
            elif intent['service'] == 'calendar':
                return self._handle_calendar_request(intent)
            elif intent['service'] == 'drive':
                return self._handle_drive_request(intent)
            elif intent['service'] == 'sheets':
                return self._handle_sheets_request(intent)
            elif intent['service'] == 'docs':
                return self._handle_docs_request(intent)
            elif intent['service'] == 'multi':
                return self._handle_multi_service_request(intent)
            else:
                return {
                    'status': 'error',
                    'message': f"Unsupported service: {intent['service']}"
                }
        
        except Exception as e:
            self.logger.error(f"Error processing request: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _extract_intent(self, request: str) -> Dict[str, Any]:
        """
        Use LLM to extract intent and parameters from request.
        
        Args:
            request: Natural language request
        
        Returns:
            Structured intent with service and action details
        """
        system_prompt = """
        You are an intent extraction assistant for a Google Workspace agent.
        Extract the following from a user request:
        - Target service (email, calendar, drive, sheets, docs, or multi)
        - Specific action (create, read, update, delete, etc.)
        - Relevant parameters
        
        Return a JSON with these details.
        """
        
        response = self.llm_client.generate_response(
            prompt=request, 
            system_message=system_prompt
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Fallback to default intent if parsing fails
            return {
                'service': 'multi',
                'action': 'interpret',
                'details': request
            }
    
    def _handle_email_request(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle email-related requests.
        
        Args:
            intent: Extracted intent from request
        
        Returns:
            Result of email operation
        """
        action = intent.get('action', '')
        details = intent.get('details', {})
        
        if action == 'send':
            return {
                'status': 'success',
                'result': self.gmail_client.create_item(
                    to=details.get('to', ''),
                    subject=details.get('subject', ''),
                    body=details.get('body', '')
                )
            }
        elif action == 'read':
            return {
                'status': 'success',
                'result': self.gmail_client.list_items(
                    max_results=details.get('max_results', 10),
                    query=details.get('query')
                )
            }
        # Add more email actions as needed
    
    def _handle_calendar_request(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle calendar-related requests.
        
        Args:
            intent: Extracted intent from request
        
        Returns:
            Result of calendar operation
        """
        action = intent.get('action', '')
        details = intent.get('details', {})
        
        if action == 'create':
            return {
                'status': 'success',
                'result': self.calendar_client.create_item(
                    summary=details.get('summary', ''),
                    start_time=details.get('start_time'),
                    end_time=details.get('end_time'),
                    description=details.get('description'),
                    attendees=details.get('attendees')
                )
            }
        elif action == 'list':
            return {
                'status': 'success',
                'result': self.calendar_client.list_items(
                    max_results=details.get('max_results', 10),
                    time_min=details.get('time_min'),
                    time_max=details.get('time_max')
                )
            }
        # Add more calendar actions as needed
    
    def _handle_drive_request(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle drive-related requests.
        
        Args:
            intent: Extracted intent from request
        
        Returns:
            Result of drive operation
        """
        action = intent.get('action', '')
        details = intent.get('details', {})
        
        if action == 'upload':
            return {
                'status': 'success',
                'result': self.drive_client.upload_file(
                    local_path=details.get('local_path', ''),
                    name=details.get('name'),
                    parent_id=details.get('parent_id')
                )
            }
        elif action == 'list':
            return {
                'status': 'success',
                'result': self.drive_client.list_items(
                    max_results=details.get('max_results', 10),
                    query=details.get('query')
                )
            }
        # Add more drive actions as needed
    
    def _handle_sheets_request(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle sheets-related requests.
        
        Args:
            intent: Extracted intent from request
        
        Returns:
            Result of sheets operation
        """
        action = intent.get('action', '')
        details = intent.get('details', {})
        
        if action == 'create':
            return {
                'status': 'success',
                'result': self.sheets_client.create_item(
                    title=details.get('title', ''),
                    sheets=details.get('sheets')
                )
            }
        elif action == 'read':
            return {
                'status': 'success',
                'result': self.sheets_client.read_values(
                    spreadsheet_id=details.get('spreadsheet_id', ''),
                    range_name=details.get('range_name', '')
                )
            }
        # Add more sheets actions as needed
    
    def _handle_docs_request(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle docs-related requests.
        
        Args:
            intent: Extracted intent from request
        
        Returns:
            Result of docs operation
        """
        action = intent.get('action', '')
        details = intent.get('details', {})
        
        if action == 'create':
            return {
                'status': 'success',
                'result': self.docs_client.create_item(
                    title=details.get('title', ''),
                    content=details.get('content')
                )
            }
        elif action == 'append':
            return {
                'status': 'success',
                'result': self.docs_client.append_text(
                    document_id=details.get('document_id', ''),
                    text=details.get('text', '')
                )
            }
        # Add more docs actions as needed
    
    def _handle_multi_service_request(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle complex requests involving multiple services.
        
        Args:
            intent: Extracted intent from request
        
        Returns:
            Result of multi-service operation
        """
        # Use LLM to break down complex request into service-specific actions
        breakdown_prompt = f"""
        Break down this multi-service request into specific actions:
        {intent.get('details', '')}
        
        Provide a JSON with a list of actions for each service.
        """
        
        breakdown = self.llm_client.generate_response(
            prompt=breakdown_prompt, 
            system_message="You are a workflow decomposition assistant."
        )
        
        try:
            actions = json.loads(breakdown)
            results = {}
            
            # Execute actions for each service
            for service, service_actions in actions.items():
                service_intent = {
                    'service': service,
                    'action': service_actions.get('action'),
                    'details': service_actions.get('details', {})
                }
                
                results[service] = self.process_natural_language_request(
                    json.dumps(service_intent)
                )
            
            return {
                'status': 'success',
                'results': results
            }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Multi-service request processing failed: {e}"
            }
