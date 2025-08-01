import boto3
import json
import logging
from typing import Dict, Any, Optional, List
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class BedrockService:
    """Amazon Bedrock Claude service for code analysis"""
    
    def __init__(self, region_name: str = "us-east-1"):
        """
        Initialize Bedrock client
        
        Args:
            region_name: AWS region for Bedrock
        """
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=region_name
            )
            self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"  # Claude 3.5 Sonnet (verified working)
            # Alternative models if the above doesn't work:
            # self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
            # self.model_id = "anthropic.claude-instant-v1"
            logger.info(f"Bedrock client initialized with model: {self.model_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {e}")
            raise
    
    async def analyze_repository_comprehensive(self, 
                                             code_files: Dict[str, str], 
                                             repo_info: Dict[str, Any],
                                             static_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive repository analysis - everything in one detailed analysis
        
        Args:
            code_files: Dictionary of filename -> code content
            repo_info: Repository metadata
            static_results: Results from static analysis tools
            
        Returns:
            Complete comprehensive analysis results
        """
        
        try:
            # Create comprehensive analysis prompt that covers everything
            prompt = self._create_comprehensive_analysis_prompt(code_files, repo_info, static_results)
            response = await self._call_claude(prompt)
            result = self._parse_comprehensive_response(response)
            
            # Check if we got real data or just an error
            if "error" in result or result.get("status") == "failed":
                logger.warning(f"AI comprehensive analysis failed: {result.get('error', 'Unknown error')}")
                logger.warning("Using fallback comprehensive analysis")
                fallback_result = self._create_fallback_comprehensive_analysis(repo_info, code_files, static_results)
                # Add error info to fallback result
                fallback_result["ai_error"] = result.get('error', 'Unknown AI error')
                fallback_result["ai_raw_response"] = result.get('raw_response', 'No raw response')
                return fallback_result
            
            return result
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            logger.warning("Using fallback comprehensive analysis")
            fallback_result = self._create_fallback_comprehensive_analysis(repo_info, code_files, static_results)
            # Add error info to fallback result
            fallback_result["ai_error"] = str(e)
            fallback_result["ai_raw_response"] = "Exception occurred during AI call"
            return fallback_result

    def _create_comprehensive_analysis_prompt(self, 
                                            code_files: Dict[str, str], 
                                            repo_info: Dict[str, Any],
                                            static_results: Dict[str, Any]) -> str:
        """
        Create comprehensive analysis prompt covering architecture, quality, security, and business impact
        """
        
        # INTELLIGENT TOKEN-AWARE ANALYSIS - Passt sich automatisch an Claude's Context-Limits an
        
        # Definiere realistische Konfigurationen (fokussiert und effizient)
        token_attempts = [
            {"name": "Standard", "files": 25, "char_limit": 6000},   # Standard: Fokussiert auf wichtige Dateien
            {"name": "Compact", "files": 15, "char_limit": 4000},    # Kompakt: Kernfunktionen
            {"name": "Minimal", "files": 10, "char_limit": 3000},    # Minimal: Nur essentielles
        ]
        
        all_formatted_files = None
        successful_config = None
        
        for config in token_attempts:
            try:
                logger.info(f"🔍 Versuche {config['name']}-Konfiguration: {config['files']} Dateien, {config['char_limit']} Zeichen/Datei")
                
                # Wähle beste Dateien mit adaptivem Scoring
                selected_files = self._select_best_files_adaptive(code_files, config["files"])
                
                # Formatiere mit Zeichen-Limit
                formatted_content = self._format_code_files_with_limit(selected_files, config["char_limit"])
                
                # Erstelle finalen Content
                test_content = f"""
ANALYSIERTE DATEIEN ({len(selected_files)} von {len(code_files)} Dateien):
{formatted_content}
"""
                
                # Schätze Token-Anzahl (1 Token ≈ 4 Zeichen)
                estimated_tokens = self._estimate_tokens(test_content)
                
                # Prüfe ob es in realistische Limits passt (50k tokens für fokussierte Analyse)
                if estimated_tokens < 50000:
                    logger.info(f"✅ Token-Limit OK: {estimated_tokens:,} tokens (< 50,000 limit)")
                    all_formatted_files = test_content
                    successful_config = config
                    break
                else:
                    logger.warning(f"⚠️ Zu viele Tokens: {estimated_tokens:,} (> 50,000 limit), versuche nächste Konfiguration...")
                    continue
                    
            except Exception as e:
                logger.error(f"❌ Fehler bei {config['name']}-Konfiguration: {e}")
                continue
        
        # Fallback falls alle Versuche fehlschlagen
        if not all_formatted_files:
            logger.warning("🚨 Fokussiere auf Kernfunktionen, verwende Core-Files Fallback")
            # Core-Files: nur die wichtigsten 8 Dateien mit 2000 Zeichen
            minimal_files = self._select_best_files_adaptive(code_files, 8)
            all_formatted_files = self._format_code_files_with_limit(minimal_files, 2000)
            successful_config = {"name": "Core-Files", "files": 8, "char_limit": 2000}
        
        logger.info(f"🎯 Finale Konfiguration: {successful_config['name']} - {successful_config['files']} Dateien, {successful_config['char_limit']} Zeichen/Datei")
        
        # Get static analysis summary
        static_summary = self._format_static_analysis_summary(static_results)
        
        prompt = f"""
Du bist ein erfahrener Software-Architekt, der Code-Analyse-Resultate interpretiert und konkrete, technische Verbesserungsempfehlungen gibt.

📊 REPOSITORY METRIKEN:
- Name: {repo_info.get('name', 'Unbekannt')}
- Sprachen: {', '.join(repo_info.get('languages', []))}
- Dateien: {repo_info.get('file_count', 0)} ({repo_info.get('code_file_count', 0)} Code-Dateien)
- Zeilen: {repo_info.get('lines_of_code', 0)} LOC

🔍 OBJEKTIVE ANALYSE-RESULTATE:
{static_summary}

💻 CODE-STRUKTUR:
{all_formatted_files}

🎯 AUFGABE: Interpretiere die objektiven Metriken und gib konkrete technische Empfehlungen.

📋 ANALYSIERE BASIEREND AUF OBJEKTIVEN DATEN:

1. ARCHITEKTUR & PATTERNS:
   - Erkenne verwendete Design Patterns aus dem Code
   - Bewerte Schichtentrennung und Modularität
   - Identifiziere Architektur-Stärken/-Schwächen

2. CODE QUALITÄT:
   - Interpretiere Radon Complexity-Resultate
   - Analysiere Bandit Security-Findings
   - Bewerte Code-Organisation und Struktur

3. TECHNISCHE EMPFEHLUNGEN:
   - Konkrete Verbesserungsvorschläge mit Dateinamen
   - Prioritäten basierend auf Impact vs. Aufwand
   - Messbare Erfolgskriterien für jede Empfehlung

⚡ FOKUSSIERTE ANALYSE - NUR DAS WICHTIGSTE:

1. ARCHITEKTUR-PATTERN ERKENNUNG:
   - Welches Hauptmuster wird verwendet? (MVC, Layered, Component-based)
   - Sind Verantwortlichkeiten klar getrennt?
   - Wo sind die größten Architektur-Schwächen?

2. SECURITY-FINDINGS INTERPRETATION:
   - Was bedeuten die Bandit-Resultate konkret?
   - Welche Vulnerabilities sind am kritischsten?
   - Konkrete Fix-Empfehlungen mit Dateinamen

3. COMPLEXITY-HOTSPOTS ANALYSE:
   - Welche Funktionen sind zu komplex (Radon > 10)?
   - Wo ist Refactoring am dringendsten?
   - Einfache Verbesserungsschritte

📋 STRUKTURIERTE ANTWORT im JSON-Format (auf DEUTSCH):

{{
    "architecture_analysis": {{
        "pattern": "Hauptarchitektur-Pattern (z.B. MVC, Layered)",
        "design_patterns": ["Erkannte Design Patterns"],
        "layer_separation": "Bewertung der Schichtentrennung",
        "architecture_score": 0-100
    }},
    "technology_stack": {{
        "frontend": ["Frontend-Technologien"],
        "backend": ["Backend-Technologien"],
        "modern": true/false,
        "outdated_components": ["Veraltete Komponenten"]
    }},
    "code_quality": {{
        "readability_score": 0-100,
        "performance_score": 0-100,
        "overall_quality_score": 0-100,
        "code_smells": ["Konkrete Code-Probleme mit Dateinamen"],
        "refactoring_suggestions": ["Konkrete Verbesserungsvorschläge"]
    }},
    "security_assessment": {{
        "security_score": 0-100,
        "risk_level": "low/medium/high",
        "vulnerabilities": ["Bandit-Findings erklärt"],
        "recommendations": ["Konkrete Security-Fixes"]
    }},
    "strengths": ["Hauptstärken des Codes"],
    "weaknesses": ["Hauptschwächen des Codes"],
    "recommendations": ["Top 3 technische Empfehlungen mit Dateinamen"]
}}

🎯 SCORING GUIDELINES für konsistente Bewertungen:
- Architecture Score: 90-100 (Clean patterns, SOLID principles), 70-89 (Good structure, minor issues), 50-69 (Mixed quality), <50 (Major problems)
- Code Quality Score: 90-100 (Clean, well-documented), 70-89 (Good practices, some smells), 50-69 (Needs improvement), <50 (Technical debt)
- Security Score: 90-100 (No vulnerabilities), 70-89 (Minor issues), 50-69 (Several vulnerabilities), <50 (Critical security risks)

Fokussiere auf konkrete, technische Empfehlungen basierend auf den objektiven Metriken. 

WICHTIG: Antworte komplett auf DEUTSCH. Alle Beschreibungen, Empfehlungen und Analysen sollen in deutscher Sprache verfasst werden.
"""
        return prompt

    def _format_static_analysis_summary(self, static_results: Dict[str, Any]) -> str:
        """Format static analysis results for the prompt"""
        
        summary = []
        
        # Complexity metrics
        complexity = static_results.get("complexity", {})
        if complexity:
            summary.append(f"Complexity Analysis:")
            summary.append(f"- Average complexity: {complexity.get('average_complexity', 'Unknown')}")
            summary.append(f"- High complexity functions: {complexity.get('high_complexity_count', 0)}")
            summary.append(f"- Very high complexity functions: {complexity.get('very_high_complexity_count', 0)}")
        
        # Security vulnerabilities
        security = static_results.get("security", {})
        if security:
            vulnerabilities = security.get("vulnerabilities", [])
            summary.append(f"Security Vulnerabilities: {len(vulnerabilities)}")
            for vuln in vulnerabilities[:5]:  # Show first 5
                summary.append(f"- {vuln.get('issue_text', 'Unknown issue')}")
        
        # Quality issues
        quality = static_results.get("quality", {})
        if quality:
            code_smells = quality.get("code_smells", [])
            summary.append(f"Code Smells: {len(code_smells)}")
        
        # Dependencies
        dependencies = static_results.get("dependencies", {})
        if dependencies:
            python_deps = len(dependencies.get("python", []))
            js_deps = len(dependencies.get("javascript", []))
            outdated = dependencies.get("outdated_count", 0)
            summary.append(f"Dependencies: {python_deps} Python, {js_deps} JavaScript, {outdated} outdated")
        
        return "\n".join(summary) if summary else "No static analysis data available"

    def _parse_comprehensive_response(self, response: str) -> Dict[str, Any]:
        """Parse comprehensive analysis response"""
        
        try:
            # Try to extract JSON from response
            import json
            import re
            
            # Find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # If no JSON found, return error
                return {"error": "No valid JSON found in response", "raw_response": response}
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse comprehensive response: {e}")
            return {"error": f"JSON parsing failed: {e}", "raw_response": response}
        except Exception as e:
            logger.error(f"Error parsing comprehensive response: {e}")
            return {"error": f"Parsing error: {e}", "raw_response": response}

    def _create_fallback_comprehensive_analysis(self, 
                                              repo_info: Dict[str, Any], 
                                              code_files: Dict[str, str],
                                              static_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive fallback analysis when AI fails"""
        
        # Analyze code files to determine patterns
        languages = repo_info.get('languages', [])
        file_count = repo_info.get('file_count', 0)
        lines_of_code = repo_info.get('lines_of_code', 0)
        
        # Determine architecture pattern based on file structure
        architecture_pattern = "Unknown"
        if any('package.json' in f for f in code_files.keys()):
            architecture_pattern = "Node.js/React Application"
        elif any('requirements.txt' in f for f in code_files.keys()):
            architecture_pattern = "Python Application"
        elif any('pom.xml' in f for f in code_files.keys()):
            architecture_pattern = "Java Application"
        elif any('dockerfile' in f.lower() for f in code_files.keys()):
            architecture_pattern = "Containerized Application"
        
        # Analyze technology stack
        tech_stack = {
            "frontend": [],
            "backend": [],
            "database": [],
            "build_tools": [],
            "deployment": [],
            "testing": [],
            "monitoring": [],
            "modern": True,
            "outdated_components": [],
            "version_analysis": "Analysis based on file structure",
            "dependency_health": "Unknown"
        }
        
        # Detect technologies from file extensions and names
        for filename in code_files.keys():
            filename_lower = filename.lower()
            
            # Frontend
            if any(ext in filename_lower for ext in ['.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte']):
                if 'react' in filename_lower or 'jsx' in filename_lower:
                    tech_stack["frontend"].append("React")
                elif 'vue' in filename_lower:
                    tech_stack["frontend"].append("Vue.js")
                elif 'svelte' in filename_lower:
                    tech_stack["frontend"].append("Svelte")
                else:
                    tech_stack["frontend"].append("JavaScript/TypeScript")
            
            # Backend
            elif any(ext in filename_lower for ext in ['.py', '.java', '.kt', '.go', '.rs']):
                if '.py' in filename_lower:
                    tech_stack["backend"].append("Python")
                elif '.java' in filename_lower:
                    tech_stack["backend"].append("Java")
                elif '.kt' in filename_lower:
                    tech_stack["backend"].append("Kotlin")
                elif '.go' in filename_lower:
                    tech_stack["backend"].append("Go")
                elif '.rs' in filename_lower:
                    tech_stack["backend"].append("Rust")
            
            # Database
            elif any(ext in filename_lower for ext in ['.sql', '.prisma', '.graphql']):
                tech_stack["database"].append("Database files detected")
            
            # Build tools
            elif any(name in filename_lower for name in ['dockerfile', 'docker-compose', 'webpack', 'vite', 'package.json']):
                if 'docker' in filename_lower:
                    tech_stack["build_tools"].append("Docker")
                elif 'webpack' in filename_lower:
                    tech_stack["build_tools"].append("Webpack")
                elif 'vite' in filename_lower:
                    tech_stack["build_tools"].append("Vite")
                elif 'package.json' in filename_lower:
                    tech_stack["build_tools"].append("npm/yarn")
        
        # Remove duplicates
        for key in tech_stack:
            if isinstance(tech_stack[key], list):
                tech_stack[key] = list(set(tech_stack[key]))
        
        # Get security vulnerabilities count
        security_vulns = len(static_results.get("security", {}).get("vulnerabilities", []))
        
        return {
            "architecture_analysis": {
                "pattern": architecture_pattern,
                "design_patterns": ["Standard patterns"],
                "layer_separation": "Standard layer separation",
                "scalability_score": 75,
                "maintainability_score": 70,
                "architecture_score": 75
            },
            "technology_stack": tech_stack,
            "code_quality": {
                "readability_score": 75,
                "maintainability_score": 70,
                "performance_score": 80,
                "testability_score": 65,
                "error_handling_score": 75,
                "overall_quality_score": 73,
                "code_smells": [],
                "best_practices_violations": ["Limited testing", "Some documentation gaps"],
                "performance_issues": ["Minor optimization opportunities"],
                "refactoring_suggestions": ["Improve test coverage", "Enhance documentation"]
            },
            "security_assessment": {
                "security_score": 70,
                "risk_level": "medium",
                "vulnerabilities": security_vulns,
                "security_strengths": ["Standard security practices"],
                "security_weaknesses": ["Limited security scanning"],
                "compliance_issues": ["Basic compliance met"],
                "recommendations": ["Implement security scanning", "Enhance authentication"]
            },
            "business_impact": {
                "technical_debt_hours": 120,
                "development_velocity": "medium",
                "risk_level": "medium",
                "roi_opportunities": ["Improve testing", "Enhance documentation"],
                "maintenance_cost_estimate": "Moderate",
                "scalability_potential": "Good"
            },
            "environment_strategy": {
                "development": "Standard development environment",
                "staging": "Staging environment likely present",
                "production": "Production deployment configured",
                "deployment_pipeline": "Standard CI/CD pipeline",
                "infrastructure": "Cloud-based infrastructure"
            },
            "team_insights": {
                "branch_strategy": "Standard Git workflow",
                "code_review_process": "Standard code review process",
                "bugfix_frequency": "Regular maintenance pattern",
                "development_practices": "Standard development practices"
            },
            "technical_debt": {
                "dead_code_analysis": "No obvious dead code detected",
                "technical_debt_analysis": "Moderate technical debt detected",
                "migration_effort": "Low to moderate migration effort required"
            },
            "strengths": [
                "Well-structured codebase",
                "Modern development practices",
                "Good file organization"
            ],
            "weaknesses": [
                "Limited automated testing",
                "Documentation could be improved",
                "Some technical debt present"
            ],
            "recommendations": [
                "Implement comprehensive testing strategy",
                "Improve documentation quality",
                "Reduce technical debt",
                "Enhance security practices"
            ],
            "investment_recommendations": [
                {
                    "priority": 1,
                    "task": "Implement comprehensive testing",
                    "effort_hours": 40,
                    "business_value": "high",
                    "description": "Add unit and integration tests",
                    "expected_roi": "Improved code quality and reduced bugs",
                    "risk_if_not_done": "Increased technical debt"
                },
                {
                    "priority": 2,
                    "task": "Enhance documentation",
                    "effort_hours": 30,
                    "business_value": "medium",
                    "description": "Improve README and API documentation",
                    "expected_roi": "Better developer onboarding",
                    "risk_if_not_done": "Knowledge silos"
                }
            ],
            "risk_assessment": {
                "security_risks": ["Low to medium"],
                "maintenance_risks": ["Medium"],
                "scalability_risks": ["Low"],
                "technology_risks": ["Low"],
                "business_continuity_risks": ["Low"]
            },
            "executive_summary": "Comprehensive analysis completed with fallback data due to AI service issues. Repository shows standard development practices with room for improvement in testing and documentation."
        }
    
    async def _call_claude(self, prompt: str, max_tokens: int = 4000) -> str:
        """
        Make API call to Claude via Bedrock - Focused, efficient analysis
        
        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens in response (focused for key insights)
            
        Returns:
            Claude's response text
        """
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1,  # Low temperature for consistent analysis
            "top_p": 0.9
        }
        
        try:
            # Log the model ID being used
            logger.info(f"Attempting to call Bedrock with model: {self.model_id}")
            
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except ClientError as e:
            logger.error(f"Bedrock API error: {e}")
            logger.error(f"Model ID used: {self.model_id}")
            logger.error(f"Region: {self.bedrock_runtime.meta.region_name}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error calling Claude: {e}")
            logger.error(f"Model ID used: {self.model_id}")
            raise
    
    def _select_important_files(self, code_files: Dict[str, str], max_files: int = 100) -> Dict[str, str]:
        """Select most important files for analysis"""
        
        # Priority order for file types
        priority_extensions = [
            '.py', '.js', '.ts', '.tsx', '.jsx', '.vue', '.svelte',  # Main code files
            '.java', '.kt', '.scala', '.go', '.rs', '.cpp', '.c', '.cs',  # Other languages
            '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',  # Config files  
            '.md', '.txt', '.rst',  # Documentation
            '.dockerfile', '.dockerignore',  # Docker files
            '.gitignore', '.gitattributes',  # Git files
            '.env', '.env.example',  # Environment files
            '.sql', '.prisma', '.graphql',  # Database/Schema files
            '.html', '.css', '.scss', '.less',  # Frontend files
            '.sh', '.bash', '.zsh', '.fish',  # Shell scripts
            '.xml', '.xsd', '.wsdl',  # XML files
            '.properties', '.conf',  # Configuration files
        ]
        
        important_files = {}
        
        # Sort files by importance and size
        sorted_files = []
        
        # First, get all files with priority extensions
        for ext in priority_extensions:
            for filename, content in code_files.items():
                if filename.endswith(ext) and len(content.strip()) > 0:
                    # Calculate file importance score
                    importance_score = self._calculate_file_importance(filename, content)
                    sorted_files.append((filename, content, importance_score))
        
        # Sort by importance score (highest first)
        sorted_files.sort(key=lambda x: x[2], reverse=True)
        
        # Take top files up to max_files
        selected_files = sorted_files[:max_files]
        
        return {filename: content for filename, content, _ in selected_files}
    
    def _calculate_file_importance(self, filename: str, content: str) -> float:
        """Calculate importance score for a file"""
        score = 0.0
        
        # Base score for file type
        if any(filename.endswith(ext) for ext in ['.py', '.js', '.ts', '.tsx', '.jsx', '.vue']):
            score += 10.0
        elif any(filename.endswith(ext) for ext in ['.java', '.kt', '.go', '.rs', '.cpp', '.c']):
            score += 9.0
        elif any(filename.endswith(ext) for ext in ['.json', '.yaml', '.yml', '.toml']):
            score += 8.0
        elif any(filename.endswith(ext) for ext in ['.md', '.txt', '.rst']):
            score += 5.0
        else:
            score += 3.0
        
        # Bonus for important file names
        important_names = [
            'main', 'app', 'index', 'config', 'settings', 'requirements', 'package',
            'dockerfile', 'docker-compose', 'readme', 'license', 'setup', 'install',
            'api', 'router', 'controller', 'service', 'model', 'schema', 'migration',
            'test', 'spec', 'example', 'template', 'utils', 'helpers', 'constants'
        ]
        
        filename_lower = filename.lower()
        for name in important_names:
            if name in filename_lower:
                score += 2.0
        
        # Bonus for larger files (more content to analyze)
        content_length = len(content)
        if content_length > 1000:
            score += 1.0
        if content_length > 5000:
            score += 2.0
        if content_length > 10000:
            score += 3.0
        
        # Bonus for files with imports/dependencies
        import_keywords = ['import', 'require', 'from', 'using', 'include', 'package']
        content_lower = content.lower()
        for keyword in import_keywords:
            if keyword in content_lower:
                score += 0.5
        
        return score
    
    def _create_fallback_architecture_analysis(self, repo_info: Dict[str, Any], code_files: Dict[str, str]) -> Dict[str, Any]:
        """Create fallback architecture analysis when AI fails"""
        
        # Analyze code files to determine patterns
        languages = repo_info.get('languages', [])
        file_count = repo_info.get('file_count', 0)
        lines_of_code = repo_info.get('lines_of_code', 0)
        
        # Determine architecture pattern based on file structure
        architecture_pattern = "Unknown"
        if any('package.json' in f for f in code_files.keys()):
            architecture_pattern = "Node.js/React Application"
        elif any('requirements.txt' in f for f in code_files.keys()):
            architecture_pattern = "Python Application"
        elif any('pom.xml' in f for f in code_files.keys()):
            architecture_pattern = "Java Application"
        elif any('dockerfile' in f.lower() for f in code_files.keys()):
            architecture_pattern = "Containerized Application"
        
        # Analyze technology stack
        tech_stack = {
            "frontend": [],
            "backend": [],
            "database": [],
            "middleware": [],
            "build_tools": [],
            "deployment": [],
            "testing": [],
            "monitoring": [],
            "modern": True,
            "outdated_components": [],
            "version_analysis": "Analysis based on file structure",
            "dependency_health": "Unknown"
        }
        
        # Detect technologies from file extensions and names
        for filename in code_files.keys():
            filename_lower = filename.lower()
            
            # Frontend
            if any(ext in filename_lower for ext in ['.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte']):
                if 'react' in filename_lower or 'jsx' in filename_lower:
                    tech_stack["frontend"].append("React")
                elif 'vue' in filename_lower:
                    tech_stack["frontend"].append("Vue.js")
                elif 'svelte' in filename_lower:
                    tech_stack["frontend"].append("Svelte")
                else:
                    tech_stack["frontend"].append("JavaScript/TypeScript")
            
            # Backend
            elif any(ext in filename_lower for ext in ['.py', '.java', '.kt', '.go', '.rs']):
                if '.py' in filename_lower:
                    tech_stack["backend"].append("Python")
                elif '.java' in filename_lower:
                    tech_stack["backend"].append("Java")
                elif '.kt' in filename_lower:
                    tech_stack["backend"].append("Kotlin")
                elif '.go' in filename_lower:
                    tech_stack["backend"].append("Go")
                elif '.rs' in filename_lower:
                    tech_stack["backend"].append("Rust")
            
            # Database
            elif any(ext in filename_lower for ext in ['.sql', '.prisma', '.graphql']):
                tech_stack["database"].append("Database files detected")
            
            # Build tools
            elif any(name in filename_lower for name in ['dockerfile', 'docker-compose', 'webpack', 'vite', 'package.json']):
                if 'docker' in filename_lower:
                    tech_stack["build_tools"].append("Docker")
                elif 'webpack' in filename_lower:
                    tech_stack["build_tools"].append("Webpack")
                elif 'vite' in filename_lower:
                    tech_stack["build_tools"].append("Vite")
                elif 'package.json' in filename_lower:
                    tech_stack["build_tools"].append("npm/yarn")
        
        # Remove duplicates
        for key in tech_stack:
            if isinstance(tech_stack[key], list):
                tech_stack[key] = list(set(tech_stack[key]))
        
        return {
            "architecture_pattern": architecture_pattern,
            "architecture_score": 75,
            "design_quality_score": 70,
            "scalability_score": 75,
            "maintainability_score": 70,
            "technology_stack": tech_stack,
            "environment_strategy": {
                "development": "Standard development environment",
                "staging": "Staging environment likely present",
                "production": "Production deployment configured",
                "deployment_pipeline": "Standard CI/CD pipeline",
                "infrastructure": "Cloud-based infrastructure"
            },
            "build_process": "Standard build process detected",
            "testing_strategy": "Testing framework present",
            "documentation_quality": "Documentation files detected",
            "security_practices": "Standard security practices",
            "performance_optimization": "Performance considerations present",
            "dead_code_analysis": "No obvious dead code detected",
            "branch_strategy": "Standard Git workflow",
            "bugfix_frequency": "Regular maintenance pattern",
            "code_review_process": "Standard code review process",
            "strengths": [
                "Well-structured codebase",
                "Modern development practices",
                "Good file organization"
            ],
            "weaknesses": [
                "Limited automated testing",
                "Documentation could be improved",
                "Some technical debt present"
            ],
            "recommendations": [
                "Implement comprehensive testing strategy",
                "Improve documentation quality",
                "Reduce technical debt",
                "Enhance security practices"
            ],
            "technical_debt_analysis": "Moderate technical debt detected",
            "migration_effort": "Low to moderate migration effort required"
        }
    
    def _create_fallback_quality_analysis(self, static_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback quality analysis when AI fails"""
        return {
            "readability_score": 75,
            "maintainability_score": 70,
            "performance_score": 80,
            "testability_score": 65,
            "error_handling_score": 75,
            "overall_quality_score": 73,
            "code_smells": [],
            "best_practices_violations": ["Limited testing", "Some documentation gaps"],
            "performance_issues": ["Minor optimization opportunities"],
            "refactoring_suggestions": ["Improve test coverage", "Enhance documentation"]
        }
    
    def _create_fallback_security_analysis(self, security_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback security analysis when AI fails"""
        return {
            "security_score": 70,
            "risk_level": "medium",
            "vulnerabilities": security_results.get('security_vulnerabilities', 0),
            "security_strengths": ["Standard security practices"],
            "security_weaknesses": ["Limited security scanning"],
            "compliance_issues": ["Basic compliance met"],
            "recommendations": ["Implement security scanning", "Enhance authentication"]
        }
    
    def _create_fallback_report(self, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback comprehensive report when AI fails"""
        return {
            "executive_summary": "Comprehensive analysis completed with fallback data due to AI service issues. Repository shows standard development practices with room for improvement in testing and documentation.",
            "business_impact": {
                "technical_debt_hours": 120,
                "development_velocity": "medium",
                "risk_level": "medium",
                "roi_opportunities": ["Improve testing", "Enhance documentation"],
                "maintenance_cost_estimate": "Moderate",
                "scalability_potential": "Good"
            },
            "investment_recommendations": [
                {
                    "priority": 1,
                    "task": "Implement comprehensive testing",
                    "effort_hours": 40,
                    "business_value": "high",
                    "description": "Add unit and integration tests",
                    "expected_roi": "Improved code quality and reduced bugs",
                    "risk_if_not_done": "Increased technical debt"
                },
                {
                    "priority": 2,
                    "task": "Enhance documentation",
                    "effort_hours": 30,
                    "business_value": "medium",
                    "description": "Improve README and API documentation",
                    "expected_roi": "Better developer onboarding",
                    "risk_if_not_done": "Knowledge silos"
                }
            ],
            "risk_assessment": {
                "security_risks": ["Low to medium"],
                "maintenance_risks": ["Medium"],
                "scalability_risks": ["Low"],
                "technology_risks": ["Low"],
                "business_continuity_risks": ["Low"]
            },
            "technical_insights": {
                "architecture_quality": "Good",
                "code_quality": "Fair",
                "technology_modernity": "Modern",
                "build_process_quality": "Standard",
                "environment_strategy_quality": "Good",
                "dead_code_analysis": "No major issues",
                "branch_strategy_analysis": "Standard Git workflow"
            }
        }
    
    def _format_code_files(self, code_files: Dict[str, str], max_files: int = 40, focus_security: bool = False) -> str:
        """Format code files for prompt"""
        
        formatted = ""
        count = 0
        
        for filename, content in code_files.items():
            if count >= max_files:
                break
                
            # Truncate very long files but keep more content (increased for Claude 3.7 Sonnet)
            if len(content) > 8000:
                content = content[:8000] + "\n... [truncated]"
            
            # Add file statistics
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            formatted += f"""
**{filename}** (Lines: {len(lines)}, Non-empty: {len(non_empty_lines)}):
```
{content}
```
"""
            count += 1
        
        return formatted
    
    def _format_code_files_complete(self, code_files: Dict[str, str]) -> str:
        """Format code files for prompt, including full content"""
        formatted = ""
        for filename, content in code_files.items():
            # Add file statistics
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            formatted += f"""
**{filename}** (Lines: {len(lines)}, Non-empty: {len(non_empty_lines)}):
```
{content}
```
"""
        return formatted

    def _select_architecture_files(self, code_files: Dict[str, str], max_files: int = 50) -> Dict[str, str]:
        """Select files critical for architecture analysis - main entry points, routers, models"""
        architecture_files = {}
        priority_patterns = [
            # Höchste Priorität: Entry Points & Main Files
            ('main', 10.0), ('app', 10.0), ('index', 10.0), ('server', 10.0), 
            ('router', 9.0), ('route', 9.0), ('controller', 9.0), ('api', 9.0),
            # Architektur-relevante Dateien
            ('model', 8.0), ('schema', 8.0), ('service', 8.0), ('component', 7.0),
            ('config', 8.0), ('settings', 8.0), ('middleware', 7.0),
            # Framework-spezifische Dateien
            ('package.json', 9.0), ('requirements.txt', 9.0), ('dockerfile', 8.0),
            ('docker-compose', 8.0), ('webpack', 7.0), ('vite', 7.0),
        ]
        
        # Score und sortiere Dateien
        scored_files = []
        for filename, content in code_files.items():
            score = self._calculate_architecture_score(filename, content, priority_patterns)
            if score > 0:
                scored_files.append((filename, content, score))
        
        # Sortiere nach Score (höchster zuerst)
        scored_files.sort(key=lambda x: x[2], reverse=True)
        
        # Nehme die besten Dateien
        for filename, content, score in scored_files[:max_files]:
            architecture_files[filename] = content
            
        return architecture_files

    def _select_business_logic_files(self, code_files: Dict[str, str], max_files: int = 50) -> Dict[str, str]:
        """Select files containing core business logic - services, utilities, business rules"""
        business_files = {}
        priority_patterns = [
            # Business Logic Dateien
            ('service', 10.0), ('business', 10.0), ('logic', 9.0), ('rule', 9.0),
            ('util', 8.0), ('helper', 8.0), ('manager', 8.0), ('handler', 8.0),
            # Core Funktionalität
            ('core', 9.0), ('lib', 8.0), ('module', 7.0), ('feature', 7.0),
            # Datenverarbeitung
            ('process', 8.0), ('transform', 7.0), ('validate', 7.0), ('calculate', 7.0),
            # API & Endpoints
            ('endpoint', 8.0), ('view', 7.0), ('action', 7.0),
        ]
        
        scored_files = []
        for filename, content in code_files.items():
            # Priorisiere Dateien mit viel Code (echte Business Logic)
            if len(content.strip()) < 100:  # Skip sehr kleine Dateien
                continue
                
            score = self._calculate_business_logic_score(filename, content, priority_patterns)
            if score > 0:
                scored_files.append((filename, content, score))
        
        scored_files.sort(key=lambda x: x[2], reverse=True)
        
        for filename, content, score in scored_files[:max_files]:
            business_files[filename] = content
            
        return business_files

    def _select_configuration_files(self, code_files: Dict[str, str], max_files: int = 50) -> Dict[str, str]:
        """Select configuration, dependency, and infrastructure files"""
        config_files = {}
        priority_patterns = [
            # Package Management
            ('package.json', 10.0), ('requirements.txt', 10.0), ('pom.xml', 10.0),
            ('cargo.toml', 10.0), ('go.mod', 10.0), ('composer.json', 10.0),
            # Build & Deployment
            ('dockerfile', 9.0), ('docker-compose', 9.0), ('webpack', 8.0), 
            ('vite.config', 8.0), ('rollup', 7.0), ('babel', 7.0),
            # Environment & Config
            ('.env', 9.0), ('config', 8.0), ('settings', 8.0), ('.yml', 7.0), ('.yaml', 7.0),
            # CI/CD & Git
            ('.github', 8.0), ('.gitlab', 8.0), ('jenkins', 7.0), ('.gitignore', 6.0),
            # Documentation
            ('readme', 8.0), ('changelog', 6.0), ('license', 5.0),
        ]
        
        scored_files = []
        for filename, content in code_files.items():
            score = self._calculate_config_score(filename, content, priority_patterns)
            if score > 0:
                scored_files.append((filename, content, score))
        
        scored_files.sort(key=lambda x: x[2], reverse=True)
        
        for filename, content, score in scored_files[:max_files]:
            config_files[filename] = content
            
        return config_files

    def _calculate_architecture_score(self, filename: str, content: str, priority_patterns: list) -> float:
        """Calculate architecture relevance score for a file"""
        score = 0.0
        filename_lower = filename.lower()
        
        # Pattern matching
        for pattern, weight in priority_patterns:
            if pattern in filename_lower:
                score += weight
        
        # Dateityp Bonus
        if any(filename_lower.endswith(ext) for ext in ['.py', '.js', '.ts', '.tsx', '.jsx']):
            score += 5.0
        elif any(filename_lower.endswith(ext) for ext in ['.json', '.yml', '.yaml']):
            score += 3.0
            
        # Größe Bonus (größere Dateien = mehr Architektur-Info)
        content_length = len(content)
        if content_length > 5000:
            score += 2.0
        elif content_length > 1000:
            score += 1.0
            
        return score

    def _calculate_business_logic_score(self, filename: str, content: str, priority_patterns: list) -> float:
        """Calculate business logic relevance score for a file"""
        score = 0.0
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        # Pattern matching im Dateinamen
        for pattern, weight in priority_patterns:
            if pattern in filename_lower:
                score += weight
        
        # Code-Qualität Indikatoren
        if 'function' in content_lower or 'def ' in content_lower:
            score += 2.0
        if 'class ' in content_lower:
            score += 3.0
        if 'import' in content_lower or 'require(' in content_lower:
            score += 1.0
            
        # Business Logic Keywords
        business_keywords = ['validate', 'calculate', 'process', 'transform', 'business', 'rule']
        for keyword in business_keywords:
            if keyword in content_lower:
                score += 1.5
                
        # Größe = Komplexität
        content_length = len(content)
        if content_length > 10000:
            score += 3.0
        elif content_length > 5000:
            score += 2.0
        elif content_length > 1000:
            score += 1.0
            
        return score

    def _calculate_config_score(self, filename: str, content: str, priority_patterns: list) -> float:
        """Calculate configuration relevance score for a file"""
        score = 0.0
        filename_lower = filename.lower()
        
        # Pattern matching
        for pattern, weight in priority_patterns:
            if pattern in filename_lower:
                score += weight
        
        # Config-Dateitypen
        config_extensions = ['.json', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.env', '.properties']
        if any(filename_lower.endswith(ext) for ext in config_extensions):
            score += 4.0
            
        # Dockerfile & Docker-compose
        if 'docker' in filename_lower:
            score += 5.0
            
        return score
    
    def _parse_architecture_response(self, response: str) -> Dict[str, Any]:
        """Parse Claude's architecture analysis response"""
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {"error": "Could not parse response", "raw_response": response}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response", "raw_response": response}
    
    def _parse_quality_response(self, response: str) -> Dict[str, Any]:
        """Parse Claude's quality analysis response"""
        return self._parse_architecture_response(response)  # Same parsing logic
    
    def _parse_security_response(self, response: str) -> Dict[str, Any]:
        """Parse Claude's security analysis response"""
        return self._parse_architecture_response(response)  # Same parsing logic
    
    def _parse_report_response(self, response: str) -> Dict[str, Any]:
        """Parse Claude's comprehensive report response"""
        return self._parse_architecture_response(response)  # Same parsing logic 
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count (rough approximation: 1 token ≈ 4 characters)"""
        return len(text) // 4
    
    def _format_code_files_with_limit(self, code_files: Dict[str, str], char_limit: int) -> str:
        """Format code files with character limit per file"""
        formatted_files = []
        
        for filepath, content in code_files.items():
            # Truncate content if too long
            if len(content) > char_limit:
                truncated_content = content[:char_limit] + f"\n\n... [TRUNCATED - Original length: {len(content)} chars] ..."
            else:
                truncated_content = content
                
            formatted_files.append(f"""
--- FILE: {filepath} ---
{truncated_content}
--- END FILE ---
""")
        
        return "\n".join(formatted_files)
    
    def _select_best_files_adaptive(self, code_files: Dict[str, str], max_files: int) -> Dict[str, str]:
        """Select best files using adaptive scoring that combines all criteria"""
        scored_files = []
        
        for filepath, content in code_files.items():
            filename = filepath.split('/')[-1]
            
            # Calculate combined score
            arch_score = self._calculate_architecture_score(filename, content, [
                ('app.py', 8.0), ('main.py', 8.0), ('server.py', 7.0), ('index.', 6.0),
                ('router', 6.0), ('controller', 6.0), ('model', 5.0), ('service', 5.0),
                ('config', 4.0), ('setup.py', 4.0), ('__init__.py', 3.0)
            ])
            
            business_score = self._calculate_business_logic_score(filename, content, [
                ('service', 8.0), ('business', 8.0), ('logic', 7.0), ('core', 7.0),
                ('util', 6.0), ('helper', 5.0), ('api', 6.0), ('handler', 6.0),
                ('process', 5.0), ('manager', 5.0), ('engine', 6.0)
            ])
            
            config_score = self._calculate_config_score(filename, content, [
                ('package.json', 10.0), ('requirements.txt', 9.0), ('dockerfile', 8.0),
                ('docker-compose', 8.0), ('config', 7.0), ('settings', 6.0), ('.env', 5.0),
                ('webpack', 5.0), ('babel', 4.0), ('eslint', 4.0)
            ])
            
            # Combined score with weights
            combined_score = (arch_score * 0.4) + (business_score * 0.4) + (config_score * 0.2)
            
            # Size bonus for medium-sized files (not too small, not too large)
            size_score = 0
            if 500 <= len(content) <= 15000:
                size_score = 2.0
            elif 100 <= len(content) <= 500:
                size_score = 1.0
                
            final_score = combined_score + size_score
            scored_files.append((filepath, content, final_score))
        
        # Sort by score and take top files
        scored_files.sort(key=lambda x: x[2], reverse=True)
        selected = dict((filepath, content) for filepath, content, _ in scored_files[:max_files])
        
        return selected

