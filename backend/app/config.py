import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # GitHub API Configuration
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    GITHUB_API_BASE_URL = "https://api.github.com"
    
    # Debug: Print token info (first 10 chars for security)
    print(f"Token loaded: {GITHUB_TOKEN[:10] if GITHUB_TOKEN else 'None'}...")
    
    # App Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 8000))
    
    # Scoring Weights
    SCORING_WEIGHTS = {
        'documentation': 0.25,
        'code_quality': 0.25,
        'consistency': 0.20,
        'impact': 0.20,
        'depth': 0.10
    }
    
    # Thresholds
    MINIMUM_REPOS_FOR_SCORE = 1
    GOOD_README_LENGTH = 100  # characters
    ACTIVE_DAYS_THRESHOLD = 30  # days
    
    # Rate Limiting
    MAX_REPOS_TO_ANALYZE = 20