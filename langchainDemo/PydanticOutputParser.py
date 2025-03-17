from typing import List
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field



class Person(BaseModel):
    name: str = Field(description="The name of the person")
    height_in_meters: float = Field(..., description="The height of the person in meters"
                                    )


class People(BaseModel):
    """Identifying information about all people in a text."""
    people: List[Person]


parser = PydanticOutputParser(pydantic_object=People)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user query. Wrap the output in `json` tags\n{format_instructions}"
        ),
        ("human", "{query}")
    ]
).partial(format_instructions=parser.get_format_instructions())

query = "Anna is 23 years old and she is 6 feet tall"
print(prompt.invoke({"query": query}).to_string())
