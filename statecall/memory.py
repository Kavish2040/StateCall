"""
Memory management for StateCall library.
Handles conversation history storage and retrieval.
"""

import json
import os
import csv
from typing import List, Dict, Any, Optional
from datetime import datetime


# File paths for storage
HISTORY_FILE = ".statecall_history.json"
SESSIONS_FILE = ".statecall_sessions.json"


def _ensure_storage_files():
    """Ensure storage files exist with proper structure."""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f:
            json.dump({}, f)
    
    if not os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, 'w') as f:
            json.dump({"sessions": []}, f)


def _load_history_data() -> Dict[str, Any]:
    """Load history data from file."""
    _ensure_storage_files()
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def _save_history_data(data: Dict[str, Any]):
    """Save history data to file."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def _load_sessions_data() -> Dict[str, Any]:
    """Load sessions data from file."""
    _ensure_storage_files()
    try:
        with open(SESSIONS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"sessions": []}


def _save_sessions_data(data: Dict[str, Any]):
    """Save sessions data to file."""
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def append_to_history(session_id: str, role: str, content: str) -> None:
    """
    Add a message to the conversation history.
    
    Args:
        session_id: Unique identifier for the conversation session
        role: Message role ("user" or "assistant")
        content: Message content
    """
    if role not in ["user", "assistant"]:
        raise ValueError("Role must be 'user' or 'assistant'")
    
    history_data = _load_history_data()
    
    if session_id not in history_data:
        history_data[session_id] = []
    
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    
    history_data[session_id].append(message)
    _save_history_data(history_data)
    
    # Update sessions list
    sessions_data = _load_sessions_data()
    if session_id not in sessions_data["sessions"]:
        sessions_data["sessions"].append(session_id)
        _save_sessions_data(sessions_data)


def get_session_history(session_id: str) -> List[Dict[str, str]]:
    """
    Get raw conversation history for a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        List of message dictionaries with role and content
    """
    history_data = _load_history_data()
    
    if session_id not in history_data:
        return []
    
    # Return only role and content for LLM API compatibility
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history_data[session_id]
    ]


def load_context(session_id: str) -> List[Dict[str, str]]:
    """
    Load conversation history in the format expected by most LLM APIs.
    
    Args:
        session_id: Session identifier
        
    Returns:
        List of message dictionaries with "role" and "content" keys
    """
    return get_session_history(session_id)


def clear_session(session_id: str) -> None:
    """
    Clear all history for a specific session.
    
    Args:
        session_id: Session identifier
    """
    history_data = _load_history_data()
    
    if session_id in history_data:
        del history_data[session_id]
        _save_history_data(history_data)
    
    # Remove from sessions list
    sessions_data = _load_sessions_data()
    if session_id in sessions_data["sessions"]:
        sessions_data["sessions"].remove(session_id)
        _save_sessions_data(sessions_data)


def list_sessions() -> List[str]:
    """
    Get a list of all active session IDs.
    
    Returns:
        List of session IDs
    """
    sessions_data = _load_sessions_data()
    return sessions_data.get("sessions", [])


def get_session_info(session_id: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a session.
    
    Args:
        session_id: Session identifier
        
    Returns:
        Dictionary with session information or None if not found
    """
    history_data = _load_history_data()
    
    if session_id not in history_data:
        return None
    
    messages = history_data[session_id]
    
    return {
        "session_id": session_id,
        "message_count": len(messages),
        "created_at": messages[0]["timestamp"] if messages else None,
        "last_updated": messages[-1]["timestamp"] if messages else None,
        "user_messages": len([m for m in messages if m["role"] == "user"]),
        "assistant_messages": len([m for m in messages if m["role"] == "assistant"])
    }


def export_conversation(session_id: str, filepath: str, format: str = "json") -> None:
    """
    Export a conversation to a file.
    
    Args:
        session_id: Session identifier
        filepath: Path to save the exported file
        format: Export format ("json" or "csv")
    """
    history_data = _load_history_data()
    
    if session_id not in history_data:
        raise ValueError(f"Session '{session_id}' not found")
    
    messages = history_data[session_id]
    
    if format.lower() == "json":
        export_data = {
            "session_id": session_id,
            "exported_at": datetime.now().isoformat(),
            "message_count": len(messages),
            "messages": messages
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    elif format.lower() == "csv":
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "role", "content"])
            
            for msg in messages:
                writer.writerow([
                    msg["timestamp"],
                    msg["role"],
                    msg["content"]
                ])
    
    else:
        raise ValueError("Format must be 'json' or 'csv'")


def import_conversation(filepath: str, session_id: Optional[str] = None) -> str:
    """
    Import a conversation from a file.
    
    Args:
        filepath: Path to the exported file
        session_id: Session ID to import to (auto-generated if None)
        
    Returns:
        The session ID that was created/updated
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' not found")
    
    # Auto-generate session ID if not provided
    if session_id is None:
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        session_id = f"imported-{base_name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    # Determine format from file extension
    file_ext = os.path.splitext(filepath)[1].lower()
    
    if file_ext == ".json":
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, dict) and "messages" in data:
            messages = data["messages"]
        else:
            messages = data  # Assume it's a direct list of messages
    
    elif file_ext == ".csv":
        messages = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                messages.append({
                    "role": row["role"],
                    "content": row["content"],
                    "timestamp": row.get("timestamp", datetime.now().isoformat())
                })
    
    else:
        raise ValueError("Unsupported file format. Use .json or .csv files")
    
    # Import the messages
    history_data = _load_history_data()
    history_data[session_id] = messages
    _save_history_data(history_data)
    
    # Update sessions list
    sessions_data = _load_sessions_data()
    if session_id not in sessions_data["sessions"]:
        sessions_data["sessions"].append(session_id)
        _save_sessions_data(sessions_data)
    
    return session_id


def export_all_conversations(filepath: str, format: str = "json") -> None:
    """
    Export all conversations to a file.
    
    Args:
        filepath: Path to save the exported file
        format: Export format ("json" or "csv")
    """
    history_data = _load_history_data()
    
    if format.lower() == "json":
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "total_sessions": len(history_data),
            "sessions": history_data
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
    
    elif format.lower() == "csv":
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["session_id", "timestamp", "role", "content"])
            
            for session_id, messages in history_data.items():
                for msg in messages:
                    writer.writerow([
                        session_id,
                        msg["timestamp"],
                        msg["role"],
                        msg["content"]
                    ])
    
    else:
        raise ValueError("Format must be 'json' or 'csv'")


def get_conversation_stats() -> Dict[str, Any]:
    """
    Get statistics about all conversations.
    
    Returns:
        Dictionary with conversation statistics
    """
    history_data = _load_history_data()
    sessions_data = _load_sessions_data()
    
    total_messages = 0
    total_user_messages = 0
    total_assistant_messages = 0
    
    for session_id, messages in history_data.items():
        total_messages += len(messages)
        total_user_messages += len([m for m in messages if m["role"] == "user"])
        total_assistant_messages += len([m for m in messages if m["role"] == "assistant"])
    
    return {
        "total_sessions": len(history_data),
        "active_sessions": len(sessions_data.get("sessions", [])),
        "total_messages": total_messages,
        "total_user_messages": total_user_messages,
        "total_assistant_messages": total_assistant_messages,
        "average_messages_per_session": total_messages / len(history_data) if history_data else 0
    } 