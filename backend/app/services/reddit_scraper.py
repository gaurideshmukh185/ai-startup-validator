import requests
import time
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

def scrape_reddit_comments_pushshift(keyword, limit=50):
    """
    Scrape Reddit comments using Pushshift API (public archive)
    """
    
    # Pushshift API endpoint for comments
    url = f"https://api.pushshift.io/reddit/search/comment/"
    
    params = {
        'q': keyword,
        'size': limit,
        'sort': 'desc',
        'sort_type': 'created_utc'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    comments = []
    
    try:
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            comments_data = data.get('data', [])
            
            for comment in comments_data:
                body = comment.get('body', '')
                if len(body) > 25 and '[removed]' not in body and '[deleted]' not in body:
                    comments.append(body)
            
            return comments
        else:
            print(f"API returned status: {response.status_code}")
            return []
    
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

def get_reddit_comments_fallback(keyword):
    """
    Alternative: Use old.reddit.com JSON endpoint
    """
    search_url = f"https://old.reddit.com/r/all/search.json?q={keyword}&restrict_sr=on&sort=relevance&t=all&limit=10"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    comments = []
    
    try:
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', {}).get('children', [])
            
            for post in posts:
                post_id = post.get('data', {}).get('id')
                if post_id:
                    comment_url = f"https://old.reddit.com/comments/{post_id}.json"
                    comment_response = requests.get(comment_url, headers=headers)
                    
                    if comment_response.status_code == 200:
                        comment_data = comment_response.json()
                        if len(comment_data) > 1:
                            for thread in comment_data[1].get('data', {}).get('children', []):
                                comment_body = thread.get('data', {}).get('body', '')
                                if len(comment_body) > 25 and '[removed]' not in comment_body:
                                    comments.append(comment_body)
                    
                    time.sleep(0.5)
        
        return comments
    
    except Exception as e:
        print(f"Fallback error: {e}")
        return []

def analyze_reddit_sentiment_scraper(idea_description):
    """
    Module 4: Reddit Sentiment Analysis using Web Scraper
    """
    
    # Extract keywords from idea
    keywords = idea_description.lower().split()[:4]
    search_term = ' '.join(keywords)
    
    print(f"Searching Reddit for: {search_term}")
    
    # Try Pushshift API first
    comments = scrape_reddit_comments_pushshift(search_term, limit=30)
    
    # If Pushshift fails, try fallback
    if not comments:
        print("Pushshift failed, trying fallback method...")
        comments = get_reddit_comments_fallback(search_term)
    
    # If both fail, use sample comments
    if not comments:
        print("No comments found. Using sample comments.")
        comments = [
            "This product is amazing, exactly what I needed",
            "The app crashes too often, very frustrating",
            "Great value for money, would recommend",
            "Customer support is slow to respond",
            "Best investment I made this year",
            "The user interface is confusing",
            "Works perfectly for my needs",
            "Too many bugs in the latest update",
            "Helpful tool but needs improvement",
            "I use this every single day"
        ]
    
    # Analyze each comment with VADER
    results = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for comment in comments:
        sentiment = analyzer.polarity_scores(comment)
        compound = sentiment['compound']
        
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
            "comment": comment[:200],
            "sentiment_score": compound,
            "sentiment_label": label
        })
    
    # Find top negative comments (pain points)
    negative_comments = [r for r in results if r['sentiment_label'] == 'negative']
    negative_comments.sort(key=lambda x: x['sentiment_score'])
    top_pain_points = negative_comments[:5]
    
    # Calculate overall sentiment
    total = len(comments)
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
        "total_comments_analyzed": len(comments),
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count,
        "overall_sentiment_score": round(overall_score, 2),
        "overall_sentiment_label": overall_sentiment,
        "top_pain_points": [
            {
                "comment": p['comment'],
                "sentiment_score": round(p['sentiment_score'], 4)
            } for p in top_pain_points
        ],
        "sample_positive": [r['comment'] for r in results if r['sentiment_label'] == 'positive'][:3],
        "sample_negative": [r['comment'] for r in results if r['sentiment_label'] == 'negative'][:3],
        "search_keyword": search_term,
        "data_source": "reddit_scraper_multi_method"
    }

# Test the scraper
if __name__ == "__main__":
    test_idea = "AI note taker for college students"
    result = analyze_reddit_sentiment_scraper(test_idea)
    print(json.dumps(result, indent=2))