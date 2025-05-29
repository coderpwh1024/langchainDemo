import os

from langchain.chat_models import init_chat_model
from langgraph.constants import END, START
from langgraph.graph import StateGraph
from langchain_tavily import TavilySearch
import pprint  # 导入美观打印模块

from graph.StateGraph import graph_builder
from langchainDemo.Tool import llm_with_tools
from langchainDemo.Two import messages

tool = TavilySearch(max_results=2, tavily_api_key="")
tools = [tool]
result = tool.invoke("武汉烧烤")

apiKey = " "
endpoint = ""
open_ai_version = "2024-05-01-preview"

llm = init_chat_model(
    "azure_openai:gpt-4.0",
    azure_deployment="",
    azure_endpoint=endpoint,
    api_key=apiKey,
    openai_api_version=open_ai_version,
)

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)

import json
from langchain_core.messages import ToolMessage


class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(tool_call["args"])
            outputs.append(
                ToolMessage(content=json.dumps(tool_result), name=tool_call["name"], tool_call_id=tool_call["id"])
            )
        return {"messages": outputs}


def route_tools(
        state: State,
):
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge:{state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return END


graph_builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END},
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()


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
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break



# from typing import Annotated
#
# from langchain.chat_models import init_chat_model
# from typing_extensions import TypedDict
#
# from langgraph.graph import StateGraph, START
# from langgraph.graph.message import add_messages
#
#
# class State(TypedDict):
#     messages: Annotated[list, add_messages]
#
# graph_builder=StateGraph(State)