import time
import json
import os
import dotenv
import google.generativeai as genai
from pytrends.request import TrendReq

# Load API key
dotenv.load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Use working model
model = genai.GenerativeModel("models/gemini-2.5-flash")


def get_trends(keyword):
    """
    Fetch Google Trends data for a keyword
    """
    time.sleep(2)  # Add delay to avoid rate limiting
    try:
        # Connect to Google Trends
        pytrends = TrendReq(hl='en-US', tz=330)
        
        # Build payload
        pytrends.build_payload([keyword], timeframe='today 5-y')
        
        # Get interest over time
        data = pytrends.interest_over_time()
        
        if data.empty:
            return None
        
        # Get the latest values
        latest_values = data[keyword].tail(12).tolist()
        average_interest = sum(latest_values) / len(latest_values)
        
        # Determine trend direction
        recent = data[keyword].tail(6).mean()
        older = data[keyword].tail(12).head(6).mean()
        
        if recent > older:
            trend_direction = "rising"
        elif recent < older:
            trend_direction = "falling"
        else:
            trend_direction = "stable"
        
        # Calculate demand score (0-100)
        if trend_direction == "rising":
            demand_score = min(100, int(average_interest + 20))
        elif trend_direction == "falling":
            demand_score = max(0, int(average_interest - 20))
        else:
            demand_score = int(average_interest)
        
        return {
            "demand_score": demand_score,
            "trend_direction": trend_direction,
            "average_interest": round(average_interest, 2),
            "recent_values": latest_values[-6:]
        }
        
    except Exception as e:
        print(f"Error fetching trends: {e}")
        return None


def analyze_market_demand(idea_keyword):
    """
    Module 2: Market Demand Analysis
    Takes a keyword and returns structured market demand analysis as JSON
    """
    
    # First get trends data
    trends_data = get_trends(idea_keyword)
    
    if not trends_data:
        return {
            "demand_score": 50,
            "trend_direction": "unknown",
            "market_size": "unknown",
            "growth_potential": "unknown",
            "recommendation": "Data temporarily unavailable. Please try again later.",
            "target_audience": "unknown",
            "note": "Google Trends data unavailable"
        }
    
    # Add small delay to avoid being blocked
    time.sleep(1)
    
    # Prompt for Gemini analysis
    prompt = f"""
You are a startup market analyst. Analyze this market demand data for a startup idea:

Keyword: {idea_keyword}
Demand Score (0-100): {trends_data['demand_score']}
Trend Direction: {trends_data['trend_direction']}
Average Interest: {trends_data['average_interest']}

Return ONLY valid JSON in this exact format:
{{
  "demand_score": {trends_data['demand_score']},
  "trend_direction": "{trends_data['trend_direction']}",
  "market_size": "small/medium/large",
  "growth_potential": "low/medium/high",
  "recommendation": "short explanation of whether this market is worth entering",
  "target_audience": "who is searching for this"
}}
"""
    
    # Call Gemini
    response = model.generate_content(prompt)
    
    # Clean and parse JSON response
    try:
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        
        result = json.loads(clean_text)
        return result
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw response: {response.text}")
        return {
            "demand_score": trends_data['demand_score'],
            "trend_direction": trends_data['trend_direction'],
            "market_size": "unknown",
            "growth_potential": "unknown",
            "recommendation": "Analysis temporarily unavailable",
            "target_audience": "unknown"
        }


# Test the function
if __name__ == "__main__":
    test_keywords = ["note taking app", "food delivery", "invoicing software"]
    
    print("=" * 60)
    print("MODULE 2: MARKET DEMAND ANALYSIS")
    print("=" * 60)
    
    for keyword in test_keywords:
        print(f"\n📊 Keyword: {keyword}")
        print("-" * 40)
        
        result = analyze_market_demand(keyword)
        
        if result:
            print(f"📈 Demand Score: {result.get('demand_score')}/100")
            print(f"📉 Trend Direction: {result.get('trend_direction')}")
            print(f"🏪 Market Size: {result.get('market_size')}")
            print(f"🚀 Growth Potential: {result.get('growth_potential')}")
            print(f"💡 Recommendation: {result.get('recommendation')}")
            print(f"👥 Target Audience: {result.get('target_audience')}")
        else:
            print("❌ Failed to analyze market demand")
        
        print("\n" + "=" * 60)
        time.sleep(2)  # Delay between requests to avoid blocking