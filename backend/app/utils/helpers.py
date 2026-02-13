import re
from typing import Optional

def validate_github_username(username: str) -> bool:
    """
    Validate GitHub username format
    GitHub usernames can only contain alphanumeric characters and hyphens
    """
    if not username or len(username) > 39:
        return False
    
    pattern = r'^[a-zA-Z0-9](?:[a-zA-Z0-9]|-(?=[a-zA-Z0-9])){0,38}$'
    return bool(re.match(pattern, username))

def extract_username_from_url(url: str) -> Optional[str]:
    """Extract GitHub username from profile URL"""
    patterns = [
        r'github\.com/([^/]+)/?$',
        r'github\.com/([^/]+)/?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def format_number(num: int) -> str:
    """Format large numbers with K/M suffix"""
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return f"{num/1000:.1f}K"
    else:
        return f"{num/1000000:.1f}M"

def calculate_percentage(part: float, whole: float) -> float:
    """Calculate percentage safely"""
    if whole == 0:
        return 0
    return (part / whole) * 100