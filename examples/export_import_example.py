#!/usr/bin/env python3
"""
Example: Using StateCall Export/Import Features
This example demonstrates how to export and import conversations.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from statecall.memory import (
    append_to_history,
    export_conversation,
    import_conversation,
    export_all_conversations,
    get_conversation_stats,
    get_session_history,
    clear_session
)


def main():
    print("=== StateCall Export/Import Example ===\n")
    
    # Create a sample conversation
    session_id = "export-demo"
    clear_session(session_id)  # Start fresh
    
    print("Creating sample conversation...")
    append_to_history(session_id, "user", "Hello! What's the weather like?")
    append_to_history(session_id, "assistant", "I can't check the weather, but I can help you with other questions!")
    append_to_history(session_id, "user", "Tell me a joke")
    append_to_history(session_id, "assistant", "Why don't scientists trust atoms? Because they make up everything!")
    append_to_history(session_id, "user", "What was my first question?")
    append_to_history(session_id, "assistant", "Your first question was about the weather!")
    
    # Show the conversation
    print("Original conversation:")
    history = get_session_history(session_id)
    for msg in history:
        print(f"  {msg['role']}: {msg['content']}")
    
    # Export to JSON
    print("\nExporting conversation to JSON...")
    export_conversation(session_id, "conversation.json", "json")
    print("✅ Exported to conversation.json")
    
    # Export to CSV
    print("Exporting conversation to CSV...")
    export_conversation(session_id, "conversation.csv", "csv")
    print("✅ Exported to conversation.csv")
    
    # Clear the session
    print("\nClearing the session...")
    clear_session(session_id)
    print("✅ Session cleared")
    
    # Import from JSON
    print("\nImporting from JSON...")
    imported_session = import_conversation("conversation.json")
    print(f"✅ Imported to session: {imported_session}")
    
    # Show imported conversation
    print("Imported conversation:")
    imported_history = get_session_history(imported_session)
    for msg in imported_history:
        print(f"  {msg['role']}: {msg['content']}")
    
    # Export all conversations
    print("\nExporting all conversations...")
    export_all_conversations("all_conversations.json", "json")
    print("✅ Exported all conversations to all_conversations.json")
    
    # Show statistics
    print("\nConversation statistics:")
    stats = get_conversation_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Clean up
    print("\nCleaning up...")
    os.remove("conversation.json")
    os.remove("conversation.csv")
    os.remove("all_conversations.json")
    print("✅ Cleanup complete")


if __name__ == "__main__":
    main() 