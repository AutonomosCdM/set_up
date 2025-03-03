from src.google_workspace_agent.docs_client import DocsClient
from src.google_workspace_agent.auth import GoogleWorkspaceAuth

def main():
    try:
        # Authenticate first
        auth = GoogleWorkspaceAuth()
        credentials = auth.get_credentials()
        
        # Initialize Docs Client
        docs_client = DocsClient(credentials)
        
        # Test listing recent documents (limit to 5)
        documents = docs_client.list_items(max_results=5)
        
        print("Docs Client Test:")
        print(f"Number of documents retrieved: {len(documents)}")
        
        if documents:
            print("\nRecent Documents:")
            for doc in documents:
                print(f"- {doc.get('name', 'Untitled Document')}")
                
                # Attempt to get more details if possible
                try:
                    doc_id = doc.get('id')
                    doc_details = docs_client.get_item(doc_id)
                    print(f"  Title: {doc_details.get('title', 'No Title')}")
                except Exception as detail_error:
                    print(f"  Could not fetch document details: {detail_error}")
        
    except Exception as e:
        print(f"Docs Client Test Failed: {e}")

if __name__ == "__main__":
    main()
