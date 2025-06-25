#!/usr/bin/env python3
"""
Example: Using StateCall with Groq API
This example demonstrates the built-in Groq integration with StateCall
for easy conversation memory management.
"""

import os
import sys
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from statecall.groq_client import GroqClient
from statecall.memory import append_to_history, get_session_history, list_sessions


def main():
    # Set up Groq API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Please set GROQ_API_KEY environment variable")
        print("You can get a free API key from https://console.groq.com/")
        return
    
    # Initialize Groq client
    client = GroqClient(api_key=api_key)
    session_id = "groq-demo-session"
    
    print("=== StateCall with Groq Example ===\n")
    
    # Example conversation
    conversation = [
        "Who won the World Cup in 2022?",
        "What was the final score?",
        "Who scored the goals?",
        "What was my first question about?"
    ]
    
    print("Starting conversation with Groq...\n")
    
    for i, user_message in enumerate(conversation, 1):
        print(f"User {i}: {user_message}")
        
        try:
            # Use the convenient chat_with_memory method
            response = client.chat_with_memory(session_id, user_message)
            print(f"Assistant: {response}\n")
            
        except Exception as e:
            print(f"Error: {e}\n")
    
    print("=== Session Information ===")
    from statecall.memory import get_session_info
    info = get_session_info(session_id)
    
    if info:
        print(f"Session ID: {info['session_id']}")
        print(f"Total Messages: {info['message_count']}")
        print(f"User Messages: {info['user_messages']}")
        print(f"Assistant Messages: {info['assistant_messages']}")
        print(f"Created: {info['created_at']}")
        print(f"Last Updated: {info['last_updated']}")
    
    print(f"\n=== All Sessions ===")
    sessions = list_sessions()
    print(f"Active sessions: {sessions}")
    
    print(f"\n=== Full Conversation History ===")
    history = get_session_history(session_id)
    
    for msg in history:
        print(f"{msg['role'].title()}: {msg['content']}")


def interactive_chat():
    """Interactive chat mode with Groq."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Please set GROQ_API_KEY environment variable")
        return
    
    client = GroqClient(api_key=api_key)
    session_id = "interactive-session"
    
    print("=== Interactive Chat with Groq ===")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            
            if not user_input:
                continue
            
            response = client.chat_with_memory(session_id, user_input)
            print(f"Assistant: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    # Check if interactive mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_chat()
    else:
        main()

# Get download stats for your package
url = "https://pypi.org/pypi/statecall/json"
response = requests.get(url)
data = response.json()

print(f"Latest version: {data['info']['version']}")
print(f"Total downloads: {data['info']['downloads']['total']}") 