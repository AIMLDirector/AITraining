import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon if you haven't already
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    nltk.download('vader_lexicon')

# Initialize the VADER sentiment intensity analyzer
analyzer = SentimentIntensityAnalyzer()

# Define some example texts
texts = [
    "This product is absolutely amazing! I love it.",
    "The service was terrible and I am very disappointed.",
    "The movie was okay, nothing special.",
    "I'm not happy with the results.",
    "What a fantastic experience!"
]

# Analyze the sentiment of each text
for text in texts:
    scores = analyzer.polarity_scores(text)
    print(f"Text: '{text}'")
    print(f"Sentiment Scores: {scores}")
    
    # Determine the overall sentiment based on the compound score
    if scores['compound'] >= 0.05:
        sentiment = "Positive"
    elif scores['compound'] <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    print(f"Overall Sentiment: {sentiment}\n")