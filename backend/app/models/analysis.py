from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, Text, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.relationship import relationship
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from app.core.database import Base

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AnalysisType(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    COMPREHENSIVE = "comprehensive"
    SECURITY_FOCUSED = "security_focused"
    ARCHITECTURE_FOCUSED = "architecture_focused"

class RepositoryAnalysis(Base):
    """Main analysis table storing comprehensive repository analysis results"""
    __tablename__ = "repository_analyses"

    # Primary identification
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    repository_url = Column(String, nullable=False, index=True)
    repository_name = Column(String, nullable=False)
    repository_owner = Column(String, nullable=False)
    branch = Column(String, default="main")
    commit_hash = Column(String, nullable=True)
    
    # Analysis metadata
    analysis_type = Column(String, default=AnalysisType.STANDARD)
    status = Column(String, default=AnalysisStatus.PENDING, index=True)
    created_at = Column(DateTime, default=func.now())
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    analysis_duration_seconds = Column(Integer, nullable=True)
    
    # Overall scores (1-6 scale)
    overall_quality_score = Column(Float, nullable=True)
    maintainability_score = Column(Float, nullable=True)
    reliability_score = Column(Float, nullable=True)
    security_score = Column(Float, nullable=True)
    performance_score = Column(Float, nullable=True)
    
    # Code quality metrics
    lines_of_code = Column(Integer, nullable=True)
    cyclomatic_complexity_avg = Column(Float, nullable=True)
    cyclomatic_complexity_max = Column(Float, nullable=True)
    code_duplication_percentage = Column(Float, nullable=True)
    comment_density_percentage = Column(Float, nullable=True)
    test_coverage_percentage = Column(Float, nullable=True)
    
    # Technical debt
    technical_debt_ratio = Column(Float, nullable=True)
    code_smells_count = Column(Integer, nullable=True)
    bugs_count = Column(Integer, nullable=True)
    vulnerabilities_count = Column(Integer, nullable=True)
    
    # Dependencies and technologies
    dependencies_total = Column(Integer, nullable=True)
    dependencies_outdated = Column(Integer, nullable=True)
    dependencies_vulnerable = Column(Integer, nullable=True)
    
    # Detailed analysis results (JSON)
    frameworks_analysis = Column(JSON, nullable=True)  # Languages, frameworks by layer
    architecture_analysis = Column(JSON, nullable=True)  # Patterns, violations, structure
    security_analysis = Column(JSON, nullable=True)  # Vulnerabilities, security issues
    build_analysis = Column(JSON, nullable=True)  # Build process, CI/CD
    team_analysis = Column(JSON, nullable=True)  # Commit patterns, contributors
    documentation_analysis = Column(JSON, nullable=True)  # Documentation quality
    performance_analysis = Column(JSON, nullable=True)  # Performance issues
    
    # Recommendations and action items
    recommendations = Column(JSON, nullable=True)
    critical_issues = Column(JSON, nullable=True)
    improvement_suggestions = Column(JSON, nullable=True)
    
    # Analysis configuration
    analysis_config = Column(JSON, nullable=True)
    error_log = Column(Text, nullable=True)
    
    # User and session info
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    session_id = Column(String, nullable=True)
    
    # Relationships
    # user = relationship("User", back_populates="analyses")
    # code_metrics = relationship("CodeMetrics", back_populates="analysis", cascade="all, delete-orphan")
    # security_findings = relationship("SecurityFinding", back_populates="analysis", cascade="all, delete-orphan")

class CodeMetrics(Base):
    """Detailed code metrics for specific files/modules"""
    __tablename__ = "code_metrics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String, ForeignKey("repository_analyses.id"), nullable=False)
    
    # File/module identification
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # .py, .js, .java, etc.
    module_name = Column(String, nullable=True)
    
    # Metrics
    lines_of_code = Column(Integer, nullable=True)
    lines_of_comments = Column(Integer, nullable=True)
    lines_blank = Column(Integer, nullable=True)
    cyclomatic_complexity = Column(Integer, nullable=True)
    maintainability_index = Column(Float, nullable=True)
    
    # Quality indicators
    code_smells = Column(JSON, nullable=True)
    duplications = Column(JSON, nullable=True)
    violations = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=func.now())

class SecurityFinding(Base):
    """Security vulnerabilities and issues found in the repository"""
    __tablename__ = "security_findings"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String, ForeignKey("repository_analyses.id"), nullable=False)
    
    # Finding details
    severity = Column(String, nullable=False)  # critical, high, medium, low
    category = Column(String, nullable=False)  # SQL injection, XSS, etc.
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Location
    file_path = Column(String, nullable=True)
    line_number = Column(Integer, nullable=True)
    code_snippet = Column(Text, nullable=True)
    
    # Remediation
    recommendation = Column(Text, nullable=True)
    cwe_id = Column(String, nullable=True)  # Common Weakness Enumeration
    cvss_score = Column(Float, nullable=True)
    
    # Status
    is_false_positive = Column(Boolean, default=False)
    is_suppressed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=func.now())

class ArchitecturePattern(Base):
    """Detected architecture patterns and design patterns"""
    __tablename__ = "architecture_patterns"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String, ForeignKey("repository_analyses.id"), nullable=False)
    
    # Pattern details
    pattern_name = Column(String, nullable=False)  # MVC, Singleton, Factory, etc.
    pattern_type = Column(String, nullable=False)  # architectural, creational, behavioral, structural
    confidence_score = Column(Float, nullable=False)  # 0.0 - 1.0
    
    # Implementation details
    implementation_quality = Column(String, nullable=True)  # excellent, good, poor
    files_involved = Column(JSON, nullable=True)
    description = Column(Text, nullable=True)
    
    # Compliance and violations
    violations = Column(JSON, nullable=True)
    suggestions = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=func.now())

class DependencyAnalysis(Base):
    """Analysis of project dependencies"""
    __tablename__ = "dependency_analyses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String, ForeignKey("repository_analyses.id"), nullable=False)
    
    # Dependency details
    name = Column(String, nullable=False)
    current_version = Column(String, nullable=False)
    latest_version = Column(String, nullable=True)
    ecosystem = Column(String, nullable=False)  # npm, pip, maven, etc.
    
    # Status
    is_outdated = Column(Boolean, default=False)
    is_vulnerable = Column(Boolean, default=False)
    is_deprecated = Column(Boolean, default=False)
    
    # Vulnerability details
    vulnerabilities = Column(JSON, nullable=True)
    license = Column(String, nullable=True)
    
    # Usage analysis
    usage_frequency = Column(String, nullable=True)  # high, medium, low
    is_dev_dependency = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=func.now()) 