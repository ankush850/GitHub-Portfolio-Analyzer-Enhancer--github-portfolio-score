from typing import Dict, List, Any
from ..config import Config

class ScoreCalculator:
    def __init__(self):
        self.weights = Config.SCORING_WEIGHTS
    
    def calculate_portfolio_score(self, user_data: Dict[str, Any], 
                                 repositories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall portfolio score"""
        
        # Component scores
        doc_score = self._calculate_documentation_score(repositories)
        code_score = self._calculate_code_quality_score(repositories)
        consistency_score = self._calculate_consistency_score(repositories, user_data)
        impact_score = self._calculate_impact_score(repositories)
        depth_score = self._calculate_technical_depth_score(repositories)
        
        # Calculate weighted overall score
        overall = (
            doc_score * self.weights['documentation'] +
            code_score * self.weights['code_quality'] +
            consistency_score * self.weights['consistency'] +
            impact_score * self.weights['impact'] +
            depth_score * self.weights['depth']
        )
        
        return {
            "overall": round(overall, 2),
            "components": {
                "documentation": round(doc_score, 2),
                "code_quality": round(code_score, 2),
                "consistency": round(consistency_score, 2),
                "impact": round(impact_score, 2),
                "depth": round(depth_score, 2)
            },
            "grade": self._get_grade(overall),
            "red_flags": self._identify_red_flags(repositories),
            "strengths": self._identify_portfolio_strengths(repositories)
        }
    
    def _calculate_documentation_score(self, repositories: List[Dict]) -> float:
        """Calculate documentation quality score across all repos"""
        if not repositories:
            return 0
        
        total_doc_score = 0
        for repo in repositories:
            doc_analysis = repo.get("documentation_analysis", {})
            total_doc_score += doc_analysis.get("quality_score", 0)
        
        return total_doc_score / len(repositories)
    
    def _calculate_code_quality_score(self, repositories: List[Dict]) -> float:
        """Calculate code quality score across all repos"""
        if not repositories:
            return 0
        
        total_code_score = 0
        for repo in repositories:
            repo_score = repo.get("score", {})
            total_code_score += repo_score.get("code_quality", 50)
        
        return total_code_score / len(repositories)
    
    def _calculate_consistency_score(self, repositories: List[Dict], user_data: Dict) -> float:
        """Calculate consistency of contributions"""
        if not repositories:
            return 0
        
        # Check if any repos are recently active
        active_repos = sum(1 for repo in repositories 
                          if repo.get("activity_analysis", {}).get("is_active", False))
        
        activity_ratio = active_repos / len(repositories) if repositories else 0
        
        # Consider recent events
        recent_activity = user_data.get("recent_activity", 0)
        activity_bonus = min(recent_activity, 50) / 50 * 20  # Up to 20 points
        
        score = (activity_ratio * 80) + activity_bonus
        return min(score, 100)
    
    def _calculate_impact_score(self, repositories: List[Dict]) -> float:
        """Calculate project impact based on stars and forks"""
        if not repositories:
            return 0
        
        total_stars = sum(repo.get("stars", 0) for repo in repositories)
        total_forks = sum(repo.get("forks", 0) for repo in repositories)
        
        # Impact score formula
        impact_score = min(total_stars * 2 + total_forks * 3, 100)
        return impact_score
    
    def _calculate_technical_depth_score(self, repositories: List[Dict]) -> float:
        """Calculate technical depth based on language diversity"""
        if not repositories:
            return 0
        
        # Collect all languages
        all_languages = set()
        for repo in repositories:
            languages = repo.get("languages", {})
            all_languages.update(languages.keys())
        
        # Score based on language diversity
        language_count = len(all_languages)
        if language_count >= 5:
            return 100
        elif language_count >= 3:
            return 80
        elif language_count >= 2:
            return 60
        elif language_count >= 1:
            return 40
        else:
            return 20
    
    def _identify_red_flags(self, repositories: List[Dict]) -> List[str]:
        """Identify red flags in the portfolio"""
        red_flags = []
        
        if not repositories:
            red_flags.append("No public repositories")
            return red_flags
        
        # Check for inactive repos
        inactive_repos = sum(1 for repo in repositories 
                           if not repo.get("activity_analysis", {}).get("is_active", False))
        if inactive_repos == len(repositories):
            red_flags.append("All repositories are inactive")
        
        # Check for missing READMEs
        repos_without_readme = sum(1 for repo in repositories 
                                 if not repo.get("documentation_analysis", {}).get("has_readme", False))
        if repos_without_readme > len(repositories) / 2:
            red_flags.append("Most repositories missing README files")
        
        # Check for low star count
        total_stars = sum(repo.get("stars", 0) for repo in repositories)
        if total_stars == 0:
            red_flags.append("No stars on any repositories")
        
        return red_flags
    
    def _identify_portfolio_strengths(self, repositories: List[Dict]) -> List[str]:
        """Identify overall portfolio strengths"""
        strengths = []
        
        if len(repositories) >= 5:
            strengths.append(f"Strong portfolio with {len(repositories)} repositories")
        
        # Check for well-documented repos
        well_documented = sum(1 for repo in repositories 
                            if repo.get("documentation_analysis", {}).get("quality_score", 0) > 70)
        if well_documented >= 3:
            strengths.append("Multiple well-documented projects")
        
        # Check for diverse languages
        all_languages = set()
        for repo in repositories:
            languages = repo.get("languages", {})
            all_languages.update(languages.keys())
        if len(all_languages) >= 3:
            strengths.append(f"Demonstrates proficiency in {len(all_languages)} programming languages")
        
        return strengths[:3]
    
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