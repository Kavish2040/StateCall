#!/usr/bin/env python3
"""
Simple test script for StateCall library
"""

from statecall.memory import (
    append_to_history,
    load_context,
    get_session_history,
    clear_session,
    list_sessions,
    get_session_info
)
from statecall.groq_client import GroqClient


def test_memory_functions():
    """Test basic memory functions."""
    print("Testing memory functions...")
    
    session_id = "test-session"
    
    # Clear any existing test session to start fresh
    clear_session(session_id)
    
    # Test append_to_history
    append_to_history(session_id, "user", "Hello, how are you?")
    append_to_history(session_id, "assistant", "I'm doing well, thank you!")
    append_to_history(session_id, "user", "What's the weather like?")
    
    # Test get_session_history
    history = get_session_history(session_id)
    print(f"Session history: {len(history)} messages")
    for msg in history:
        print(f"  {msg['role']}: {msg['content']}")
    
    # Test load_context
    context = load_context(session_id)
    print(f"Context loaded: {len(context)} messages")
    
    # Test get_session_info
    info = get_session_info(session_id)
    print(f"Session info: {info}")
    
    # Test list_sessions
    sessions = list_sessions()
    print(f"All sessions: {sessions}")
    
    print("Memory functions test completed!\n")


def test_groq_client():
    """Test Groq client (without API key)."""
    print("Testing Groq client...")
    
    try:
        # This should raise an error since no API key is provided
        client = GroqClient()
        print("ERROR: Should have raised an error for missing API key")
    except ValueError as e:
        print(f"Expected error caught: {e}")
    
    # Test client creation with dummy key
    client = GroqClient(api_key="dummy-key")
    print(f"Client created with model: {client.model}")
    
    print("Groq client test completed!\n")


def main():
    """Run all tests."""
    print("=== StateCall Library Test ===\n")
    
    test_memory_functions()
    test_groq_client()
    
    print("All tests completed successfully!")
    print("\nTo test with real APIs:")
    print("1. Set OPENAI_API_KEY for OpenAI example")
    print("2. Set GROQ_API_KEY for Groq example")
    print("3. Run: python examples/groq_chat_example.py")


if __name__ == "__main__":
    main() 