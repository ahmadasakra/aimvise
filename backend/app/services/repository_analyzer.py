import asyncio
import logging
import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import git
import json
from dataclasses import dataclass

from app.core.config import settings
from app.core.database import get_db_context
from app.models.analysis import RepositoryAnalysis, AnalysisStatus, AnalysisType
from app.services.github_service import GitHubService
from app.services.analyzers.code_quality_analyzer import CodeQualityAnalyzer
from app.services.analyzers.security_analyzer import SecurityAnalyzer
from app.services.analyzers.architecture_analyzer import ArchitectureAnalyzer
from app.services.analyzers.dependency_analyzer import DependencyAnalyzer
from app.services.analyzers.performance_analyzer import PerformanceAnalyzer
from app.services.analyzers.build_analyzer import BuildAnalyzer
from app.services.ai_service import AIService

logger = logging.getLogger(__name__)

@dataclass
class AnalysisStage:
    name: str
    description: str
    weight: float  # Contribution to overall progress (0.0 - 1.0)

class RepositoryAnalyzer:
    """
    Main orchestrator for repository analysis.
    Coordinates multiple specialized analyzers to provide comprehensive insights.
    """
    
    def __init__(self, analysis_id: str, github_token: Optional[str] = None):
        self.analysis_id = analysis_id
        self.github_token = github_token
        self.github_service = GitHubService(github_token)
        self.ai_service = AIService()
        self.temp_dir: Optional[Path] = None
        self.repo_path: Optional[Path] = None
        
        # Define analysis stages
        self.stages = [
            AnalysisStage("clone", "Cloning repository", 0.05),
            AnalysisStage("dependencies", "Analyzing dependencies", 0.15),
            AnalysisStage("code_quality", "Analyzing code quality", 0.25),
            AnalysisStage("security", "Security vulnerability scan", 0.20),
            AnalysisStage("architecture", "Architecture pattern detection", 0.15),
            AnalysisStage("performance", "Performance analysis", 0.10),
            AnalysisStage("build", "Build process analysis", 0.05),
            AnalysisStage("ai_insights", "AI-powered insights generation", 0.05)
        ]
        
        self.current_stage_index = 0
        self.results = {}
    
    async def analyze_repository(
        self,
        repository_url: str,
        analysis_type: AnalysisType,
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform comprehensive repository analysis
        """
        try:
            logger.info(f"🔍 Starting {analysis_type} analysis for {repository_url}")
            
            # Update status to running
            await self._update_analysis_status(AnalysisStatus.RUNNING, started_at=datetime.now())
            
            # Create temporary directory
            self.temp_dir = Path(tempfile.mkdtemp(prefix="ai_mvise_"))
            logger.info(f"📁 Created temp directory: {self.temp_dir}")
            
            # Stage 1: Clone repository
            await self._run_stage("clone", self._clone_repository, repository_url)
            
            # Get repository metadata
            repo_metadata = await self._get_repository_metadata()
            self.results["metadata"] = repo_metadata
            
            # Stage 2: Dependency analysis (always run as it's foundational)
            dependency_analyzer = DependencyAnalyzer(self.repo_path)
            await self._run_stage(
                "dependencies",
                dependency_analyzer.analyze,
                store_key="dependencies"
            )
            
            # Stage 3: Code quality analysis
            if analysis_type in [AnalysisType.STANDARD, AnalysisType.COMPREHENSIVE]:
                code_analyzer = CodeQualityAnalyzer(self.repo_path)
                await self._run_stage(
                    "code_quality",
                    code_analyzer.analyze,
                    store_key="code_quality"
                )
            
            # Stage 4: Security analysis
            if config.get("include_security", True):
                security_analyzer = SecurityAnalyzer(self.repo_path)
                await self._run_stage(
                    "security",
                    security_analyzer.analyze,
                    store_key="security"
                )
            
            # Stage 5: Architecture analysis
            if config.get("include_architecture", True):
                arch_analyzer = ArchitectureAnalyzer(self.repo_path)
                await self._run_stage(
                    "architecture",
                    arch_analyzer.analyze,
                    store_key="architecture"
                )
            
            # Stage 6: Performance analysis
            if config.get("include_performance", True) and analysis_type == AnalysisType.COMPREHENSIVE:
                perf_analyzer = PerformanceAnalyzer(self.repo_path)
                await self._run_stage(
                    "performance",
                    perf_analyzer.analyze,
                    store_key="performance"
                )
            
            # Stage 7: Build process analysis
            build_analyzer = BuildAnalyzer(self.repo_path)
            await self._run_stage(
                "build",
                build_analyzer.analyze,
                store_key="build"
            )
            
            # Stage 8: AI-powered insights and recommendations
            await self._run_stage(
                "ai_insights",
                self._generate_ai_insights,
                store_key="ai_insights"
            )
            
            # Calculate overall scores
            overall_scores = await self._calculate_overall_scores()
            self.results["scores"] = overall_scores
            
            # Generate recommendations
            recommendations = await self._generate_recommendations()
            self.results["recommendations"] = recommendations
            
            # Save final results
            await self._save_final_results()
            
            # Update status to completed
            await self._update_analysis_status(AnalysisStatus.COMPLETED, completed_at=datetime.now())
            
            logger.info(f"✅ Analysis {self.analysis_id} completed successfully")
            return self.results
            
        except Exception as e:
            logger.error(f"❌ Analysis {self.analysis_id} failed: {str(e)}")
            await self._update_analysis_status(AnalysisStatus.FAILED, error_log=str(e))
            raise
        
        finally:
            # Cleanup
            await self._cleanup()
    
    async def _run_stage(self, stage_name: str, func, *args, store_key: Optional[str] = None):
        """Run a single analysis stage with progress tracking"""
        try:
            stage = next(s for s in self.stages if s.name == stage_name)
            logger.info(f"🔄 Running stage: {stage.description}")
            
            # Call the analysis function
            if asyncio.iscoroutinefunction(func):
                result = await func(*args)
            else:
                result = func(*args)
            
            # Store result if key provided
            if store_key and result:
                self.results[store_key] = result
            
            # Update progress
            self.current_stage_index += 1
            progress = sum(s.weight for s in self.stages[:self.current_stage_index]) * 100
            
            logger.info(f"✅ Completed stage: {stage.description} ({progress:.1f}%)")
            
        except Exception as e:
            logger.error(f"❌ Stage {stage_name} failed: {str(e)}")
            raise
    
    async def _clone_repository(self, repository_url: str):
        """Clone the repository to temporary directory"""
        try:
            self.repo_path = self.temp_dir / "repo"
            
            logger.info(f"📥 Cloning repository from {repository_url}")
            
            # Clone with depth=1 for faster download
            git.Repo.clone_from(
                repository_url,
                self.repo_path,
                depth=1,
                single_branch=True
            )
            
            logger.info(f"✅ Repository cloned to {self.repo_path}")
            
        except git.exc.GitCommandError as e:
            logger.error(f"Git clone failed: {str(e)}")
            raise Exception(f"Failed to clone repository: {str(e)}")
    
    async def _get_repository_metadata(self) -> Dict[str, Any]:
        """Extract basic repository metadata"""
        try:
            repo = git.Repo(self.repo_path)
            
            # Get file statistics
            file_stats = self._get_file_statistics()
            
            # Get git statistics
            commits = list(repo.iter_commits(max_count=100))
            
            metadata = {
                "total_files": file_stats["total_files"],
                "code_files": file_stats["code_files"],
                "total_lines": file_stats["total_lines"],
                "languages": file_stats["languages"],
                "recent_commits": len(commits),
                "latest_commit": {
                    "hash": commits[0].hexsha[:8] if commits else None,
                    "message": commits[0].message.strip() if commits else None,
                    "author": str(commits[0].author) if commits else None,
                    "date": commits[0].committed_datetime.isoformat() if commits else None
                } if commits else None,
                "repo_size_mb": self._get_directory_size(self.repo_path) / (1024 * 1024)
            }
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to get repository metadata: {str(e)}")
            return {}
    
    def _get_file_statistics(self) -> Dict[str, Any]:
        """Get file and language statistics"""
        file_extensions = {}
        total_files = 0
        code_files = 0
        total_lines = 0
        
        code_extensions = {
            '.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php',
            '.rb', '.go', '.rs', '.swift', '.kt', '.scala', '.r',
            '.html', '.css', '.scss', '.less', '.vue', '.jsx', '.tsx'
        }
        
        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file() and not str(file_path).startswith('.git'):
                total_files += 1
                ext = file_path.suffix.lower()
                
                if ext in code_extensions:
                    code_files += 1
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = len(f.readlines())
                            total_lines += lines
                            file_extensions[ext] = file_extensions.get(ext, 0) + lines
                    except Exception:
                        pass
        
        # Map extensions to languages
        language_map = {
            '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
            '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
            '.php': 'PHP', '.rb': 'Ruby', '.go': 'Go', '.rs': 'Rust',
            '.swift': 'Swift', '.kt': 'Kotlin', '.scala': 'Scala',
            '.html': 'HTML', '.css': 'CSS', '.vue': 'Vue'
        }
        
        languages = {}
        for ext, lines in file_extensions.items():
            lang = language_map.get(ext, ext.replace('.', '').title())
            languages[lang] = languages.get(lang, 0) + lines
        
        return {
            "total_files": total_files,
            "code_files": code_files,
            "total_lines": total_lines,
            "languages": dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))
        }
    
    def _get_directory_size(self, path: Path) -> int:
        """Get total size of directory in bytes"""
        total_size = 0
        for file_path in path.rglob('*'):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                except Exception:
                    pass
        return total_size
    
    async def _generate_ai_insights(self) -> Dict[str, Any]:
        """Generate AI-powered insights and analysis"""
        try:
            logger.info("🧠 Generating AI insights...")
            
            # Prepare context for AI analysis
            context = {
                "metadata": self.results.get("metadata", {}),
                "code_quality": self.results.get("code_quality", {}),
                "security": self.results.get("security", {}),  
                "architecture": self.results.get("architecture", {}),
                "dependencies": self.results.get("dependencies", {})
            }
            
            # Generate insights using AI service
            insights = await self.ai_service.analyze_repository_context(context)
            
            return insights
            
        except Exception as e:
            logger.error(f"AI insights generation failed: {str(e)}")
            return {"error": str(e)}
    
    async def _calculate_overall_scores(self) -> Dict[str, float]:
        """Calculate overall quality scores (1-6 scale)"""
        try:
            scores = {}
            
            # Code Quality Score
            code_quality = self.results.get("code_quality", {})
            if code_quality:
                complexity_score = min(6.0, max(1.0, 6.0 - (code_quality.get("avg_complexity", 5) - 5) * 0.5))
                duplication_score = min(6.0, max(1.0, 6.0 - code_quality.get("duplication_percentage", 10) * 0.2))
                scores["code_quality"] = (complexity_score + duplication_score) / 2
            
            # Security Score
            security = self.results.get("security", {})
            if security:
                vuln_count = security.get("vulnerabilities_count", 0)
                scores["security"] = min(6.0, max(1.0, 6.0 - vuln_count * 0.5))
            
            # Architecture Score
            architecture = self.results.get("architecture", {})
            if architecture:
                patterns_score = len(architecture.get("design_patterns", [])) * 0.5
                violations_score = len(architecture.get("violations", [])) * -0.3
                scores["architecture"] = min(6.0, max(1.0, 4.0 + patterns_score + violations_score))
            
            # Dependencies Score
            dependencies = self.results.get("dependencies", {})
            if dependencies:
                outdated_ratio = dependencies.get("outdated_count", 0) / max(dependencies.get("total_count", 1), 1)
                scores["dependencies"] = min(6.0, max(1.0, 6.0 - outdated_ratio * 4.0))
            
            # Overall Score (weighted average)
            if scores:
                weights = {"code_quality": 0.3, "security": 0.3, "architecture": 0.2, "dependencies": 0.2}
                overall = sum(scores.get(key, 3.0) * weight for key, weight in weights.items())
                scores["overall"] = round(overall, 2)
            
            return scores
            
        except Exception as e:
            logger.error(f"Score calculation failed: {str(e)}")
            return {}
    
    async def _generate_recommendations(self) -> Dict[str, Any]:
        """Generate actionable recommendations based on analysis results"""
        recommendations = {
            "critical": [],
            "high_priority": [],
            "medium_priority": [],
            "low_priority": [],
            "best_practices": []
        }
        
        try:
            # Security recommendations
            security = self.results.get("security", {})
            if security.get("vulnerabilities_count", 0) > 0:
                recommendations["critical"].append({
                    "title": "Address Security Vulnerabilities",
                    "description": f"Found {security['vulnerabilities_count']} security vulnerabilities",
                    "action": "Review and fix all critical and high severity vulnerabilities immediately"
                })
            
            # Code quality recommendations
            code_quality = self.results.get("code_quality", {})
            if code_quality.get("avg_complexity", 0) > 10:
                recommendations["high_priority"].append({
                    "title": "Reduce Code Complexity",
                    "description": f"Average cyclomatic complexity is {code_quality['avg_complexity']:.1f}",
                    "action": "Refactor complex functions into smaller, more manageable units"
                })
            
            # Dependency recommendations
            dependencies = self.results.get("dependencies", {})
            outdated_count = dependencies.get("outdated_count", 0)
            if outdated_count > 0:
                priority = "high_priority" if outdated_count > 10 else "medium_priority"
                recommendations[priority].append({
                    "title": "Update Dependencies",
                    "description": f"{outdated_count} dependencies are outdated",
                    "action": "Update dependencies to latest stable versions"
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {str(e)}")
            return recommendations
    
    async def _save_final_results(self):
        """Save final analysis results to database"""
        try:
            with get_db_context() as db:
                analysis = db.query(RepositoryAnalysis).filter(
                    RepositoryAnalysis.id == self.analysis_id
                ).first()
                
                if analysis:
                    # Update all fields with results
                    metadata = self.results.get("metadata", {})
                    scores = self.results.get("scores", {})
                    code_quality = self.results.get("code_quality", {})
                    
                    # Basic metrics
                    analysis.lines_of_code = metadata.get("total_lines")
                    analysis.cyclomatic_complexity_avg = code_quality.get("avg_complexity")
                    analysis.code_duplication_percentage = code_quality.get("duplication_percentage")
                    
                    # Scores
                    analysis.overall_quality_score = scores.get("overall")
                    analysis.maintainability_score = scores.get("code_quality")
                    analysis.security_score = scores.get("security")
                    
                    # Detailed results
                    analysis.frameworks_analysis = self.results.get("metadata", {}).get("languages")
                    analysis.architecture_analysis = self.results.get("architecture")
                    analysis.security_analysis = self.results.get("security")
                    analysis.build_analysis = self.results.get("build")
                    analysis.recommendations = self.results.get("recommendations")
                    
                    # Vulnerability counts
                    security = self.results.get("security", {})
                    analysis.vulnerabilities_count = security.get("vulnerabilities_count", 0)
                    
                    # Dependency counts
                    dependencies = self.results.get("dependencies", {})
                    analysis.dependencies_total = dependencies.get("total_count", 0)
                    analysis.dependencies_outdated = dependencies.get("outdated_count", 0)
                    
                    db.commit()
                    logger.info("💾 Final results saved to database")
                    
        except Exception as e:
            logger.error(f"Failed to save final results: {str(e)}")
            raise
    
    async def _update_analysis_status(
        self,
        status: AnalysisStatus,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        error_log: Optional[str] = None
    ):
        """Update analysis status in database"""
        try:
            with get_db_context() as db:
                analysis = db.query(RepositoryAnalysis).filter(
                    RepositoryAnalysis.id == self.analysis_id
                ).first()
                
                if analysis:
                    analysis.status = status
                    if started_at:
                        analysis.started_at = started_at
                    if completed_at:
                        analysis.completed_at = completed_at
                        if analysis.started_at:
                            duration = (completed_at - analysis.started_at).total_seconds()
                            analysis.analysis_duration_seconds = int(duration)
                    if error_log:
                        analysis.error_log = error_log
                    
                    db.commit()
                    
        except Exception as e:
            logger.error(f"Failed to update analysis status: {str(e)}")
    
    async def _cleanup(self):
        """Clean up temporary files and resources"""
        try:
            if self.temp_dir and self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
                logger.info(f"🧹 Cleaned up temp directory: {self.temp_dir}")
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}") 