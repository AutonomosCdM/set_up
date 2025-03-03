from src.google_workspace_agent.drive_client import DriveClient
from src.google_workspace_agent.auth import GoogleWorkspaceAuth

def main():
    try:
        # Authenticate first
        auth = GoogleWorkspaceAuth()
        credentials = auth.get_credentials()
        
        # Initialize Drive Client
        drive_client = DriveClient(credentials)
        
        # Test listing recent files (limit to 10)
        files = drive_client.list_items(max_results=10)
        
        print("Drive Client Test:")
        print(f"Number of files retrieved: {len(files)}")
        
        if files:
            print("\nRecent Files:")
            for file in files:
                print(f"- {file.get('name', 'Unnamed File')} (Type: {file.get('mimeType', 'Unknown')}, Modified: {file.get('modifiedTime', 'Unknown')})")
                
                # Optional: Get more details about each file
                try:
                    file_details = drive_client.get_item(file['id'])
                    print(f"  Web View Link: {file_details.get('webViewLink', 'No link available')}")
                except Exception as detail_error:
                    print(f"  Could not fetch file details: {detail_error}")
        
    except Exception as e:
        print(f"Drive Client Test Failed: {e}")

if __name__ == "__main__":
    main()
