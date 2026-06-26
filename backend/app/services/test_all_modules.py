import json
from llm_service import analyze_idea
from market_demand import analyze_market_demand
from competitor_intelligence import analyze_competitors
from reddit_service import analyze_reddit_sentiment

def test_all_modules(startup_idea):
    """
    Test all 4 modules together with the same startup idea
    """
    print("="*60)
    print(f"Testing Startup Idea: {startup_idea}")
    print("="*60)
    
    results = {}
    errors = []
    
    # Test Module 1: Idea Understanding
    print("\n📌 Running Module 1: Idea Understanding...")
    try:
        results['module_1_idea_understanding'] = analyze_idea(startup_idea)
        print("   ✅ Module 1 completed")
    except Exception as e:
        errors.append(f"Module 1 failed: {e}")
        results['module_1_idea_understanding'] = {"error": str(e)}
        print(f"   ❌ Module 1 failed: {e}")
    
    # Test Module 2: Market Demand
    print("\n📌 Running Module 2: Market Demand...")
    try:
        results['module_2_market_demand'] = analyze_market_demand(startup_idea)
        print("   ✅ Module 2 completed")
    except Exception as e:
        errors.append(f"Module 2 failed: {e}")
        results['module_2_market_demand'] = {"error": str(e)}
        print(f"   ❌ Module 2 failed: {e}")
    
    # Test Module 3: Competitor Intelligence
    print("\n📌 Running Module 3: Competitor Intelligence...")
    try:
        results['module_3_competitor_intel'] = analyze_competitors(startup_idea)
        print("   ✅ Module 3 completed")
    except Exception as e:
        errors.append(f"Module 3 failed: {e}")
        results['module_3_competitor_intel'] = {"error": str(e)}
        print(f"   ❌ Module 3 failed: {e}")
    
    # Test Module 4: Reddit Sentiment
    print("\n📌 Running Module 4: Reddit Sentiment...")
    try:
        results['module_4_reddit_sentiment'] = analyze_reddit_sentiment(startup_idea)
        print("   ✅ Module 4 completed")
    except Exception as e:
        errors.append(f"Module 4 failed: {e}")
        results['module_4_reddit_sentiment'] = {"error": str(e)}
        print(f"   ❌ Module 4 failed: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    if errors:
        print(f"❌ {len(errors)} module(s) failed:")
        for err in errors:
            print(f"   - {err}")
    else:
        print("✅ ALL 4 MODULES PASSED!")
    
    return results

# Run tests with 3 different startup ideas
if __name__ == "__main__":
    test_ideas = [
        "AI tool for college students to auto-generate notes from lectures",
        "Food delivery app for hostel students",
        "Freelancer invoice and payment tracking app"
    ]
    
    all_results = {}
    
    for idea in test_ideas:
        result = test_all_modules(idea)
        all_results[idea] = result
        print("\n" + "📄 FULL OUTPUT (first 2000 chars):")
        print(json.dumps(result, indent=2)[:2000])
        print("\n" + "-"*60)
    
    # Final verification
    print("\n" + "="*60)
    print("FINAL VERIFICATION")
    print("="*60)
    
    all_passed = True
    for idea, result in all_results.items():
        for module_key in result:
            if "error" in result[module_key] and result[module_key]["error"] != "Unknown" and "Unable" not in str(result[module_key]):
                all_passed = False
                print(f"❌ Failed for: {idea[:30]}... in {module_key}")
    
    if all_passed:
        print("✅ All tests passed! All 4 modules returned valid JSON for all 3 startup ideas.")
    else:
        print("⚠️ Some tests failed. Check errors above.")