import transformers

from transformers import pipeline

chatbot = pipeline("text-generation", model="gpt2")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "exit", "quit"]:
        print("Bot: Goodbye!")
        break
    response = chatbot(user_input, max_length=50, num_return_sequences=1,truncation=True)
    print("Bot:", response[0]['generated_text'])
    
