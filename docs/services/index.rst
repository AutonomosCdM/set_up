Google Workspace Services
========================

The Google Workspace Intelligent Agent provides comprehensive service clients for seamless interaction with various Google Workspace APIs.

Service Clients
---------------

Each service client is designed to provide a robust, type-safe, and intuitive interface for interacting with Google Workspace services.

Gmail Client
^^^^^^^^^^^^

.. code-block:: python

   from google_workspace_agent.gmail_client import GmailClient

   # List recent emails
   emails = gmail_client.list_items(max_results=10)

   # Send an email
   gmail_client.create_item(
       to='recipient@example.com',
       subject='Important Message',
       body='Hello, World!'
   )

Drive Client
^^^^^^^^^^^^

.. code-block:: python

   from google_workspace_agent.drive_client import DriveClient

   # List recent files
   files = drive_client.list_items(max_results=10)

   # Upload a file
   drive_client.upload_file(
       local_path='/path/to/file.txt',
       name='My Document'
   )

Sheets Client
^^^^^^^^^^^^^

.. code-block:: python

   from google_workspace_agent.sheets_client import SheetsClient

   # List spreadsheets
   spreadsheets = sheets_client.list_items(max_results=5)

   # Read sheet values
   values = sheets_client.read_values(
       spreadsheet_id='your_spreadsheet_id', 
       range_name='Sheet1!A1:D10'
   )

Docs Client
^^^^^^^^^^^

.. code-block:: python

   from google_workspace_agent.docs_client import DocsClient

   # List recent documents
   documents = docs_client.list_items(max_results=5)

   # Create a new document
   docs_client.create_item(
       title='Project Report',
       content=[{'text': 'Initial document content'}]
   )

Calendar Client
^^^^^^^^^^^^^^^

.. code-block:: python

   from google_workspace_agent.calendar_client import CalendarClient

   # List upcoming events
   events = calendar_client.list_items(
       start_time=datetime.now(),
       end_time=datetime.now() + timedelta(days=7)
   )

Common Methods
--------------

Each service client follows a consistent interface:

- ``list_items()``: Retrieve a list of items
- ``get_item()``: Fetch details of a specific item
- ``create_item()``: Create a new item
- ``update_item()``: Modify an existing item
- ``delete_item()``: Remove an item

Authentication
--------------

All service clients require OAuth 2.0 credentials obtained through the ``GoogleWorkspaceAuth`` class.

Error Handling
--------------

Service clients include robust error handling with detailed error messages and logging.

Best Practices
--------------

- Always use the ``GoogleWorkspaceAuth`` class for authentication
- Handle potential API errors gracefully
- Respect API quotas and rate limits
- Use appropriate scopes for your operations
