import os
from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI


class Joke(BaseModel):
    """Joke to tell user."""
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is,from 1 to 10"
    )

endpoint = ""
deployment = ""
apiKey = ""

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    openai_api_version="2024-08-01-preview",
)

query = "Tell me a joke about cats"

structured_llm =model.with_structured_output(Joke)
print(structured_llm.invoke(query))