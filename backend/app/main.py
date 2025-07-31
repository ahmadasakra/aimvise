import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv

from app.services.analysis_service import AnalysisService
from app.services.pdf_service import PDFService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI-mVISE Repository Analyzer",
    description="AI-powered repository analysis platform with Amazon Bedrock Claude",
    version="2.0.0"
)

# Configure CORS - More permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Initialize Analysis Service
try:
    aws_region = os.getenv("AWS_REGION", "us-east-1")
    analysis_service = AnalysisService(aws_region=aws_region)
    pdf_service = PDFService()
    logger.info(f"Analysis service initialized with AWS region: {aws_region}")
    logger.info("PDF service initialized")
except Exception as e:
    logger.error(f"Failed to initialize services: {e}")
    analysis_service = None
    pdf_service = None

# Pydantic Models
class AnalysisRequest(BaseModel):
    repository_url: str
    github_token: Optional[str] = None
    analysis_type: str = "comprehensive"  # quick, standard, comprehensive

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    message: str

class RepositoryInfo(BaseModel):
    id: str
    name: str
    url: str
    last_analyzed: Optional[str] = None
    quality_score: Optional[int] = None

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AI-mVISE Repository Analyzer",
        "version": "2.0.0",
        "description": "AI-powered repository analysis with Amazon Bedrock Claude",
        "endpoints": {
            "start_analysis": "POST /api/analysis/start",
            "get_progress": "GET /api/analysis/{analysis_id}/progress",
            "get_result": "GET /api/analysis/{analysis_id}",
            "list_analyses": "GET /api/analysis",
            "delete_analysis": "DELETE /api/analysis/{analysis_id}"
        },
        "status": "operational" if analysis_service else "error - analysis service not initialized"
    }

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handle OPTIONS requests for CORS preflight"""
    return {"message": "OK"}

@app.post("/api/analysis/start", response_model=AnalysisResponse)
async def start_analysis(request: AnalysisRequest):
    """
    Start comprehensive repository analysis with AI
    
    This endpoint starts a comprehensive analysis that includes:
    - Repository cloning and file analysis
    - Static code analysis (complexity, security, quality)
    - AI-powered architecture analysis using Amazon Bedrock Claude
    - AI-powered code quality assessment
    - AI-powered security risk analysis
    - Comprehensive report generation with business insights
    """
    
    if not analysis_service:
        raise HTTPException(
            status_code=503, 
            detail="Analysis service not available. Please check AWS Bedrock configuration."
        )
    
    try:
        logger.info(f"Starting analysis for repository: {request.repository_url}")
        
        result = await analysis_service.start_comprehensive_analysis(
            repository_url=request.repository_url,
            github_token=request.github_token,
            analysis_type=request.analysis_type
        )
        
        return AnalysisResponse(
            analysis_id=result["analysis_id"],
            status=result["status"],
            message=result["message"]
        )
        
    except Exception as e:
        logger.error(f"Failed to start analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")

@app.get("/api/analysis/{analysis_id}/progress")
async def get_analysis_progress(analysis_id: str):
    """
    Get real-time progress of running analysis
    
    Returns current stage, progress percentage, and estimated completion
    """
    
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Analysis service not available")
    
    try:
        progress = await analysis_service.get_analysis_progress(analysis_id)
        
        if "error" in progress:
            raise HTTPException(status_code=404, detail=progress["error"])
        
        return progress
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get progress for {analysis_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get progress: {str(e)}")

@app.get("/api/analysis/{analysis_id}")
async def get_analysis_result(analysis_id: str):
    """
    Get comprehensive analysis results
    
    Returns detailed analysis including:
    - Repository overview and statistics
    - Overall quality scores (1-100 scale)
    - Technical metrics (complexity, vulnerabilities, etc.)
    - AI insights (architecture patterns, recommendations)
    - Executive summary and business impact
    - Investment recommendations with priority
    """
    
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Analysis service not available")
    
    try:
        result = await analysis_service.get_analysis_result(analysis_id)
        
        if "error" in result:
            if result.get("status") == "not_found":
                raise HTTPException(status_code=404, detail="Analysis not found")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analysis result for {analysis_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get analysis result: {str(e)}")

@app.get("/api/analysis/{analysis_id}/report")
async def get_analysis_report(analysis_id: str):
    """
    Generate and download comprehensive report for analysis
    
    Returns a professional text report with:
    - Executive summary for business stakeholders
    - Detailed technical analysis
    - Security assessment
    - Business impact analysis
    - Investment recommendations
    - Technology stack analysis
    - Environment strategy
    - mVISE branding and professional formatting
    """
    
    if not analysis_service or not pdf_service:
        raise HTTPException(status_code=503, detail="Services not available")
    
    try:
        # Get analysis result
        result = await analysis_service.get_analysis_result(analysis_id)
        if not result:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        # Generate report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"mVISE_analysis_{analysis_id}_{timestamp}.pdf"
        report_path = pdf_service.generate_report(result, report_filename)
        
        # Return report file
        from fastapi.responses import FileResponse
        return FileResponse(
            path=report_path,
            filename=report_filename,
            media_type='application/pdf'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report for {analysis_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@app.get("/api/analysis")
async def list_analyses():
    """
    List all analyses with their current status
    
    Returns summary of all analyses including progress and completion status
    """
    
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Analysis service not available")
    
    try:
        analyses = await analysis_service.list_analyses()
        return analyses
        
    except Exception as e:
        logger.error(f"Failed to list analyses: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list analyses: {str(e)}")

@app.delete("/api/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """
    Delete analysis and cleanup resources
    
    Removes analysis from memory and cleans up any temporary files
    """
    
    if not analysis_service:
        raise HTTPException(status_code=503, detail="Analysis service not available")
    
    try:
        result = await analysis_service.delete_analysis(analysis_id)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete analysis {analysis_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete analysis: {str(e)}")

@app.get("/api/repositories")
async def list_repositories():
    """
    List example repositories for demo purposes
    
    In a production environment, this would connect to a database
    or repository management system
    """
    
    demo_repos = [
        {
            "id": "1",
            "name": "ai-mvise-frontend",
            "url": "https://github.com/vercel/next.js",
            "description": "React Next.js Framework",
            "last_analyzed": "2024-01-15T10:30:00Z",
            "quality_score": 92,
            "languages": ["TypeScript", "JavaScript"],
            "stars": 120000
        },
        {
            "id": "2", 
            "name": "fastapi-example",
            "url": "https://github.com/tiangolo/fastapi",
            "description": "FastAPI Framework",
            "last_analyzed": "2024-01-14T15:45:00Z",
            "quality_score": 95,
            "languages": ["Python"],
            "stars": 70000
        },
        {
            "id": "3",
            "name": "react-example",
            "url": "https://github.com/facebook/react",
            "description": "React Library",
            "last_analyzed": "2024-01-13T09:20:00Z",
            "quality_score": 89,
            "languages": ["JavaScript", "TypeScript"],
            "stars": 220000
        }
    ]
    
    return {"repositories": demo_repos}

@app.get("/api/dashboard/stats")  
async def get_dashboard_stats():
    """
    Get dashboard statistics
    
    Returns overall platform statistics and metrics
    """
    
    if not analysis_service:
        return {
            "error": "Analysis service not available",
            "total_repositories": 0,
            "analyses_completed": 0,
            "average_quality_score": 0,
            "vulnerabilities_found": 0
        }
    
    try:
        analyses = await analysis_service.list_analyses()
        analyses_list = analyses.get("analyses", [])
        
        completed_analyses = [a for a in analyses_list if a["status"] == "completed"]
        
        return {
            "total_repositories": len(analyses_list),
            "analyses_completed": len(completed_analyses),
            "analyses_running": len([a for a in analyses_list if a["status"] == "running"]),
            "analyses_failed": len([a for a in analyses_list if a["status"] == "failed"]),
            "average_quality_score": 85.2,  # This would be calculated from actual results
            "vulnerabilities_found": len(completed_analyses) * 3,  # Placeholder
            "last_updated": "2024-01-15T12:00:00Z",
            "ai_model": "Claude 3.5 Sonnet",
            "platform_status": "operational"
        }
        
    except Exception as e:
        logger.error(f"Failed to get dashboard stats: {e}")
        return {
            "error": f"Failed to get stats: {str(e)}",
            "total_repositories": 0,
            "analyses_completed": 0
        }

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for monitoring
    
    Checks availability of all required services
    """
    
    health_status = {
        "status": "healthy",
        "timestamp": "2024-01-15T12:00:00Z",
        "services": {
            "analysis_service": "healthy" if analysis_service else "unhealthy",
            "aws_bedrock": "unknown",  # Would need actual check
            "git_tools": "unknown"    # Would need actual check
        }
    }
    
    # Set overall status based on critical services
    if not analysis_service:
        health_status["status"] = "unhealthy"
    
    return health_status

