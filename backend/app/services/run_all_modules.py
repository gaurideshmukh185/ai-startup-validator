def run_all_modules(idea_description):
    """
    Run all 9 modules and return complete JSON with final score
    """
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    from market_demand import analyze_market_demand
    from competitor_intelligence import analyze_competitors
    from reddit_scraper_ddg import analyze_reddit_sentiment_scraper
    from revenue import analyze_revenue
    from mvp import analyze_mvp
    from risk import analyze_risk
    from virality import analyze_virality
    from pitch_assist import generate_pitch
    from scoring_service import calculate_final_score
    
    # Import analyze_idea from the same module
    # Since we're already in llm_service.py, analyze_idea is available
    
    results = {}
    
    # Module 1
    results['module_1_idea_understanding'] = analyze_idea(idea_description)
    print("✅ Module 1 complete")
    
    # Module 2
    results['module_2_market_demand'] = analyze_market_demand(idea_description)
    print("✅ Module 2 complete")
    
    # Module 3
    results['module_3_competitor_intel'] = analyze_competitors(idea_description)
    print("✅ Module 3 complete")
    
    # Module 4
    results['module_4_reddit_sentiment'] = analyze_reddit_sentiment_scraper(idea_description)
    print("✅ Module 4 complete")
    
    # Module 5
    results['module_5_revenue'] = analyze_revenue(idea_description)
    print("✅ Module 5 complete")
    
    # Module 6
    results['module_6_mvp'] = analyze_mvp(idea_description)
    print("✅ Module 6 complete")
    
    # Module 7
    results['module_7_risk'] = analyze_risk(idea_description)
    print("✅ Module 7 complete")
    
    # Module 8
    results['module_8_virality'] = analyze_virality(idea_description)
    print("✅ Module 8 complete")
    
    # Calculate final score
    scoring_result = calculate_final_score(results)
    results['final_score'] = scoring_result['final_score']
    results['final_verdict'] = scoring_result['final_verdict']
    results['scoring_breakdown'] = scoring_result['breakdown']
    
    # Module 9 (depends on final score)
    results['module_9_pitch_assist'] = generate_pitch(idea_description, results, results['final_score'])
    print("✅ Module 9 complete")
    
    return {
        "startup_idea": idea_description,
        "final_score": results['final_score'],
        "final_verdict": results['final_verdict'],
        "modules": results
    }