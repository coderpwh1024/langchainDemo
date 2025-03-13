from langchain_core.prompts import PromptTemplate

from langchain.chains.question_answering.map_reduce_prompt import messages
from langchain.chains.summarize.map_reduce_prompt import prompt_template
from langchain_openai import AzureChatOpenAI

endpoint = " "
deployment = ""
apiKey = " "

from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    openai_api_version="2024-05-01-preview",
)

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")

response = model.invoke(prompt_template.invoke({"topic": "eat"}))
print(response.content)
