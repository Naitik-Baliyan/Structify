import os
import logging
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from services import generate_analysis_response, generate_brd

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Structify Backend", version="1.0.0")

# Configure CORS - Allow all origins for prototype demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS configured: All origins allowed for prototype demo")

# Request model
class IdeaInput(BaseModel):
    idea: str = Field(..., min_length=1, description="The business idea")
    target_market: str = Field(..., min_length=1, description="Target market description")
    problem_statement: str = Field(..., min_length=1, description="Problem statement")

# Response model - Extended with AI analysis fields
class AnalysisResponse(BaseModel):
    idea: str
    target_market: str
    problem_statement: str
    analysis: str
    compatibility_score: int
    improvement_suggestions: List[str] = Field(default_factory=list, description="Suggested improvements")
    risk_level: str = Field(default="medium", description="Risk classification: low, medium, high, critical")
    domain_tags: List[str] = Field(default_factory=list, description="Relevant industry and domain tags")

# BRD Generation request model
class BRDGenerationRequest(BaseModel):
    format: str = Field(default="txt", description="Output format: pdf, docx, txt, image")
    analysis_data: dict = Field(..., description="Analysis data from /analyze endpoint")

@app.get("/")
def home():
    """Health check endpoint"""
    logger.info("Health check request received")
    return {"message": "Structify Backend Running 🚀", "timestamp": datetime.now().isoformat()}

@app.options("/analyze")
def options_analyze():
    """CORS preflight for /analyze"""
    return {}

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_idea(data: IdeaInput):
    """Analyze a business idea and return structured feedback"""
    
    logger.info(f"Incoming analysis request - Idea: {data.idea[:50]}...")
    
    try:
        # Validate input is not empty or whitespace-only
        if not data.idea.strip() or not data.target_market.strip() or not data.problem_statement.strip():
            logger.warning("Empty field validation failed")
            raise HTTPException(status_code=400, detail="All fields must contain non-empty text")
        
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
        api_provider = os.getenv("API_PROVIDER", "gemini")
        api_timeout = int(os.getenv("API_TIMEOUT", "30"))
        
        if not api_key:
            logger.warning("API key not configured, using heuristic analysis")
        
        # Generate analysis using AI service
        analysis_result = generate_analysis_response(
            idea=data.idea,
            target_market=data.target_market,
            problem_statement=data.problem_statement,
            api_key=api_key,
            api_provider=api_provider,
            timeout=api_timeout
        )
        
        logger.info(f"Analysis generated successfully - Score: {analysis_result['compatibility_score']}")
        
        return AnalysisResponse(
            idea=data.idea,
            target_market=data.target_market,
            problem_statement=data.problem_statement,
            analysis=analysis_result["analysis"],
            compatibility_score=analysis_result["compatibility_score"],
            improvement_suggestions=analysis_result["improvement_suggestions"],
            risk_level=analysis_result["risk_level"],
            domain_tags=analysis_result["domain_tags"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Analysis processing failed. Please try again.")

@app.options("/generate_brd")
def options_generate_brd():
    """CORS preflight for /generate_brd"""
    return {}

@app.post("/generate_brd")
def generate_brd_document(request: BRDGenerationRequest):
    """Generate a Business Requirements Document (BRD) from analysis data"""
    
    logger.info(f"BRD generation request - Format: {request.format}")
    
    try:
        # Validate format parameter
        valid_formats = ["pdf", "docx", "txt", "image"]
        if request.format.lower() not in valid_formats:
            logger.warning(f"Invalid BRD format requested: {request.format}")
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid format '{request.format}'. Supported formats: {', '.join(valid_formats)}"
            )
        
        # Validate analysis_data has required fields
        required_fields = ["idea", "analysis", "compatibility_score", "improvement_suggestions", "risk_level", "domain_tags"]
        missing_fields = [f for f in required_fields if f not in request.analysis_data]
        
        if missing_fields:
            logger.warning(f"Missing required fields in analysis data: {missing_fields}")
            raise HTTPException(
                status_code=400,
                detail=f"Analysis data missing required fields: {', '.join(missing_fields)}"
            )
        
        # Generate BRD document
        document_buffer, file_ext, mime_type = generate_brd(
            analysis_data=request.analysis_data,
            format=request.format.lower()
        )
        
        # Create filename based on idea and format
        idea_slug = request.analysis_data.get("idea", "BRD")[:30].replace(" ", "_").replace("/", "_")
        filename = f"BRD_{idea_slug}.{file_ext}"
        
        logger.info(f"BRD generated successfully - Size: {len(document_buffer.getvalue())} bytes, Format: {request.format}")
        
        # Return as streaming response for file download
        document_buffer.seek(0)
        return StreamingResponse(
            iter([document_buffer.getvalue()]),
            media_type=mime_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"BRD generation error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Document generation failed. Please try again.")