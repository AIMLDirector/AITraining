def learning_chatbot():

    print("Hello! I'm a learning chatbot 🤖. Type 'bye' to exit.")

    # Store known responses

    memory = {
        "hello": "Hi there! 👋",
        "how are you": "I'm doing great!",
        "bye": "Goodbye! See you next time.",
    }

    while True:

        user_input = input("You: ").lower().strip()

        if user_input in memory:

            print("Chatbot:", memory[user_input])

            if user_input == "bye":

                break

        else:

            print("Chatbot: I don’t know how to respond to that. 🤔")

            new_response = input("You can teach me! What should I reply? ")

            memory[user_input] = new_response

            print("Chatbot: Got it! I’ll remember that.")


learning_chatbot()
