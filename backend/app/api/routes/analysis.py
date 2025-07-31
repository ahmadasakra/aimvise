from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, HttpUrl
import logging
from datetime import datetime
import asyncio

from app.core.database import get_db
from app.models.analysis import RepositoryAnalysis, AnalysisStatus, AnalysisType
from app.services.repository_analyzer import RepositoryAnalyzer
from app.services.github_service import GitHubService
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models for API requests/responses
class AnalysisRequest(BaseModel):
    repository_url: HttpUrl
    github_token: Optional[str] = None
    analysis_type: AnalysisType = AnalysisType.STANDARD
    branch: str = "main"
    include_security: bool = True
    include_architecture: bool = True
    include_dependencies: bool = True
    include_performance: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "repository_url": "https://github.com/user/repository",
                "github_token": "ghp_xxxxxxxxxxxxxxxxxxxx",
                "analysis_type": "comprehensive",
                "branch": "main",
                "include_security": True,
                "include_architecture": True,
                "include_dependencies": True,
                "include_performance": True
            }
        }

class AnalysisResponse(BaseModel):
    analysis_id: str
    status: AnalysisStatus
    repository_url: str
    repository_name: str
    created_at: datetime
    estimated_completion_minutes: int
    progress_url: str
    
    class Config:
        from_attributes = True

class AnalysisProgress(BaseModel):
    analysis_id: str
    status: AnalysisStatus
    progress_percentage: int
    current_stage: str
    stages_completed: List[str]
    estimated_remaining_minutes: int
    error_message: Optional[str] = None
    
class AnalysisResult(BaseModel):
    analysis_id: str
    repository_url: str
    repository_name: str
    status: AnalysisStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    # Overall scores
    overall_quality_score: Optional[float] = None
    maintainability_score: Optional[float] = None
    reliability_score: Optional[float] = None
    security_score: Optional[float] = None
    performance_score: Optional[float] = None
    
    # Key metrics
    lines_of_code: Optional[int] = None
    cyclomatic_complexity_avg: Optional[float] = None
    code_duplication_percentage: Optional[float] = None
    test_coverage_percentage: Optional[float] = None
    vulnerabilities_count: Optional[int] = None
    dependencies_outdated: Optional[int] = None
    
    # Detailed results
    frameworks_analysis: Optional[dict] = None
    architecture_analysis: Optional[dict] = None
    security_analysis: Optional[dict] = None
    recommendations: Optional[dict] = None
    
    class Config:
        from_attributes = True

