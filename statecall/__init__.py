"""
StateCall - A lightweight library to add memory to stateless LLM APIs
"""

from .memory import (
    append_to_history,
    load_context,
    get_session_history,
    clear_session,
    list_sessions,
    get_session_info,
    export_conversation,
    import_conversation,
    export_all_conversations,
    get_conversation_stats,
)
from .groq_client import GroqClient

__version__ = "0.2.0"
__author__ = "Kavish Soningra"

__all__ = [
    "append_to_history",
    "load_context", 
    "get_session_history",
    "clear_session",
    "list_sessions",
    "get_session_info",
    "export_conversation",
    "import_conversation",
    "export_all_conversations",
    "get_conversation_stats",
    "GroqClient",
] 