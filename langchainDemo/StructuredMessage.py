from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate

examples = [

    HumanMessage("Tell me a joke about planes", name="example_user"),

    AIMessage("", name="example_assistant", tool_calls=[
        {
            "name": "joke",
            "args": {
                "setup": "Why don't planes ever get tired?",
                "punchline": "Because they have rest wings!",
                "rating": 2,
            },
            "id": "1",
        }

    ], ),

    ToolMessage("", tool_call_id="1"),

    HumanMessage("Tell me a joke about planes", name="example_user"),

    AIMessage(
        "",
        name="example_assistant",
        tool_calls=[
            {
                "name": "joke",
                "args": {
                    "setup": "Cargo",
                    "punchline": "Cargo 'vroom vroom', but planes go 'zoom zoom'!",
                    "rating": 10,
                },
                "id": "2"
            }
        ],
    ),

    ToolMessage("", tool_call_id="2"),

    HumanMessage("Now about caterpillars", name="example_user"),
    AIMessage("", name="example_assistant", tool_calls=[
        {
            "name": "joke",
            "args": {
                "setup": "Caterpillar",
                "punchline": "Caterpillar really slow, but watch me turn into a butterfly and steal the show!",
                "rating": 5,
            },
            "id": "3"
        }

    ], ),

    ToolMessage("", tool_call_id="3"),
]

system = """You are a hilarious comedian. Your specialty is knock-knock jokes. \
Return a joke which has the setup (the response to "Who's there?") \
and the final punchline (the response to "<setup> who?")."""

prompt = ChatPromptTemplate.from_messages([("system", system), ("placeholder", "{examples}"), ("human", "{input}")])

few_shot_structured_llm = prompt

few_shot_structured_llm.invoke({"input": "crocodiles", "examples": examples})

endpoint = " "
deployment = ""
apiKey = ""

from langchain_openai import AzureChatOpenAI

model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=apiKey,
    openai_api_version="2024-05-01-preview",
)

result: str = model.invoke(few_shot_structured_llm.invoke({"input": "crocodiles", "examples": examples}))
print("结果为:\n")
print(result)
