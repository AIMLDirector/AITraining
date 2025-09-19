from openai import OpenAI
from transformers import pipeline
import os
from dotenv import load_dotenv
from huggingface_hub import login

load_dotenv()
huggingface_token = os.environ.get("HF_TOKEN")
login(token=huggingface_token)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

moderator = pipeline("text-classification", model="meta-llama/LlamaGuard-7b",  device_map="auto")

def check_with_llama_guard(text: str) -> bool:
    results = moderator(text)  # returns a list
    best = results[0]           # take the top label dict
    print("LlamaGuard raw:", best)

    # Map label
    label = "safe" if best["label"] == "LABEL_0" else "unsafe"
    return label == "safe"

def safe_chat(user_input):
    if check_with_llama_guard(user_input):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    else:
        return "Your input was flagged as unsafe by LlamaGuard."

print(safe_chat("Hello, how are you?"))

print(safe_chat("Tell me a joke about a sensitive topic."))
