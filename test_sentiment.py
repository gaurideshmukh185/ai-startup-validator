from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Create the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Test 3 sentences
sentences = [
    "This app is amazing! It changed my life.",
    "This app keeps crashing. I hate it so much.",
    "The app works fine. Nothing special."
]

print("SENTIMENT ANALYSIS TEST")
print("-" * 40)

for sentence in sentences:
    # Get sentiment scores
    scores = analyzer.polarity_scores(sentence)
    compound = scores['compound']
    
    # Determine sentiment
    if compound >= 0.05:
        sentiment = "POSITIVE 😊"
    elif compound <= -0.05:
        sentiment = "NEGATIVE 😠"
    else:
        sentiment = "NEUTRAL 😐"
    
    print(f"Text: {sentence}")
    print(f"Score: {compound}")
    print(f"Sentiment: {sentiment}")
    print("-" * 40)
