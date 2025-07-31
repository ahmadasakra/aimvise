import asyncio
import json
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import hashlib
import requests

logger = logging.getLogger(__name__)

class SecurityAnalyzer:
    """
    Comprehensive security analyzer that identifies:
    - Known vulnerabilities in dependencies
    - Security code patterns and anti-patterns
    - Secrets and sensitive data exposure
    - Common security misconfigurations
    - OWASP Top 10 violations
    """
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.findings = []
        
        # Security patterns for different languages
        self.security_patterns = {
            'sql_injection': [
                r'SELECT\s+.+\s+FROM\s+.+\s+WHERE\s+.+\s*\+\s*["\']',
                r'execute\s*\(\s*["\'].+["\'].+\+',
                r'query\s*\(\s*["\'].+["\'].+\+',
                r'cursor\.execute\s*\([^,]+\+',
            ],
            'xss_vulnerability': [
                r'innerHTML\s*=\s*[^;]+\+',
                r'document\.write\s*\([^)]+\+',
                r'eval\s*\(',
                r'setTimeout\s*\(\s*["\'][^"\']*["\']\s*\+',
            ],
            'command_injection': [
                r'os\.system\s*\([^)]+\+',
                r'subprocess\.(call|run|Popen)\s*\([^)]+\+',
                r'exec\s*\(',
                r'shell_exec\s*\(',
                r'system\s*\(',
            ],
            'path_traversal': [
                r'\.\./',
                r'\.\.\\',
                r'open\s*\([^)]*\.\./[^)]*\)',
            ],
            'hardcoded_secrets': [
                r'password\s*=\s*["\'][^"\']{8,}["\']',
                r'api_key\s*=\s*["\'][^"\']{20,}["\']',
                r'secret\s*=\s*["\'][^"\']{16,}["\']',
                r'token\s*=\s*["\'][^"\']{20,}["\']',
                r'key\s*=\s*["\'][^"\']{16,}["\']',
            ],
            'weak_crypto': [
                r'MD5\s*\(',
                r'SHA1\s*\(',
                r'DES\s*\(',
                r'RC4\s*\(',
                r'hashlib\.md5',
                r'hashlib\.sha1',
            ],
            'insecure_random': [
                r'random\.random\s*\(',
                r'Math\.random\s*\(',
                r'Random\s*\(',
            ],
            'ldap_injection': [
                r'LdapContext\s*\([^)]+\+',
                r'search\s*\([^)]+\+[^)]*\)',
            ]
        }
        
        # File patterns that might contain sensitive information
        self.sensitive_files = [
            r'\.env',
            r'\.env\.',
            r'config\.json',
            r'secrets\.json',
            r'credentials\.json',
            r'\.htpasswd',
            r'\.htaccess',
            r'web\.config',
            r'\.git/config',
            r'id_rsa',
            r'id_dsa',
            r'\.pem',
            r'\.key',
            r'\.crt',
        ]
    
    def analyze(self) -> Dict[str, Any]:
        """
        Perform comprehensive security analysis
        """
        try:
            logger.info("🔒 Starting security analysis...")
            
            results = {
                "summary": {},
                "vulnerabilities": [],
                "secrets_found": [],
                "security_misconfigurations": [],
                "dependency_vulnerabilities": [],
                "file_permissions_issues": [],
                "sensitive_files_exposed": [],
                "security_score": 6.0,
                "recommendations": []
            }
            
            # 1. Scan for code-level security issues
            code_vulnerabilities = self._scan_code_vulnerabilities()
            results["vulnerabilities"].extend(code_vulnerabilities)
            
            # 2. Scan for hardcoded secrets
            secrets = self._scan_for_secrets()
            results["secrets_found"].extend(secrets)
            
            # 3. Check for sensitive files
            sensitive_files = self._check_sensitive_files()
            results["sensitive_files_exposed"].extend(sensitive_files)
            
            # 4. Analyze file permissions
            permission_issues = self._check_file_permissions()
            results["file_permissions_issues"].extend(permission_issues)
            
            # 5. Security configuration analysis
            misconfigs = self._analyze_security_configurations()
            results["security_misconfigurations"].extend(misconfigs)
            
            # 6. Dependency vulnerability scanning
            dependency_vulns = await self._scan_dependency_vulnerabilities()
            results["dependency_vulnerabilities"].extend(dependency_vulns)
            
            # Calculate summary
            total_issues = (len(results["vulnerabilities"]) + 
                          len(results["secrets_found"]) + 
                          len(results["sensitive_files_exposed"]) +
                          len(results["dependency_vulnerabilities"]))
            
            critical_issues = len([v for v in results["vulnerabilities"] if v.get("severity") == "critical"])
            high_issues = len([v for v in results["vulnerabilities"] if v.get("severity") == "high"])
            
            results["summary"] = {
                "total_issues": total_issues,
                "critical_issues": critical_issues,
                "high_issues": high_issues,
                "medium_issues": len([v for v in results["vulnerabilities"] if v.get("severity") == "medium"]),
                "low_issues": len([v for v in results["vulnerabilities"] if v.get("severity") == "low"]),
                "secrets_count": len(results["secrets_found"]),
                "sensitive_files_count": len(results["sensitive_files_exposed"]),
                "dependency_vulnerabilities_count": len(results["dependency_vulnerabilities"])
            }
            
            # Calculate security score (1-6 scale)
            results["security_score"] = self._calculate_security_score(results)
            
            # Generate recommendations
            results["recommendations"] = self._generate_security_recommendations(results)
            
            # Add fields for main analyzer
            results["vulnerabilities_count"] = total_issues
            
            logger.info(f"✅ Security analysis completed. Found {total_issues} issues. Score: {results['security_score']}/6.0")
            return results
            
        except Exception as e:
            logger.error(f"Security analysis failed: {str(e)}")
            return {"error": str(e)}
    
    def _scan_code_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Scan source code for security vulnerabilities"""
        vulnerabilities = []
        
        try:
            # Get all source files
            source_files = []
            for pattern in ['**/*.py', '**/*.js', '**/*.ts', '**/*.java', '**/*.php', '**/*.cs', '**/*.rb']:
                source_files.extend(self.repo_path.rglob(pattern))
            
            for file_path in source_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    file_vulns = self._analyze_file_security(file_path, content)
                    vulnerabilities.extend(file_vulns)
                    
                except Exception as e:
                    logger.warning(f"Failed to scan {file_path}: {str(e)}")
                    continue
            
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"Code vulnerability scanning failed: {str(e)}")
            return []
    
    def _analyze_file_security(self, file_path: Path, content: str) -> List[Dict[str, Any]]:
        """Analyze a single file for security issues"""
        vulnerabilities = []
        relative_path = file_path.relative_to(self.repo_path)
        lines = content.split('\n')
        
        for vuln_type, patterns in self.security_patterns.items():
            for pattern in patterns:
                for line_num, line in enumerate(lines, 1):
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        severity = self._get_vulnerability_severity(vuln_type)
                        
                        vulnerabilities.append({
                            "type": vuln_type,
                            "severity": severity,
                            "file": str(relative_path),
                            "line": line_num,
                            "column": match.start() + 1,
                            "code_snippet": line.strip(),
                            "description": self._get_vulnerability_description(vuln_type),
                            "recommendation": self._get_vulnerability_recommendation(vuln_type),
                            "cwe_id": self._get_cwe_id(vuln_type),
                            "owasp_category": self._get_owasp_category(vuln_type)
                        })
        
        return vulnerabilities
    
    def _scan_for_secrets(self) -> List[Dict[str, Any]]:
        """Scan for hardcoded secrets and sensitive data"""
        secrets = []
        
        try:
            # Common secret patterns
            secret_patterns = {
                'api_key': [
                    r'api_key["\'\s]*[:=]["\'\s]*([a-zA-Z0-9_\-]{20,})',
                    r'apikey["\'\s]*[:=]["\'\s]*([a-zA-Z0-9_\-]{20,})',
                    r'API_KEY["\'\s]*[:=]["\'\s]*([a-zA-Z0-9_\-]{20,})',
                ],
                'password': [
                    r'password["\'\s]*[:=]["\'\s]*([^\s"\']{8,})',
                    r'passwd["\'\s]*[:=]["\'\s]*([^\s"\']{8,})',
                    r'pwd["\'\s]*[:=]["\'\s]*([^\s"\']{8,})',
                ],
                'database_url': [
                    r'DATABASE_URL["\'\s]*[:=]["\'\s]*([^\s"\']+)',
                    r'db_url["\'\s]*[:=]["\'\s]*([^\s"\']+)',
                ],
                'jwt_secret': [
                    r'jwt_secret["\'\s]*[:=]["\'\s]*([a-zA-Z0-9_\-]{16,})',
                    r'JWT_SECRET["\'\s]*[:=]["\'\s]*([a-zA-Z0-9_\-]{16,})',
                ],
                'private_key': [
                    r'-----BEGIN [A-Z ]+ PRIVATE KEY-----',
                    r'private_key["\'\s]*[:=]["\'\s]*([a-zA-Z0-9+/=]{100,})',
                ],
                'oauth_token': [
                    r'oauth_token["\'\s]*[:=]["\'\s]*([a-zA-Z0-9_\-]{20,})',
                    r'access_token["\'\s]*[:=]["\'\s]*([a-zA-Z0-9_\-]{20,})',
                ],
                'github_token': [
                    r'github_token["\'\s]*[:=]["\'\s]*(ghp_[a-zA-Z0-9_]{36})',
                    r'GITHUB_TOKEN["\'\s]*[:=]["\'\s]*(ghp_[a-zA-Z0-9_]{36})',
                ],
                'aws_credentials': [
                    r'AKIA[0-9A-Z]{16}',  # AWS Access Key ID
                    r'aws_secret_access_key["\'\s]*[:=]["\'\s]*([a-zA-Z0-9+/]{40})',
                ]
            }
            
            # Scan all text files
            text_files = []
            for pattern in ['**/*.py', '**/*.js', '**/*.ts', '**/*.java', '**/*.json', 
                          '**/*.yml', '**/*.yaml', '**/*.env', '**/*.config', '**/*.properties']:
                text_files.extend(self.repo_path.rglob(pattern))
            
            for file_path in text_files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    relative_path = file_path.relative_to(self.repo_path)
                    lines = content.split('\n')
                    
                    for secret_type, patterns in secret_patterns.items():
                        for pattern in patterns:
                            for line_num, line in enumerate(lines, 1):
                                matches = re.finditer(pattern, line, re.IGNORECASE)
                                for match in matches:
                                    # Extract the secret value (usually in group 1)
                                    secret_value = match.group(1) if match.groups() else match.group(0)
                                    
                                    # Skip common false positives
                                    if self._is_false_positive_secret(secret_value, secret_type):
                                        continue
                                    
                                    secrets.append({
                                        "type": secret_type,
                                        "severity": "high",
                                        "file": str(relative_path),
                                        "line": line_num,
                                        "description": f"Potential {secret_type.replace('_', ' ')} found in source code",
                                        "secret_hash": hashlib.sha256(secret_value.encode()).hexdigest()[:16],
                                        "recommendation": f"Remove {secret_type} from source code and use environment variables or secure key management"
                                    })
                    
                except Exception as e:
                    logger.warning(f"Failed to scan {file_path} for secrets: {str(e)}")
                    continue
            
            return secrets
            
        except Exception as e:
            logger.error(f"Secret scanning failed: {str(e)}")
            return []
    
    def _check_sensitive_files(self) -> List[Dict[str, Any]]:
        """Check for sensitive files that might be exposed"""
        sensitive_files = []
        
        try:
            all_files = list(self.repo_path.rglob('*'))
            
            for file_path in all_files:
                if file_path.is_file():
                    file_name = file_path.name.lower()
                    relative_path = file_path.relative_to(self.repo_path)
                    
                    # Check against sensitive file patterns
                    for pattern in self.sensitive_files:
                        if re.search(pattern, str(relative_path), re.IGNORECASE):
                            sensitive_files.append({
                                "file": str(relative_path),
                                "type": "sensitive_file",
                                "severity": "medium",
                                "description": f"Sensitive file '{file_name}' may contain confidential information",
                                "recommendation": "Ensure this file is not publicly accessible and contains no sensitive data"
                            })
                            break
            
            return sensitive_files
            
        except Exception as e:
            logger.error(f"Sensitive file check failed: {str(e)}")
            return []
    
    def _check_file_permissions(self) -> List[Dict[str, Any]]:
        """Check for file permission issues"""
        permission_issues = []
        
        try:
            # Only check on Unix-like systems
            if os.name != 'posix':
                return permission_issues
            
            executable_files = []
            for pattern in ['**/*.sh', '**/*.py', '**/*.pl', '**/*.rb']:
                executable_files.extend(self.repo_path.rglob(pattern))
            
            for file_path in executable_files:
                try:
                    stat_info = file_path.stat()
                    mode = stat_info.st_mode
                    
                    # Check if file is world-writable
                    if mode & 0o002:
                        permission_issues.append({
                            "file": str(file_path.relative_to(self.repo_path)),
                            "type": "world_writable",
                            "severity": "medium",
                            "description": "File is world-writable",
                            "recommendation": "Remove world-write permissions"
                        })
                    
                    # Check if executable has overly permissive permissions
                    if mode & 0o111 and mode & 0o044:  # Executable and world/group readable
                        permission_issues.append({
                            "file": str(file_path.relative_to(self.repo_path)),
                            "type": "overly_permissive",
                            "severity": "low",
                            "description": "Executable file has broad read permissions",
                            "recommendation": "Review and restrict file permissions if necessary"
                        })
                    
                except Exception as e:
                    logger.warning(f"Failed to check permissions for {file_path}: {str(e)}")
                    continue
            
            return permission_issues
            
        except Exception as e:
            logger.error(f"File permission check failed: {str(e)}")
            return []
    
    def _analyze_security_configurations(self) -> List[Dict[str, Any]]:
        """Analyze security configurations in various config files"""
        misconfigurations = []
        
        try:
            # Check Docker configurations
            dockerfile_paths = list(self.repo_path.rglob('Dockerfile*'))
            for dockerfile in dockerfile_paths:
                misconfigs = self._analyze_dockerfile_security(dockerfile)
                misconfigurations.extend(misconfigs)
            
            # Check web server configurations
            config_files = list(self.repo_path.rglob('*.conf')) + list(self.repo_path.rglob('nginx.conf'))
            for config_file in config_files:
                misconfigs = self._analyze_web_config_security(config_file)
                misconfigurations.extend(misconfigs)
            
            # Check application configurations
            app_configs = (list(self.repo_path.rglob('config.json')) + 
                          list(self.repo_path.rglob('settings.py')) +
                          list(self.repo_path.rglob('application.properties')))
            for config_file in app_configs:
                misconfigs = self._analyze_app_config_security(config_file)
                misconfigurations.extend(misconfigs)
            
            return misconfigurations
            
        except Exception as e:
            logger.error(f"Security configuration analysis failed: {str(e)}")
            return []
    
    def _analyze_dockerfile_security(self, dockerfile_path: Path) -> List[Dict[str, Any]]:
        """Analyze Dockerfile for security issues"""
        issues = []
        
        try:
            with open(dockerfile_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            relative_path = dockerfile_path.relative_to(self.repo_path)
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Check for running as root
                if line.startswith('USER root') or 'USER 0' in line:
                    issues.append({
                        "file": str(relative_path),
                        "line": line_num,
                        "type": "docker_root_user",
                        "severity": "high",
                        "description": "Container runs as root user",
                        "recommendation": "Use non-root user for better security"
                    })
                
                # Check for ADD instruction with URLs
                if line.startswith('ADD') and ('http://' in line or 'https://' in line):
                    issues.append({
                        "file": str(relative_path),
                        "line": line_num,
                        "type": "docker_remote_add",
                        "severity": "medium",
                        "description": "ADD instruction with remote URL",
                        "recommendation": "Use COPY instead of ADD for local files, verify remote sources"
                    })
                
                # Check for --privileged flag
                if '--privileged' in line:
                    issues.append({
                        "file": str(relative_path),
                        "line": line_num,
                        "type": "docker_privileged",
                        "severity": "critical",
                        "description": "Container runs with privileged flag",
                        "recommendation": "Remove --privileged flag unless absolutely necessary"
                    })
            
            return issues
            
        except Exception as e:
            logger.warning(f"Failed to analyze Dockerfile {dockerfile_path}: {str(e)}")
            return []
    
    def _analyze_web_config_security(self, config_path: Path) -> List[Dict[str, Any]]:
        """Analyze web server configuration for security issues"""
        issues = []
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = config_path.relative_to(self.repo_path)
            
            # Check for missing security headers
            security_headers = ['X-Frame-Options', 'X-Content-Type-Options', 'X-XSS-Protection', 
                              'Strict-Transport-Security', 'Content-Security-Policy']
            
            for header in security_headers:
                if header.lower() not in content.lower():
                    issues.append({
                        "file": str(relative_path),
                        "type": "missing_security_header",
                        "severity": "medium",
                        "description": f"Missing security header: {header}",
                        "recommendation": f"Add {header} header for better security"
                    })
            
            # Check for server tokens exposure
            if 'server_tokens on' in content.lower():
                issues.append({
                    "file": str(relative_path),
                    "type": "server_tokens_exposed",
                    "severity": "low",
                    "description": "Server tokens are exposed",
                    "recommendation": "Set server_tokens to off to hide server version"
                })
            
            return issues
            
        except Exception as e:
            logger.warning(f"Failed to analyze web config {config_path}: {str(e)}")
            return []
    
    def _analyze_app_config_security(self, config_path: Path) -> List[Dict[str, Any]]:
        """Analyze application configuration for security issues"""
        issues = []
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = config_path.relative_to(self.repo_path)
            
            # Check for debug mode in production
            if re.search(r'debug\s*[=:]\s*true', content, re.IGNORECASE):
                issues.append({
                    "file": str(relative_path),
                    "type": "debug_mode_enabled",
                    "severity": "medium",
                    "description": "Debug mode appears to be enabled",
                    "recommendation": "Disable debug mode in production environments"
                })
            
            # Check for insecure cookie settings
            if re.search(r'secure\s*[=:]\s*false', content, re.IGNORECASE):
                issues.append({
                    "file": str(relative_path),
                    "type": "insecure_cookie",
                    "severity": "medium",
                    "description": "Cookies are not set to secure",
                    "recommendation": "Set secure flag on cookies for HTTPS connections"
                })
            
            return issues
            
        except Exception as e:
            logger.warning(f"Failed to analyze app config {config_path}: {str(e)}")
            return []
    
    async def _scan_dependency_vulnerabilities(self) -> List[Dict[str, Any]]:
        """Scan dependencies for known vulnerabilities"""
        vulnerabilities = []
        
        try:
            # Check for package files
            package_files = (list(self.repo_path.rglob('package.json')) +
                           list(self.repo_path.rglob('requirements.txt')) +
                           list(self.repo_path.rglob('pom.xml')) +
                           list(self.repo_path.rglob('Gemfile')) +
                           list(self.repo_path.rglob('composer.json')))
            
            for package_file in package_files:
                try:
                    if package_file.name == 'package.json':
                        vulns = await self._scan_npm_vulnerabilities(package_file)
                    elif package_file.name == 'requirements.txt':
                        vulns = await self._scan_python_vulnerabilities(package_file)
                    elif package_file.name == 'pom.xml':
                        vulns = await self._scan_maven_vulnerabilities(package_file)
                    else:
                        continue
                    
                    vulnerabilities.extend(vulns)
                    
                except Exception as e:
                    logger.warning(f"Failed to scan {package_file}: {str(e)}")
                    continue
            
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"Dependency vulnerability scanning failed: {str(e)}")
            return []
    
    async def _scan_npm_vulnerabilities(self, package_file: Path) -> List[Dict[str, Any]]:
        """Scan npm packages for vulnerabilities"""
        # This is a simplified implementation
        # In production, you'd integrate with npm audit API or vulnerability databases
        return [
            {
                "type": "dependency_vulnerability",
                "package": "example-package",
                "version": "1.0.0",
                "severity": "high",
                "description": "Known vulnerability in example-package",
                "recommendation": "Update to version 2.0.0 or higher",
                "cve_id": "CVE-2023-12345"
            }
        ]
    
    async def _scan_python_vulnerabilities(self, requirements_file: Path) -> List[Dict[str, Any]]:
        """Scan Python packages for vulnerabilities"""
        # Simplified implementation - would use safety, pip-audit, or similar tools
        return []
    
    async def _scan_maven_vulnerabilities(self, pom_file: Path) -> List[Dict[str, Any]]:
        """Scan Maven dependencies for vulnerabilities"""
        # Simplified implementation - would use OWASP Dependency Check or similar
        return []
    
    def _is_false_positive_secret(self, secret_value: str, secret_type: str) -> bool:
        """Check if detected secret is likely a false positive"""
        false_positive_patterns = [
            'example', 'test', 'demo', 'placeholder', 'changeme', 'password123',
            'your_api_key', 'your_password', 'your_secret', 'replace_me',
            'xxxxxxxx', '********', '12345678'
        ]
        
        secret_lower = secret_value.lower()
        return any(pattern in secret_lower for pattern in false_positive_patterns)
    
    def _get_vulnerability_severity(self, vuln_type: str) -> str:
        """Get severity level for vulnerability type"""
        severity_map = {
            'sql_injection': 'critical',
            'command_injection': 'critical',
            'xss_vulnerability': 'high',
            'path_traversal': 'high',
            'hardcoded_secrets': 'high',
            'weak_crypto': 'medium',
            'insecure_random': 'medium',
            'ldap_injection': 'high'
        }
        return severity_map.get(vuln_type, 'medium')
    
    def _get_vulnerability_description(self, vuln_type: str) -> str:
        """Get description for vulnerability type"""
        descriptions = {
            'sql_injection': 'Potential SQL injection vulnerability detected',
            'xss_vulnerability': 'Potential Cross-Site Scripting (XSS) vulnerability',
            'command_injection': 'Potential command injection vulnerability',
            'path_traversal': 'Potential path traversal vulnerability',
            'hardcoded_secrets': 'Hardcoded secret or credential detected',
            'weak_crypto': 'Use of weak cryptographic algorithm',
            'insecure_random': 'Use of insecure random number generator',
            'ldap_injection': 'Potential LDAP injection vulnerability'
        }
        return descriptions.get(vuln_type, 'Security vulnerability detected')
    
    def _get_vulnerability_recommendation(self, vuln_type: str) -> str:
        """Get recommendation for vulnerability type"""
        recommendations = {
            'sql_injection': 'Use parameterized queries or prepared statements',
            'xss_vulnerability': 'Properly encode output and validate input',
            'command_injection': 'Avoid executing user input, use safe APIs',
            'path_traversal': 'Validate and sanitize file paths, use whitelist approach',
            'hardcoded_secrets': 'Use environment variables or secure key management',
            'weak_crypto': 'Use strong cryptographic algorithms (AES, SHA-256, etc.)',
            'insecure_random': 'Use cryptographically secure random number generators',
            'ldap_injection': 'Properly escape LDAP queries and validate input'
        }
        return recommendations.get(vuln_type, 'Review and fix the security issue')
    
    def _get_cwe_id(self, vuln_type: str) -> str:
        """Get CWE ID for vulnerability type"""
        cwe_map = {
            'sql_injection': 'CWE-89',
            'xss_vulnerability': 'CWE-79',
            'command_injection': 'CWE-78',
            'path_traversal': 'CWE-22',
            'hardcoded_secrets': 'CWE-798',
            'weak_crypto': 'CWE-327',
            'insecure_random': 'CWE-338',
            'ldap_injection': 'CWE-90'
        }
        return cwe_map.get(vuln_type, 'CWE-00')
    
    def _get_owasp_category(self, vuln_type: str) -> str:
        """Get OWASP Top 10 category for vulnerability type"""
        owasp_map = {
            'sql_injection': 'A03:2021 - Injection',
            'xss_vulnerability': 'A03:2021 - Injection',
            'command_injection': 'A03:2021 - Injection',
            'path_traversal': 'A01:2021 - Broken Access Control',
            'hardcoded_secrets': 'A07:2021 - Identification and Authentication Failures',
            'weak_crypto': 'A02:2021 - Cryptographic Failures',
            'insecure_random': 'A02:2021 - Cryptographic Failures',
            'ldap_injection': 'A03:2021 - Injection'
        }
        return owasp_map.get(vuln_type, 'A10:2021 - Server-Side Request Forgery')
    
    def _calculate_security_score(self, results: Dict[str, Any]) -> float:
        """Calculate security score (1-6 scale)"""
        try:
            score = 6.0  # Start with perfect score
            
            # Critical issues penalty
            critical_count = results["summary"].get("critical_issues", 0)
            score -= critical_count * 2.0
            
            # High issues penalty
            high_count = results["summary"].get("high_issues", 0)
            score -= high_count * 1.0
            
            # Medium issues penalty
            medium_count = results["summary"].get("medium_issues", 0)
            score -= medium_count * 0.5
            
            # Secrets penalty
            secrets_count = results["summary"].get("secrets_count", 0)
            score -= secrets_count * 1.5
            
            # Dependency vulnerabilities penalty
            dep_vulns = results["summary"].get("dependency_vulnerabilities_count", 0)
            score -= dep_vulns * 0.5
            
            return max(1.0, min(6.0, round(score, 1)))
            
        except Exception as e:
            logger.error(f"Security score calculation failed: {str(e)}")
            return 3.0
    
    def _generate_security_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate security recommendations based on findings"""
        recommendations = []
        
        if results["summary"].get("critical_issues", 0) > 0:
            recommendations.append("🚨 Address all critical security vulnerabilities immediately")
        
        if results["summary"].get("secrets_count", 0) > 0:
            recommendations.append("🔐 Remove all hardcoded secrets and use secure key management")
        
        if results["summary"].get("dependency_vulnerabilities_count", 0) > 0:
            recommendations.append("📦 Update vulnerable dependencies to secure versions")
        
        if results["summary"].get("high_issues", 0) > 5:
            recommendations.append("🔒 Implement comprehensive input validation and output encoding")
        
        recommendations.extend([
            "🛡️ Implement automated security scanning in CI/CD pipeline",
            "📋 Conduct regular security code reviews",
            "🔍 Enable security logging and monitoring",
            "📚 Provide security training for development team"
        ])
        
        return recommendations[:6]  # Limit to top 6 recommendations 