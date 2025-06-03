import os
from langchain.chat_models import init_chat_model

from graph.TimeTravel import llm_with_tools

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
