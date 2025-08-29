import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

client = openai.Client(api_key=api_key)

# Generate text using the API
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Once upon a time"}
    ],
    
    max_tokens=100
)

print(response.choices[0].message.content)
