# LangGraph Tutorial Project

## Summary
Code from my implementation of the [LangGraph Tutorial](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/)

## Getting Started

### Prerequisites
First make sure you have [uv](https://docs.astral.sh/uv/) installed. It's a
great package manager + virtual environment for Python, written in Rust, that
is about 100x faster than pip.

### Install dependencies
```bash
uv sync
```

### Environment
Create a `.env` file. Add your Anthropic api key as `ANTHROPIC_API_KEY`

example:
```
ANTHROPIC_API_KEY=xxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyxxxxxxxxxxxxxxxyyyyyyyy
```

## Operations
### Run
To start the chatbot, just run
```bash
uv run ./chatbot.py
```

### Quit
At the `User: ` prompt, type 'q', 'quit', or 'exit'

### Using the chatbot
At the `User: ` prompt, type any question or comment in natural language.

example:
```
User: Ho there, brave friend!
```

Bot responses will be returned at the `Assistant: ` prompts.

example:
```
Assistant:  *Gives a friendly wave* Well met! How can I assist you on this fine day?
```
