from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',

    # required but ignored
    api_key='ollama',
)

chat_completion = client.chat.completions.create(
    messages=[
        {'role': 'user', 'content': 'how to learn data engineering?'},
        {'role': "system", 'content': "you are an AI assistant and expert in data engineering field and troubleshooting.  please provide the answer with troubleshooting steps and also the  web link of the source document "},
    ],

    model='llama3.2',  # or any other model you have pulled in Ollama
    temperature=0.7,
    max_tokens=500,
)