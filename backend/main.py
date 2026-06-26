import sys
import os

# Add services folder to path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'app', 'services'))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Import the main function from llm_service
from llm_service import run_all_modules

# Create FastAPI app
app = FastAPI(
    title="AI Startup Validator API",
    description="API that analyzes startup ideas using 9 AI modules",
    version="1.0.0"
)

# Define request model
class StartupIdeaRequest(BaseModel):
    idea: str
    user_id: Optional[str] = None

# Define response model (optional but good practice)
class StartupIdeaResponse(BaseModel):
    startup_idea: str
    final_score: int
    final_verdict: str
    modules: dict

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "AI Startup Validator API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/v1/analyze": "Analyze a startup idea",
            "GET /docs": "Interactive API documentation"
        }
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "modules_loaded": 9}

# Main analysis endpoint
@app.post("/api/v1/analyze", response_model=StartupIdeaResponse)
async def analyze_startup_idea(request: StartupIdeaRequest):
    """
    Analyze a startup idea and return detailed results from all 9 modules.
    
    - **idea**: Your startup idea description (required)
    - **user_id**: Optional user identifier for tracking
    """
    try:
        if not request.idea or len(request.idea.strip()) < 5:
            raise HTTPException(status_code=400, detail="Idea description is too short. Please provide at least 5 characters.")
        
        print(f"\n📊 Processing startup idea: {request.idea[:50]}...")
        
        # Run all 9 modules
        result = run_all_modules(request.idea)
        
        print(f"✅ Analysis complete. Final Score: {result['final_score']}/100")
        
        return result
    
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)