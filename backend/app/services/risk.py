import json
from groq import Groq
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()

# Setup Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def analyze_risk(idea_description):
    """
    Module 7: Risk Analysis
    Identifies top risks and provides mitigation suggestions
    """
    
    prompt = f"""
You are a risk analyst for startups. Analyze the risks for this startup idea:

Idea: {idea_description}

Return ONLY valid JSON in this exact format. Do not add any other text. Do not use markdown.

{{
    "risk_level": "Medium",
    "risk_score": 45,
    "specific_risks": [
        {{
            "risk": "High competition from established players",
            "severity": "High",
            "mitigation": "Focus on niche segment first, differentiate with unique features"
        }},
        {{
            "risk": "High customer acquisition cost",
            "severity": "Medium",
            "mitigation": "Use referral programs and organic growth strategies"
        }},
        {{
            "risk": "Technical challenges with AI accuracy",
            "severity": "Medium",
            "mitigation": "Start with MVP, iterate based on user feedback"
        }}
    ],
    "summary": "One sentence summarizing the biggest risk and how to address it"
}}

Rules:
- risk_level: Low (few risks, easy to overcome) / Medium (manageable risks) / High (significant challenges)
- risk_score: 0-100 (0 = no risk, 100 = extremely high risk)
- Include 3-5 specific risks with their severity (Low/Medium/High)
- Each risk must have a practical mitigation suggestion
- Be realistic about the startup's challenges

Common risk categories to consider:
- Market risk (competition, demand, timing)
- Technical risk (feasibility, development challenges)
- Financial risk (funding, profitability, CAC)
- Operational risk (execution, team, partnerships)
- Regulatory risk (legal, compliance)
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a risk analyst. Always return valid JSON only. Be realistic and practical with mitigations."},
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
        print(f"Error in analyze_risk: {e}")
        return {
            "risk_level": "Medium",
            "risk_score": 50,
            "specific_risks": [
                {
                    "risk": "Unable to analyze risks",
                    "severity": "Medium",
                    "mitigation": "Please try again"
                }
            ],
            "summary": "Risk analysis unavailable",
            "error": str(e)
        }

# Test the module
if __name__ == "__main__":
    test_idea = "AI tool for college students to auto-generate notes from lectures"
    result = analyze_risk(test_idea)
    print(json.dumps(result, indent=2))