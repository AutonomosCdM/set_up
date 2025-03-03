from src.google_workspace_agent.auth import GoogleWorkspaceAuth

def main():
    try:
        # Initialize the authentication
        auth = GoogleWorkspaceAuth()
        
        # Perform authentication
        credentials = auth.authenticate()
        
        print("Authentication successful!")
        print(f"Credentials valid: {credentials.valid}")
        print(f"Credentials expired: {credentials.expired}")
    except Exception as e:
        print(f"Authentication failed: {e}")

if __name__ == "__main__":
    main()
