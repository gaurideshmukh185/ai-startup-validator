import json
from groq import Groq
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()

# Setup Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def analyze_virality(idea_description):
    """
    Module 8: Virality Score
    Analyzes how likely people are to share and talk about this product
    """
    
    prompt = f"""
You are a growth marketing expert. Analyze the virality potential for this startup idea:

Idea: {idea_description}

Virality = how likely users are to share and talk about this product on social media, with friends, or through word-of-mouth.

Return ONLY valid JSON in this exact format. Do not add any other text. Do not use markdown.

{{
    "virality_score": 68,
    "virality_drivers": [
        "Driver 1 - what makes people want to share",
        "Driver 2 - what makes people want to share"
    ],
    "virality_limiters": [
        "Limiter 1 - what prevents sharing",
        "Limiter 2 - what prevents sharing"
    ],
    "k_factor_estimate": 1.2,
    "organic_growth_potential": "Good / Average / Poor",
    "recommended_actions": [
        "Action 1 to increase virality",
        "Action 2 to increase virality"
    ],
    "summary": "One sentence explaining the virality potential"
}}

Rules for virality_score (0-100):
- 0-20: Not shareable, private product, no social features
- 21-40: Low virality, limited sharing incentives
- 41-60: Average virality, some sharing but not explosive
- 61-80: Good virality, clear sharing mechanisms
- 81-100: Highly viral, strong incentives to share

K-factor estimate: Number of new users each existing user brings in.
- K < 1: Not viral (needs paid acquisition)
- K = 1: Stable viral growth
- K > 1: Exponential viral growth
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a growth marketing expert. Always return valid JSON only. Be realistic about virality."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Clean markdown if present
        if result_text.startswith('```json'):
            result_text = result_text[7:]
        if result_text.startswith('```'):
            result_text = result_text[3:]
        if result_text.endswith('```'):
            result_text = result_text[:-3]
        
        result = json.loads(result_text)
        return result
    
    except Exception as e:
        print(f"Error in analyze_virality: {e}")
        return {
            "virality_score": 50,
            "virality_drivers": [],
            "virality_limiters": [],
            "k_factor_estimate": 1.0,
            "organic_growth_potential": "Average",
            "recommended_actions": [],
            "summary": "Unable to analyze virality potential",
            "error": str(e)
        }

# Test the module
if __name__ == "__main__":
    test_idea = "AI tool for college students to auto-generate notes from lectures"
    result = analyze_virality(test_idea)
    print(json.dumps(result, indent=2))