import random

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


llm = ChatOllama(model="llama3")

output_parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a person whose mood keeps changing. Give a response based on your mood, which is {mood}."
    ),
    MessagesPlaceholder(variable_name="messages")
])

chain = prompt | llm | output_parser

moods: dict[int, str] = {
    1: "Angry",
    2: "Sad",
    3: "Happy",
    4: "Sarcastic",
    5: "Fearful",
}


def templatize_message_history(history: list) -> list:
    messages: list[HumanMessage | AIMessage] = []

    for _history in history:
        messages.extend([
            HumanMessage(content=_history["user"]["message"]),
            AIMessage(content=_history["system"]["message"])
        ])

    return messages


def generate_random_mood() -> int:
    return random.randrange(1, len(moods) + 1)


def get_llm_response(history: list, _user_message: str) -> dict[str, str]:
    messages: list = templatize_message_history(history)
    key: int = generate_random_mood()

    messages.append(HumanMessage(content=_user_message))

    response: str = chain.invoke(
        {"messages": messages, "mood": moods[key]}
    )

    return {
        "message": response,
        "mood": key
    }
