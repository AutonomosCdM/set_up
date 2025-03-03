"""
Setup script for Google Workspace Intelligent Agent.

Helps users configure their environment and install dependencies.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """
    Verify Python version compatibility.
    """
    if sys.version_info < (3, 9):
        print("Error: Python 3.9+ is required.")
        sys.exit(1)

def install_poetry():
    """
    Install Poetry if not already installed.
    """
    try:
        subprocess.run([sys.executable, '-m', 'poetry', '--version'], 
                       check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("Installing Poetry...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'poetry'], 
                       check=True)

def create_env_file():
    """
    Create .env file from .env.example if it doesn't exist.
    """
    env_example = Path('.env.example')
    env_file = Path('.env')

    if not env_file.exists():
        print("Creating .env file from .env.example...")
        shutil.copy(env_example, env_file)
        print("Please edit .env and add your credentials.")

def install_dependencies():
    """
    Install project dependencies using Poetry.
    """
    print("Installing project dependencies...")
    subprocess.run(['poetry', 'install'], check=True)

def configure_google_credentials():
    """
    Guide user through Google Workspace credentials setup.
    """
    print("\nGoogle Workspace Credentials Setup")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select an existing one")
    print("3. Enable the following APIs:")
    print("   - Gmail API")
    print("   - Google Calendar API")
    print("   - Google Drive API")
    print("   - Google Sheets API")
    print("   - Google Docs API")
    print("4. Create OAuth 2.0 credentials")
    print("5. Download the credentials JSON file")
    
    input("\nPress Enter after downloading the credentials file...")

def configure_groq_api():
    """
    Guide user through Groq API key setup.
    """
    print("\nGroq API Key Setup")
    print("1. Go to https://console.groq.com/")
    print("2. Create an account or log in")
    print("3. Generate a new API key")
    
    input("\nPress Enter after obtaining your Groq API key...")

def main():
    """
    Main setup script execution.
    """
    print("Google Workspace Intelligent Agent - Setup")
    
    # Check Python version
    check_python_version()
    
    # Install Poetry
    install_poetry()
    
    # Create .env file
    create_env_file()
    
    # Guide credential setup
    configure_google_credentials()
    configure_groq_api()
    
    # Install dependencies
    install_dependencies()
    
    print("\nSetup complete!")
    print("Next steps:")
    print("1. Edit .env with your credentials")
    print("2. Run authentication setup: poetry run python -m google_workspace_agent.auth")
    print("3. Try an example workflow: poetry run python examples/workflow_example.py")

if __name__ == '__main__':
    main()
