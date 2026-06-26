import json
from groq import Groq
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()

# Setup Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def analyze_revenue(idea_description):
    """
    Module 5: Revenue Potential Analysis
    Analyzes monetization model, CAC, LTV, and revenue potential
    """
    
    prompt = f"""
You are a revenue analyst and financial expert. Analyze the revenue potential for this startup idea:

Idea: {idea_description}

Important definitions:
- CAC = Customer Acquisition Cost (how much money to get one customer)
- LTV = Lifetime Value (how much a customer pays over their entire relationship with the business)
- A good business has LTV > CAC (at least 3x is ideal)

Return ONLY valid JSON in this exact format. Do not add any other text. Do not use markdown.

{{
    "monetization_score": 75,
    "model_suggestion": "Freemium with premium features",
    "pricing_tiers": [
        {{"tier": "Free", "price": 0, "features": "Basic features"}},
        {{"tier": "Pro", "price": 9.99, "features": "Advanced features"}},
        {{"tier": "Enterprise", "price": 49.99, "features": "Team collaboration"}}
    ],
    "estimated_cac": 15.50,
    "estimated_ltv": 120.00,
    "ltv_cac_ratio": 7.74,
    "profitability_verdict": "Highly Profitable / Profitable / Breakeven / Unprofitable",
    "revenue_streams": ["subscription", "one-time purchase", "commission", "ads", "affiliate"],
    "summary": "One sentence explaining revenue potential"
}}

Rules for monetization_score (0-100):
- 0-20: No clear monetization, very difficult
- 21-40: Weak monetization, limited options
- 41-60: Moderate potential, needs work
- 61-80: Good potential, multiple options
- 81-100: Excellent potential, high willingness to pay

Be realistic. For B2C students, keep prices low ($5-15/month). For B2B, higher is fine ($50-500/month).
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a revenue analyst. Always return valid JSON only. Be realistic with pricing."},
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
        print(f"Error in analyze_revenue: {e}")
        return {
            "monetization_score": 50,
            "model_suggestion": "Unknown",
            "pricing_tiers": [],
            "estimated_cac": 0,
            "estimated_ltv": 0,
            "ltv_cac_ratio": 0,
            "profitability_verdict": "Unknown",
            "revenue_streams": [],
            "summary": "Unable to analyze revenue potential",
            "error": str(e)
        }

# Test the module
if __name__ == "__main__":
    test_idea = "AI tool for college students to auto-generate notes from lectures"
    result = analyze_revenue(test_idea)
    print(json.dumps(result, indent=2))