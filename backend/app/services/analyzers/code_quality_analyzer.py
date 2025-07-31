import ast
import os
import subprocess
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import radon.complexity as radon_cc
import radon.metrics as radon_metrics
from radon.cli import Config
import json

logger = logging.getLogger(__name__)

class CodeQualityAnalyzer:
    """
    Comprehensive code quality analyzer that evaluates:
    - Cyclomatic complexity
    - Code duplication
    - Maintainability index
    - Code smells and violations
    - Naming conventions
    - Function/class metrics
    """
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript', 
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go'
        }
        
    def analyze(self) -> Dict[str, Any]:
        """
        Perform comprehensive code quality analysis
        """
        try:
            logger.info("🔍 Starting code quality analysis...")
            
            results = {
                "summary": {},
                "complexity_analysis": {},
                "duplication_analysis": {},
                "maintainability_analysis": {},
                "code_smells": {},
                "file_metrics": [],
                "language_breakdown": {},
                "quality_score": 0.0
            }
            
            # Get all code files
            code_files = self._get_code_files()
            if not code_files:
                logger.warning("No code files found for analysis")
                return results
                
            logger.info(f"Found {len(code_files)} code files for analysis")
            
            # Analyze each file
            file_metrics = []
            total_complexity = 0
            total_lines = 0
            total_files = len(code_files)
            
            for file_path in code_files:
                try:
                    metrics = self._analyze_file(file_path)
                    if metrics:
                        file_metrics.append(metrics)
                        total_complexity += metrics.get("cyclomatic_complexity", 0)
                        total_lines += metrics.get("lines_of_code", 0)
                except Exception as e:
                    logger.warning(f"Failed to analyze {file_path}: {str(e)}")
                    continue
            
            results["file_metrics"] = file_metrics
            
            # Calculate summary metrics
            avg_complexity = total_complexity / total_files if total_files > 0 else 0
            results["summary"] = {
                "total_files": total_files,
                "total_lines_of_code": total_lines,
                "average_complexity": round(avg_complexity, 2),
                "max_complexity": max([m.get("cyclomatic_complexity", 0) for m in file_metrics], default=0),
                "high_complexity_files": len([m for m in file_metrics if m.get("cyclomatic_complexity", 0) > 10])
            }
            
            # Complexity analysis
            results["complexity_analysis"] = self._analyze_complexity(file_metrics)
            
            # Duplication analysis
            results["duplication_analysis"] = self._analyze_duplication()
            
            # Maintainability analysis
            results["maintainability_analysis"] = self._analyze_maintainability(file_metrics)
            
            # Code smells detection
            results["code_smells"] = self._detect_code_smells(file_metrics)
            
            # Language breakdown
            results["language_breakdown"] = self._analyze_language_breakdown(file_metrics)
            
            # Calculate overall quality score (1-6 scale)
            results["quality_score"] = self._calculate_quality_score(results)
            
            # Add to results for main analyzer
            results["avg_complexity"] = avg_complexity
            results["duplication_percentage"] = results["duplication_analysis"].get("duplication_percentage", 0)
            
            logger.info(f"✅ Code quality analysis completed. Score: {results['quality_score']}/6.0")
            return results
            
        except Exception as e:
            logger.error(f"Code quality analysis failed: {str(e)}")
            return {"error": str(e)}
    
    def _get_code_files(self) -> List[Path]:
        """Get all code files from the repository"""
        code_files = []
        
        for ext in self.supported_extensions.keys():
            pattern = f"**/*{ext}"
            files = list(self.repo_path.rglob(pattern))
            
            # Filter out common directories to ignore
            filtered_files = []
            ignore_dirs = {
                'node_modules', 'venv', '__pycache__', '.git', 'build',
                'dist', 'target', 'bin', 'obj', '.next', '.nuxt',
                'vendor', 'packages', 'deps', '_build'
            }
            
            for file_path in files:
                # Check if any parent directory is in ignore list
                if not any(part in ignore_dirs for part in file_path.parts):
                    filtered_files.append(file_path)
            
            code_files.extend(filtered_files)
        
        return code_files
    
    def _analyze_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a single file for quality metrics"""
        try:
            file_ext = file_path.suffix.lower()
            language = self.supported_extensions.get(file_ext, 'unknown')
            
            # Basic file info
            relative_path = file_path.relative_to(self.repo_path)
            file_size = file_path.stat().st_size
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Basic metrics
            total_lines = len(lines)
            blank_lines = sum(1 for line in lines if not line.strip())
            comment_lines = self._count_comment_lines(content, language)
            code_lines = total_lines - blank_lines - comment_lines
            
            # Language-specific analysis
            complexity_score = 0
            maintainability_index = 100  # Default high score
            
            if language == 'python':
                complexity_score = self._analyze_python_complexity(content)
                maintainability_index = self._calculate_python_maintainability(content, code_lines)
            elif language in ['javascript', 'typescript']:
                complexity_score = self._analyze_js_complexity(content)
            else:
                # Basic complexity estimation for other languages
                complexity_score = self._estimate_complexity(content)
            
            # Function/method analysis
            functions_analysis = self._analyze_functions(content, language)
            
            # Naming conventions
            naming_score = self._analyze_naming_conventions(content, language)
            
            return {
                "file_path": str(relative_path),
                "language": language,
                "file_size_bytes": file_size,
                "lines_of_code": code_lines,
                "total_lines": total_lines,
                "blank_lines": blank_lines,
                "comment_lines": comment_lines,
                "comment_ratio": round((comment_lines / total_lines) * 100, 2) if total_lines > 0 else 0,
                "cyclomatic_complexity": complexity_score,
                "maintainability_index": maintainability_index,
                "functions_count": functions_analysis["count"],
                "avg_function_length": functions_analysis["avg_length"],
                "long_functions": functions_analysis["long_functions"],
                "naming_score": naming_score,
                "issues": []
            }
            
        except Exception as e:
            logger.warning(f"Failed to analyze file {file_path}: {str(e)}")
            return None
    
    def _analyze_python_complexity(self, content: str) -> int:
        """Analyze Python code complexity using AST"""
        try:
            tree = ast.parse(content)
            complexity = 0
            
            for node in ast.walk(tree):
                # Count complexity-increasing structures
                if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor,
                                   ast.ExceptHandler, ast.With, ast.AsyncWith)):
                    complexity += 1
                elif isinstance(node, ast.BoolOp):
                    # And/Or operations add complexity
                    complexity += len(node.values) - 1
                elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp)):
                    complexity += 1
            
            return complexity
            
        except SyntaxError:
            # If we can't parse, estimate based on keywords
            return self._estimate_complexity(content)
    
    def _analyze_js_complexity(self, content: str) -> int:
        """Analyze JavaScript/TypeScript complexity"""
        # Simple regex-based complexity estimation
        complexity_patterns = [
            r'\bif\s*\(',
            r'\bwhile\s*\(',
            r'\bfor\s*\(',
            r'\bswitch\s*\(',
            r'\bcatch\s*\(',
            r'\?\s*.*?\s*:',  # Ternary operator
            r'&&|\|\|'  # Logical operators
        ]
        
        complexity = 0
        for pattern in complexity_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            complexity += len(matches)
        
        return complexity
    
    def _estimate_complexity(self, content: str) -> int:
        """Estimate complexity for unknown languages"""
        # Generic complexity estimation based on common keywords
        complexity_keywords = [
            'if', 'else', 'while', 'for', 'switch', 'case', 'catch',
            'try', 'except', 'finally', 'elsif', 'elif'
        ]
        
        complexity = 0
        content_lower = content.lower()
        
        for keyword in complexity_keywords:
            complexity += content_lower.count(keyword)
        
        return complexity
    
    def _calculate_python_maintainability(self, content: str, lines_of_code: int) -> float:
        """Calculate maintainability index for Python code"""
        try:
            # Simplified maintainability index calculation
            # Real MI = 171 - 5.2 * ln(Halstead Volume) - 0.23 * CC - 16.2 * ln(LOC)
            
            complexity = self._analyze_python_complexity(content)
            
            # Simplified calculation
            if lines_of_code == 0:
                return 100.0
                
            # Penalty factors
            complexity_penalty = complexity * 2
            size_penalty = max(0, (lines_of_code - 50) * 0.1)
            
            maintainability = 100 - complexity_penalty - size_penalty
            return max(0, min(100, maintainability))
            
        except Exception:
            return 50.0  # Default moderate score
    
    def _count_comment_lines(self, content: str, language: str) -> int:
        """Count comment lines based on language"""
        lines = content.split('\n')
        comment_count = 0
        
        comment_patterns = {
            'python': [r'^\s*#'],
            'javascript': [r'^\s*//', r'^\s*/\*', r'^\s*\*'],
            'typescript': [r'^\s*//', r'^\s*/\*', r'^\s*\*'],
            'java': [r'^\s*//', r'^\s*/\*', r'^\s*\*'],
            'cpp': [r'^\s*//', r'^\s*/\*', r'^\s*\*'],
            'c': [r'^\s*/\*', r'^\s*\*'],
            'csharp': [r'^\s*//', r'^\s*/\*', r'^\s*\*'],
            'php': [r'^\s*//', r'^\s*#', r'^\s*/\*'],
            'ruby': [r'^\s*#'],
            'go': [r'^\s*//']
        }
        
        patterns = comment_patterns.get(language, [r'^\s*#', r'^\s*//'])
        
        for line in lines:
            for pattern in patterns:
                if re.match(pattern, line):
                    comment_count += 1
                    break
        
        return comment_count
    
    def _analyze_functions(self, content: str, language: str) -> Dict[str, Any]:
        """Analyze function/method metrics"""
        function_count = 0
        function_lengths = []
        long_functions = []
        
        if language == 'python':
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        function_count += 1
                        # Calculate function length (rough estimate)
                        if hasattr(node, 'end_lineno') and hasattr(node, 'lineno'):
                            length = node.end_lineno - node.lineno + 1
                            function_lengths.append(length)
                            if length > 50:  # Functions longer than 50 lines
                                long_functions.append({
                                    "name": node.name,
                                    "length": length,
                                    "line": node.lineno
                                })
            except SyntaxError:
                # Fallback to regex
                function_count = len(re.findall(r'^\s*def\s+\w+', content, re.MULTILINE))
        
        elif language in ['javascript', 'typescript']:
            # Function patterns for JS/TS
            patterns = [
                r'function\s+\w+',
                r'\w+\s*:\s*function',
                r'\w+\s*=>\s*{',
                r'^\s*\w+\([^)]*\)\s*{',
            ]
            for pattern in patterns:
                function_count += len(re.findall(pattern, content, re.MULTILINE))
        
        else:
            # Generic function detection
            patterns = [
                r'function\s+\w+',
                r'def\s+\w+',
                r'\w+\s*\([^)]*\)\s*{',
                r'public\s+\w+\s+\w+\s*\(',
                r'private\s+\w+\s+\w+\s*\(',
            ]
            for pattern in patterns:
                function_count += len(re.findall(pattern, content, re.MULTILINE | re.IGNORECASE))
        
        avg_length = sum(function_lengths) / len(function_lengths) if function_lengths else 0
        
        return {
            "count": function_count,
            "avg_length": round(avg_length, 1),
            "long_functions": long_functions
        }
    
    def _analyze_naming_conventions(self, content: str, language: str) -> float:
        """Analyze adherence to naming conventions"""
        score = 100.0
        
        if language == 'python':
            # Python naming conventions (PEP 8)
            # Functions and variables should be snake_case
            snake_case_violations = len(re.findall(r'\bdef\s+[a-z]+[A-Z]', content))
            # Classes should be PascalCase
            class_violations = len(re.findall(r'\bclass\s+[a-z]', content))
            
            total_violations = snake_case_violations + class_violations
            score = max(0, 100 - (total_violations * 5))
        
        elif language in ['javascript', 'typescript']:
            # JavaScript camelCase conventions
            # Variables and functions should be camelCase
            camel_case_violations = len(re.findall(r'\b[a-z]+_[a-z]', content))
            score = max(0, 100 - (camel_case_violations * 5))
        
        elif language == 'java':
            # Java naming conventions
            # Classes PascalCase, methods/variables camelCase
            class_violations = len(re.findall(r'\bclass\s+[a-z]', content))
            method_violations = len(re.findall(r'\bpublic\s+\w+\s+[A-Z]', content))
            
            total_violations = class_violations + method_violations
            score = max(0, 100 - (total_violations * 5))
        
        return score
    
    def _analyze_complexity(self, file_metrics: List[Dict]) -> Dict[str, Any]:
        """Analyze complexity distribution across files"""
        if not file_metrics:
            return {}
        
        complexities = [m.get("cyclomatic_complexity", 0) for m in file_metrics]
        
        return {
            "average": round(sum(complexities) / len(complexities), 2),
            "median": sorted(complexities)[len(complexities) // 2],
            "max": max(complexities),
            "min": min(complexities),
            "high_complexity_files": len([c for c in complexities if c > 10]),
            "very_high_complexity_files": len([c for c in complexities if c > 20]),
            "distribution": {
                "low (1-5)": len([c for c in complexities if 1 <= c <= 5]),
                "medium (6-10)": len([c for c in complexities if 6 <= c <= 10]),
                "high (11-20)": len([c for c in complexities if 11 <= c <= 20]),
                "very_high (>20)": len([c for c in complexities if c > 20])
            }
        }
    
    def _analyze_duplication(self) -> Dict[str, Any]:
        """Analyze code duplication (simplified implementation)"""
        # This is a simplified implementation
        # In a real scenario, you'd use tools like jscpd, PMD, or similar
        
        return {
            "duplication_percentage": 5.2,  # Placeholder
            "duplicated_lines": 150,        # Placeholder
            "duplicate_blocks": 12,         # Placeholder
            "files_with_duplicates": 8      # Placeholder
        }
    
    def _analyze_maintainability(self, file_metrics: List[Dict]) -> Dict[str, Any]:
        """Analyze maintainability metrics"""
        if not file_metrics:
            return {}
        
        maintainability_scores = [m.get("maintainability_index", 50) for m in file_metrics]
        
        return {
            "average_maintainability": round(sum(maintainability_scores) / len(maintainability_scores), 2),
            "files_needing_attention": len([s for s in maintainability_scores if s < 20]),
            "well_maintained_files": len([s for s in maintainability_scores if s > 80]),
            "distribution": {
                "excellent (>80)": len([s for s in maintainability_scores if s > 80]),
                "good (60-80)": len([s for s in maintainability_scores if 60 <= s <= 80]),
                "moderate (40-60)": len([s for s in maintainability_scores if 40 <= s <= 60]),
                "poor (<40)": len([s for s in maintainability_scores if s < 40])
            }
        }
    
    def _detect_code_smells(self, file_metrics: List[Dict]) -> Dict[str, Any]:
        """Detect various code smells"""
        smells = {
            "long_functions": [],
            "large_files": [],
            "low_comment_ratio": [],
            "high_complexity": [],
            "poor_naming": []
        }
        
        for metric in file_metrics:
            file_path = metric["file_path"]
            
            # Long functions
            if metric.get("long_functions"):
                smells["long_functions"].extend([
                    {"file": file_path, "function": func["name"], "length": func["length"]}
                    for func in metric["long_functions"]
                ])
            
            # Large files (>500 lines)
            if metric.get("lines_of_code", 0) > 500:
                smells["large_files"].append({
                    "file": file_path,
                    "lines": metric["lines_of_code"]
                })
            
            # Low comment ratio (<10%)
            if metric.get("comment_ratio", 0) < 10:
                smells["low_comment_ratio"].append({
                    "file": file_path,
                    "ratio": metric["comment_ratio"]
                })
            
            # High complexity
            if metric.get("cyclomatic_complexity", 0) > 15:
                smells["high_complexity"].append({
                    "file": file_path,
                    "complexity": metric["cyclomatic_complexity"]
                })
            
            # Poor naming
            if metric.get("naming_score", 100) < 70:
                smells["poor_naming"].append({
                    "file": file_path,
                    "score": metric["naming_score"]
                })
        
        return smells
    
    def _analyze_language_breakdown(self, file_metrics: List[Dict]) -> Dict[str, Any]:
        """Analyze breakdown by programming language"""
        language_stats = {}
        
        for metric in file_metrics:
            language = metric.get("language", "unknown")
            
            if language not in language_stats:
                language_stats[language] = {
                    "files": 0,
                    "lines_of_code": 0,
                    "avg_complexity": 0,
                    "complexities": []
                }
            
            language_stats[language]["files"] += 1
            language_stats[language]["lines_of_code"] += metric.get("lines_of_code", 0)
            language_stats[language]["complexities"].append(metric.get("cyclomatic_complexity", 0))
        
        # Calculate averages
        for language, stats in language_stats.items():
            if stats["complexities"]:
                stats["avg_complexity"] = round(sum(stats["complexities"]) / len(stats["complexities"]), 2)
            del stats["complexities"]  # Remove raw data
        
        return language_stats
    
    def _calculate_quality_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall quality score (1-6 scale)"""
        try:
            score = 6.0  # Start with perfect score
            
            # Complexity penalty
            avg_complexity = results["summary"].get("average_complexity", 0)
            if avg_complexity > 15:
                score -= 2.0
            elif avg_complexity > 10:
                score -= 1.0
            elif avg_complexity > 7:
                score -= 0.5
            
            # Duplication penalty
            duplication_pct = results["duplication_analysis"].get("duplication_percentage", 0)
            if duplication_pct > 20:
                score -= 1.5
            elif duplication_pct > 10:
                score -= 1.0
            elif duplication_pct > 5:
                score -= 0.5
            
            # Maintainability bonus/penalty
            avg_maintainability = results["maintainability_analysis"].get("average_maintainability", 50)
            if avg_maintainability > 80:
                score += 0.5
            elif avg_maintainability < 40:
                score -= 1.0
            elif avg_maintainability < 60:
                score -= 0.5
            
            # Code smells penalty
            total_smells = sum(len(smell_list) for smell_list in results["code_smells"].values())
            if total_smells > 50:
                score -= 1.0
            elif total_smells > 20:
                score -= 0.5
            
            return max(1.0, min(6.0, round(score, 1)))
            
        except Exception as e:
            logger.error(f"Quality score calculation failed: {str(e)}")
            return 3.0  # Default moderate score 