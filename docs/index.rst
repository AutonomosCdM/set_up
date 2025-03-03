Google Workspace Intelligent Agent
=====================================

.. image:: https://img.shields.io/pypi/v/google-workspace-agent.svg
   :target: https://pypi.org/project/google-workspace-agent/
   :alt: PyPI Version

.. image:: https://github.com/cline-ai/google-workspace-agent/workflows/CI/CD/badge.svg
   :target: https://github.com/cline-ai/google-workspace-agent/actions
   :alt: CI/CD Status

.. image:: https://codecov.io/gh/cline-ai/google-workspace-agent/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/cline-ai/google-workspace-agent
   :alt: Code Coverage

Overview
--------

The Google Workspace Intelligent Agent is an advanced, AI-powered tool that seamlessly integrates with Google Workspace services, enabling natural language interactions across Gmail, Calendar, Drive, Sheets, and Docs.

Features
--------

- 🤖 Natural Language Processing
- 📧 Gmail Management
- 📅 Calendar Coordination
- 📁 Drive File Operations
- 📊 Sheets Manipulation
- 📝 Docs Editing
- 🔒 Secure OAuth 2.0 Authentication

Installation
------------

.. code-block:: bash

   pip install google-workspace-agent

Quick Start
-----------

.. code-block:: python

   from google_workspace_agent.auth import GoogleWorkspaceAuth
   from google_workspace_agent.integration import WorkspaceIntegration

   # Initialize authentication
   auth = GoogleWorkspaceAuth()
   credentials = auth.authenticate()

   # Create integration instance
   workspace = WorkspaceIntegration(credentials)

   # Natural language interactions
   result = workspace.process_natural_language_request(
       "Send an email to team@example.com about the quarterly report"
   )

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   authentication
   services/index
   examples
   api_reference
   contributing
   changelog

Services
--------

The Intelligent Agent supports seamless interactions with:

- Gmail
- Google Calendar
- Google Drive
- Google Sheets
- Google Docs

Authentication
--------------

Secure OAuth 2.0 authentication with minimal token scope and robust error handling.

Example Workflows
-----------------

Explore complex, multi-service workflows powered by natural language processing.

Contributing
------------

We welcome contributions! Please see our :doc:`contributing` guide.

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License
-------

Distributed under the MIT License. See ``LICENSE`` for more information.
