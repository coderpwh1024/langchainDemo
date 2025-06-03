import os
from langchain.chat_models import init_chat_model
from tenacity import retry

apiKey = ""
endpoint = ""
open_ai_version = "2024-08-01-preview"
azure_deployment = ""

llm = init_chat_model(
    "azure_openai:gpt-4.0",
    azure_deployment=azure_deployment,
    azure_endpoint=endpoint,
    api_key=apiKey,
    openai_api_version=open_ai_version,
)

from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Query that is optimized web search.")
    justification: str = Field(None, description="Why this query is relevant to the user's request.")


structured_llm = llm.with_structured_output(SearchQuery)

output = structured_llm.invoke("How does Calcium CT score relate to high cholesterol?")


def multiply(a: int, b: int) -> int:
    return a * b


llm_with_tools = llm.bind_tools([multiply])

msg = llm_with_tools.invoke("What is 2 * 3?")

msg.tool_calls
print("msg:", msg)
print("-------------------------------------------------------------------------------------------------------")

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display


class State(TypedDict):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str


def generate_joke(state: State):
    """First LLM call to generate initial joke"""
    msg = llm.invoke(f"Tell me a joke about {state['topic']}")
    return {"joke": msg.content}


def check_punchline(state: State):
    """Gate function to check if the joke has a punchline """
    if "?" in state["joke"] or "!" in state["joke"]:
        return "Pass"
    return "Fail"


def improve_joke(state: State):
    """Second LLM call to improve the joke"""
    msg = llm.invoke(f"Make this joke funnier by  adding wordplay:{state['joke']}")
    return {"improved_joke": msg.content}


def polish_joke(state: State):
    """Third LLM call for final polish"""
    msg = llm.invoke(f"Add a surprising twist to this joke: {state['improved_joke']}")
    return {"final_joke": msg.content}


workflow = StateGraph(State)

workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)
workflow.add_node("polish_joke", polish_joke)

workflow.add_edge(START, "generate_joke")
workflow.add_conditional_edges("generate_joke", check_punchline, {"Fail": "improve_joke", "Pass": END})
workflow.add_edge("improve_joke", "polish_joke")
workflow.add_edge("polish_joke", END)

chain = workflow.compile()
display(Image(chain.get_graph().draw_mermaid_png()))

state = chain.invoke("topic", "cats")
print("Initial joke")
print(state["joke"])
print("\n--- --- ---\n")
if  "improved_joke" in state:
    print("Improvted joke:")
    print(state["improved_joke"])
    print("\n--- --- ---\n")

    print("Final joke:")
    print(state["final_joke"])

else:
    print("Joke failed quality gate - no punchline detected!")


