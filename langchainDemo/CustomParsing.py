import json
import re
from typing import List
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from pydantic.v1.schema import schema


class Person(BaseModel):
    """Information about a person."""
    name: str = Field(..., description="The name of the person")
    height_in_meters: float = Field(..., description="The height of the person in meters")


class People(BaseModel):
    """Information about a group of people."""
    people: List[Person]


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer the user query. Output your answer as JSON that",
            "matches the given schema: ```json\n{schema}\n```. "
            "Make sure to wrap the answer in ```json and ``` tags",
        ),
        ("human", "{query}")
    ]

).partial(schema=People.schema())
