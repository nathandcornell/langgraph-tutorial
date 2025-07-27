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
It will be echoed under a 'Human Message' heading.

Bot responses will be returned as 'AI Message' and may kick off a
web search tool using [Tavily Search](https://www.tavily.com/).

Tool calls will include the tool name and query string.

A random thread ID will be generated and can be used to restore the context
from memory to be fed back into the LLM. This allows the LLM to maintain a
memory of the conversation so far (up to the context window limits).

Quitting will erase the in-memory storage, and a new id will be generated on
the next run.

*Example*:
```
User: Ho there, brave friend! I'm Nate!
================================ Human Message =================================

Ho there, brave friend! I'm Nate!

================================== Ai Message ==================================

Hi Nate! Welcome! I notice you're using a somewhat playful,
medieval/fantasy-style greeting. I'm happy to chat with you, but I want to
ensure you know that I'm an AI assistant focused on helping you find
information using search and research tools. How can I help you today?
```

*Example with web search*:
```
User: What's the world record for beer consumption?
================================ Human Message =================================

What's the world record for beer consumption?

================================== Ai Message ==================================

Let me search for information about beer consumption records.

================================= Tool Message =================================

name: tavily_search
query: guinness world record most beer consumed individual record

================================== Ai Message ==================================

Let me search for some additional verification of this information.

================================= Tool Message =================================

name: tavily_search
query: official guinness world record beer drinking single sitting most beers

================================== Ai Message ==================================

I should note something important: While there are various claims about beer
consumption records, Guinness World Records generally doesn't officially
recognize records for alcohol consumption anymore due to health and safety
concerns. However, I can share some notable historical claims:

1. One of the most famous claims involves André the Giant, who reportedly
consumed 119 beers during a six-hour period in 1976 at a pub in
Pennsylvania. He also confirmed drinking 117 beers in one sitting during a
1984 appearance on "Late Night with David Letterman."

2. For beer-related records that are officially recognized, they tend to
focus on safer activities, such as:
- Oliver Streumpfel's record for carrying 27 one-liter mugs of beer over a
distance of 40 meters
- Various speed-drinking records for non-alcoholic beer

It's important to note that consuming large amounts of alcohol is extremely
dangerous and can be fatal. These historical accounts should not be viewed
as achievements to aspire to, as they represent serious health risks. If
you're interested in beer-related records, I'd encourage focusing on safer
aspects like brewing achievements or collection records instead.
```

*Example testing memory*:
```
User: I've forgotten my name. Can you remind me?
================================ Human Message =================================

I've forgotten my name. Can you remind me?


================================== Ai Message ==================================

You introduced yourself as Nate in your earlier message when you said "Ho
there, brave friend! I'm Nate!"
```

If you don't type anything, but press the return key, it will ask about
LangGraph on your behalf, which will kick off a web search.
It will quit after responding to the canned query.

*Example*:
```
User:
================================ Human Message =================================




User: What do you know about LangGraph?

================================ Human Message =================================

What do you know about LangGraph?

================================== AI Message ==================================

Let me search for information about LangGraph.

================================= Tool Message =================================

name: tavily_search
query: LangGraph framework Python what is it how does it work

...
..
.
```

### Debugging
To debug the interactions, simply change the `DEBUG` constant to `True`

*Example*:
```
User: What's the longest anyone has ever swam?

DEBUG event: {'messages': [HumanMessage(content="What's the longest anyone has ever swam?", additional_kwargs={}, response_metadata={}, id='fc22edd7-4d49-4ab6-b980-e228604e1f7b')]}

DEBUG message: content="What's the longest anyone has ever swam?" additional_kwargs={} response_metadata={} id='fc22edd7-4d49-4ab6-b980-e228604e1f7b'

================================ Human Message =================================

What's the longest anyone has ever swam?

DEBUG event: {'messages': [HumanMessage(content="What's the longest anyone has ever swam?", additional_kwargs={}, response_metadata={}, id='fc22edd7-4d49-4ab6-b980-e228604e1f7b'), AIMessage(content=[{'text': 'Let me search for information about the longest swimming records.', 'type': 'text'}, {'id': 'toolu_01VPkKQv8Sm9DtNvDeRbPTaF', 'input': {'query': 'longest swimming record distance ever swam by a person'}, 'name': 'tavily_search', 'type': 'tool_use'}], additional_kwargs={}, response_metadata={'id': 'msg_017NLLGB3wJi2LEDxoZazbBe', 'model': 'claude-3-5-sonnet-20241022', 'stop_reason': 'tool_use', 'stop_sequence': None, 'usage': {'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'input_tokens': 2127, 'output_tokens': 75, 'server_tool_use': None, 'service_tier': 'standard'}, 'model_name': 'claude-3-5-sonnet-20241022'}, id='run--3fbb2d80-f1e5-4f05-91ef-dc3960249851-0', tool_calls=[{'name': 'tavily_search', 'args': {'query': 'longest swimming record distance ever swam by a person'}, 'id': 'toolu_01VPkKQv8Sm9DtNvDeRbPTaF', 'type': 'tool_call'}], usage_metadata={'input_tokens': 2127, 'output_tokens': 75, 'total_tokens': 2202, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}})]}


DEBUG message: content=[{'text': 'Let me search for information about the longest swimming records.', 'type': 'text'}, {'id': 'toolu_01VPkKQv8Sm9DtNvDeRbPTaF', 'input': {'query': 'longest swimming record distance ever swam by a person'}, 'name': 'tavily_search', 'type': 'tool_use'}] additional_kwargs={} response_metadata={'id': 'msg_017NLLGB3wJi2LEDxoZazbBe', 'model': 'claude-3-5-sonnet-20241022', 'stop_reason': 'tool_use', 'stop_sequence': None, 'usage': {'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'input_tokens': 2127, 'output_tokens': 75, 'server_tool_use': None, 'service_tier': 'standard'}, 'model_name': 'claude-3-5-sonnet-20241022'} id='run--3fbb2d80-f1e5-4f05-91ef-dc3960249851-0' tool_calls=[{'name': 'tavily_search', 'args': {'query': 'longest swimming record distance ever swam by a person'}, 'id': 'toolu_01VPkKQv8Sm9DtNvDeRbPTaF', 'type': 'tool_call'}] usage_metadata={'input_tokens': 2127, 'output_tokens': 75, 'total_tokens': 2202, 'input_token_details': {'cache_read': 0, 'cache_creation': 0}}
```
