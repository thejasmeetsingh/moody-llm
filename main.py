from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)


def get_llm_response(_user_message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a person who gives very sarcastic response"
        },
        {"role": "user", "content": _user_message}
    ]

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

    return tokenizer.decode(response, skip_special_tokens=True)


while True:
    print("1. Send a message")
    print("2. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        user_message = input("Enter your message: ")
        response = get_llm_response(user_message)
        print(response)
    elif choice == "2":
        break
