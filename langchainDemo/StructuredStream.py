from typing_extensions import Annotated, TypedDict
from typing import Optional
from langchain_openai import AzureChatOpenAI


class Joke(TypedDict):
    setup: Annotated[str, ..., "The setup of the joke"]
    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is,from 1 to 10"]


endpoint = ""
deployment = ""
apiKey = ""

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    openai_api_version="2024-08-01-preview",
)

structured_llm = model.with_structured_output(Joke)

for chunk in structured_llm.stream("Tell me a joke about a dog"):
    print(chunk)
