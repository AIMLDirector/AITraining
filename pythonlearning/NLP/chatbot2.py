def simplechatbot1():
    print("Hello! I am a simple chatbot. How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! Have a great day!")
            break
        elif "hello" in user_input.lower():
            print("Chatbot: Hello! How can I assist you?")
        elif "how are you" in user_input.lower():
            print("Chatbot: I'm just a program, but thanks for asking!")
        elif "name" in user_input.lower():
            print("Chatbot: I am a simple chatbot created to assist you.")
        else:
            print("Chatbot: I'm not sure how to respond to that. Can you ask something else?")
            
simplechatbot1()