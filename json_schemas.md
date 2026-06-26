# AI Startup Validator - JSON Schemas

## Module 1: Reddit Post Fetcher
{
  "post_id": "string",
  "title": "string",
  "text": "string",
  "url": "string",
  "score": "integer",
  "num_comments": "integer",
  "created_utc": "float"
}

## Module 2: Sentiment Analyzer (VADER)
{
  "post_id": "string",
  "sentiment_score": "float",
  "sentiment_label": "string",
  "positive_score": "float",
  "negative_score": "float",
  "neutral_score": "float"
}

## Module 3: Startup Validator (Gemini)
{
  "post_id": "string",
  "verdict": "string",
  "score": "integer",
  "strengths": "string",
  "weaknesses": "string",
  "opportunity": "string"
}

## Module 4: Aggregate Report
{
  "total_posts": "integer",
  "positive_count": "integer",
  "negative_count": "integer",
  "average_sentiment": "float",
  "top_opportunities": "array",
  "recommendation": "string"
}