from typing import Union, Optional

from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI


class Joke(BaseModel):
    """Joke to tell user."""
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is,from 1 to 10"
    )


class ConversationalResponse(BaseModel):
    """Respond in a conversational manner. Be kind and helpful."""
    response: str = Field(description="A conversational response to the user's query")


class FinalResponse(BaseModel):
    final_output: Union[Joke, ConversationalResponse]


endpoint = ""
deployment = ""
apiKey = ""

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    openai_api_version="2024-08-01-preview",
)

structured_llm = model.with_structured_output(FinalResponse)
print(structured_llm.invoke("Tell me a joke about cats"))
