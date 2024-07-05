import random
from typing import Iterable

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import AIMessage, AIMessageChunk, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableGenerator

from utils import markdown_to_html


llm = ChatOllama(model="llama3")


def custom_output_parser(chunks: Iterable[AIMessageChunk]) -> Iterable[str]:
    for chunk in chunks:
        yield markdown_to_html(chunk.content)


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a person whose mood keeps changing. Give a response based on your mood, which is {mood}."
    ),
    MessagesPlaceholder(variable_name="messages")
])

chain = prompt | llm | RunnableGenerator(custom_output_parser)

moods: dict[int, str] = {
    1: "Angry",
    2: "Sad",
    3: "Happy",
    4: "Sarcastic",
    5: "Fearful",
}


def templatize_message_history(history: list) -> list:
    messages: list[HumanMessage | AIMessage] = []

    for _history in reversed(history):
        messages.extend([
            HumanMessage(content=_history["message"]["user"]["message"]),
            AIMessage(content=_history["message"]["ai"]["message"])
        ])

    return messages


def generate_random_mood() -> int:
    return random.randrange(1, len(moods) + 1)


async def get_llm_response(history: list, _user_message: str) -> dict[str, str]:
    messages: list = templatize_message_history(history)
    key: int = generate_random_mood()

    messages.append(HumanMessage(content=_user_message))
    response: str = ""

    for chunk in chain.stream(
        {"messages": messages, "mood": moods[key]}
    ):
        response += chunk

    return {
        "message": response,
        "mood": key
    }
