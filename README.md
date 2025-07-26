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
Create a `.env` file. Add your Anthropic api key as `ANTHROPIC_API_KEY`, and
Tavily api key as `TAVILY_API_KEY`

example:
```
ANTHROPIC_API_KEY=sk-xxx-xxxxx-xxxxyyyyyyyyyyyyyyyyyyyxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyxxxxxxxxxxxxxxxyyyyyyyyxyy-xyxyxyxy
TAVILY_API_KEY=tvly-dev-xxxxxxxxxxxxxxxxxxxyyyyyyyyyyyyy
```

## Operations
### Run
To start the chatbot, just run
```bash
uv run ./chatbot.py
```

It will draw the current graph, and greet you with an input prompt

*Example*:
```
$ uv run ./chatbot.py
        +-----------+
        | __start__ |
        +-----------+
               *
               *
               *
          +---------+
          | chatbot |
          +---------+
          .         .
        ..           ..
       .               .
+---------+         +-------+
| __end__ |         | tools |
+---------+         +-------+
User: 
```

### Quit
At the `User: ` prompt, type 'q', 'quit', or 'exit'

*Example*:
```
User: q
Goodbye!
```

### Using the chatbot
At the `User: ` prompt, type any question or comment in natural language.

Bot responses will be returned at the `Assistant: ` prompts and may kick off a
web search using [Tavily Search](https://www.tavily.com/).

*Example*:
```
User: Ho there, brave friend!
Assistant:  *Gives a friendly wave* Well met! How can I assist you on this fine day?
```

*Example with web search*:
```
User: What's the world record for beer consumption?
Assistant: Let me search for information about the world record for beer consumption.

Assistant: Let me search for more specific details about this record.

Assistant: Based on the search results, I can tell you about the most famous verified beer consumption record:

André the Giant (André Rene Roussimoff) holds what is considered to be the record for most beer consumed in a single sitting. The most commonly cited instance occurred in 1976 at a Pennsylvania pub, where he reportedly consumed 119 beers in a six-hour period. Each beer was 12 ounces, meaning he drank approximately one beer every three minutes.

It's worth noting that André the Giant was a unique case - he was billed at 7 feet 4 inches tall and weighed over 500 pounds. In a 1984 appearance on "Late Night with David Letterman," André himself confirmed drinking 117 beers in one sitting, though this may have been a different occasion.

It's important to note that attempting to break this kind of record would be extremely dangerous and potentially lethal for most people. Such extreme alcohol consumption can lead to severe health consequences including alcohol poisoning and death.
```

If you don't type anything, but press the return key, it will ask about
LangGraph on your behalf, which will kick off a web search.

*Example*:
```
User:
User: What do you know about LangGraph?
Assistant: Let me search for information about LangGraph.

Assistant: Based on the search results, I can provide you with comprehensive information about LangGraph:

LangGraph is an open-source AI agent framework that was created by LangChain and is designed to build, deploy, and manage complex generative AI agent workflows. Here are the key points about LangGraph:

1. Core Purpose:
- It provides a framework for defining, coordinating, and executing multiple LLM agents (or chains) in a structured and efficient manner
- It's specifically designed for creating stateful, multi-agent systems
- Uses graph-based architectures to model and manage relationships between various components of an AI agent workflow

2. Key Features:
- State Management: Unlike traditional LangChain, LangGraph has persistent state features, making it ideal for applications that need to remember past interactions
- Transparency: It illuminates the processes within an AI workflow, allowing full visibility of the agent's state
- Node-based Architecture: Uses nodes to represent individual components or agents within an AI workflow
- Enhanced Decision-making: Models complex relationships between nodes and uses AI agents to analyze their past actions and feedback

3. Main Benefits:
- Simplifies the development of complex LLM applications
- Allows developers to focus on high-level logic rather than agent coordination details
- Provides structured framework for managing state and coordinating agent interactions
- Offers versatile platform for developing various AI solutions including chatbots, state graphs, and agent-based systems

4. Use Cases:
- Best suited for applications that need to:
  - Remember past interactions
  - Use historical information for future decisions
  - Handle complex, stateful workflows
  - Coordinate multiple AI agents
  - Manage dynamic workflow adjustments based on past interactions

LangGraph is part of the larger LangChain ecosystem but serves a distinct purpose, particularly when it comes to handling stateful, complex agent interactions and workflows. It's particularly valuable when building applications that require persistent memory and sophisticated agent coordination.```
