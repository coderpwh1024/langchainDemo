import getpass
import os

from langchain.chains.question_answering.map_reduce_prompt import messages
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

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage("这里是系统提示词"),
    HumanMessage("这里是用户输入")
]

print(model.invoke(messages))
print(model.invoke("Hello"))
print(model.invoke([{"role": "user", "content": "Hello"}]))
print(model.invoke([HumanMessage("Hello")]))

print("----------------------------------------------------------------------------------------------")

for token in model.stream(messages):
    print(token.content, end="|")
