import getpass
import os

from langchain.chains.question_answering.map_reduce_prompt import messages
from langchain.chains.summarize.map_reduce_prompt import prompt_template
from langchain_openai import AzureChatOpenAI
from  langchain_core.prompts import  ChatPromptTemplate
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

System_template="Translate the following from English into {language}"

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", System_template),
        ("user", "{text}"),
    ]
)

prompt  = prompt_template.invoke({"language":"Italian","text":"hi"})
prompt.to_messages()
response = model.invoke(prompt)
print(response.content)