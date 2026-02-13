from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel

class UserProfile(BaseModel):
    """User profile model"""
    username: str
    user_data: Dict[str, Any]
    repositories: List[Dict[str, Any]]
    score: Dict[str, Any]
    recruiter_feedback: Dict[str, Any]
    roadmap: Dict[str, Any]
    analyzed_at: datetime = datetime.now()
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "user_data": {
                    "name": "John Doe",
                    "bio": "Full Stack Developer",
                    "public_repos": 10
                },
                "score": {
                    "overall": 75.5,
                    "grade": "B"
                }
            }
        }

class Repository(BaseModel):
    """Repository model"""
    name: str
    full_name: str
    description: Optional[str]
    url: str
    stars: int
    forks: int
    open_issues: int
    created_at: str
    updated_at: str
    languages: Dict[str, int]
    documentation_analysis: Dict[str, Any]
    code_analysis: Dict[str, Any]
    activity_analysis: Dict[str, Any]
    score: Dict[str, Any]
    strengths: List[str]
    weaknesses: List[str]