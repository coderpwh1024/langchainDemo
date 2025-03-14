import os
from typing import Optional
from pydantic import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from typing_extensions import Annotated, TypedDict

# Pydantic
# class Joke(BaseModel):
#     """Joke to tell user."""
#     setup: str = Field(description="The setup of the joke")
#     punchline: str = Field(description="The punchline of the joke")
#     rating: Optional[int] = Field(
#         default=None, description="How funny the joke is,from 1 to 10"
#     )


# TypedDict
# class Joke(TypedDict):
#     """Joke to tell user."""
#     setup: Annotated[str, ..., "The setup of the joke"]
#     punchline: Annotated[str, ..., "The punchline of the joke"]
#     rating: Annotated[Optional[int], None, "How funny the joke is,from 1 to 10"]


json_schema = {
    "title": "joke",
    "description": "Joke to tell user.",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "The setup of the joke",
        },
        "punchline": {
            "type": "string",
            "description": "The punchline to the joke",
        },
        "rating": {
            "type": "integer",
            "description": "How funny the joke is, from 1 to 10",
            "default": None,
        },
    },
    "required": ["setup", "punchline"],
}

endpoint = ""
deployment = ""
apiKey = ""

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    openai_api_version="2024-08-01-preview",
)

query = "How are you today?"

# structured_llm = model.with_structured_output(Joke)
# print(structured_llm.invoke(query))

structured_llm = model.with_structured_output(json_schema)
print(structured_llm.invoke(query))
