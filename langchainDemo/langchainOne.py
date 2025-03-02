import getpass
import os
from asyncio import Timeout

from openai import api_key



endpoint = "https"
deployment = ""
apiKey = "";

from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    openai_api_version="2024-05-01-preview",

)

print(model.invoke("帮我推荐一下深圳旅游景点"))
