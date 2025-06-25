"""
Groq client integration for StateCall library.
Provides easy access to Groq API with conversation memory.
"""

import os
import requests
from typing import List, Dict, Any, Optional


class GroqClient:
    """
    Client for interacting with Groq API.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama3-8b-8192"):
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key (can also be set via GROQ_API_KEY env var)
            model: Model to use for chat completions
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key is required. Set it as parameter or GROQ_API_KEY environment variable.")
        
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Send messages to Groq API and get response.
        
        Args:
            messages: List of message dictionaries with "role" and "content"
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            Assistant's response as string
        """
        payload = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Groq API request failed: {str(e)}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected response format from Groq API: {str(e)}")
    
    def chat_with_memory(self, session_id: str, user_message: str, **kwargs) -> str:
        """
        Send a user message and get response with automatic memory management.
        
        Args:
            session_id: Session identifier for memory
            user_message: User's message
            **kwargs: Additional parameters for the API call
            
        Returns:
            Assistant's response as string
        """
        from .memory import append_to_history, get_session_history
        
        # Add user message to history
        append_to_history(session_id, "user", user_message)
        
        # Get conversation history
        history = get_session_history(session_id)
        
        # Get response from Groq
        response = self.chat(history, **kwargs)
        
        # Add assistant response to history
        append_to_history(session_id, "assistant", response)
        
        return response
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models from Groq.
        
        Returns:
            List of model information dictionaries
        """
        try:
            response = requests.get(
                f"{self.base_url}/models",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("data", [])
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch models: {str(e)}")
    
    def get_model_info(self, model_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific model.
        
        Args:
            model_id: Model ID (uses self.model if not provided)
            
        Returns:
            Model information dictionary or None if not found
        """
        model_id = model_id or self.model
        
        try:
            response = requests.get(
                f"{self.base_url}/models/{model_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch model info: {str(e)}")
    
    def set_model(self, model: str):
        """
        Change the model used for chat completions.
        
        Args:
            model: New model identifier
        """
        self.model = model 