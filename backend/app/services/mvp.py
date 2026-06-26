import json
from groq import Groq
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()

# Setup Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def analyze_mvp(idea_description):
    """
    Module 6: MVP Generator
    Recommends minimum features, tech stack, timeline, and cost for MVP launch
    """
    
    prompt = f"""
You are a product manager and technical advisor. Define the Minimum Viable Product (MVP) for this startup idea:

Idea: {idea_description}

MVP = the simplest version that can be launched to test if people want it.

Return ONLY valid JSON in this exact format. Do not add any other text. Do not use markdown.

{{
    "core_features": [
        "Feature 1 - brief description",
        "Feature 2 - brief description",
        "Feature 3 - brief description"
    ],
    "tech_stack_suggestion": "e.g., React Native, Firebase, Gemini API",
    "timeline_weeks": 6,
    "cost_estimate_usd": 5000,
    "team_size_suggestion": 3,
    "development_stages": [
        {{"stage": "Week 1-2", "focus": "Core setup and authentication"}},
        {{"stage": "Week 3-4", "focus": "Main feature development"}},
        {{"stage": "Week 5-6", "focus": "Testing and launch preparation"}}
    ],
    "success_metrics": [
        "Metric 1 to measure success",
        "Metric 2 to measure success"
    ],
    "summary": "One sentence explaining the MVP approach"
}}

Rules:
- Core features: 3-5 essential features only (no nice-to-have)
- Timeline: 4-12 weeks depending on complexity
- Cost estimate: Realistic for the scope (B2C: lower, B2B: higher)
- Team size: 1-5 people
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a product manager. Always return valid JSON only. Be realistic with timelines and costs."},
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
        print(f"Error in analyze_mvp: {e}")
        return {
            "core_features": [],
            "tech_stack_suggestion": "Unknown",
            "timeline_weeks": 8,
            "cost_estimate_usd": 10000,
            "team_size_suggestion": 3,
            "development_stages": [],
            "success_metrics": [],
            "summary": "Unable to analyze MVP requirements",
            "error": str(e)
        }

# Test the module
if __name__ == "__main__":
    test_idea = "AI tool for college students to auto-generate notes from lectures"
    result = analyze_mvp(test_idea)
    print(json.dumps(result, indent=2))