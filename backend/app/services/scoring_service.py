import json

def calculate_final_score(module_results):
    """
    Calculate final startup score (0-100) based on weighted formula
    
    Weights:
    - Market Demand: 25% (from Module 2 demand_score)
    - Competition Level: 20% (from Module 3 - inverted: less competition = higher score)
    - Reddit Sentiment: 20% (from Module 4 sentiment score)
    - Revenue Potential: 15% (from Module 5 monetization_score)
    - Virality: 10% (from Module 8 virality_score)
    - Risk (inverted): 10% (from Module 7 - lower risk = higher score)
    """
    
    # Extract scores from modules
    # Module 2: Market Demand
    demand_score = module_results.get('module_2_market_demand', {}).get('demand_score', 50)
    
    # Module 3: Competition (inverted - less competition = higher score)
    market_saturation = module_results.get('module_3_competitor_intel', {}).get('market_saturation', 'Medium')
    saturation_map = {'Low': 80, 'Medium': 50, 'High': 20, 'Unknown': 50}
    competition_score = saturation_map.get(market_saturation, 50)
    
    # Module 4: Reddit Sentiment
    sentiment_label = module_results.get('module_4_reddit_sentiment', {}).get('overall_sentiment_label', 'Neutral')
    sentiment_map = {
        'Very Positive': 90,
        'Positive': 70,
        'Neutral': 50,
        'Negative': 30,
        'Very Negative': 10,
        'Unknown': 50
    }
    sentiment_score = sentiment_map.get(sentiment_label, 50)
    
    # Module 5: Revenue Potential
    revenue_score = module_results.get('module_5_revenue', {}).get('monetization_score', 50)
    
    # Module 8: Virality
    virality_score = module_results.get('module_8_virality', {}).get('virality_score', 50)
    
    # Module 7: Risk (inverted - lower risk = higher score)
    risk_level = module_results.get('module_7_risk', {}).get('risk_level', 'Medium')
    risk_map = {'Low': 80, 'Medium': 50, 'High': 20, 'Unknown': 50}
    risk_score = risk_map.get(risk_level, 50)
    
    # Calculate weighted score
    weighted_score = (
        (demand_score * 0.25) +
        (competition_score * 0.20) +
        (sentiment_score * 0.20) +
        (revenue_score * 0.15) +
        (virality_score * 0.10) +
        (risk_score * 0.10)
    )
    
    # Round to integer
    final_score = round(weighted_score)
    
    # Determine verdict
    if final_score >= 80:
        verdict = "Strong Opportunity - High potential for success"
    elif final_score >= 60:
        verdict = "Promising Opportunity - Good potential with some risks"
    elif final_score >= 40:
        verdict = "Needs Work - Moderate potential, address key risks"
    else:
        verdict = "Weak Opportunity - Significant challenges, reconsider"
    
    return {
        "final_score": final_score,
        "final_verdict": verdict,
        "breakdown": {
            "market_demand_score": demand_score,
            "market_demand_weight": "25%",
            "competition_score": competition_score,
            "competition_weight": "20%",
            "sentiment_score": sentiment_score,
            "sentiment_weight": "20%",
            "revenue_score": revenue_score,
            "revenue_weight": "15%",
            "virality_score": virality_score,
            "virality_weight": "10%",
            "risk_score": risk_score,
            "risk_weight": "10%"
        }
    }

# Test the scoring service
if __name__ == "__main__":
    # Sample module results for testing
    sample_results = {
        "module_2_market_demand": {"demand_score": 70},
        "module_3_competitor_intel": {"market_saturation": "Medium"},
        "module_4_reddit_sentiment": {"overall_sentiment_label": "Positive"},
        "module_5_revenue": {"monetization_score": 75},
        "module_8_virality": {"virality_score": 68},
        "module_7_risk": {"risk_level": "Medium"}
    }
    
    result = calculate_final_score(sample_results)
    print(json.dumps(result, indent=2))