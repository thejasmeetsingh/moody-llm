import random

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


llm = ChatOllama(model="llama3")

# Set base chat prompt for LLM
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a person whose mood keeps changing. Give a response based on your mood, which is {mood}."
    ),
    MessagesPlaceholder(variable_name="messages")
])

chain = prompt | llm | StrOutputParser()

# Pre-defined moods
moods: dict[int, str] = {
    1: "Angry",
    2: "Sad",
    3: "Happy",
    4: "Sarcastic",
    5: "Fearful",
}


def templatize_message_history(history: list) -> list:
    """
    Given chat message history in JSON or dict. Transform them to langchain message objects.
    """

    messages: list[HumanMessage | AIMessage] = []

    for _history in reversed(history):
        messages.extend([
            HumanMessage(content=_history["message"]["user"]["content"]),
            AIMessage(content=_history["message"]["ai"]["content"])
        ])

    return messages


def generate_random_mood() -> int:
    """
    Generate random number which helps to feed a different mood (probably) to the LLM
    """

    return random.randrange(1, len(moods) + 1)


async def get_llm_response(history: list, _user_message: str) -> dict[str, str]:
    """
    Generate LLM response based on chat message history and user current message.
    """

    messages: list = templatize_message_history(history)
    key: int = generate_random_mood()

    messages.append(HumanMessage(content=_user_message))

    response: str = chain.invoke(
        {"messages": messages, "mood": moods[key]}
    )

    return {
        "content": response,
        "mood": key
    }
