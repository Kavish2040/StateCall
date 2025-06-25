#!/usr/bin/env python3
"""
Simple Groq test with StateCall
"""

import os
from statecall.groq_client import GroqClient
from statecall.memory import append_to_history, get_session_history

# Set your Groq API key
os.environ["GROQ_API_KEY"] = "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"

def test_groq_with_memory():
    """Test Groq integration with memory."""
    print("=== Testing StateCall with Groq ===\n")
    
    # Initialize Groq client
    client = GroqClient()
    session_id = "groq-test-session"
    
    # Clear any existing session
    from statecall.memory import clear_session
    clear_session(session_id)
    
    # Test conversation
    messages = [
        "Hello! What's the weather like today?",
        "Can you tell me a joke?",
        "What was my first question about?"
    ]
    
    for i, user_message in enumerate(messages, 1):
        print(f"User {i}: {user_message}")
        
        try:
            # Use the convenient chat_with_memory method
            response = client.chat_with_memory(session_id, user_message)
            print(f"Assistant: {response}\n")
            
        except Exception as e:
            print(f"Error: {e}\n")
    
    # Show conversation history
    print("=== Full Conversation History ===")
    history = get_session_history(session_id)
    
    for msg in history:
        print(f"{msg['role'].title()}: {msg['content']}")
    
    print(f"\nTotal messages: {len(history)}")

if __name__ == "__main__":
    test_groq_with_memory() 