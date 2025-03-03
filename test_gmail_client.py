from src.google_workspace_agent.gmail_client import GmailClient
from src.google_workspace_agent.auth import GoogleWorkspaceAuth

def main():
    try:
        # Authenticate first
        auth = GoogleWorkspaceAuth()
        credentials = auth.get_credentials()
        
        # Initialize Gmail Client
        gmail_client = GmailClient(credentials)
        
        # Test listing recent emails (limit to 5)
        emails = gmail_client.list_items(max_results=5)
        
        print("Gmail Client Test:")
        print(f"Number of emails retrieved: {len(emails)}")
        
        if emails:
            print("\nRecent Emails:")
            for email in emails:
                # Fetch full email details
                full_email = gmail_client.get_item(email['id'])
                print(f"- Email ID: {email['id']}")
        
    except Exception as e:
        print(f"Gmail Client Test Failed: {e}")

if __name__ == "__main__":
    main()
