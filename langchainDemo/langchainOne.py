import getpass
import os
from langchain_openai import AzureChatOpenAI

azure_openAi_api_key = os.getenv("azure_openAi_api_key",
                                 "")
azure_openAi_endpoint = os.getenv("azure_openAi_endpoint",
                                  "")
azure_openAi_deployment_name = os.getenv("azure_openAi_deployment_name", "gpt-40")
azure_openAi_version = os.getenv("azure_openAi_version", "2024-05-01-preview")

client = AzureChatOpenAI(
    azure_key=azure_openAi_api_key,
    azure_endpoint=azure_openAi_endpoint,
    openai_api_version=azure_openAi_version,
)

from typing import Optional
from pydantic import BaseModel, Field


class Joke(BaseModel):
    """Joke to tell user."""
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")
    rating: Optional[int] = Field(default=None, description="How funny the joke is,from 1 to 10")


structured_llm = client.with_structured_output(Joke)
structured_llm.invoke("Tell me a joke about a duck.")
