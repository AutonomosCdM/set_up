"""
Unit tests for Groq LLM Client module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from google_workspace_agent.llm_client import GroqLLMClient, ConversationContext

class TestGroqLLMClient:
    @pytest.fixture
    def mock_env(self, monkeypatch):
        """Set up mock environment variables for testing."""
        monkeypatch.setenv('GROQ_API_KEY', 'test_api_key')
    
    def test_initialization(self, mock_env):
        """Test client initialization."""
        client = GroqLLMClient()
        
        assert client.api_key == 'test_api_key'
        assert client.model == 'llama2-70b-4096'
        assert len(client.context.messages) == 0
    
    def test_initialization_with_custom_key(self):
        """Test initialization with custom API key."""
        client = GroqLLMClient(api_key='custom_key')
        
        assert client.api_key == 'custom_key'
    
    def test_missing_api_key(self, monkeypatch):
        """Test initialization without API key raises ValueError."""
        monkeypatch.delenv('GROQ_API_KEY', raising=False)
        
        with pytest.raises(ValueError, match="Groq API key is required"):
            GroqLLMClient()
    
    def test_conversation_context(self):
        """Test conversation context management."""
        context = ConversationContext()
        
        context.add_message("user", "Hello")
        context.add_message("assistant", "Hi there!")
        
        assert len(context.messages) == 2
        assert context.messages[0]["role"] == "user"
        assert context.messages[1]["role"] == "assistant"
    
    def test_context_max_length(self):
        """Test context length limitation."""
        context = ConversationContext(max_context_length=3)
        
        # Add more messages than max length
        for i in range(5):
            context.add_message("user", f"Message {i}")
        
        assert len(context.messages) == 3
        assert context.messages[0]["content"] == "Message 2"
    
    @patch('groq.Groq')
    def test_generate_response(self, mock_groq, mock_env):
        """Test response generation."""
        # Mock Groq client response
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content="Test response"))
        ]
        
        mock_groq_instance = mock_groq.return_value
        mock_groq_instance.chat.completions.create.return_value = mock_response
        
        client = GroqLLMClient()
        response = client.generate_response("Test prompt")
        
        assert response == "Test response"
        assert len(client.context.messages) == 2
    
    def test_summarize_text(self, mock_env):
        """Test text summarization."""
        with patch.object(GroqLLMClient, 'generate_response', 
                          return_value="Short summary of long text") as mock_generate:
            client = GroqLLMClient()
            summary = client.summarize_text("Long text to summarize", max_length=20)
            
            assert len(summary) <= 20
            mock_generate.assert_called_once()
    
    def test_reset_context(self, mock_env):
        """Test context reset."""
        client = GroqLLMClient()
        
        # Add some messages
        client.generate_response("Test prompt")
        
        assert len(client.context.messages) > 0
        
        client.reset_context()
        
        assert len(client.context.messages) == 0
