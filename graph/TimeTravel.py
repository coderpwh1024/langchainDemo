import os
from langchain.chat_models import init_chat_model

apiKey = ""
endpoint = ""
open_ai_version = "2024-05-01-preview"
azure_deployment = ""

llm = init_chat_model(
    "azure_openai:gpt-4.0",
    azure_deployment=azure_deployment,
    azure_endpoint=endpoint,
    api_key=apiKey,
    openai_api_version=open_ai_version,
)

from typing import Annotated

from langchain_tavily import TavilySearch
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

tool = TavilySearch(max_results=2, tavily_api_key="")
tools = [tool]
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges("chatbot", tools_condition, )
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}
events = graph.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "I'm learning LangGraph. "
                    "Could you do some research on it for me?"
                ),
            },
        ],
    },
    config,
    stream_mode="values"
)
for event in events:
    if "messages" in event:
        event["messages"][-1].pretty_print()

# events = graph.stream(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": (
#                     "Ya that's helpful. Maybe I'll "
#                     "build an autonomous agent with it!"
#                 ),
#             },
#         ],
#     },
#     config,
#     stream_mode="values"
# )
# for event in events:
#     if "messages" in event:
#         event["messages"][-1].pretty_print()
#
# to_replay = None
# for state in graph.get_state_history(config):
#     print("Num messages: ", len(state.values["messages"]), "Next: ", state.next)
#     print("-" * 80)
#     if len(state.values["messages"]) == 6:
#         to_replay = state
#
# print(to_replay.next)
# print(to_replay.config)
#
# for event in graph.stream(None, to_replay.config, stream_mode="values"):
#      if "messages" in event:
#         event["messages"][-1].pretty_print()
