import os
import shutil
import tempfile
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import git
from git import Repo, GitCommandError
import chardet
import subprocess
import json

logger = logging.getLogger(__name__)

class RepositoryService:
    """Service for repository cloning and file analysis"""
    
    def __init__(self):
        self.temp_dir = None
        self.repo_path = None
        self.repo = None
    
    async def clone_repository(self, repo_url: str, github_token: Optional[str] = None) -> Dict[str, Any]:
        """
        Clone repository and prepare for analysis
        
        Args:
            repo_url: Git repository URL
            github_token: Optional GitHub token for private repos
            
        Returns:
            Repository metadata and status
        """
        
        try:
            # Create temporary directory
            self.temp_dir = tempfile.mkdtemp(prefix="ai_mvise_")
            self.repo_path = os.path.join(self.temp_dir, "repo")
            
            logger.info(f"Cloning repository: {repo_url}")
            
            # Prepare clone URL with token if provided
            clone_url = self._prepare_clone_url(repo_url, github_token)
            
            # Clone repository
            self.repo = Repo.clone_from(clone_url, self.repo_path)
            
            # Get repository metadata
            repo_info = await self._extract_repo_metadata()
            
            logger.info(f"Successfully cloned repository: {repo_info['name']}")
            return {
                "status": "success",
                "repo_path": self.repo_path,
                "repo_info": repo_info
            }
            
        except GitCommandError as e:
            logger.error(f"Git clone error: {e}")
            return {"status": "error", "message": f"Failed to clone repository: {e}"}
        except Exception as e:
            logger.error(f"Repository clone failed: {e}")
            return {"status": "error", "message": str(e)}
    
    async def analyze_code_files(self) -> Dict[str, Any]:
        """
        Analyze all code files in the repository
        
        Returns:
            Dictionary of filename -> content and metadata
        """
        
        if not self.repo_path:
            raise ValueError("Repository not cloned yet")
        
        code_files = {}
        file_stats = {
            "total_files": 0,
            "code_files": 0,
            "lines_of_code": 0,
            "file_types": {},
            "languages": set()
        }
        
        try:
            for root, dirs, files in os.walk(self.repo_path):
                # Skip .git and other hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    if file.startswith('.'):
                        continue
                    
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, self.repo_path)
                    
                    file_stats["total_files"] += 1
                    
                    # Check if it's a code file
                    if self._is_code_file(file):
                        try:
                            content = await self._read_file_content(file_path)
                            if content:
                                code_files[relative_path] = content
                                file_stats["code_files"] += 1
                                file_stats["lines_of_code"] += len(content.split('\n'))
                                
                                # Track file extension
                                ext = Path(file).suffix.lower()
                                file_stats["file_types"][ext] = file_stats["file_types"].get(ext, 0) + 1
                                
                                # Detect programming language
                                language = self._detect_language(ext)
                                if language:
                                    file_stats["languages"].add(language)
                        
                        except Exception as e:
                            logger.warning(f"Failed to read file {relative_path}: {e}")
            
            file_stats["languages"] = list(file_stats["languages"])
            
            return {
                "code_files": code_files,
                "file_stats": file_stats
            }
            
        except Exception as e:
            logger.error(f"File analysis failed: {e}")
            return {"error": str(e)}
    
    async def run_static_analysis(self) -> Dict[str, Any]:
        """
        Run static analysis tools on the repository
        
        Returns:
            Combined results from multiple analysis tools
        """
        
        if not self.repo_path:
            raise ValueError("Repository not cloned yet")
        
        results = {
            "complexity": {},
            "security": {},
            "quality": {},
            "dependencies": {}
        }
        
        try:
            # Run analyses in parallel
            tasks = [
                self._run_complexity_analysis(),
                self._run_security_analysis(), 
                self._run_dependency_analysis()
            ]
            
            complexity_results, security_results, dependency_results = await asyncio.gather(
                *tasks, return_exceptions=True
            )
            
            # Collect results (handle exceptions)
            if not isinstance(complexity_results, Exception):
                results["complexity"] = complexity_results
            if not isinstance(security_results, Exception):
                results["security"] = security_results
            if not isinstance(dependency_results, Exception):
                results["dependencies"] = dependency_results
            
            # Add basic quality metrics (without pylint)
            results["quality"] = await self._run_basic_quality_analysis()
            
            return results
            
        except Exception as e:
            logger.error(f"Static analysis failed: {e}")
            return {"error": str(e)}
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.info("Cleanup completed")
            except Exception as e:
                logger.error(f"Cleanup failed: {e}")
    
    def _prepare_clone_url(self, repo_url: str, github_token: Optional[str]) -> str:
        """Prepare clone URL with authentication if needed"""
        
        if github_token and "github.com" in repo_url:
            # Convert HTTPS URL to use token
            if repo_url.startswith("https://github.com/"):
                repo_url = repo_url.replace("https://github.com/", f"https://{github_token}@github.com/")
            elif repo_url.startswith("git@github.com:"):
                # Convert SSH to HTTPS with token
                repo_url = repo_url.replace("git@github.com:", f"https://{github_token}@github.com/")
                if repo_url.endswith(".git"):
                    repo_url = repo_url[:-4]
        
        return repo_url
    
    async def _extract_repo_metadata(self) -> Dict[str, Any]:
        """Extract metadata from the cloned repository"""
        
        try:
            # Basic repo info
            repo_name = os.path.basename(self.repo.working_dir)
            
            # Git info
            try:
                latest_commit = self.repo.head.commit
                commit_info = {
                    "hash": latest_commit.hexsha[:8],
                    "message": latest_commit.message.strip(),
                    "author": str(latest_commit.author),
                    "date": latest_commit.committed_datetime.isoformat()
                }
            except:
                commit_info = {}
            
            # Count files and estimate size
            file_count = 0
            for root, dirs, files in os.walk(self.repo_path):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                file_count += len([f for f in files if not f.startswith('.')])
            
            return {
                "name": repo_name,
                "path": self.repo_path,
                "file_count": file_count,
                "latest_commit": commit_info,
                "languages": [],  # Will be filled by file analysis
                "lines_of_code": 0  # Will be filled by file analysis
            }
            
        except Exception as e:
            logger.error(f"Failed to extract repo metadata: {e}")
            return {"name": "Unknown", "error": str(e)}
    
    async def _read_file_content(self, file_path: str) -> Optional[str]:
        """Read and decode file content"""
        
        try:
            # Read raw bytes
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            
            # Skip very large files (>1MB)
            if len(raw_data) > 1024 * 1024:
                return None
            
            # Detect encoding
            result = chardet.detect(raw_data)
            encoding = result.get('encoding', 'utf-8')
            
            if not encoding:
                encoding = 'utf-8'
            
            # Decode content
            try:
                content = raw_data.decode(encoding)
                return content
            except UnicodeDecodeError:
                # Fallback to utf-8 with error handling
                content = raw_data.decode('utf-8', errors='ignore')
                return content
                
        except Exception as e:
            logger.warning(f"Failed to read file {file_path}: {e}")
            return None
    
    def _is_code_file(self, filename: str) -> bool:
        """Check if file is a code file"""
        
        code_extensions = {
            # Programming languages
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.php', '.rb', '.go', '.rs', '.kt', '.swift', '.scala',
            '.r', '.sql', '.sh', '.bash', '.ps1',
            
            # Web technologies
            '.html', '.htm', '.css', '.scss', '.sass', '.less', '.vue',
            
            # Configuration files
            '.json', '.yaml', '.yml', '.xml', '.toml', '.ini', '.cfg',
            '.conf', '.config', '.env',
            
            # Documentation
            '.md', '.txt', '.rst', '.adoc',
            
            # Build files
            '.dockerfile', '.dockerignore', '.gitignore', '.gitattributes'
        }
        
        ext = Path(filename).suffix.lower()
        return ext in code_extensions or filename.lower() in ['dockerfile', 'makefile', 'rakefile']
    
    def _detect_language(self, extension: str) -> Optional[str]:
        """Detect programming language from file extension"""
        
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript', 
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'React TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.rs': 'Rust',
            '.kt': 'Kotlin',
            '.swift': 'Swift',
            '.scala': 'Scala',
            '.r': 'R',
            '.sql': 'SQL',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.vue': 'Vue.js',
            '.sh': 'Shell',
            '.bash': 'Bash'
        }
        
        return language_map.get(extension.lower())
    
    async def _run_complexity_analysis(self) -> Dict[str, Any]:
        """Run code complexity analysis using Radon"""
        
        try:
            # Find Python files for complexity analysis
            python_files = []
            for root, dirs, files in os.walk(self.repo_path):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
            
            if not python_files:
                return {"message": "No Python files found for complexity analysis"}
            
            # Run radon for cyclomatic complexity
            cmd = ['radon', 'cc', '--json'] + python_files
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode == 0:
                complexity_data = json.loads(result.stdout)
                
                # Calculate average complexity
                total_complexity = 0
                function_count = 0
                
                for file_path, file_data in complexity_data.items():
                    for item in file_data:
                        if item['type'] in ['function', 'method']:
                            total_complexity += item['complexity']
                            function_count += 1
                
                avg_complexity = total_complexity / function_count if function_count > 0 else 0
                
                return {
                    "average_complexity": round(avg_complexity, 2),
                    "total_functions": function_count,
                    "complexity_data": complexity_data,
                    "high_complexity_functions": [
                        {"file": k, "function": item["name"], "complexity": item["complexity"]}
                        for k, v in complexity_data.items()
                        for item in v
                        if item.get("complexity", 0) > 10
                    ]
                }
            else:
                return {"error": f"Radon failed: {result.stderr}"}
                
        except Exception as e:
            logger.error(f"Complexity analysis failed: {e}")
            return {"error": str(e)}
    
    async def _run_security_analysis(self) -> Dict[str, Any]:
        """Run security analysis using Bandit"""
        
        try:
            # Run bandit for Python security analysis
            cmd = ['bandit', '-r', self.repo_path, '-f', 'json']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode in [0, 1]:  # Bandit returns 1 if issues found
                try:
                    security_data = json.loads(result.stdout)
                    
                    vulnerabilities = []
                    for result_item in security_data.get('results', []):
                        vulnerabilities.append({
                            "type": result_item.get('test_name', 'Unknown'),
                            "severity": result_item.get('issue_severity', 'Unknown'),
                            "confidence": result_item.get('issue_confidence', 'Unknown'),
                            "file": result_item.get('filename', ''),
                            "line": result_item.get('line_number', 0),
                            "description": result_item.get('issue_text', ''),
                            "fix_suggestion": result_item.get('more_info', '')
                        })
                    
                    # Calculate risk level
                    high_severity_count = len([v for v in vulnerabilities if v['severity'] == 'HIGH'])
                    medium_severity_count = len([v for v in vulnerabilities if v['severity'] == 'MEDIUM'])
                    
                    if high_severity_count > 0:
                        risk_level = "high"
                    elif medium_severity_count > 3:
                        risk_level = "medium"
                    elif len(vulnerabilities) > 0:
                        risk_level = "low"
                    else:
                        risk_level = "minimal"
                    
                    return {
                        "vulnerabilities": vulnerabilities,
                        "risk_level": risk_level,
                        "total_issues": len(vulnerabilities),
                        "high_severity": high_severity_count,
                        "medium_severity": medium_severity_count,
                        "bandit_issues": len(vulnerabilities)
                    }
                    
                except json.JSONDecodeError:
                    return {"error": "Failed to parse Bandit output"}
            else:
                return {"error": f"Bandit failed: {result.stderr}"}
                
        except Exception as e:
            logger.error(f"Security analysis failed: {e}")
            return {"error": str(e), "vulnerabilities": [], "risk_level": "unknown"}
    
    async def _run_basic_quality_analysis(self) -> Dict[str, Any]:
        """Run basic quality analysis without pylint"""
        
        try:
            # Find Python files
            python_files = []
            for root, dirs, files in os.walk(self.repo_path):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                for file in files:
                    if file.endswith('.py'):
                        python_files.append(os.path.join(root, file))
            
            if not python_files:
                return {"message": "No Python files found for quality analysis"}
            
            # Basic quality metrics without external tools
            quality_metrics = {
                "linting_issues": 0,  # Placeholder - would use pylint in full version
                "code_smells": [],
                "file_count": len(python_files),
                "estimated_quality_score": 75  # Placeholder score
            }
            
            # Simple code smell detection
            code_smells = []
            for file_path in python_files[:5]:  # Check first 5 files
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        
                        # Basic code smell detection
                        for i, line in enumerate(lines, 1):
                            line = line.strip()
                            if len(line) > 120:  # Long lines
                                code_smells.append({
                                    "type": "Long Line",
                                    "file": os.path.basename(file_path),
                                    "line": i,
                                    "message": f"Line {i} is too long ({len(line)} chars)"
                                })
                            elif line and not line.startswith('#') and 'TODO' in line.upper():
                                code_smells.append({
                                    "type": "TODO Comment",
                                    "file": os.path.basename(file_path),
                                    "line": i,
                                    "message": f"TODO comment found on line {i}"
                                })
                except Exception:
                    continue
            
            quality_metrics["code_smells"] = code_smells[:10]  # Limit to 10
            quality_metrics["linting_issues"] = len(code_smells)
            
            return quality_metrics
                
        except Exception as e:
            logger.error(f"Quality analysis failed: {e}")
            return {"error": str(e)}
    
    async def _run_dependency_analysis(self) -> Dict[str, Any]:
        """Analyze project dependencies"""
        
        try:
            dependencies = {
                "python": [],
                "javascript": [],
                "outdated_count": 0,
                "vulnerable_count": 0
            }
            
            # Check for Python requirements
            requirements_files = ['requirements.txt', 'Pipfile', 'pyproject.toml']
            for req_file in requirements_files:
                req_path = os.path.join(self.repo_path, req_file)
                if os.path.exists(req_path):
                    deps = await self._analyze_python_dependencies(req_path)
                    dependencies["python"].extend(deps)
                    break
            
            # Check for JavaScript/Node.js dependencies
            package_json_path = os.path.join(self.repo_path, 'package.json')
            if os.path.exists(package_json_path):
                deps = await self._analyze_javascript_dependencies(package_json_path)
                dependencies["javascript"].extend(deps)
            
            # Estimate outdated packages (simplified)
            total_deps = len(dependencies["python"]) + len(dependencies["javascript"])
            dependencies["outdated_count"] = max(0, int(total_deps * 0.2))  # Assume ~20% might be outdated
            dependencies["vulnerable_count"] = max(0, int(total_deps * 0.05))  # Assume ~5% might have vulnerabilities
            
            return dependencies
            
        except Exception as e:
            logger.error(f"Dependency analysis failed: {e}")
            return {"error": str(e)}
    
    async def _analyze_python_dependencies(self, requirements_path: str) -> List[Dict[str, str]]:
        """Analyze Python dependencies from requirements file"""
        
        try:
            dependencies = []
            with open(requirements_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Simple parsing - just extract package name
                        package_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0].strip()
                        if package_name:
                            dependencies.append({
                                "name": package_name,
                                "type": "python",
                                "source": os.path.basename(requirements_path)
                            })
            return dependencies
        except Exception as e:
            logger.error(f"Failed to analyze Python dependencies: {e}")
            return []
    
    async def _analyze_javascript_dependencies(self, package_json_path: str) -> List[Dict[str, str]]:
        """Analyze JavaScript dependencies from package.json"""
        
        try:
            dependencies = []
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            # Extract dependencies and devDependencies
            for dep_type in ['dependencies', 'devDependencies']:
                if dep_type in package_data:
                    for package_name in package_data[dep_type]:
                        dependencies.append({
                            "name": package_name,
                            "type": "javascript",
                            "source": "package.json",
                            "dev": dep_type == "devDependencies"
                        })
            
            return dependencies
        except Exception as e:
            logger.error(f"Failed to analyze JavaScript dependencies: {e}")
            return [] 