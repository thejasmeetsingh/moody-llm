from lifespan import tokenizer, model
import random


moods: dict[int, str] = {
    1: "Angry",
    2: "Sad",
    3: "Happy",
    4: "Sarcastic",
    5: "Fearful",
}

prompt: str = "Suppose you are in {} mood, Give the response based on your mood."

def templatize_message_history(history: list) -> list:
    messages: list[dict[str, str]] = []

    for _history in history:
        messages.extend([
            {"role": "system", "content": _history["system"]["message"]},
            {"role": "user", "content": _history["user"]["message"]},
        ])

    return messages

def generate_random_mood() -> int:
    return random.randrange(1, len(moods) + 1)

def get_llm_response(history: list, _user_message: str) -> dict[str, str]:
    messages: list[dict[str, str]] = templatize_message_history(history)
    mood: str = moods[generate_random_mood()]

    messages.extend([
        {"role": "system", "content": prompt.format(mood)},
        {"role": "user", "content": _user_message}
    ])

    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=256,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.6,
        top_p=0.9,
    )

    response = outputs[0][input_ids.shape[-1]:]
    message = tokenizer.decode(response, skip_special_tokens=True)

    return {
        "message": message,
        "mood": mood
    }
