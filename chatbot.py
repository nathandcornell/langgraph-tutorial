import json
import os
import uuid

from dotenv import load_dotenv
from langchain_core.runnables import RunnableConfig
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Annotated
from typing_extensions import TypedDict

env_file = '.env'
if os.path.exists(env_file):
    load_dotenv(env_file, override=True)

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
DEBUG=False

# Our model for saving state
class State(TypedDict):
    # Messages have the type "list". The 'add_messages' function
    # in the annotation defines how this state should be updated
    # (in this case it appends messages to the list, rather than
    # overwriting them)
    messages: Annotated[list, add_messages]

# Initialize our "memory"
memory = InMemorySaver()

# Initialize our graph builder
graph_builder = StateGraph(State)

# Define our LLM chat agent
llm = init_chat_model('anthropic:claude-3-5-sonnet-latest')

# Add a websearch tool the the toolbox
tool = TavilySearch(max_results=5)
tools = [tool]

tools[0].invoke("What's a 'node' in LangGraph?")

llm_with_tools = llm.bind_tools(tools)

# Add tools to the graph
tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

# Initialize the chatbot with the current state
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# The `tools_condition` function returns "tools" if the chatbot asks to use a
# tool, and "END" if it is fine responding. This conditionional routing defines
# the main agent loop
graph_builder.add_conditional_edges("chatbot", tools_condition)

# The first argument is the unique node name
# The second is the function or argument that will be called whenever
# the node is used
graph_builder.add_node("chatbot", chatbot)

# Add the entry point
graph_builder.add_edge(START, "chatbot")
# Anytime a tool is called, return to the chatbot again
graph_builder.add_edge("tools", "chatbot")
# Add the exit point
graph_builder.add_edge("chatbot", END)

# Compile the graph
graph = graph_builder.compile(checkpointer = memory)

# Set a thread id:
thread_id = uuid.uuid4()
config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

# Display the graph
try:
    print(graph.get_graph().draw_ascii() + "\n")
except Exception:
    pass

# Print the thread id:
print(f"Thread id: ${thread_id}\n")

def stream_graph_updates(user_input: str):
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode = "values"
    )

    for event in events:
        if DEBUG:
            print(f"\nDEBUG event: {event}\n")

        message = event["messages"][-1]

        if DEBUG:
            print(f"\nDEBUG message: {message}\n")

        if message.__class__.__name__ == "HumanMessage":
            print("================================ Human Message =================================\n")
            print(message.content)
        elif message.__class__.__name__ == "AIMessage":
            print("================================== AI Message ==================================\n")
            if isinstance(message.content, list):
                print(message.content[0]["text"])
            else:
                print(message.content)
        elif message.__class__.__name__ == "ToolMessage":
            content = json.loads(message.content)

            if DEBUG:
                print(f"\nDEBUG tool content: {content}\n")

            print("================================= Tool Message =================================\n")
            print(f"name: {message.name}")
            print(f"query: {content['query']}")
        else:
            message.pretty_print()

        print("\n")

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)

        if DEBUG:
            snapshot = graph.get_state(config)
            print(f"\nDEBUG: State snapshot: {snapshot}\n")
    except:
        # fallback if input() is unavailable
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
