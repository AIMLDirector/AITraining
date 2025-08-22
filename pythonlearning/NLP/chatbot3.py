from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

feedback_date = []

def sentiment_analysis_chatbot():
    print("Hello! I am a sentiment analysis chatbot. Type 'exit' to end the conversation.")
    print("Please provide a valuable feedback about our product or service for Sony TV.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        else:
            blob = TextBlob(user_input) # postivie  0 to 1 / neutral 0 / negative -1 to 0
            sentiment_score = blob.sentiment.polarity
            if sentiment_score > 0:
                sentiment = "positive"
                response = "That's great to hear!"
            elif sentiment_score < 0:
                sentiment = "negative"
                response = "I'm sorry to hear this feedback our customer service team will look into it."
            else:
                sentiment = "neutral"
                response = "I see, it's neutral. we will connect with you soon."
            print(f"Chatbot: {response}")
            
            feedback_date.append({
            "feedback": user_input,
            "sentiment": sentiment,
            "polarity score": "{:.2f}".format(sentiment_score)
            })
    
    if feedback_date:
        df = pd.DataFrame(feedback_date)
        df.to_csv("feedback_summary.csv", index=False)
        print("\nFeedback Summary:")
        print(df)
        
        plt.figure(figsize=(10, 5))
        sentiment_counts = df['sentiment'].value_counts()
        sentiment_counts.plot(kind='bar')
        plt.title('Sentiment Analysis Results')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.xticks(rotation=0)
        plt.show()

sentiment_analysis_chatbot()

    
    