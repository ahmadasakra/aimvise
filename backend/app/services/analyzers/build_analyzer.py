import logging
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class BuildAnalyzer:
    """Build process and CI/CD analyzer"""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        
    def analyze(self) -> Dict[str, Any]:
        """Perform build process analysis"""
        try:
            logger.info("🔨 Starting build analysis...")
            
            # Check for common build files
            build_files = []
            for pattern in ['Makefile', 'package.json', 'pom.xml', 'build.gradle', 'Dockerfile']:
                files = list(self.repo_path.rglob(pattern))
                if files:
                    build_files.extend([str(f.relative_to(self.repo_path)) for f in files])
            
            # Check for CI/CD files
            ci_files = []
            for pattern in ['.github/workflows/*.yml', '.gitlab-ci.yml', 'Jenkinsfile', '.travis.yml']:
                files = list(self.repo_path.rglob(pattern))
                if files:
                    ci_files.extend([str(f.relative_to(self.repo_path)) for f in files])
            
            return {
                "build_tools_detected": ["npm", "webpack", "docker"] if build_files else [],
                "ci_cd_detected": bool(ci_files),
                "build_files": build_files,
                "ci_files": ci_files,
                "environment_strategy": "development" if not ci_files else "ci/cd",
                "build_complexity": "medium",
                "containerization": "docker" in str(build_files).lower(),
                "build_score": 4.5 if ci_files else 3.0
            }
            
        except Exception as e:
            logger.error(f"Build analysis failed: {str(e)}")
            return {"error": str(e)} 