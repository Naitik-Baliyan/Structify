from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Structify Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class IdeaInput(BaseModel):
    idea: str = Field(..., min_length=1, description="The business idea")
    target_market: str = Field(..., min_length=1, description="Target market description")
    problem_statement: str = Field(..., min_length=1, description="Problem statement")

# Response model
class AnalysisResponse(BaseModel):
    idea: str
    target_market: str
    problem_statement: str
    analysis: str
    compatibility_score: int

@app.get("/")
def home():
    """Health check endpoint"""
    return {"message": "Structify Backend Running 🚀"}

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_idea(data: IdeaInput):
    """Analyze a business idea and return structured feedback"""
    try:
        # Validate input is not empty or whitespace-only
        if not data.idea.strip() or not data.target_market.strip() or not data.problem_statement.strip():
            raise HTTPException(status_code=400, detail="All fields must contain non-empty text")
        
        # Generate analysis (placeholder for now)
        analysis = f"Analyzing idea: {data.idea} for market: {data.target_market}"
        compatibility_score = 75  # Placeholder score
        
        return AnalysisResponse(
            idea=data.idea,
            target_market=data.target_market,
            problem_statement=data.problem_statement,
            analysis=analysis,
            compatibility_score=compatibility_score
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")