import json
import logging
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import requests

logger = logging.getLogger(__name__)

class DependencyAnalyzer:
    """
    Comprehensive dependency analyzer that evaluates:
    - Package dependencies across multiple ecosystems
    - Version freshness and update recommendations
    - License compatibility
    - Security vulnerabilities in dependencies
    - Dependency tree complexity
    - Build tool configuration
    """
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.supported_manifests = {
            'package.json': 'npm',
            'requirements.txt': 'pip',
            'Pipfile': 'pipenv', 
            'poetry.lock': 'poetry',
            'pom.xml': 'maven',
            'build.gradle': 'gradle',
            'Gemfile': 'ruby',
            'composer.json': 'composer',
            'go.mod': 'go',
            'Cargo.toml': 'cargo'
        }
        
    def analyze(self) -> Dict[str, Any]:
        """
        Perform comprehensive dependency analysis
        """
        try:
            logger.info("📦 Starting dependency analysis...")
            
            results = {
                "summary": {},
                "ecosystems": {},
                "dependencies": [],
                "outdated_dependencies": [],
                "vulnerable_dependencies": [],
                "license_issues": [],
                "dependency_tree": {},
                "build_tools": [],
                "recommendations": []
            }
            
            # Find all dependency manifest files
            manifest_files = self._find_manifest_files()
            if not manifest_files:
                logger.warning("No dependency manifest files found")
                return results
            
            logger.info(f"Found {len(manifest_files)} dependency manifest files")
            
            # Analyze each ecosystem
            all_dependencies = []
            ecosystems_analyzed = {}
            
            for manifest_file, ecosystem in manifest_files.items():
                try:
                    ecosystem_analysis = self._analyze_ecosystem(manifest_file, ecosystem)
                    if ecosystem_analysis:
                        ecosystems_analyzed[ecosystem] = ecosystem_analysis
                        all_dependencies.extend(ecosystem_analysis.get("dependencies", []))
                        results["build_tools"].extend(ecosystem_analysis.get("build_tools", []))
                        
                except Exception as e:
                    logger.warning(f"Failed to analyze {manifest_file}: {str(e)}")
                    continue
            
            results["ecosystems"] = ecosystems_analyzed
            results["dependencies"] = all_dependencies
            
            # Analyze dependency health
            outdated_deps = [dep for dep in all_dependencies if dep.get("is_outdated", False)]
            vulnerable_deps = [dep for dep in all_dependencies if dep.get("has_vulnerabilities", False)]
            
            results["outdated_dependencies"] = outdated_deps
            results["vulnerable_dependencies"] = vulnerable_deps
            
            # Analyze licenses
            license_analysis = self._analyze_licenses(all_dependencies)
            results["license_issues"] = license_analysis.get("issues", [])
            
            # Build dependency tree
            results["dependency_tree"] = self._build_dependency_tree(ecosystems_analyzed)
            
            # Generate summary
            results["summary"] = {
                "total_dependencies": len(all_dependencies),
                "ecosystems_count": len(ecosystems_analyzed),
                "outdated_count": len(outdated_deps),
                "vulnerable_count": len(vulnerable_deps),
                "license_issues_count": len(results["license_issues"]),
                "direct_dependencies": len([d for d in all_dependencies if d.get("is_direct", True)]),
                "transitive_dependencies": len([d for d in all_dependencies if not d.get("is_direct", True)]),
                "high_risk_dependencies": len([d for d in all_dependencies if d.get("risk_level") == "high"])
            }
            
            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(results)
            
            # Add fields for main analyzer
            results["total_count"] = len(all_dependencies)
            results["outdated_count"] = len(outdated_deps)
            
            logger.info(f"✅ Dependency analysis completed. Found {len(all_dependencies)} dependencies, {len(outdated_deps)} outdated")
            return results
            
        except Exception as e:
            logger.error(f"Dependency analysis failed: {str(e)}")
            return {"error": str(e)}
    
    def _find_manifest_files(self) -> Dict[Path, str]:
        """Find all dependency manifest files in the repository"""
        manifest_files = {}
        
        for manifest_name, ecosystem in self.supported_manifests.items():
            pattern = f"**/{manifest_name}"
            found_files = list(self.repo_path.rglob(pattern))
            
            # Filter out node_modules and other dependency directories
            filtered_files = []
            ignore_dirs = {'node_modules', 'venv', '__pycache__', '.git', 'build', 'dist', 'target'}
            
            for file_path in found_files:
                if not any(part in ignore_dirs for part in file_path.parts):
                    filtered_files.append(file_path)
            
            for file_path in filtered_files:
                manifest_files[file_path] = ecosystem
        
        return manifest_files
    
    def _analyze_ecosystem(self, manifest_file: Path, ecosystem: str) -> Optional[Dict[str, Any]]:
        """Analyze dependencies for a specific ecosystem"""
        try:
            if ecosystem == 'npm':
                return self._analyze_npm_dependencies(manifest_file)
            elif ecosystem in ['pip', 'pipenv']:
                return self._analyze_python_dependencies(manifest_file)
            elif ecosystem == 'poetry':
                return self._analyze_poetry_dependencies(manifest_file)
            elif ecosystem == 'maven':
                return self._analyze_maven_dependencies(manifest_file)
            elif ecosystem == 'gradle':
                return self._analyze_gradle_dependencies(manifest_file)
            elif ecosystem == 'ruby':
                return self._analyze_ruby_dependencies(manifest_file)
            elif ecosystem == 'composer':
                return self._analyze_php_dependencies(manifest_file)
            elif ecosystem == 'go':
                return self._analyze_go_dependencies(manifest_file)
            elif ecosystem == 'cargo':
                return self._analyze_rust_dependencies(manifest_file)
            else:
                logger.warning(f"Unsupported ecosystem: {ecosystem}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to analyze {ecosystem} dependencies: {str(e)}")
            return None
    
    def _analyze_npm_dependencies(self, package_json: Path) -> Dict[str, Any]:
        """Analyze npm dependencies from package.json"""
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            dependencies = []
            relative_path = package_json.relative_to(self.repo_path)
            
            # Parse dependencies
            dep_sections = {
                'dependencies': True,      # Production dependencies
                'devDependencies': False,  # Development dependencies
                'peerDependencies': False, # Peer dependencies
                'optionalDependencies': False  # Optional dependencies
            }
            
            for section, is_production in dep_sections.items():
                deps = package_data.get(section, {})
                for name, version_spec in deps.items():
                    dep_info = {
                        "name": name,
                        "version_spec": version_spec,
                        "current_version": self._parse_version_spec(version_spec),
                        "ecosystem": "npm",
                        "file": str(relative_path),
                        "is_direct": True,
                        "is_production": is_production,
                        "section": section
                    }
                    
                    # Get latest version and check if outdated
                    latest_version = self._get_npm_latest_version(name)
                    if latest_version:
                        dep_info["latest_version"] = latest_version
                        dep_info["is_outdated"] = self._is_version_outdated(
                            dep_info["current_version"], latest_version
                        )
                    
                    # Check for vulnerabilities (simplified)
                    dep_info["has_vulnerabilities"] = False  # Would integrate with npm audit
                    dep_info["risk_level"] = self._assess_dependency_risk(dep_info)
                    
                    dependencies.append(dep_info)
            
            # Analyze package.json structure
            build_tools = []
            if 'scripts' in package_data:
                scripts = package_data['scripts']
                build_tools.append({
                    "tool": "npm scripts",
                    "scripts": list(scripts.keys()),
                    "has_build": "build" in scripts,
                    "has_test": "test" in scripts,
                    "has_lint": any("lint" in script for script in scripts.keys())
                })
            
            return {
                "ecosystem": "npm",
                "file": str(relative_path),
                "dependencies": dependencies,
                "build_tools": build_tools,
                "package_info": {
                    "name": package_data.get("name"),
                    "version": package_data.get("version"),
                    "description": package_data.get("description"),
                    "license": package_data.get("license"),
                    "engines": package_data.get("engines", {})
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze npm dependencies: {str(e)}")
            return {}
    
    def _analyze_python_dependencies(self, requirements_file: Path) -> Dict[str, Any]:
        """Analyze Python dependencies from requirements.txt or Pipfile"""
        try:
            dependencies = []
            relative_path = requirements_file.relative_to(self.repo_path)
            
            if requirements_file.name == 'requirements.txt':
                with open(requirements_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        dep_info = self._parse_python_requirement(line)
                        if dep_info:
                            dep_info.update({
                                "ecosystem": "pip",
                                "file": str(relative_path),
                                "is_direct": True,
                                "is_production": True
                            })
                            
                            # Get latest version
                            latest_version = self._get_pypi_latest_version(dep_info["name"])
                            if latest_version:
                                dep_info["latest_version"] = latest_version
                                dep_info["is_outdated"] = self._is_version_outdated(
                                    dep_info["current_version"], latest_version
                                )
                            
                            dep_info["risk_level"] = self._assess_dependency_risk(dep_info)
                            dependencies.append(dep_info)
            
            elif requirements_file.name == 'Pipfile':
                # Would parse Pipfile format
                pass
            
            return {
                "ecosystem": "pip",
                "file": str(relative_path),
                "dependencies": dependencies,
                "build_tools": []
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze Python dependencies: {str(e)}")
            return {}
    
    def _analyze_maven_dependencies(self, pom_file: Path) -> Dict[str, Any]:
        """Analyze Maven dependencies from pom.xml"""
        try:
            tree = ET.parse(pom_file)
            root = tree.getroot()
            namespace = {'maven': 'http://maven.apache.org/POM/4.0.0'}
            
            dependencies = []
            relative_path = pom_file.relative_to(self.repo_path)
            
            # Find dependencies
            deps = root.findall('.//maven:dependency', namespace)
            for dep in deps:
                group_id = dep.find('maven:groupId', namespace)
                artifact_id = dep.find('maven:artifactId', namespace)
                version = dep.find('maven:version', namespace)
                scope = dep.find('maven:scope', namespace)
                
                if group_id is not None and artifact_id is not None:
                    dep_info = {
                        "name": f"{group_id.text}:{artifact_id.text}",
                        "group_id": group_id.text,
                        "artifact_id": artifact_id.text,
                        "version_spec": version.text if version is not None else "unknown",
                        "current_version": version.text if version is not None else "unknown",
                        "scope": scope.text if scope is not None else "compile",
                        "ecosystem": "maven",
                        "file": str(relative_path),
                        "is_direct": True,
                        "is_production": scope.text != "test" if scope is not None else True
                    }
                    
                    dep_info["risk_level"] = self._assess_dependency_risk(dep_info)
                    dependencies.append(dep_info)
            
            # Analyze build configuration
            build_tools = []
            build = root.find('.//maven:build', namespace)
            if build is not None:
                plugins = build.findall('.//maven:plugin', namespace)
                plugin_names = []
                for plugin in plugins:
                    artifact_id = plugin.find('maven:artifactId', namespace)
                    if artifact_id is not None:
                        plugin_names.append(artifact_id.text)
                
                build_tools.append({
                    "tool": "Maven",
                    "plugins": plugin_names,
                    "has_build": True,
                    "has_test": "maven-surefire-plugin" in plugin_names
                })
            
            return {
                "ecosystem": "maven",
                "file": str(relative_path),
                "dependencies": dependencies,
                "build_tools": build_tools
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze Maven dependencies: {str(e)}")
            return {}
    
    def _parse_python_requirement(self, requirement_line: str) -> Optional[Dict[str, Any]]:
        """Parse a Python requirement line"""
        try:
            # Handle various requirement formats
            # Simple format: package==1.0.0
            # Complex format: package>=1.0.0,<2.0.0
            # Git format: git+https://...
            # Local format: -e ./local_package
            
            if requirement_line.startswith('-e') or requirement_line.startswith('git+'):
                return None  # Skip editable and git dependencies for now
            
            # Extract package name and version spec
            match = re.match(r'^([a-zA-Z0-9_-]+)(.*)', requirement_line)
            if match:
                name = match.group(1)
                version_spec = match.group(2).strip()
                
                # Extract current version
                version_match = re.search(r'==\s*([^\s,]+)', version_spec)
                current_version = version_match.group(1) if version_match else "latest"
                
                return {
                    "name": name,
                    "version_spec": version_spec,
                    "current_version": current_version
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"Failed to parse requirement: {requirement_line}: {str(e)}")
            return None
    
    def _parse_version_spec(self, version_spec: str) -> str:
        """Parse version specification to extract current version"""
        # Remove version prefixes like ^, ~, >=, etc.
        version = re.sub(r'^[\^~>=<]+', '', version_spec)
        # Extract first version number
        version_match = re.match(r'([0-9]+(?:\.[0-9]+)*)', version)
        return version_match.group(1) if version_match else version_spec
    
    def _get_npm_latest_version(self, package_name: str) -> Optional[str]:
        """Get latest version from npm registry (simplified)"""
        try:
            # In a real implementation, you'd call npm registry API
            # For now, return a placeholder
            return "latest"
        except Exception:
            return None
    
    def _get_pypi_latest_version(self, package_name: str) -> Optional[str]:
        """Get latest version from PyPI (simplified)"""
        try:
            # In a real implementation, you'd call PyPI API
            return "latest"
        except Exception:
            return None
    
    def _is_version_outdated(self, current: str, latest: str) -> bool:
        """Check if current version is outdated compared to latest"""
        # Simplified version comparison
        # In a real implementation, you'd use proper semantic versioning
        if current == "latest" or latest == "latest":
            return False
        
        try:
            current_parts = [int(x) for x in current.split('.')]
            latest_parts = [int(x) for x in latest.split('.')]
            
            # Pad shorter version with zeros
            max_len = max(len(current_parts), len(latest_parts))
            current_parts.extend([0] * (max_len - len(current_parts)))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            
            return current_parts < latest_parts
        except Exception:
            return False
    
    def _assess_dependency_risk(self, dep_info: Dict[str, Any]) -> str:
        """Assess risk level of a dependency"""
        risk_score = 0
        
        # Check if outdated
        if dep_info.get("is_outdated", False):
            risk_score += 2
        
        # Check if has vulnerabilities
        if dep_info.get("has_vulnerabilities", False):
            risk_score += 3
        
        # Check if production dependency
        if dep_info.get("is_production", True):
            risk_score += 1
        
        # Check version constraints
        version_spec = dep_info.get("version_spec", "")
        if ">=0.0.0" in version_spec or "*" in version_spec:
            risk_score += 1  # Too permissive
        
        if risk_score >= 4:
            return "high"
        elif risk_score >= 2:
            return "medium"
        else:
            return "low"
    
    def _analyze_licenses(self, dependencies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze license compatibility"""
        license_issues = []
        
        # Define problematic licenses
        problematic_licenses = [
            'GPL-3.0', 'GPL-2.0', 'AGPL-3.0', 'AGPL-1.0',
            'CPAL-1.0', 'EPL-1.0', 'EPL-2.0'
        ]
        
        for dep in dependencies:
            license_info = dep.get("license")
            if license_info and license_info in problematic_licenses:
                license_issues.append({
                    "dependency": dep["name"],
                    "license": license_info,
                    "severity": "medium",
                    "description": f"Dependency uses {license_info} license which may have restrictions",
                    "recommendation": "Review license compatibility with your project"
                })
        
        return {"issues": license_issues}
    
    def _build_dependency_tree(self, ecosystems: Dict[str, Any]) -> Dict[str, Any]:
        """Build dependency tree structure"""
        tree = {}
        
        for ecosystem_name, ecosystem_data in ecosystems.items():
            dependencies = ecosystem_data.get("dependencies", [])
            
            tree[ecosystem_name] = {
                "total_dependencies": len(dependencies),
                "direct_dependencies": len([d for d in dependencies if d.get("is_direct", True)]),
                "production_dependencies": len([d for d in dependencies if d.get("is_production", True)]),
                "development_dependencies": len([d for d in dependencies if not d.get("is_production", True)]),
                "outdated_dependencies": len([d for d in dependencies if d.get("is_outdated", False)]),
                "high_risk_dependencies": len([d for d in dependencies if d.get("risk_level") == "high"])
            }
        
        return tree
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate dependency management recommendations"""
        recommendations = []
        
        summary = results["summary"]
        
        if summary.get("outdated_count", 0) > 0:
            recommendations.append(f"📦 Update {summary['outdated_count']} outdated dependencies to latest versions")
        
        if summary.get("vulnerable_count", 0) > 0:
            recommendations.append(f"🚨 Address {summary['vulnerable_count']} dependencies with known vulnerabilities")
        
        if summary.get("high_risk_dependencies", 0) > 0:
            recommendations.append(f"⚠️ Review {summary['high_risk_dependencies']} high-risk dependencies")
        
        if summary.get("license_issues_count", 0) > 0:
            recommendations.append(f"⚖️ Review {summary['license_issues_count']} license compatibility issues")
        
        recommendations.extend([
            "🔄 Set up automated dependency updates (e.g., Dependabot, Renovate)",
            "🔍 Implement dependency scanning in CI/CD pipeline",
            "📋 Maintain a dependency inventory and review policy",
            "🎯 Consider using dependency pinning for production deployments"
        ])
        
        return recommendations[:6]  # Limit to top 6 recommendations
    
    # Placeholder methods for other ecosystems
    def _analyze_poetry_dependencies(self, poetry_file: Path) -> Dict[str, Any]:
        return {"ecosystem": "poetry", "dependencies": [], "build_tools": []}
    
    def _analyze_gradle_dependencies(self, gradle_file: Path) -> Dict[str, Any]:
        return {"ecosystem": "gradle", "dependencies": [], "build_tools": []}
    
    def _analyze_ruby_dependencies(self, gemfile: Path) -> Dict[str, Any]:
        return {"ecosystem": "ruby", "dependencies": [], "build_tools": []}
    
    def _analyze_php_dependencies(self, composer_file: Path) -> Dict[str, Any]:
        return {"ecosystem": "composer", "dependencies": [], "build_tools": []}
    
    def _analyze_go_dependencies(self, go_mod: Path) -> Dict[str, Any]:
        return {"ecosystem": "go", "dependencies": [], "build_tools": []}
    
    def _analyze_rust_dependencies(self, cargo_file: Path) -> Dict[str, Any]:
        return {"ecosystem": "cargo", "dependencies": [], "build_tools": []} 