@router.post("/start", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def start_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    🚀 Start a comprehensive repository analysis
    
    This endpoint initiates a complete analysis of a GitHub repository including:
    - Code quality and maintainability metrics
    - Security vulnerability scanning
    - Architecture pattern detection
    - Dependency analysis
    - Performance assessment
    - Build process evaluation
    """
    try:
        logger.info(f"Starting analysis for repository: {request.repository_url}")
        
        # Extract repository information
        github_service = GitHubService(request.github_token)
        repo_info = await github_service.get_repository_info(str(request.repository_url))
        
        # Create analysis record
        analysis = RepositoryAnalysis(
            repository_url=str(request.repository_url),
            repository_name=repo_info["name"],
            repository_owner=repo_info["owner"],
            branch=request.branch,
            analysis_type=request.analysis_type,
            status=AnalysisStatus.PENDING,
            analysis_config={
                "include_security": request.include_security,
                "include_architecture": request.include_architecture,
                "include_dependencies": request.include_dependencies,
                "include_performance": request.include_performance,
                "github_token_provided": request.github_token is not None
            }
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # Start background analysis
        background_tasks.add_task(
            run_repository_analysis,
            analysis.id,
            str(request.repository_url),
            request.github_token,
            request.analysis_type,
            analysis.analysis_config
        )
        
        # Estimate completion time based on analysis type
        completion_times = {
            AnalysisType.QUICK: 5,
            AnalysisType.STANDARD: 15,
            AnalysisType.COMPREHENSIVE: 30,
            AnalysisType.SECURITY_FOCUSED: 20,
            AnalysisType.ARCHITECTURE_FOCUSED: 25
        }
        
        return AnalysisResponse(
            analysis_id=analysis.id,
            status=analysis.status,
            repository_url=analysis.repository_url,
            repository_name=analysis.repository_name,
            created_at=analysis.created_at,
            estimated_completion_minutes=completion_times.get(request.analysis_type, 15),
            progress_url=f"/api/analysis/{analysis.id}/progress"
        )
        
    except Exception as e:
        logger.error(f"Failed to start analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start analysis: {str(e)}"
        )

@router.get("/{analysis_id}/progress", response_model=AnalysisProgress)
async def get_analysis_progress(analysis_id: str, db: Session = Depends(get_db)):
    """
    📊 Get real-time analysis progress
    
    Returns the current status and progress of a running analysis,
    including completion percentage and current processing stage.
    """
    analysis = db.query(RepositoryAnalysis).filter(
        RepositoryAnalysis.id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Calculate progress based on status and completed stages
    progress_stages = {
        AnalysisStatus.PENDING: (0, "Queued for processing"),
        AnalysisStatus.RUNNING: (50, "Analyzing repository"),
        AnalysisStatus.COMPLETED: (100, "Analysis completed"),
        AnalysisStatus.FAILED: (0, "Analysis failed"),
        AnalysisStatus.CANCELLED: (0, "Analysis cancelled")
    }
    
    progress_percentage, current_stage = progress_stages.get(
        analysis.status, (0, "Unknown status")
    )
    
    # Estimate remaining time
    if analysis.status == AnalysisStatus.RUNNING:
        elapsed_minutes = (datetime.now() - analysis.started_at).total_seconds() / 60 if analysis.started_at else 0
        estimated_total = 15  # Default estimate
        estimated_remaining = max(0, int(estimated_total - elapsed_minutes))
    else:
        estimated_remaining = 0
    
    return AnalysisProgress(
        analysis_id=analysis.id,
        status=analysis.status,
        progress_percentage=progress_percentage,
        current_stage=current_stage,
        stages_completed=["Repository cloned", "Dependencies analyzed"] if progress_percentage > 25 else [],
        estimated_remaining_minutes=estimated_remaining,
        error_message=analysis.error_log if analysis.status == AnalysisStatus.FAILED else None
    )

@router.get("/{analysis_id}", response_model=AnalysisResult)
async def get_analysis_result(analysis_id: str, db: Session = Depends(get_db)):
    """
    📋 Get complete analysis results
    
    Returns the full analysis results including all metrics, scores,
    findings, and recommendations.
    """
    analysis = db.query(RepositoryAnalysis).filter(
        RepositoryAnalysis.id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return AnalysisResult.from_orm(analysis)

@router.get("/{analysis_id}/report")
async def get_analysis_report(analysis_id: str, db: Session = Depends(get_db)):
    """
    📄 Get comprehensive analysis report
    
    Returns a detailed, formatted report suitable for presentation
    to stakeholders and technical teams.
    """
    analysis = db.query(RepositoryAnalysis).filter(
        RepositoryAnalysis.id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    if analysis.status != AnalysisStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Analysis not yet completed"
        )
    
    # Generate comprehensive report
    from app.services.report_generator import ReportGenerator
    report_generator = ReportGenerator()
    
    return await report_generator.generate_comprehensive_report(analysis)

@router.get("/", response_model=List[AnalysisResult])
async def list_analyses(
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[AnalysisStatus] = None,
    db: Session = Depends(get_db)
):
    """
    📚 List all analyses
    
    Returns a paginated list of all repository analyses,
    optionally filtered by status.
    """
    query = db.query(RepositoryAnalysis)
    
    if status_filter:
        query = query.filter(RepositoryAnalysis.status == status_filter)
    
    analyses = query.order_by(RepositoryAnalysis.created_at.desc()).offset(skip).limit(limit).all()
    
    return [AnalysisResult.from_orm(analysis) for analysis in analyses]

@router.delete("/{analysis_id}")
async def cancel_analysis(analysis_id: str, db: Session = Depends(get_db)):
    """
    ❌ Cancel a running analysis
    
    Cancels a running analysis and cleans up associated resources.
    """
    analysis = db.query(RepositoryAnalysis).filter(
        RepositoryAnalysis.id == analysis_id
    ).first()
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    if analysis.status in [AnalysisStatus.COMPLETED, AnalysisStatus.FAILED]:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot cancel completed or failed analysis"
        )
    
    analysis.status = AnalysisStatus.CANCELLED
    db.commit()
    
    return {"message": "Analysis cancelled successfully"}

# Background task function
async def run_repository_analysis(
    analysis_id: str,
    repository_url: str,
    github_token: Optional[str],
    analysis_type: AnalysisType,
    analysis_config: dict
):
    """
    Background task to run the complete repository analysis
    """
    try:
        logger.info(f"Starting background analysis for {analysis_id}")
        
        # Initialize analyzer
        analyzer = RepositoryAnalyzer(
            analysis_id=analysis_id,
            github_token=github_token
        )
        
        # Run analysis
        await analyzer.analyze_repository(
            repository_url=repository_url,
            analysis_type=analysis_type,
            config=analysis_config
        )
        
        logger.info(f"Analysis {analysis_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Analysis {analysis_id} failed: {str(e)}")
        
        # Update analysis status to failed
        from app.core.database import get_db_context
        with get_db_context() as db:
            analysis = db.query(RepositoryAnalysis).filter(
                RepositoryAnalysis.id == analysis_id
            ).first()
            if analysis:
                analysis.status = AnalysisStatus.FAILED
                analysis.error_log = str(e)
                analysis.completed_at = datetime.now()
                db.commit() 