import asyncio
import logging
import uuid
from typing import Dict, Any, Optional
from datetime import datetime

from .bedrock_service import BedrockService
from .repository_service import RepositoryService

logger = logging.getLogger(__name__)

class AnalysisService:
    """Main service that coordinates repository analysis with AI insights"""
    
    def __init__(self, aws_region: str = "us-east-1"):
        """
        Initialize analysis service
        
        Args:
            aws_region: AWS region for Bedrock service
        """
        self.bedrock_service = BedrockService(region_name=aws_region)
        self.active_analyses = {}  # Store ongoing analyses
        
    async def start_comprehensive_analysis(self, 
                                         repository_url: str,
                                         github_token: Optional[str] = None,
                                         analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Start comprehensive repository analysis
        
        Args:
            repository_url: Git repository URL
            github_token: Optional GitHub token
            analysis_type: Type of analysis (quick, standard, comprehensive)
            
        Returns:
            Analysis ID and initial status
        """
        
        analysis_id = str(uuid.uuid4())
        
        # Initialize analysis record
        analysis_record = {
            "id": analysis_id,
            "repository_url": repository_url,
            "analysis_type": analysis_type,
            "status": "initializing",
            "progress": 0,
            "current_stage": "Initializing analysis...",
            "started_at": datetime.utcnow().isoformat(),
            "github_token": github_token,
            "results": {}
        }
        
        self.active_analyses[analysis_id] = analysis_record
        
        # Start analysis in background
        asyncio.create_task(self._run_comprehensive_analysis(analysis_id))
        
        return {
            "analysis_id": analysis_id,
            "status": "started",
            "message": "Analysis started successfully"
        }
    
    async def get_analysis_progress(self, analysis_id: str) -> Dict[str, Any]:
        """Get current analysis progress"""
        
        if analysis_id not in self.active_analyses:
            return {"error": "Analysis not found", "status": "not_found"}
        
        analysis = self.active_analyses[analysis_id]
        
        return {
            "analysis_id": analysis_id,
            "status": analysis["status"],
            "progress_percentage": analysis["progress"],
            "current_stage": analysis["current_stage"],
            "started_at": analysis["started_at"],
            "repository_url": analysis["repository_url"]
        }
    
    async def get_analysis_result(self, analysis_id: str) -> Dict[str, Any]:
        """Get final analysis results"""
        
        if analysis_id not in self.active_analyses:
            return {"error": "Analysis not found", "status": "not_found"}
        
        analysis = self.active_analyses[analysis_id]
        
        if analysis["status"] != "completed":
            return {
                "error": "Analysis not completed yet",
                "status": analysis["status"],
                "progress": analysis["progress"]
            }
        
        return analysis["results"]
    
    async def delete_analysis(self, analysis_id: str) -> Dict[str, Any]:
        """Delete analysis and cleanup resources"""
        
        if analysis_id not in self.active_analyses:
            return {"error": "Analysis not found"}
        
        # TODO: Add cleanup for any temporary files
        del self.active_analyses[analysis_id]
        
        return {"message": "Analysis deleted successfully"}
    
    async def list_analyses(self) -> Dict[str, Any]:
        """List all analyses with their status"""
        
        analyses_list = []
        for analysis_id, analysis in self.active_analyses.items():
            analyses_list.append({
                "id": analysis_id,
                "repository_url": analysis["repository_url"],
                "status": analysis["status"],
                "progress": analysis["progress"],
                "started_at": analysis["started_at"],
                "analysis_type": analysis["analysis_type"]
            })
        
        return {"analyses": analyses_list}
    
    async def _run_comprehensive_analysis(self, analysis_id: str):
        """Run the complete analysis pipeline"""
        
        analysis = self.active_analyses[analysis_id]
        repo_service = None
        
        try:
            # Stage 1: Repository Cloning (10%)
            analysis["current_stage"] = "Cloning repository..."
            analysis["progress"] = 10
            analysis["status"] = "running"
            
            repo_service = RepositoryService()
            clone_result = await repo_service.clone_repository(
                analysis["repository_url"],
                analysis["github_token"]
            )
            
            if clone_result["status"] != "success":
                raise Exception(f"Failed to clone repository: {clone_result.get('message', 'Unknown error')}")
            
            repo_info = clone_result["repo_info"]
            logger.info(f"Repository cloned successfully: {repo_info['name']}")
            
            # Stage 2: File Analysis (25%)
            analysis["current_stage"] = "Analyzing code files..."
            analysis["progress"] = 25
            
            file_analysis = await repo_service.analyze_code_files()
            if "error" in file_analysis:
                raise Exception(f"File analysis failed: {file_analysis['error']}")
            
            code_files = file_analysis["code_files"]
            file_stats = file_analysis["file_stats"]
            
            # Update repo info with file stats
            repo_info.update({
                "languages": file_stats["languages"],
                "lines_of_code": file_stats["lines_of_code"],
                "file_count": file_stats["total_files"],
                "code_file_count": file_stats["code_files"]
            })
            
            logger.info(f"Analyzed {len(code_files)} code files")
            
            # Stage 3: Static Analysis (40%)
            analysis["current_stage"] = "Running static analysis tools..."
            analysis["progress"] = 40
            
            static_results = await repo_service.run_static_analysis()
            logger.info("Static analysis completed")
            
            # Stage 4: AI Comprehensive Analysis (55% - 95%)
            analysis["current_stage"] = "AI performing comprehensive analysis..."
            analysis["progress"] = 55
            
            # Single comprehensive analysis covering everything
            comprehensive_analysis = await self.bedrock_service.analyze_repository_comprehensive(
                code_files, repo_info, static_results
            )
            logger.info("Comprehensive AI analysis completed")
            
            # Update progress through the analysis stages
            analysis["progress"] = 70
            analysis["current_stage"] = "Processing architecture insights..."
            
            analysis["progress"] = 80
            analysis["current_stage"] = "Analyzing code quality patterns..."
            
            analysis["progress"] = 90
            analysis["current_stage"] = "Assessing security and business impact..."
            
            analysis["progress"] = 95
            analysis["current_stage"] = "Finalizing comprehensive report..."
            
            # Stage 8: Finalization (100%)
            analysis["current_stage"] = "Analysis completed"
            analysis["progress"] = 100
            analysis["status"] = "completed"
            analysis["completed_at"] = datetime.utcnow().isoformat()
            
            # Store final results
            final_results = {
                "id": analysis_id,
                "repository_url": analysis["repository_url"],
                "repository_name": repo_info.get("name", "Unknown"),
                "status": "completed",
                "analysis_type": analysis["analysis_type"],
                "started_at": analysis["started_at"],
                "completed_at": analysis["completed_at"],
                
                # Repository Overview
                "repository_overview": {
                    "name": repo_info.get("name", "Unknown"),
                    "languages": repo_info.get("languages", []),
                    "total_files": repo_info.get("file_count", 0),
                    "code_files": repo_info.get("code_file_count", 0),
                    "lines_of_code": repo_info.get("lines_of_code", 0),
                    "latest_commit": repo_info.get("latest_commit", {})
                },
                
                # Overall Scores (ONLY from real analysis - no fallbacks)
                "overall_scores": {
                    "overall_quality_score": self._calculate_real_quality_score(static_results),
                    "architecture_score": self._calculate_real_architecture_score(static_results, repo_info),
                    "code_quality_score": self._calculate_real_code_quality_score(static_results),
                    "security_score": self._calculate_real_security_score(static_results),
                    "maintainability_score": self._calculate_real_maintainability_score(static_results),
                    "performance_score": self._calculate_real_performance_score(static_results, repo_info)
                },
                
                # Technical Metrics
                "technical_metrics": {
                    "complexity_metrics": static_results.get("complexity", {}),
                    "security_vulnerabilities": len(static_results.get("security", {}).get("vulnerabilities", [])),
                    "code_smells": len(static_results.get("quality", {}).get("code_smells", [])),
                    "dependencies_total": (
                        len(static_results.get("dependencies", {}).get("python", [])) +
                        len(static_results.get("dependencies", {}).get("javascript", []))
                    ),
                    "dependencies_outdated": static_results.get("dependencies", {}).get("outdated_count", 0)
                },
                
                # AI Insights (from comprehensive analysis)
                "ai_insights": {
                    "architecture_pattern": comprehensive_analysis.get("architecture_analysis", {}).get("pattern", "Unknown"),
                    "technology_stack": comprehensive_analysis.get("technology_stack", {}),
                    "strengths": comprehensive_analysis.get("strengths", []),
                    "weaknesses": comprehensive_analysis.get("weaknesses", []),
                    "security_risks": comprehensive_analysis.get("security_assessment", {}).get("vulnerabilities", []),
                    "performance_issues": comprehensive_analysis.get("code_quality", {}).get("performance_issues", []),
                    "recommendations": comprehensive_analysis.get("recommendations", [])
                },
                
                # Executive Summary (from comprehensive analysis)
                "executive_summary": comprehensive_analysis.get("executive_summary", ""),
                "business_impact": comprehensive_analysis.get("business_impact", {}),
                "investment_recommendations": comprehensive_analysis.get("investment_recommendations", []),
                "risk_assessment": comprehensive_analysis.get("risk_assessment", {}),
                
                # Detailed Results (for deep dive)
                "detailed_analysis": {
                    "static_analysis_results": static_results,
                    "comprehensive_ai_analysis": comprehensive_analysis
                }
            }
            
            analysis["results"] = final_results
            logger.info(f"Analysis {analysis_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Analysis {analysis_id} failed: {e}")
            analysis["status"] = "failed"
            analysis["error"] = str(e)
            analysis["failed_at"] = datetime.utcnow().isoformat()
            analysis["results"] = {
                "error": str(e),
                "status": "failed",
                "analysis_id": analysis_id
            }
        
        finally:
            # Cleanup repository files
            if repo_service:
                repo_service.cleanup()
    
    def _extract_score(self, analysis_result: Dict[str, Any], score_key: str, default: int = None) -> int:
        """Extract score from AI analysis result - NO FALLBACK, returns None if no real data"""
        
        if not analysis_result or "error" in analysis_result:
            return None  # No fallback - return None to indicate missing data
        
        # Handle nested keys like "code_quality.overall_quality_score"
        if "." in score_key:
            keys = score_key.split(".")
            value = analysis_result
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return None  # No fallback data
                    break
            score = value
        else:
            score = analysis_result.get(score_key)
        
        # Only return valid scores, no fallback
        try:
            if score is not None:
                score = int(score)
                return max(0, min(100, score))
            else:
                return None  # Missing data - no fallback
        except (ValueError, TypeError):
            return None  # Invalid data - no fallback
    
    def _calculate_real_quality_score(self, static_results: Dict[str, Any]) -> int:
        """Calculate quality score ONLY from real static analysis data"""
        if not static_results:
            return None
            
        try:
            score = 100  # Start with perfect score
            
            # Real Radon complexity metrics
            complexity = static_results.get("complexity", {})
            if complexity:
                avg_complexity = complexity.get("average_complexity", 0)
                high_complexity_count = complexity.get("high_complexity_count", 0)
                very_high_complexity_count = complexity.get("very_high_complexity_count", 0)
                
                # Penalize based on real complexity
                if avg_complexity > 10:
                    score -= min(30, (avg_complexity - 10) * 3)
                score -= min(20, high_complexity_count * 2)
                score -= min(30, very_high_complexity_count * 5)
            
            # Real Bandit security vulnerabilities
            security = static_results.get("security", {})
            if security:
                vulns = len(security.get("vulnerabilities", []))
                score -= min(40, vulns * 8)  # Heavy penalty for security issues
            
            # Real code quality issues
            quality = static_results.get("quality", {})
            if quality:
                code_smells = len(quality.get("code_smells", []))
                score -= min(20, code_smells * 2)
            
            return max(0, min(100, int(score)))
            
        except Exception as e:
            logger.error(f"Real quality score calculation failed: {e}")
            return None
    
    def _calculate_real_security_score(self, static_results: Dict[str, Any]) -> int:
        """Calculate security score ONLY from real Bandit scan results"""
        if not static_results:
            return None
            
        try:
            security = static_results.get("security", {})
            if not security:
                return None  # No security scan data
                
            vulns = security.get("vulnerabilities", [])
            vuln_count = len(vulns)
            
            if vuln_count == 0:
                return 95  # Excellent security
            elif vuln_count <= 2:
                return 80  # Good security with minor issues
            elif vuln_count <= 5:
                return 60  # Moderate security concerns
            elif vuln_count <= 10:
                return 35  # Significant security issues
            else:
                return 15  # Critical security problems
                
        except Exception as e:
            logger.error(f"Real security score calculation failed: {e}")
            return None
    
    def _calculate_real_architecture_score(self, static_results: Dict[str, Any], repo_info: Dict[str, Any]) -> int:
        """Calculate architecture score from real file metrics"""
        if not static_results or not repo_info:
            return None
            
        try:
            score = 70  # Base score
            
            # Real file size analysis
            lines_of_code = repo_info.get("lines_of_code", 0)
            file_count = repo_info.get("file_count", 1)
            avg_file_size = lines_of_code / file_count if file_count > 0 else 0
            
            # Good file size distribution
            if 50 <= avg_file_size <= 200:
                score += 20
            elif 200 < avg_file_size <= 350:
                score += 10
            elif avg_file_size > 500:
                score -= 20  # Too large files indicate poor architecture
                
            # Project structure
            if file_count > 20 and avg_file_size < 300:
                score += 10  # Good modularization
            elif file_count < 5 and lines_of_code > 5000:
                score -= 15  # Monolithic structure
                
            return max(0, min(100, int(score)))
            
        except Exception as e:
            logger.error(f"Real architecture score calculation failed: {e}")
            return None
    
    def _calculate_real_code_quality_score(self, static_results: Dict[str, Any]) -> int:
        """Calculate code quality from real static analysis"""
        return self._calculate_real_quality_score(static_results)  # Same calculation
    
    def _calculate_real_maintainability_score(self, static_results: Dict[str, Any]) -> int:
        """Calculate maintainability from real complexity metrics"""
        if not static_results:
            return None
            
        try:
            complexity = static_results.get("complexity", {})
            if not complexity:
                return None
                
            avg_complexity = complexity.get("average_complexity", 0)
            
            # Maintainability based on complexity
            if avg_complexity <= 3:
                return 90  # Excellent maintainability
            elif avg_complexity <= 6:
                return 75  # Good maintainability
            elif avg_complexity <= 10:
                return 60  # Moderate maintainability
            elif avg_complexity <= 15:
                return 40  # Poor maintainability
            else:
                return 20  # Very poor maintainability
                
        except Exception as e:
            logger.error(f"Real maintainability score calculation failed: {e}")
            return None
    
    def _calculate_real_performance_score(self, static_results: Dict[str, Any], repo_info: Dict[str, Any]) -> int:
        """Calculate performance score from real metrics"""
        if not static_results or not repo_info:
            return None
            
        try:
            score = 75  # Base performance score
            
            # File size impact on performance
            lines_of_code = repo_info.get("lines_of_code", 0)
            if lines_of_code > 100000:
                score -= 10  # Large codebase performance concerns
            elif lines_of_code < 10000:
                score += 10  # Small, likely performant
                
            # Complexity impact on performance
            complexity = static_results.get("complexity", {})
            if complexity:
                avg_complexity = complexity.get("average_complexity", 0)
                if avg_complexity > 10:
                    score -= min(25, (avg_complexity - 10) * 2)
                    
            return max(0, min(100, int(score)))
            
        except Exception as e:
            logger.error(f"Real performance score calculation failed: {e}")
            return None 