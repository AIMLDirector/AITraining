from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
# Create chatbot
bot = ChatBot("Assistant")

# Train with English data
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english")

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "exit", "quit"]:
        print("Bot: Goodbye!")
        break
    response = bot.get_response(user_input)
    print("Bot:", response)
