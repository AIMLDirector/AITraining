import os
from dotenv import load_dotenv
import openai


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

client = openai.Client(api_key=api_key)

response = client.responses.create(
    model="gpt-3.5-turbo",
    input=[
        {"role": "user", "content": "Hello! How can I use the OpenAI API in Python?"}
    ]   
)

print(response.output[0].content)
