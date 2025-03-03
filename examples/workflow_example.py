"""
Example Workflow Demonstration for Google Workspace Intelligent Agent

This script showcases how to use the Google Workspace Intelligent Agent
to perform complex, multi-service workflows using natural language processing.
"""

import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from google_workspace_agent.auth import GoogleWorkspaceAuth
from google_workspace_agent.integration import WorkspaceIntegration

def main():
    # Load environment variables
    load_dotenv()

    # Authenticate with Google Workspace
    auth = GoogleWorkspaceAuth()
    credentials = auth.authenticate()

    # Create workspace integration instance
    workspace = WorkspaceIntegration(credentials)

    def project_management_workflow():
        """
        Example workflow demonstrating multi-service interaction:
        1. Create a project planning document
        2. Create a calendar event for project kickoff
        3. Send invitation emails to team members
        4. Create a tracking spreadsheet
        """
        try:
            # 1. Create project planning document
            project_doc = workspace.process_natural_language_request(
                "Create a new Google Docs document titled 'Q2 2025 Project Plan'"
            )
            doc_id = project_doc['result']['documentId']

            # Append initial content to the document
            workspace.process_natural_language_request(
                f"Append text to document {doc_id}: 'Project Objectives: Develop AI-powered workspace integration'"
            )

            # 2. Create project kickoff calendar event
            kickoff_event = workspace.process_natural_language_request(
                f"Create a calendar event for project kickoff next Monday at 10 AM, titled 'Q2 2025 Project Kickoff'"
            )

            # 3. Send invitation emails to team members
            email_result = workspace.process_natural_language_request(
                "Send an email to team@company.com with subject 'Q2 2025 Project Kickoff' and body 'Please join our project kickoff meeting next Monday at 10 AM. Agenda and project plan details will be shared.'"
            )

            # 4. Create project tracking spreadsheet
            tracking_sheet = workspace.process_natural_language_request(
                "Create a new Google Sheets spreadsheet titled 'Q2 2025 Project Tracking'"
            )
            sheet_id = tracking_sheet['result']['spreadsheetId']

            # Add initial tracking data to the spreadsheet
            workspace.process_natural_language_request(
                f"Write values to spreadsheet {sheet_id} in range 'Sheet1!A1:C3' with data: [['Task', 'Status', 'Owner'], ['Project Setup', 'In Progress', 'Team Lead'], ['Initial Development', 'Not Started', 'Development Team']]"
            )

            print("Project management workflow completed successfully!")
            return {
                'document': project_doc['result'],
                'event': kickoff_event['result'],
                'email': email_result['result'],
                'spreadsheet': tracking_sheet['result']
            }

        except Exception as e:
            print(f"Error in project management workflow: {e}")
            return None

    def meeting_preparation_workflow():
        """
        Example workflow for meeting preparation:
        1. Find recent emails about a meeting
        2. Create a meeting summary document
        3. Update calendar event with notes
        """
        try:
            # 1. Search for recent meeting-related emails
            email_search = workspace.process_natural_language_request(
                "Find emails from the last week containing the word 'meeting'"
            )

            # 2. Create a meeting summary document
            summary_doc = workspace.process_natural_language_request(
                "Create a new Google Docs document titled 'Meeting Summary'"
            )
            doc_id = summary_doc['result']['documentId']

            # Append email summaries to the document
            workspace.process_natural_language_request(
                f"Append text to document {doc_id}: 'Meeting Email Summaries:\n{email_search['result']}'"
            )

            # 3. Update or create a calendar event with meeting notes
            calendar_update = workspace.process_natural_language_request(
                f"Create a calendar event for team meeting next week, including notes from document {doc_id}"
            )

            print("Meeting preparation workflow completed successfully!")
            return {
                'emails': email_search['result'],
                'summary_document': summary_doc['result'],
                'calendar_event': calendar_update['result']
            }

        except Exception as e:
            print(f"Error in meeting preparation workflow: {e}")
            return None

    # Run example workflows
    print("Running Project Management Workflow:")
    project_workflow_result = project_management_workflow()

    print("\nRunning Meeting Preparation Workflow:")
    meeting_workflow_result = meeting_preparation_workflow()

if __name__ == "__main__":
    main()
