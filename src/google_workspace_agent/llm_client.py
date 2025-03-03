"""
LLM Client module for Google Workspace Intelligent Agent.

Provides natural language processing capabilities using Groq API.
"""

from typing import List, Dict, Any, Optional
import os
import logging

from groq import Groq
from pydantic import BaseModel, Field

class ConversationContext(BaseModel):
    """
    Represents the context of a conversation.
    
    Helps maintain state and provide contextual understanding
    for language model interactions.
    """
    
    messages: List[Dict[str, str]] = Field(default_factory=list)
    max_context_length: int = 10
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation context.
        
        Args:
            role: Message role (system, user, assistant)
            content: Message content
        """
        self.messages.append({"role": role, "content": content})
        
        # Trim context if it exceeds max length
        if len(self.messages) > self.max_context_length:
            self.messages = self.messages[-self.max_context_length:]
    
    def clear(self) -> None:
        """Reset conversation context."""
        self.messages.clear()

class GroqLLMClient:
    """
    Client for interacting with Groq Language Model API.
    
    Provides methods for generating natural language responses,
    processing queries, and managing conversation context.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 model: str = 'llama2-70b-4096'):
        """
        Initialize Groq LLM Client.
        
        Args:
            api_key: Groq API key. If not provided, reads from environment
            model: LLM model to use
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY env var.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model
        self.context = ConversationContext()
        
        # Configure logging
        logging.basicConfig(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def generate_response(self, 
                          prompt: str, 
                          system_message: Optional[str] = None) -> str:
        """
        Generate a response using the LLM.
        
        Args:
            prompt: User's input/query
            system_message: Optional system-level context/instruction
        
        Returns:
            Generated response from the LLM
        """
        # Prepare messages
        messages = []
        
        if system_message:
            messages.append({
                "role": "system", 
                "content": system_message
            })
        
        # Add conversation history
        messages.extend(self.context.messages)
        
        # Add current user prompt
        messages.append({
            "role": "user", 
            "content": prompt
        })
        
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=1024,
                temperature=0.7
            )
            
            # Extract response text
            generated_text = response.choices[0].message.content
            
            # Update conversation context
            self.context.add_message("user", prompt)
            self.context.add_message("assistant", generated_text)
            
            return generated_text
        
        except Exception as e:
            self.logger.error(f"LLM generation error: {e}")
            raise
    
    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """
        Summarize given text using LLM.
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
        
        Returns:
            Summarized text
        """
        system_message = f"Summarize the following text concisely in under {max_length} characters:"
        
        summary = self.generate_response(
            prompt=text, 
            system_message=system_message
        )
        
        return summary[:max_length]
    
    def reset_context(self) -> None:
        """Reset the conversation context."""
        self.context.clear()
