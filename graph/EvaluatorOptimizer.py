from typing import TypedDict, Literal
from pydantic import BaseModel, Field
from IPython.core.display_functions import display
from langchain.chat_models import init_chat_model
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from pydantic import BaseModel
from IPython.display import Image, display

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



class State(TypedDict):
    joke: str
    topic: str
    feedback: str
    funny_or_not: str


class Feedback(BaseModel):
    grade: Literal["funny", "not funny"] = Field(
        description="Decide if the joke is funny or not.",
    )
    feedback: str = Field(
        description="If the joke is not funny, provide feedback on how to improve it.",
    )


evaluator = llm.with_structured_output(Feedback)


def llm_call_generator(state: State) -> Feedback:
    """LLM generates a joke"""
    if state.get("feedback"):
        msg = llm.invoke(
            f"Write a joke about {state['topic']} but take into account the feedback: {state['feedback']}"
        )
    else:
        msg = llm.invoke(f"Write a joke about {state['topic']}")
    return {"joke": msg.content}


def llm_call_evaluator(state: State):
    """LLM evaluates the joke"""
    grade = evaluator.invoke(f"Grade the joke {state['joke']}")
    return {"funny_or_not": grade.grade, "feedback": grade.feedback}


def route_joke(state: State):
    """Route back to joke generator or end based upon feedback from the evaluator"""

    if state["funny_or_not"] == "funny":
        return "Accepted"
    elif state["funny_or_not"] == "not funny":
        return "Rejected + Feedback"


optimizer_builder = StateGraph(State)

optimizer_builder.add_node("llm_call_generator", llm_call_generator)
optimizer_builder.add_node("llm_call_evaluator", llm_call_evaluator)

optimizer_builder.add_edge(START, "llm_call_generator")
optimizer_builder.add_edge("llm_call_generator", "llm_call_evaluator")
optimizer_builder.add_conditional_edges(
    "llm_call_evaluator",
    route_joke,
    {
        "Accepted": END,
        "Rejected + Feedback": "llm_call_generator",
    },
)

optimizer_workflow = optimizer_builder.compile()

# Show the workflow
display(Image(optimizer_workflow.get_graph().draw_mermaid_png()))

state = optimizer_workflow.invoke({"topic": "cats"})
print(state["joke"])
