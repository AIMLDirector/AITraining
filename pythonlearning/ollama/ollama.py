from openai import OpenAI

# Configure client to point to Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1", # Default Ollama API endpoint
    api_key="ollama", # Can be any string, not strictly required for local
)

# Use the chat completions API similar to OpenAI
response = client.chat.completions.create(
    model="llama3", # Or any other model you have pulled in Ollama
    messages=[
        {"role": "user", "content": "Explain the concept of quantum entanglement."}
    ]
)

print(response.choices[0].message.content)