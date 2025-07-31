import logging
import re
from typing import Dict, Any, Optional
from urllib.parse import urlparse
import httpx

logger = logging.getLogger(__name__)

class GitHubService:
    """Service for interacting with GitHub API"""
    
    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        
    async def get_repository_info(self, repository_url: str) -> Dict[str, Any]:
        """Extract repository information from GitHub URL"""
        try:
            # Parse GitHub URL to extract owner and repo
            parsed = urlparse(repository_url)
            path_parts = parsed.path.strip('/').split('/')
            
            if len(path_parts) >= 2:
                owner = path_parts[0]
                repo = path_parts[1].replace('.git', '')
                
                return {
                    "owner": owner,
                    "name": repo,
                    "full_name": f"{owner}/{repo}",
                    "clone_url": repository_url,
                    "api_url": f"{self.base_url}/repos/{owner}/{repo}"
                }
            else:
                raise ValueError("Invalid GitHub URL format")
                
        except Exception as e:
            logger.error(f"Failed to parse repository URL {repository_url}: {str(e)}")
            # Fallback - extract from URL pattern
            match = re.search(r'github\.com[/:]([^/]+)/([^/]+?)(?:\.git)?/?$', repository_url)
            if match:
                owner, repo = match.groups()
                return {
                    "owner": owner,
                    "name": repo,
                    "full_name": f"{owner}/{repo}",
                    "clone_url": repository_url,
                    "api_url": f"{self.base_url}/repos/{owner}/{repo}"
                }
            else:
                raise ValueError(f"Cannot parse GitHub URL: {repository_url}")
    
    async def get_repository_details(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get detailed repository information from GitHub API"""
        try:
            if not self.github_token:
                logger.warning("No GitHub token provided, skipping API call")
                return None
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"GitHub API returned {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"Failed to fetch repository details: {str(e)}")
            return None
    
    async def get_contributors(self, owner: str, repo: str) -> Optional[list]:
        """Get repository contributors"""
        try:
            if not self.github_token:
                return None
            
            headers = {
                "Authorization": f"token {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/repos/{owner}/{repo}/contributors",
                    headers=headers
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return None
                    
        except Exception as e:
            logger.error(f"Failed to fetch contributors: {str(e)}")
            return None 