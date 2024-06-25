from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import random

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

moods = {
    1: "Angry",
    2: "Sad",
    3: "Happy",
    4: "Sarcastic",
    5: "Anxious",
    6: "Fearful",
    7: "Disgusted",
    8: "Excited",
    9: "Bored",
    10: "Lonely",
    11: "Listless"
}

messages = [{
    "role": "system",
    "content": "You are a person who gives response based on your mood, And right now your mood is {}. You will also tell your mood to the user and how you are feeling"
}]


def get_llm_response(_user_message: str) -> str:
    mood = moods[random.randrange(1, len(moods) + 1)]
    messages[0]["content"].format(mood)

    messages.append({"role": "user", "content": _user_message})

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

    return tokenizer.decode(response, skip_special_tokens=True), mood