# Error Handlers

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return {"error": "Resource not found", "status_code": 404}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {exc}")
    return {"error": "Internal server error", "status_code": 500}

# Startup and Shutdown Events

@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info("🚀 AI-mVISE Repository Analyzer starting up...")
    
    # Check AWS credentials
    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
        logger.warning("⚠️  AWS credentials not found in environment variables")
        logger.warning("⚠️  Amazon Bedrock integration may not work")
    else:
        logger.info("✅ AWS credentials found")
    
    # Check required tools
    import shutil
    tools_status = {
        "git": shutil.which("git") is not None,
        "radon": shutil.which("radon") is not None,
        "bandit": shutil.which("bandit") is not None,
        "pylint": shutil.which("pylint") is not None
    }
    
    for tool, available in tools_status.items():
        if available:
            logger.info(f"✅ {tool} is available")
        else:
            logger.warning(f"⚠️  {tool} is not available - some analysis features may be limited")
    
    logger.info("🎯 AI-mVISE Repository Analyzer ready!")

@app.on_event("shutdown") 
async def shutdown_event():
    """Application shutdown tasks"""
    logger.info("🔄 AI-mVISE Repository Analyzer shutting down...")
    
    # Cleanup any running analyses
    if analysis_service:
        # In a production environment, you'd want to gracefully handle ongoing analyses
        logger.info("🧹 Cleaning up analysis service...")
    
    logger.info("👋 AI-mVISE Repository Analyzer stopped")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=os.getenv("DEBUG", "false").lower() == "true"
    ) 