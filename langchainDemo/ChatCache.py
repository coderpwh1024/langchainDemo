import  os
from getpass import  getpass

from langchain.globals import set_llm_cache
from langchain_openai import AzureChatOpenAI

endpoint = ""
deployment = ""
apiKey = ""

from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    openai_api_version="2024-05-01-preview",

)


from langchain_core.caches import  InMemoryCache

set_llm_cache( InMemoryCache())
print(model.invoke("Tell me a joke"))
