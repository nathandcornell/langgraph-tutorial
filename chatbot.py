import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
# from IPython.display import TextDisplayObject, display

env_file = '.env'
if os.path.exists(env_file):
    load_dotenv(env_file, override=True)

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

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

# Initialize the chatbot with the current state
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# The first argument is the unique node name
# The second is the function or argument that will be called whenever
# the node is used
graph_builder.add_node("chatbot", chatbot)

# Add the entry point
graph_builder.add_edge(START, "chatbot")
# ...and the exit point
graph_builder.add_edge("chatbot", END)

# Compile the graph
graph = graph_builder.compile()

'''
# Display the graph
try:
    display(TextDisplayObject(graph.get_graph().draw_ascii()))
except Exception:
    pass
'''

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant: ", value["messages"][-1].content)

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

