# Google Workspace Intelligent Agent

## Overview

An advanced, AI-powered agent that seamlessly integrates with Google Workspace services, enabling natural language interactions across Gmail, Calendar, Drive, Sheets, and Docs.

## Features

- 🤖 Natural Language Processing
  - Interpret complex requests across multiple services
  - Context-aware interactions using Groq LLM
- 📧 Gmail Management
  - Send, read, and manage emails
- 📅 Calendar Coordination
  - Create, update, and list events
- 📁 Drive File Operations
  - Upload, list, and manage files
- 📊 Sheets Manipulation
  - Read, write, and analyze spreadsheet data
- 📝 Docs Editing
  - Create, append, and modify documents
- 🔒 Secure OAuth 2.0 Authentication

## Prerequisites

- Python 3.9+
- Poetry (dependency management)
- Google Cloud Project with:
  - Workspace API enabled
  - OAuth 2.0 credentials
- Groq API Key

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/google-workspace-agent.git
cd google-workspace-agent

# Install Poetry (if not already installed)
pip install poetry

# Install dependencies
poetry install
```

## Configuration

1. Copy `.env.example` to `.env`
2. Fill in your credentials:
   - Google OAuth 2.0 client credentials
   - Groq API Key

## Authentication Setup

```bash
# Run authentication setup
poetry run python -m google_workspace_agent.auth
```

## Usage Examples

### Natural Language Interactions

```python
from google_workspace_agent.auth import GoogleWorkspaceAuth
from google_workspace_agent.integration import WorkspaceIntegration

# Initialize authentication
auth = GoogleWorkspaceAuth()
credentials = auth.authenticate()

# Create integration instance
workspace = WorkspaceIntegration(credentials)

# Natural language requests
result = workspace.process_natural_language_request(
    "Send an email to team@example.com about the quarterly report"
)

result = workspace.process_natural_language_request(
    "Create a calendar event for team meeting next Tuesday at 10 AM"
)
```

## Development

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run specific test suite
poetry run pytest tests/test_gmail_client.py
```

### Code Quality

```bash
# Type checking
poetry run mypy src

# Code formatting
poetry run black src

# Linting
poetry run flake8 src
```

## Project Structure

```
google-workspace-agent/
├── src/
│   └── google_workspace_agent/
│       ├── auth.py
│       ├── integration.py
│       ├── llm_client.py
│       ├── service_client.py
│       ├── gmail_client.py
│       ├── calendar_client.py
│       ├── drive_client.py
│       ├── sheets_client.py
│       └── docs_client.py
├── tests/
│   ├── test_auth.py
│   ├── test_integration.py
│   ├── test_llm_client.py
│   ├── test_gmail_client.py
│   ├── test_calendar_client.py
│   ├── test_drive_client.py
│   ├── test_sheets_client.py
│   └── test_docs_client.py
└── pyproject.toml
```

## Roadmap

- [x] Authentication Framework
- [x] Service Clients Development
- [x] LLM Integration
- [ ] Advanced Workflow Automation
- [ ] Enhanced Natural Language Understanding
- [ ] Performance Optimization

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/google-workspace-agent](https://github.com/yourusername/google-workspace-agent)
