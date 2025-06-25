# StateCall Installation Guide

Quick Installation

From Local Directory
```bash
# Navigate to the StateCall directory
cd /Users/kavishsoningra/StateCall

# Install in development mode
pip install -e .
```

Install Dependencies
```bash
pip install -r requirements.txt
```

Testing the Installation

Run the test script to verify everything is working:
```bash
python test_statecall.py
```

Using StateCall

Basic Usage
```python
from statecall.memory import append_to_history, load_context

# Add messages to conversation history
append_to_history("my-session", "user", "Hello!")
append_to_history("my-session", "assistant", "Hi there!")

# Load conversation context for LLM API
history = load_context("my-session")
```

With Groq Integration
```python
from statecall.groq_client import GroqClient

# Set your Groq API key
import os
os.environ["GROQ_API_KEY"] = "your-api-key-here"

# Use the client
client = GroqClient()
response = client.chat_with_memory("session-id", "Your message here")
```

Examples

Run the example scripts:
```bash
# OpenAI example (requires OPENAI_API_KEY)
python examples/custom_llm_openai_example.py

# Groq example (requires GROQ_API_KEY)
python examples/groq_chat_example.py

# Interactive Groq chat
python examples/groq_chat_example.py --interactive
```

API Keys

You'll need API keys for the AI services:

1. OpenAI: Get from https://platform.openai.com/api-keys
2. Groq: Get from https://console.groq.com/ (free tier available)

Set them as environment variables:
```bash
export OPENAI_API_KEY="your-openai-key"
export GROQ_API_KEY="your-groq-key"
``` 