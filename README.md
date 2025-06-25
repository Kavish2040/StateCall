# StateCall

A simple Python library that adds memory to AI chatbots. StateCall remembers your conversations so AI can reference previous messages.

What it does

Most AI chatbots forget everything when you start a new conversation. StateCall saves your chat history so the AI can remember what you talked about before.

Features

- Works with any AI service (OpenAI, Groq, Claude, etc.)
- Built-in Groq support
- Saves conversations locally on your computer
- No database or internet connection needed
- Simple to use
- Export/import conversations (JSON/CSV)
- Conversation statistics and analytics

Installation

```bash
pip install statecall
```

Quick start

Basic usage

```python
from statecall.memory import append_to_history, load_context
import openai

openai.api_key = "your-openai-api-key"
session_id = "my-chat"

# Save a message
append_to_history(session_id, "user", "Tell me a joke.")
history = load_context(session_id)

# Get AI response
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=history
)

assistant_msg = response["choices"][0]["message"]["content"]
append_to_history(session_id, "assistant", assistant_msg)

print("AI:", assistant_msg)
```

Using Groq

```python
from statecall.groq_client import GroqClient
from statecall.memory import append_to_history, get_session_history

session_id = "groq-chat"
client = GroqClient(api_key="your-groq-api-key")

append_to_history(session_id, "user", "Who won the World Cup in 2022?")
history = get_session_history(session_id)
response = client.chat(history)

append_to_history(session_id, "assistant", response)
print("AI:", response)
```

Export and Import

Export a conversation to JSON or CSV:

```python
from statecall.memory import export_conversation, import_conversation

# Export to JSON
export_conversation("my-chat", "conversation.json", "json")

# Export to CSV
export_conversation("my-chat", "conversation.csv", "csv")

# Import a conversation
imported_session = import_conversation("conversation.json")
```

Get conversation statistics:

```python
from statecall.memory import get_conversation_stats

stats = get_conversation_stats()
print(f"Total sessions: {stats['total_sessions']}")
print(f"Total messages: {stats['total_messages']}")
```

How it works

StateCall saves your conversations in two files on your computer:

- `.statecall_history.json` - stores all your messages
- `.statecall_sessions.json` - tracks your chat sessions

This way your conversations are saved between app restarts without needing a database.

Examples

Check the `examples/` folder:

- `custom_llm_openai_example.py` - using OpenAI
- `groq_chat_example.py` - using Groq
- `export_import_example.py` - export/import features

To run an example:

```bash
python examples/groq_chat_example.py
```

License

MIT License
