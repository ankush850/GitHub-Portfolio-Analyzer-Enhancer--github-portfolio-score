from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import asyncio

from ..services.github_service import GitHubService
from ..services.analyzer_service import AnalyzerService
from ..services.score_calculator import ScoreCalculator
from ..services.recruiter_simulator import RecruiterSimulator
from ..services.roadmap_generator import RoadmapGenerator
from ..models.user_profile import UserProfile
from ..utils.helpers import validate_github_username
from ..config import Config

router = APIRouter()

@router.get("/analyze/{username}")
async def analyze_github_profile(username: str):
    """
    Analyze a GitHub profile and return comprehensive portfolio analysis
    """
    try:
        # Validate username
        if not validate_github_username(username):
            raise HTTPException(status_code=400, detail="Invalid GitHub username")
        
        # Initialize services
        github_service = GitHubService()
        analyzer = AnalyzerService()
        score_calculator = ScoreCalculator()
        recruiter_sim = RecruiterSimulator()
        roadmap_gen = RoadmapGenerator()
        
        # Fetch GitHub data
        user_data = await github_service.get_user_profile(username)
        repositories = await github_service.get_repositories(username)
        
        # Limit repositories for performance
        repositories = repositories[:Config.MAX_REPOS_TO_ANALYZE]
        
        # Analyze each repository
        analyzed_repos = []
        for repo in repositories:
            repo_analysis = await analyzer.analyze_repository(repo)
            analyzed_repos.append(repo_analysis)
        
        # Calculate scores
        portfolio_score = score_calculator.calculate_portfolio_score(
            user_data, analyzed_repos
        )
        
        # Generate recruiter feedback
        recruiter_feedback = recruiter_sim.simulate_review(
            user_data, analyzed_repos, portfolio_score
        )
        
        # Generate improvement roadmap
        roadmap = roadmap_gen.generate_roadmap(
            portfolio_score, analyzed_repos
        )
        
        # Create user profile
        profile = UserProfile(
            username=username,
            user_data=user_data,
            repositories=analyzed_repos,
            score=portfolio_score,
            recruiter_feedback=recruiter_feedback,
            roadmap=roadmap
        )
        
        return profile.dict()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{username}/basic")
async def get_basic_profile(username: str):
    """
    Get basic GitHub profile information
    """
    try:
        github_service = GitHubService()
        user_data = await github_service.get_user_profile(username)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))