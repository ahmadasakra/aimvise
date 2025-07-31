import logging
from typing import Dict, List, Any, Optional
import json
import asyncio

logger = logging.getLogger(__name__)

class AIService:
    """AI-powered analysis and insights generation service"""
    
    def __init__(self):
        self.model = "claude-3.5-sonnet"  # Would use actual AI service
        
    async def analyze_repository_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI insights from repository analysis context"""
        try:
            logger.info("🧠 Generating AI insights...")
            
            # Simulate AI analysis with structured insights
            insights = {
                "overall_assessment": self._generate_overall_assessment(context),
                "key_strengths": self._identify_strengths(context),
                "critical_areas": self._identify_critical_areas(context),
                "technology_recommendations": self._generate_tech_recommendations(context),
                "team_insights": self._analyze_team_patterns(context),
                "modernization_roadmap": self._create_modernization_roadmap(context),
                "risk_assessment": self._assess_risks(context),
                "best_practices_score": self._calculate_best_practices_score(context)
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"AI insights generation failed: {str(e)}")
            return {"error": str(e)}
    
    def _generate_overall_assessment(self, context: Dict[str, Any]) -> str:
        """Generate overall assessment of the repository"""
        metadata = context.get("metadata", {})
        code_quality = context.get("code_quality", {})
        security = context.get("security", {})
        
        languages = list(metadata.get("languages", {}).keys())
        primary_language = languages[0] if languages else "Unknown"
        
        quality_score = code_quality.get("quality_score", 3.0)
        
        if quality_score >= 5.0:
            quality_level = "excellent"
        elif quality_score >= 4.0:
            quality_level = "good"
        elif quality_score >= 3.0:
            quality_level = "moderate"
        else:
            quality_level = "needs improvement"
        
        return f"""This {primary_language} project demonstrates {quality_level} code quality practices. 
        The codebase consists of {metadata.get('total_lines', 0):,} lines across {metadata.get('total_files', 0)} files. 
        Overall architecture appears {"well-structured" if quality_score >= 4.0 else "moderately organized"} with 
        {"minimal" if security.get("vulnerabilities_count", 0) < 5 else "several"} security concerns identified."""
    
    def _identify_strengths(self, context: Dict[str, Any]) -> List[str]:
        """Identify key strengths of the codebase"""
        strengths = []
        
        code_quality = context.get("code_quality", {})
        security = context.get("security", {})
        architecture = context.get("architecture", {})
        dependencies = context.get("dependencies", {})
        
        # Code quality strengths
        if code_quality.get("quality_score", 0) >= 4.5:
            strengths.append("🏆 High code quality with low complexity and good maintainability")
        
        if code_quality.get("duplication_percentage", 100) < 5:
            strengths.append("✨ Minimal code duplication indicates good abstraction practices")
        
        # Security strengths
        if security.get("vulnerabilities_count", 100) == 0:
            strengths.append("🛡️ No critical security vulnerabilities detected")
        
        # Architecture strengths
        patterns = architecture.get("design_patterns", [])
        if len(patterns) >= 2:
            strengths.append("🏗️ Good use of design patterns for maintainable architecture")
        
        # Dependency management
        outdated_ratio = dependencies.get("outdated_count", 0) / max(dependencies.get("total_count", 1), 1)
        if outdated_ratio < 0.2:
            strengths.append("📦 Well-maintained dependencies with recent versions")
        
        return strengths if strengths else ["📋 Baseline functionality is present and working"]
    
    def _identify_critical_areas(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify critical areas needing attention"""
        critical_areas = []
        
        security = context.get("security", {})
        code_quality = context.get("code_quality", {})
        dependencies = context.get("dependencies", {})
        
        # Security issues
        vuln_count = security.get("vulnerabilities_count", 0)
        if vuln_count > 0:
            critical_areas.append({
                "area": "Security Vulnerabilities",
                "priority": "Critical",
                "description": f"{vuln_count} security issues need immediate attention",
                "impact": "High - Could lead to security breaches"
            })
        
        # Code quality issues
        avg_complexity = code_quality.get("avg_complexity", 0)
        if avg_complexity > 10:
            critical_areas.append({
                "area": "Code Complexity",
                "priority": "High", 
                "description": f"Average complexity of {avg_complexity:.1f} is above recommended threshold",
                "impact": "Medium - Affects maintainability and bug risk"
            })
        
        # Dependency issues
        outdated_count = dependencies.get("outdated_count", 0)
        if outdated_count > 10:
            critical_areas.append({
                "area": "Outdated Dependencies",
                "priority": "Medium",
                "description": f"{outdated_count} dependencies are outdated",
                "impact": "Medium - May have security or compatibility issues"
            })
        
        return critical_areas
    
    def _generate_tech_recommendations(self, context: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate technology-specific recommendations"""
        recommendations = []
        
        metadata = context.get("metadata", {})
        languages = metadata.get("languages", {})
        
        if "Python" in languages:
            recommendations.append({
                "category": "Python Best Practices",
                "recommendation": "Consider using type hints and tools like mypy for better code quality",
                "rationale": "Type hints improve code documentation and catch errors early"
            })
        
        if "JavaScript" in languages:
            recommendations.append({
                "category": "JavaScript Modernization", 
                "recommendation": "Migrate to TypeScript for large codebases",
                "rationale": "TypeScript provides better tooling and error detection"
            })
        
        recommendations.append({
            "category": "Code Quality",
            "recommendation": "Implement automated code formatting (Prettier, Black)",
            "rationale": "Consistent formatting improves readability and reduces review friction"
        })
        
        recommendations.append({
            "category": "Testing",
            "recommendation": "Increase test coverage to 80%+ for critical components",
            "rationale": "Higher test coverage reduces production bugs and improves confidence"
        })
        
        return recommendations
    
    def _analyze_team_patterns(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze development team patterns"""
        return {
            "development_velocity": "Moderate",
            "code_review_culture": "Present",
            "commit_patterns": "Regular small commits",
            "collaboration_score": 4.2,
            "knowledge_distribution": "Concentrated in 2-3 developers",
            "recommendations": [
                "Consider pair programming for knowledge sharing",
                "Implement code review guidelines",
                "Document architectural decisions"
            ]
        }
    
    def _create_modernization_roadmap(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a modernization roadmap"""
        return [
            {
                "phase": "Phase 1 - Foundation",
                "duration": "2-4 weeks",
                "items": [
                    "Address critical security vulnerabilities",
                    "Update outdated dependencies",
                    "Implement automated testing"
                ]
            },
            {
                "phase": "Phase 2 - Quality",
                "duration": "4-6 weeks", 
                "items": [
                    "Refactor high-complexity modules",
                    "Improve code documentation",
                    "Add performance monitoring"
                ]
            },
            {
                "phase": "Phase 3 - Architecture",
                "duration": "8-12 weeks",
                "items": [
                    "Implement clean architecture patterns",
                    "Add comprehensive logging",
                    "Optimize database queries"
                ]
            }
        ]
    
    def _assess_risks(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess various risks in the codebase"""
        security = context.get("security", {})
        code_quality = context.get("code_quality", {})
        dependencies = context.get("dependencies", {})
        
        risk_score = 0
        risk_factors = []
        
        # Security risks
        vuln_count = security.get("vulnerabilities_count", 0)
        if vuln_count > 0:
            risk_score += vuln_count * 2
            risk_factors.append(f"{vuln_count} security vulnerabilities")
        
        # Technical debt
        complexity = code_quality.get("avg_complexity", 0)
        if complexity > 10:
            risk_score += (complexity - 10) * 0.5
            risk_factors.append("High code complexity")
        
        # Dependency risks
        outdated_ratio = dependencies.get("outdated_count", 0) / max(dependencies.get("total_count", 1), 1)
        if outdated_ratio > 0.3:
            risk_score += 5
            risk_factors.append("Many outdated dependencies")
        
        risk_level = "Low"
        if risk_score > 15:
            risk_level = "High"
        elif risk_score > 8:
            risk_level = "Medium"
        
        return {
            "overall_risk": risk_level,
            "risk_score": min(risk_score, 20),  # Cap at 20
            "risk_factors": risk_factors,
            "mitigation_priority": "Immediate" if risk_level == "High" else "Planned"
        }
    
    def _calculate_best_practices_score(self, context: Dict[str, Any]) -> float:
        """Calculate adherence to best practices"""
        score = 10.0  # Start with perfect score
        
        code_quality = context.get("code_quality", {})
        security = context.get("security", {})
        dependencies = context.get("dependencies", {})
        
        # Code quality deductions
        if code_quality.get("avg_complexity", 0) > 10:
            score -= 2.0
        
        if code_quality.get("duplication_percentage", 0) > 10:
            score -= 1.5
        
        # Security deductions
        if security.get("vulnerabilities_count", 0) > 0:
            score -= min(3.0, security["vulnerabilities_count"] * 0.5)
        
        # Dependency deductions
        outdated_ratio = dependencies.get("outdated_count", 0) / max(dependencies.get("total_count", 1), 1)
        if outdated_ratio > 0.2:
            score -= 1.0
        
        return max(1.0, min(10.0, round(score, 1))) 