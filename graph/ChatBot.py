import os
from langchain.chat_models import init_chat_model
from langgraph.constants import START
from openai import azure_endpoint
from torch.cuda import graph

from graph.StateGraph import graph_builder, State


apiKey = " "
endpoint = ""
open_ai_version = "2024-05-01-previe"
azure_deployment = " "

llm = init_chat_model(
    "azure_openai:gpt-4.0",
    azure_deployment=azure_deployment,
    azure_endpoint=endpoint,
    api_key=apiKey,
    openai_api_version=open_ai_version,

)


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)


graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()

# from IPython.display import Image, display
# try:
#     display(Image(graph.get_graph().draw_mermaid_png()))
# except Exception:
#     pass


def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        user_input = "What do you know about LangGraph?"
        stream_graph_updates(user_input)
        break
