import os
from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = None
model = None

@asynccontextmanager
async def load_model(app: FastAPI):
    global tokenizer, model

    token = os.getenv("HF_TOKEN")

    if not token:
        raise PermissionError("HugginFace token is not configured")

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        token=token,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    yield
