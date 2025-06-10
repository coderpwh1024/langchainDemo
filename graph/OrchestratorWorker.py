# 协调器
import os
from typing import TypedDict

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.constants import Send
from typing import Annotated, List
import operator

from pydantic import BaseModel, Field

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


class Section(BaseModel):
    name: str = Field(
        description="Name for this section of the report.",
    )
    description: str = Field(
        description="Brief overview of the main topics and concepts to be covered in this section.",
    )


class Sections(BaseModel):
    sections: List[Section] = Field(
        description="The sections of the book",
    )


planner = llm.with_structured_output(Sections)


class State(TypedDict):
    topic: str
    sections: list[Section]
    completed_sections: Annotated[
        list, operator.add
    ]
    final_report: str


class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[
        list, operator.add
    ]


def orchestrator(state: State):
    """Orchestrator that generates a plan for the report"""
    report_sections = planner.invoke([
        SystemMessage(content="Generate a plan for the report."),
        HumanMessage(content=f"Here is the report topic: {state['topic']}")
    ])
    return {"sections": report_sections.sections}


def llm_call(state: WorkerState):
    """Worker writes a section of the report"""
    section = llm.invoke([
        SystemMessage(
            content="Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."),
        HumanMessage(
            content=f"Here is the section name: {state['section'].name} and description: {state['section'].description}"
        ),
    ])

    return {"completed_sections": [section.content]}
