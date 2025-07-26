import os

from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
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
graph = graph_builder.compile()

# Display the graph
try:
    print(graph.get_graph().draw_ascii())
except Exception:
    pass

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            if DEBUG:
                print(f"\nDebug: {value}\n")
            msg = ""

            if isinstance(value["messages"][-1], ToolMessage):
                continue
            elif isinstance(value["messages"][-1].content, list):
                msg = value["messages"][-1].content[0]["text"]
            elif isinstance(value["messages"][-1].content, str):
                msg = value["messages"][-1].content
            else:
                continue

            print(f"Assistant: {msg}\n")

while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is unavailable
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break
