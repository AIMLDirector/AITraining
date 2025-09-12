import re
import random


class SimpleChatbot:
    def __init__(self, name="ChatBot"):
        self.name = name
        self.responses = {
            r"hi|hello|hey": ["Hello!", "Hi there!", "Hey! How can I help?"],
            r"how are you": [
                "I'm doing great, thanks!",
                "Feeling awesome!",
                "All good!",
            ],
            r"what is your name": [
                f"My name is {self.name}.",
                f"You can call me {self.name}.",
            ],
            r"bye|goodbye": ["Bye!", "See you later!", "Goodbye!"],
        }

    def get_response(self, user_input):
        user_input = user_input.lower()
        for pattern, replies in self.responses.items():
            if re.search(pattern, user_input):
                return random.choice(replies)
        return "Sorry, I don't understand that."

    def chat(self):
        print(f"{self.name}: Hello! Type 'bye' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["bye", "goodbye", "exit"]:
                print(f"{self.name}: Goodbye!")
                break
            print(f"{self.name}: {self.get_response(user_input)}")
