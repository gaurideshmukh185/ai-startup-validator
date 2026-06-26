import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import random

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Mock Reddit comments (will replace with real Reddit API later)
MOCK_COMMENTS = {
    "AI note-taker for students": [
        "This app saved my semester! I actually understand the lectures now",
        "Keeps crashing during important lectures, very frustrating",
        "The transcription is okay but sometimes misses key points",
        "Best purchase ever, worth every rupee",
        "Free version is useless, need to pay for basic features",
        "Voice recognition doesn't work well with Indian accents",
        "My grades improved because of this app",
        "Customer support never responds to emails",
        "The AI summaries are surprisingly accurate",
        "Too expensive for students on a budget"
    ],
    "Food delivery for hostels": [
        "Finally hot food delivered to my room at 2 AM",
        "Delivery takes 1 hour+ every single time",
        "Drivers keep calling asking for directions",
        "Love the late night options",
        "Too many extra fees, ends up being expensive",
        "App crashes when applying coupon codes",
        "Best thing that happened to hostel life",
        "Missing items in my order twice this week",
        "Customer care resolved my issue quickly",
        "Why is the minimum order so high?"
    ],
    "Freelancer invoice app": [
        "Created my first professional invoice in 2 minutes",
        "Payment tracking feature is buggy",
        "Finally an app that understands freelancers",
        "Export to PDF sometimes breaks formatting",
        "The recurring invoice feature saved me hours",
        "Mobile app is very slow to load",
        "Best invoicing tool I've used so far",
        "Wish there were more payment gateway options",
        "Free tier is very generous",
        "Reports feature needs more customization"
    ]
}

def get_mock_comments(startup_idea):
    """
    Returns mock comments based on startup idea
    Will be replaced with real Reddit API later
    """
    # Find matching mock data or use default
    for key in MOCK_COMMENTS:
        if key.lower() in startup_idea.lower():
            return MOCK_COMMENTS[key]
    
    # Default mock comments if no match found
    return [
        "This is a great product, highly recommend",
        "Had some issues but support helped quickly",
        "Not worth the money honestly",
        "Works as expected, no complaints",
        "Could be better but it's okay"
    ]

def analyze_reddit_sentiment(idea_description):
    """
    Module 4: Reddit Sentiment Analysis
    Analyzes Reddit comments to gauge sentiment about the startup idea
    """
    
    try:
        # Get comments (mock for now, will be real Reddit later)
        comments = get_mock_comments(idea_description)
        
        # Filter out short comments (less than 25 characters)
        filtered_comments = [c for c in comments if len(c) >= 25]
        
        # Analyze each comment with VADER
        results = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for comment in filtered_comments:
            sentiment = analyzer.polarity_scores(comment)
            compound = sentiment['compound']
            
            # Classify sentiment
            if compound >= 0.05:
                label = "positive"
                positive_count += 1
            elif compound <= -0.05:
                label = "negative"
                negative_count += 1
            else:
                label = "neutral"
                neutral_count += 1
            
            results.append({
                "comment": comment,
                "sentiment_score": compound,
                "sentiment_label": label
            })
        
        # Find top 5 negative comments (pain points)
        negative_comments = [r for r in results if r['sentiment_label'] == 'negative']
        negative_comments.sort(key=lambda x: x['sentiment_score'])
        top_pain_points = negative_comments[:5]
        
        # Calculate overall sentiment
        total = len(filtered_comments)
        overall_score = (positive_count - negative_count) / total if total > 0 else 0
        
        if overall_score >= 0.2:
            overall_sentiment = "Very Positive"
        elif overall_score >= 0.05:
            overall_sentiment = "Positive"
        elif overall_score >= -0.05:
            overall_sentiment = "Neutral"
        elif overall_score >= -0.2:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Very Negative"
        
        return {
            "total_comments_analyzed": len(filtered_comments),
            "positive_count": positive_count,
            "negative_count": negative_count,
            "neutral_count": neutral_count,
            "overall_sentiment_score": round(overall_score, 2),
            "overall_sentiment_label": overall_sentiment,
            "top_pain_points": [
                {
                    "comment": p['comment'],
                    "sentiment_score": p['sentiment_score']
                } for p in top_pain_points
            ],
            "sample_positive": [r['comment'] for r in results if r['sentiment_label'] == 'positive'][:3],
            "data_source": "mock_data_will_replace_with_reddit_api"
        }
    
    except Exception as e:
        print(f"Error in analyze_reddit_sentiment: {e}")
        return {
            "total_comments_analyzed": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "overall_sentiment_score": 0,
            "overall_sentiment_label": "Unknown",
            "top_pain_points": [],
            "sample_positive": [],
            "error": str(e)
        }

# Test the module
if __name__ == "__main__":
    test_ideas = [
        "AI note-taker for students",
        "Food delivery for hostels",
        "Freelancer invoice app"
    ]
    
    for idea in test_ideas:
        print(f"\n{'='*50}")
        print(f"Startup Idea: {idea}")
        print('='*50)
        result = analyze_reddit_sentiment(idea)
        print(json.dumps(result, indent=2))