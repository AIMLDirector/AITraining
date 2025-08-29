
# rule based chatbot
# sentence matching or keyword matching chatbot
# sentiment analysis chatbot. --textblob
# intent based chatbot -- cloud based chatbot -- lex bot 
# Q&A chatbot--LLM based chatbot - chatgpt , gemini, grok



def simplebot():
    print("Hello! I am a simple chatbot. Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        else:
            print(f"Chatbot: You said '{user_input}'")
            
simplebot()

