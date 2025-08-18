while True:
    print("This is an infinite loop")
    break

while True:
    user_input = input("Enter 'exit' to stop the loop: ")
    if user_input.lower() == 'exit':
        print("Exiting the loop.")
        break
    else:
        print(f"You entered: {user_input}")

n = 2
while n < 10:
    print(n)
    n += 1
    
n = 0
while n < 20:
    print(n)
    if n == 5:
        print("Reached 5, breaking the loop.")
        break
    n += 1
        

n = 0
while n < 20:
    n += 1
    if n == 5:
        continue
    print(n)
   
    
from textblob import TextBlob
while True:
     text = input("Enter text to analyze sentiment (or 'exit' to quit): ")
     if text.lower() == 'exit':
         print("Exiting the loop.")
         break
     blob = TextBlob(text)
     print(f"Sentiment: {blob.sentiment}")
     print("sentiment.polarity:", blob.sentiment.polarity)
     
     


