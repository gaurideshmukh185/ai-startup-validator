import json
import sys
import os

# Add the backend path
backend_path = os.path.join(os.path.dirname(__file__), 'backend', 'app', 'services')
sys.path.insert(0, backend_path)

# Import all 4 modules
try:
    from llm_service import analyze_idea
    print("✅ Module 1 imported")
except Exception as e:
    print(f"❌ Module 1 import failed: {e}")
    sys.exit(1)

try:
    from market_demand import analyze_market_demand
    print("✅ Module 2 imported")
except Exception as e:
    print(f"❌ Module 2 import failed: {e}")
    sys.exit(1)

try:
    from competitor_intelligence import analyze_competitors
    print("✅ Module 3 imported")
except Exception as e:
    print(f"❌ Module 3 import failed: {e}")
    sys.exit(1)

try:
    from reddit_service import analyze_reddit_sentiment
    print("✅ Module 4 imported")
except Exception as e:
    print(f"❌ Module 4 import failed: {e}")
    sys.exit(1)


def test_all_modules(idea_text, keyword):
    """
    Test all 4 modules with the same startup idea
    Returns combined results as JSON
    """
    print("\n" + "=" * 70)
    print(f"TESTING STARTUP IDEA: {idea_text}")
    print("=" * 70)
    
    results = {
        "startup_idea": idea_text,
        "keyword_used": keyword,
        "module_1_idea_understanding": None,
        "module_2_market_demand": None,
        "module_3_competitor_intel": None,
        "module_4_reddit_sentiment": None,
        "errors": []
    }
    
    # Module 1: Idea Understanding Engine
    print("\n📌 MODULE 1: Idea Understanding Engine")
    print("-" * 40)
    try:
        result1 = analyze_idea(idea_text)
        if result1:
            results["module_1_idea_understanding"] = result1
            print(f"   ✅ Category: {result1.get('category')}")
            print(f"   ✅ Business Model: {result1.get('business_model')}")
            print(f"   ✅ Target User: {result1.get('target_user')}")
        else:
            results["errors"].append("Module 1 returned None")
            print("   ❌ Failed")
    except Exception as e:
        results["errors"].append(f"Module 1 error: {str(e)}")
        print(f"   ❌ Error: {e}")
    
    # Module 2: Market Demand
    print("\n📌 MODULE 2: Market Demand Analysis")
    print("-" * 40)
    try:
        result2 = analyze_market_demand(keyword)
        if result2:
            results["module_2_market_demand"] = result2
            print(f"   ✅ Demand Score: {result2.get('demand_score')}/100")
            print(f"   ✅ Trend Direction: {result2.get('trend_direction')}")
            print(f"   ✅ Market Size: {result2.get('market_size')}")
        else:
            results["errors"].append("Module 2 returned None")
            print("   ❌ Failed")
    except Exception as e:
        results["errors"].append(f"Module 2 error: {str(e)}")
        print(f"   ❌ Error: {e}")
    
    # Module 3: Competitor Intelligence
    print("\n📌 MODULE 3: Competitor Intelligence")
    print("-" * 40)
    try:
        result3 = analyze_competitors(idea_text)
        if result3:
            results["module_3_competitor_intel"] = result3
            competitors = result3.get('competitors', [])
            print(f"   ✅ Competitors Found: {len(competitors)}")
            print(f"   ✅ Competition Level: {result3.get('market_competition_level')}")
        else:
            results["errors"].append("Module 3 returned None")
            print("   ❌ Failed")
    except Exception as e:
        results["errors"].append(f"Module 3 error: {str(e)}")
        print(f"   ❌ Error: {e}")
    
    # Module 4: Reddit Sentiment
    print("\n📌 MODULE 4: Reddit Sentiment Analysis")
    print("-" * 40)
    try:
        result4 = analyze_reddit_sentiment(keyword)
        if result4:
            results["module_4_reddit_sentiment"] = result4
            print(f"   ✅ Comments Analyzed: {result4.get('total_comments_analyzed')}")
            print(f"   ✅ Positive: {result4.get('positive_count')}")
            print(f"   ✅ Negative: {result4.get('negative_count')}")
            print(f"   ✅ Pain Points Found: {len(result4.get('pain_points', []))}")
        else:
            results["errors"].append("Module 4 returned None")
            print("   ❌ Failed")
    except Exception as e:
        results["errors"].append(f"Module 4 error: {str(e)}")
        print(f"   ❌ Error: {e}")
    
    return results


def validate_json(data):
    """Check if data can be serialized to JSON"""
    try:
        json.dumps(data, indent=2)
        return True
    except TypeError as e:
        print(f"JSON Validation Error: {e}")
        return False


# Run tests with 3 different startup ideas
if __name__ == "__main__":
    test_cases = [
        {
            "idea": "AI tool for college students to auto-generate notes from lectures",
            "keyword": "note taking"
        },
        {
            "idea": "Food delivery app for hostel students with no minimum order",
            "keyword": "food delivery"
        },
        {
            "idea": "Freelancer invoice app that auto-calculates taxes",
            "keyword": "invoicing software"
        }
    ]
    
    print("=" * 70)
    print("TESTING ALL 4 MODULES TOGETHER")
    print("=" * 70)
    
    all_results = []
    
    for test_case in test_cases:
        result = test_all_modules(test_case["idea"], test_case["keyword"])
        all_results.append(result)
        
        # Validate JSON
        print("\n📋 JSON VALIDATION:")
        print("-" * 40)
        if validate_json(result):
            print("   ✅ Result is valid JSON")
        else:
            print("   ❌ Result is NOT valid JSON")
        
        print("\n" + "=" * 70)
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    for i, result in enumerate(all_results, 1):
        print(f"\n{i}. {result['startup_idea'][:50]}...")
        print(f"   Errors: {len(result['errors'])}")
        if result['errors']:
            for err in result['errors']:
                print(f"     - {err}")
    
    # Print full JSON output for first test case
    print("\n" + "=" * 70)
    print("SAMPLE JSON OUTPUT (Test Case 1)")
    print("=" * 70)
    print(json.dumps(all_results[0], indent=2, default=str))