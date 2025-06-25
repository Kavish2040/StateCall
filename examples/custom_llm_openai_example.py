#!/usr/bin/env python3
"""
Example: Using StateCall with OpenAI API
This example demonstrates how to integrate StateCall with OpenAI's API
to add conversation memory to your LLM applications.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from statecall.memory import append_to_history, load_context
import openai


def main():
    # Set up OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return
    
    openai.api_key = api_key
    session_id = "openai-demo-session"
    
    print("=== StateCall with OpenAI Example ===\n")
    
    # Example conversation
    conversation = [
        "Hello! What's the weather like today?",
        "Can you tell me a joke?",
        "What was my first question?"
    ]
    
    for i, user_message in enumerate(conversation, 1):
        print(f"User {i}: {user_message}")
        
        # Add user message to history
        append_to_history(session_id, "user", user_message)
        
        # Load conversation context
        history = load_context(session_id)
        
        try:
            # Get response from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=history,
                max_tokens=150
            )
            
            assistant_msg = response["choices"][0]["message"]["content"]
            
            # Add assistant response to history
            append_to_history(session_id, "assistant", assistant_msg)
            
            print(f"Assistant: {assistant_msg}\n")
            
        except Exception as e:
            print(f"Error: {e}\n")
    
    print("=== Conversation History ===")
    from statecall.memory import get_session_history
    history = get_session_history(session_id)
    
    for msg in history:
        print(f"{msg['role'].title()}: {msg['content']}")
    
    print(f"\nTotal messages: {len(history)}")


if __name__ == "__main__":
    main() 