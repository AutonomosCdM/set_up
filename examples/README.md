# Google Workspace Intelligent Agent - Example Workflows

## Overview

This directory contains example workflows demonstrating the capabilities of the Google Workspace Intelligent Agent. These examples showcase how to use natural language processing to interact with multiple Google Workspace services seamlessly.

## Prerequisites

Before running these examples, ensure you have:
- Completed the main project setup
- Configured your `.env` file with necessary credentials
- Installed all project dependencies
- Run the authentication setup script

## Available Workflows

### 1. Project Management Workflow (`workflow_example.py`)

This example demonstrates a comprehensive project management workflow that:
- Creates a project planning document in Google Docs
- Schedules a project kickoff meeting in Google Calendar
- Sends team invitation emails via Gmail
- Creates a project tracking spreadsheet in Google Sheets

#### Key Services Used
- Google Docs: Document creation and editing
- Google Calendar: Event scheduling
- Gmail: Email communication
- Google Sheets: Spreadsheet creation and data entry

### 2. Meeting Preparation Workflow

This workflow showcases:
- Searching recent emails
- Creating a meeting summary document
- Updating calendar events with meeting notes

## Running Examples

```bash
# Navigate to the project root directory
cd google-workspace-agent

# Run the example workflow
poetry run python examples/workflow_example.py
```

## Important Notes

- Ensure you have completed the authentication setup
- These examples require active Google Workspace and Groq API credentials
- Workflows are demonstrative and may need adaptation to specific use cases

## Workflow Details

### Project Management Workflow

1. **Document Creation**
   - Creates a new Google Docs document
   - Adds initial project objectives
   - Demonstrates document manipulation

2. **Calendar Event**
   - Schedules a project kickoff meeting
   - Shows calendar event creation
   - Illustrates date and time handling

3. **Email Communication**
   - Sends invitation emails to team members
   - Demonstrates email composition and sending

4. **Spreadsheet Tracking**
   - Creates a project tracking spreadsheet
   - Adds initial task and status data
   - Shows spreadsheet data manipulation

### Meeting Preparation Workflow

1. **Email Search**
   - Retrieves recent meeting-related emails
   - Demonstrates email filtering and search

2. **Document Summarization**
   - Creates a summary document
   - Appends email content
   - Shows document editing capabilities

3. **Calendar Integration**
   - Creates or updates meeting events
   - Incorporates document notes

## Customization

Feel free to modify these examples to:
- Add more complex workflows
- Integrate with additional services
- Demonstrate specific use cases for your organization

## Troubleshooting

- Check your `.env` file for correct credentials
- Verify network connectivity
- Ensure you have the necessary API permissions
- Run authentication setup if encountering token issues

## Contributing

Have an interesting workflow example? We welcome contributions! 
Please read our [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

These examples are part of the Google Workspace Intelligent Agent project 
and are distributed under the MIT License.

## Performance and Limitations

- Example workflows demonstrate basic interactions
- Actual performance may vary based on API rate limits
- Some operations might require additional error handling in production

## Learning Resources

- [Google Workspace API Documentation](https://developers.google.com/workspace)
- [Groq LLM Documentation](https://console.groq.com/docs)
- Project GitHub Repository
