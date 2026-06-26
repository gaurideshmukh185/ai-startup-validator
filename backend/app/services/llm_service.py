import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

# Configure Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def analyze_idea(idea_description):
    """
    Module 1: Idea Understanding Engine
    Takes a startup idea and returns JSON with category, business model, target user, etc.
    """
    
    prompt = f"""
You are a startup expert. Analyze the following startup idea:

Idea: {idea_description}

Return ONLY valid JSON in this exact format. Do not add any other text outside the JSON.
Do not use markdown. Do not explain. Only return the JSON.

{{
    "category": "one word category (e.g., EdTech, FoodTech, FinTech, SaaS, Marketplace)",
    "business_model": "how it makes money (e.g., subscription, freemium, commission, advertising)",
    "target_user": "who will use this (e.g., college students, hostel residents, freelancers)",
    "problem_solved": "what problem does this solve in one sentence",
    "unique_value": "what makes it different from existing solutions",
    "verdict": "Strong Opportunity / Promising / Needs Work / Weak"
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a startup expert. Always return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Clean the response (remove markdown if present)
        if result_text.startswith('```json'):
            result_text = result_text[7:]
        if result_text.startswith('```'):
            result_text = result_text[3:]
        if result_text.endswith('```'):
            result_text = result_text[:-3]
        
        # Parse JSON
        result = json.loads(result_text.strip())
        return result
    
    except Exception as e:
        print(f"Error in analyze_idea: {e}")
        return {
            "category": "Unknown",
            "business_model": "Unknown",
            "target_user": "Unknown",
            "problem_solved": "Unable to analyze",
            "unique_value": "Unable to analyze",
            "verdict": "Needs Work",
            "error": str(e)
        }


def run_all_modules(idea_description):
    """
    Run all 9 modules and return complete JSON with final score
    """
    from market_demand import analyze_market_demand
    from competitor_intelligence import analyze_competitors
    from reddit_scraper_ddg import analyze_reddit_sentiment_scraper
    from revenue import analyze_revenue
    from mvp import analyze_mvp
    from risk import analyze_risk
    from virality import analyze_virality
    from pitch_assist import generate_pitch
    from scoring_service import calculate_final_score
    
    results = {}
    
    print("="*50)
    print(f"Analyzing: {idea_description}")
    print("="*50)
    
    # Module 1
    print("Running Module 1: Idea Understanding...")
    results['module_1_idea_understanding'] = analyze_idea(idea_description)
    print("  ✅ Module 1 complete")
    
    # Module 2
    print("Running Module 2: Market Demand...")
    results['module_2_market_demand'] = analyze_market_demand(idea_description)
    print("  ✅ Module 2 complete")
    
    # Module 3
    print("Running Module 3: Competitor Intelligence...")
    results['module_3_competitor_intel'] = analyze_competitors(idea_description)
    print("  ✅ Module 3 complete")
    
    # Module 4
    print("Running Module 4: Reddit Sentiment...")
    results['module_4_reddit_sentiment'] = analyze_reddit_sentiment_scraper(idea_description)
    print("  ✅ Module 4 complete")
    
    # Module 5
    print("Running Module 5: Revenue Potential...")
    results['module_5_revenue'] = analyze_revenue(idea_description)
    print("  ✅ Module 5 complete")
    
    # Module 6
    print("Running Module 6: MVP Generator...")
    results['module_6_mvp'] = analyze_mvp(idea_description)
    print("  ✅ Module 6 complete")
    
    # Module 7
    print("Running Module 7: Risk Analysis...")
    results['module_7_risk'] = analyze_risk(idea_description)
    print("  ✅ Module 7 complete")
    
    # Module 8
    print("Running Module 8: Virality Score...")
    results['module_8_virality'] = analyze_virality(idea_description)
    print("  ✅ Module 8 complete")
    
    # Calculate final score
    print("Calculating Final Score...")
    scoring_result = calculate_final_score(results)
    results['final_score'] = scoring_result['final_score']
    results['final_verdict'] = scoring_result['final_verdict']
    results['scoring_breakdown'] = scoring_result['breakdown']
    print(f"  ✅ Final Score: {results['final_score']}/100")
    
    # Module 9 (depends on final score)
    print("Running Module 9: Pitch Assist...")
    results['module_9_pitch_assist'] = generate_pitch(idea_description, results, results['final_score'])
    print("  ✅ Module 9 complete")
    
    print("="*50)
    print("✅ ALL MODULES COMPLETE!")
    print("="*50)
    
    return {
        "startup_idea": idea_description,
        "final_score": results['final_score'],
        "final_verdict": results['final_verdict'],
        "modules": results
    }


# Test the function (remove this later)
if __name__ == "__main__":
    test_idea = "AI note-taker for students"
    result = analyze_idea(test_idea)
    print(json.dumps(result, indent=2))
    
    # Test all modules
    print("\n" + "="*60)
    print("TESTING ALL MODULES TOGETHER")
    print("="*60)
    full_result = run_all_modules(test_idea)
    print("\n📊 FINAL SUMMARY:")
    print(f"   Startup: {full_result['startup_idea']}")
    print(f"   Final Score: {full_result['final_score']}/100")
    print(f"   Verdict: {full_result['final_verdict']}")