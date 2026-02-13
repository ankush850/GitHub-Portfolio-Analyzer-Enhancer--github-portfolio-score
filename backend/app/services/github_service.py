import httpx
from typing import Dict, List, Any
from ..config import Config

class GitHubService:
    def __init__(self):
        self.base_url = Config.GITHUB_API_BASE_URL
        self.headers = {
            "Authorization": f"token {Config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.client = httpx.AsyncClient(headers=self.headers, timeout=30.0)
    
    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Fetch user profile information"""
        try:
            response = await self.client.get(
                f"{self.base_url}/users/{username}"
            )
            response.raise_for_status()
            data = response.json()
            
            # Get additional contribution data
            events = await self.get_user_events(username)
            
            return {
                "login": data["login"],
                "name": data["name"],
                "bio": data["bio"],
                "public_repos": data["public_repos"],
                "followers": data["followers"],
                "following": data["following"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
                "avatar_url": data["avatar_url"],
                "html_url": data["html_url"],
                "recent_activity": len(events) if events else 0
            }
        except httpx.HTTPError as e:
            raise Exception(f"GitHub API error: {str(e)}")
    
    async def get_repositories(self, username: str) -> List[Dict[str, Any]]:
        """Fetch all public repositories for a user"""
        try:
            response = await self.client.get(
                f"{self.base_url}/users/{username}/repos",
                params={"sort": "updated", "per_page": 100}
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"GitHub API error: {str(e)}")
    
    async def get_repository_details(self, username: str, repo_name: str) -> Dict[str, Any]:
        """Fetch detailed repository information"""
        try:
            response = await self.client.get(
                f"{self.base_url}/repos/{username}/{repo_name}"
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise Exception(f"GitHub API error: {str(e)}")
    
    async def get_readme_content(self, username: str, repo_name: str) -> str:
        """Fetch README content for a repository"""
        try:
            response = await self.client.get(
                f"{self.base_url}/repos/{username}/{repo_name}/readme"
            )
            if response.status_code == 404:
                return ""
            
            response.raise_for_status()
            data = response.json()
            
            # Decode content from base64
            import base64
            content = base64.b64decode(data["content"]).decode("utf-8")
            return content
        except:
            return ""
    
    async def get_languages(self, username: str, repo_name: str) -> Dict[str, int]:
        """Fetch languages used in a repository"""
        try:
            response = await self.client.get(
                f"{self.base_url}/repos/{username}/{repo_name}/languages"
            )
            response.raise_for_status()
            return response.json()
        except:
            return {}
    
    async def get_commits(self, username: str, repo_name: str) -> List[Dict[str, Any]]:
        """Fetch recent commits for a repository"""
        try:
            response = await self.client.get(
                f"{self.base_url}/repos/{username}/{repo_name}/commits",
                params={"per_page": 30}
            )
            response.raise_for_status()
            return response.json()
        except:
            return []
    
    async def get_user_events(self, username: str) -> List[Dict[str, Any]]:
        """Fetch user events for activity analysis"""
        try:
            response = await self.client.get(
                f"{self.base_url}/users/{username}/events",
                params={"per_page": 30}
            )
            response.raise_for_status()
            return response.json()
        except:
            return []
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()