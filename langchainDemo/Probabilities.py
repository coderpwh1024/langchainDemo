import  getpass
import os

endpoint = ""
deployment = " "
apiKey = ""

from langchain_openai import AzureChatOpenAI

llm  = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    openai_api_version="2024-05-01-preview",

)

msg =  llm.invoke(("human","how are you today"))

msg.response_metadata["logprobs"]["content"][:5]


