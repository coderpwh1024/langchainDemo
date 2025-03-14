from typing_extensions import Annotated, TypedDict


class add(TypedDict):
    """Add two integers."""
    a: Annotated[int, "First integer"]
    b: Annotated[int, "Second integer"]


class multiply(TypedDict):
    """Multiply two integers."""
    a: Annotated[int, "First integer"]
    b: Annotated[int, "Second integer"]


tools = [add, multiply]

import os
from langchain_openai import AzureChatOpenAI

endpoint = ""
deployment = ""
apiKey = ""

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    openai_api_version="2024-05-01-preview",
)

llm_with_tools = model.bind_tools(tools)

query = "What is 3*12 ?"

print(llm_with_tools.invoke(query))
