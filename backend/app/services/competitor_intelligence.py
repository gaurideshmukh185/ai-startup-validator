import json
from groq import Groq
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()

# Setup Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def analyze_competitors(idea_description):
    """
    Module 3: Competitor Intelligence
    Identifies 3-5 real competitors with funding, pricing, strengths, weaknesses
    """
    
    prompt = f"""
You are a competitive intelligence analyst. Identify real competitors for this startup idea:

Idea: {idea_description}

IMPORTANT RULES:
1. Only mention real, well-known companies that actually exist
2. If you are not sure about a fact, write "Unknown" instead of guessing
3. Do NOT invent companies or funding amounts

Return ONLY valid JSON in this exact format. Do not add any other text. Do not use markdown.

{{
    "competitors": [
        {{
            "name": "Company name",
            "funding": "Total funding in USD (write Unknown if unsure)",
            "pricing": "Pricing model (e.g., Free, Freemium, $X/month, Enterprise)",
            "strengths": "2-3 key strengths",
            "weaknesses": "2-3 key weaknesses"
        }}
    ],
    "market_saturation": "Low / Medium / High",
    "barrier_to_entry": "Low / Medium / High",
    "differentiation_opportunity": "One sentence explaining how this idea can stand out"
}}

Return 3-5 competitors. If fewer exist, return what's available.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a competitive intelligence analyst. Always return valid JSON only. Never invent companies or facts. Write 'Unknown' if unsure."},
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
        print(f"Error in analyze_competitors: {e}")
        return {
            "competitors": [],
            "market_saturation": "Unknown",
            "barrier_to_entry": "Unknown",
            "differentiation_opportunity": "Unable to analyze",
            "error": str(e)
        }

# Test the module
if __name__ == "__main__":
    test_idea = "AI tool for college students to auto-generate notes from lectures"
    result = analyze_competitors(test_idea)
    print(json.dumps(result, indent=2))