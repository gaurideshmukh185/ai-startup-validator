import json
from groq import Groq
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()

# Setup Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def generate_pitch(idea_description, module_results, final_score):
    """
    Module 9: Pitch Assist
    Generates elevator pitch, market sizes, and investor bullet points
    Depends on all previous modules
    """
    
    # Extract key information from modules
    category = module_results.get('module_1_idea_understanding', {}).get('category', 'Unknown')
    unique_value = module_results.get('module_1_idea_understanding', {}).get('unique_value', 'Unknown')
    target_user = module_results.get('module_1_idea_understanding', {}).get('target_user', 'Unknown')
    
    demand_score = module_results.get('module_2_market_demand', {}).get('demand_score', 50)
    market_size = module_results.get('module_2_market_demand', {}).get('market_size', 'Medium')
    
    sentiment_label = module_results.get('module_4_reddit_sentiment', {}).get('overall_sentiment_label', 'Neutral')
    
    revenue_score = module_results.get('module_5_revenue', {}).get('monetization_score', 50)
    
    virality_score = module_results.get('module_8_virality', {}).get('virality_score', 50)
    
    risk_level = module_results.get('module_7_risk', {}).get('risk_level', 'Medium')
    
    prompt = f"""
You are a pitch coach and startup advisor. Create a compelling pitch for this startup idea:

Idea: {idea_description}

Key Information from Analysis:
- Category: {category}
- Target User: {target_user}
- Unique Value: {unique_value}
- Market Demand Score: {demand_score}/100
- Market Size: {market_size}
- Reddit Sentiment: {sentiment_label}
- Revenue Score: {revenue_score}/100
- Virality Score: {virality_score}/100
- Risk Level: {risk_level}
- Overall Score: {final_score}/100

Return ONLY valid JSON in this exact format. Do not add any other text. Do not use markdown.

{{
    "elevator_pitch": "One sentence pitch that captures the problem, solution, and value proposition (30-40 words)",
    "tam": 50000000,
    "tam_description": "Total Addressable Market - description of total market size globally",
    "sam": 5000000,
    "sam_description": "Serviceable Addressable Market - description of market you can realistically reach",
    "som": 250000,
    "som_description": "Serviceable Obtainable Market - description of market share you can capture in 2-3 years",
    "investor_bullets": [
        "Bullet point 1 - key investment highlight",
        "Bullet point 2 - market opportunity",
        "Bullet point 3 - competitive advantage",
        "Bullet point 4 - growth potential",
        "Bullet point 5 - team or execution strength"
    ],
    "ask_amount_usd": 250000,
    "use_of_funds": "40% Product Development, 30% Marketing, 20% Operations, 10% Contingency",
    "summary": "One sentence summarizing why this is a good investment opportunity"
}}

Guidelines:
- TAM (Total Addressable Market): Total market demand (usually in millions/billions)
- SAM (Serviceable Addressable Market): Market you can reach with your business model
- SOM (Serviceable Obtainable Market): Market share you can realistically capture
- For B2C students: Keep TAM/SAM/SOM realistic (India has ~40M college students)
- Ask amount: $100K - $1M depending on complexity
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a pitch coach. Always return valid JSON only. Be realistic with market sizes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
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
        print(f"Error in generate_pitch: {e}")
        return {
            "elevator_pitch": f"{idea_description[:150]} - A promising opportunity in the {category} space.",
            "tam": 10000000,
            "tam_description": "Total Addressable Market - global market size estimate",
            "sam": 1000000,
            "sam_description": "Serviceable Addressable Market - realistic reachable market",
            "som": 100000,
            "som_description": "Serviceable Obtainable Market - achievable market share",
            "investor_bullets": [
                "Growing market with increasing demand",
                "Unique value proposition with clear differentiation",
                "Scalable business model",
                "Strong unit economics",
                "Experienced team ready to execute"
            ],
            "ask_amount_usd": 250000,
            "use_of_funds": "40% Product Development, 30% Marketing, 20% Operations, 10% Contingency",
            "summary": "A promising investment opportunity with significant growth potential.",
            "error": str(e)
        }

# Test the module
if __name__ == "__main__":
    # Sample module results
    sample_results = {
        "module_1_idea_understanding": {
            "category": "EdTech",
            "unique_value": "AI-powered notes that summarize lectures automatically",
            "target_user": "college students"
        },
        "module_2_market_demand": {"demand_score": 70, "market_size": "Large"},
        "module_4_reddit_sentiment": {"overall_sentiment_label": "Positive"},
        "module_5_revenue": {"monetization_score": 75},
        "module_8_virality": {"virality_score": 68},
        "module_7_risk": {"risk_level": "Medium"}
    }
    
    test_idea = "AI tool for college students to auto-generate notes from lectures"
    final_score = 65
    
    result = generate_pitch(test_idea, sample_results, final_score)
    print(json.dumps(result, indent=2))