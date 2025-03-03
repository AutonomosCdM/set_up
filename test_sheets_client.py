from src.google_workspace_agent.sheets_client import SheetsClient
from src.google_workspace_agent.auth import GoogleWorkspaceAuth

def main():
    try:
        # Authenticate first
        auth = GoogleWorkspaceAuth()
        credentials = auth.get_credentials()
        
        # Initialize Sheets Client
        sheets_client = SheetsClient(credentials)
        
        # Test listing spreadsheets (limit to 5)
        spreadsheets = sheets_client.list_items(max_results=5)
        
        print("Sheets Client Test:")
        print(f"Number of spreadsheets retrieved: {len(spreadsheets)}")
        
        if spreadsheets:
            print("\nRecent Spreadsheets:")
            for sheet in spreadsheets:
                print(f"- {sheet.get('name', 'Untitled Spreadsheet')}")
                
                # Attempt to get more details and read values if possible
                try:
                    sheet_id = sheet.get('id')
                    sheet_details = sheets_client.get_item(sheet_id)
                    
                    # Try to read values from the first sheet
                    first_sheet_name = sheet_details.get('sheets', [{}])[0].get('properties', {}).get('title', 'Sheet1')
                    values = sheets_client.read_values(sheet_id, f'{first_sheet_name}!A1:D5')
                    
                    if values:
                        print("  Sample Data:")
                        for row in values:
                            print(f"  {row}")
                except Exception as read_error:
                    print(f"  Could not fetch sheet details or data: {read_error}")
        
    except Exception as e:
        print(f"Sheets Client Test Failed: {e}")

if __name__ == "__main__":
    main()
