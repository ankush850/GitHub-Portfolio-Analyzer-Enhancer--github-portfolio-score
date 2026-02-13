from typing import Dict, List, Any
from datetime import datetime, timedelta
import re

from .github_service import GitHubService
from ..config import Config

class AnalyzerService:
    def __init__(self):
        self.github_service = GitHubService()
    
    async def analyze_repository(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive analysis on a single repository"""
        username = repo_data["owner"]["login"]
        repo_name = repo_data["name"]
        
        # Fetch additional data
        readme_content = await self.github_service.get_readme_content(username, repo_name)
        languages = await self.github_service.get_languages(username, repo_name)
        commits = await self.github_service.get_commits(username, repo_name)
        
        # Analyze documentation
        doc_analysis = self._analyze_documentation(readme_content, repo_data)
        
        # Analyze code structure (simplified for now)
        code_analysis = self._analyze_code_structure(repo_data, languages)
        
        # Analyze activity
        activity_analysis = self._analyze_activity(commits, repo_data)
        
        # Calculate repository score
        repo_score = self._calculate_repo_score(
            doc_analysis, code_analysis, activity_analysis, repo_data
        )
        
        return {
            "name": repo_name,
            "full_name": repo_data["full_name"],
            "description": repo_data["description"],
            "url": repo_data["html_url"],
            "stars": repo_data["stargazers_count"],
            "forks": repo_data["forks_count"],
            "open_issues": repo_data["open_issues_count"],
            "created_at": repo_data["created_at"],
            "updated_at": repo_data["updated_at"],
            "languages": languages,
            "documentation_analysis": doc_analysis,
            "code_analysis": code_analysis,
            "activity_analysis": activity_analysis,
            "score": repo_score,
            "strengths": self._identify_strengths(repo_data, doc_analysis, activity_analysis),
            "weaknesses": self._identify_weaknesses(repo_data, doc_analysis, activity_analysis)
        }
    
    def _analyze_documentation(self, readme_content: str, repo_data: Dict) -> Dict:
        """Analyze README and documentation quality"""
        if not readme_content:
            return {
                "has_readme": False,
                "readme_length": 0,
                "has_setup_instructions": False,
                "has_examples": False,
                "has_badges": False,
                "quality_score": 0
            }
        
        # Check for key sections
        has_setup = bool(re.search(r"(install|setup|getting started)", readme_content, re.I))
        has_examples = bool(re.search(r"(example|usage|demo)", readme_content, re.I))
        has_badges = bool(re.search(r"!\[.*\]\(.*\)", readme_content))
        has_api_docs = bool(re.search(r"(api|endpoint|route)", readme_content, re.I))
        
        # Calculate quality score
        quality_score = 0
        if len(readme_content) > 500:
            quality_score += 30
        elif len(readme_content) > 200:
            quality_score += 15
        
        if has_setup:
            quality_score += 20
        if has_examples:
            quality_score += 20
        if has_badges:
            quality_score += 15
        if has_api_docs:
            quality_score += 15
        
        return {
            "has_readme": True,
            "readme_length": len(readme_content),
            "has_setup_instructions": has_setup,
            "has_examples": has_examples,
            "has_badges": has_badges,
            "has_api_documentation": has_api_docs,
            "quality_score": min(quality_score, 100)
        }
    
    def _analyze_code_structure(self, repo_data: Dict, languages: Dict) -> Dict:
        """Analyze code organization and structure"""
        has_multiple_languages = len(languages) > 1
        primary_language = repo_data.get("language")
        
        # Simplified analysis for MVP
        return {
            "primary_language": primary_language,
            "languages_used": list(languages.keys()),
            "language_diversity": len(languages),
            "has_multiple_languages": has_multiple_languages,
            "size_kb": repo_data.get("size", 0),
            "has_issues_enabled": repo_data.get("has_issues", False),
            "has_projects_enabled": repo_data.get("has_projects", False),
            "has_wiki_enabled": repo_data.get("has_wiki", False)
        }
    
    def _analyze_activity(self, commits: List, repo_data: Dict) -> Dict:
        """Analyze commit activity and consistency"""
        if not commits:
            return {
                "total_commits_recent": 0,
                "commit_frequency": 0,
                "last_commit_date": None,
                "is_active": False,
                "activity_score": 0
            }
        
        # Calculate commit frequency
        commit_dates = [commit["commit"]["committer"]["date"] for commit in commits]
        if len(commit_dates) > 1:
            first_date = datetime.fromisoformat(commit_dates[-1].replace("Z", "+00:00"))
            last_date = datetime.fromisoformat(commit_dates[0].replace("Z", "+00:00"))
            days_diff = (last_date - first_date).days
            if days_diff > 0:
                commit_frequency = len(commits) / days_diff
            else:
                commit_frequency = len(commits)
        else:
            commit_frequency = 1
        
        # Check if recently active (using timezone-aware datetime)
        last_commit = datetime.fromisoformat(commit_dates[0].replace("Z", "+00:00"))
        from datetime import timezone
        now = datetime.now(timezone.utc)
        days_since_last_commit = (now - last_commit).days
        is_active = days_since_last_commit < Config.ACTIVE_DAYS_THRESHOLD
        
        # Calculate activity score
        activity_score = 0
        if is_active:
            activity_score += 40
        if commit_frequency > 0.5:  # More than 1 commit every 2 days
            activity_score += 30
        elif commit_frequency > 0.1:
            activity_score += 15
        
        activity_score += min(len(commits), 30)  # Up to 30 points for volume
        
        return {
            "total_commits_recent": len(commits),
            "commit_frequency": round(commit_frequency, 2),
            "last_commit_date": commit_dates[0],
            "days_since_last_commit": days_since_last_commit,
            "is_active": is_active,
            "activity_score": min(activity_score, 100)
        }
    
    def _calculate_repo_score(self, doc_analysis: Dict, code_analysis: Dict, 
                             activity_analysis: Dict, repo_data: Dict) -> Dict:
        """Calculate individual repository score"""
        # Weights for different aspects
        doc_weight = 0.35
        code_weight = 0.25
        activity_weight = 0.25
        popularity_weight = 0.15
        
        # Get individual scores
        doc_score = doc_analysis.get("quality_score", 0)
        activity_score = activity_analysis.get("activity_score", 0)
        
        # Code score (simplified)
        code_score = 50  # Base score
        if code_analysis.get("has_multiple_languages"):
            code_score += 20
        if code_analysis.get("has_wiki_enabled"):
            code_score += 15
        code_score = min(code_score, 100)
        
        # Popularity score
        stars = repo_data.get("stargazers_count", 0)
        forks = repo_data.get("forks_count", 0)
        popularity_score = min(stars * 2 + forks * 3, 100)
        
        # Calculate overall
        overall = (
            doc_score * doc_weight +
            code_score * code_weight +
            activity_score * activity_weight +
            popularity_score * popularity_weight
        )
        
        return {
            "overall": round(overall, 2),
            "documentation": doc_score,
            "code_quality": code_score,
            "activity": activity_score,
            "popularity": popularity_score,
            "grade": self._get_grade(overall)
        }
    
    def _identify_strengths(self, repo_data: Dict, doc_analysis: Dict, activity_analysis: Dict) -> List[str]:
        """Identify repository strengths"""
        strengths = []
        
        if doc_analysis.get("quality_score", 0) > 70:
            strengths.append("Excellent documentation")
        elif doc_analysis.get("has_readme"):
            strengths.append("Has README")
        
        if repo_data.get("stargazers_count", 0) > 10:
            strengths.append(f"Popular ({repo_data['stargazers_count']} stars)")
        
        if activity_analysis.get("is_active"):
            strengths.append("Actively maintained")
        
        if repo_data.get("language"):
            strengths.append(f"Built with {repo_data['language']}")
        
        return strengths[:3]  # Return top 3
    
    def _identify_weaknesses(self, repo_data: Dict, doc_analysis: Dict, activity_analysis: Dict) -> List[str]:
        """Identify repository weaknesses"""
        weaknesses = []
        
        if not doc_analysis.get("has_readme"):
            weaknesses.append("Missing README")
        elif doc_analysis.get("readme_length", 0) < 100:
            weaknesses.append("README too brief")
        
        if not doc_analysis.get("has_setup_instructions"):
            weaknesses.append("No setup instructions")
        
        if not activity_analysis.get("is_active"):
            weaknesses.append("Inactive repository")
        
        if activity_analysis.get("total_commits_recent", 0) < 5:
            weaknesses.append("Low commit activity")
        
        return weaknesses[:3]
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"