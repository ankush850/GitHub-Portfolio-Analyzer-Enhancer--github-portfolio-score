from typing import Dict, List, Any
import random

class RecruiterSimulator:
    def __init__(self):
        self.recruiter_personalities = [
            "Technical Recruiter",
            "Hiring Manager",
            "Tech Lead",
            "HR Specialist"
        ]
    
    def simulate_review(self, user_data: Dict, repositories: List[Dict], 
                       portfolio_score: Dict) -> Dict[str, Any]:
        """Generate recruiter-like feedback"""
        
        # Choose random recruiter type
        recruiter_type = random.choice(self.recruiter_personalities)
        
        # Generate first impression
        first_impression = self._generate_first_impression(user_data, repositories)
        
        # Determine hire decision
        hire_decision = self._determine_hire_decision(portfolio_score)
        
        # Generate interview questions
        interview_questions = self._generate_interview_questions(repositories)
        
        return {
            "recruiter_type": recruiter_type,
            "first_impression": first_impression,
            "decision": hire_decision,
            "summary": self._generate_summary(portfolio_score, repositories),
            "strengths": portfolio_score.get("strengths", []),
            "concerns": portfolio_score.get("red_flags", []),
            "interview_questions": interview_questions,
            "recommendations": self._generate_recruiter_recommendations(repositories)
        }
    
    def _generate_first_impression(self, user_data: Dict, repositories: List[Dict]) -> str:
        """Generate first impression text"""
        name = user_data.get("name") or user_data.get("login")
        repo_count = len(repositories)
        
        if repo_count == 0:
            return f"⚠️ {name} has no public repositories. This is a major concern."
        
        # Check for well-documented repos
        good_readme_count = sum(1 for repo in repositories 
                              if repo.get("documentation_analysis", {}).get("quality_score", 0) > 50)
        
        if good_readme_count > repo_count / 2:
            return f"✅ Positive first impression! {name} maintains {good_readme_count} well-documented repositories."
        elif repo_count >= 3:
            return f"👀 {name} has {repo_count} repositories, but documentation quality varies."
        else:
            return f"🔍 Limited portfolio with only {repo_count} repositories to evaluate."
    
    def _determine_hire_decision(self, portfolio_score: Dict) -> Dict[str, Any]:
        """Determine hire/maybe/reject decision"""
        overall_score = portfolio_score.get("overall", 0)
        grade = portfolio_score.get("grade", "F")
        
        if overall_score >= 80:
            decision = "HIRE"
            confidence = "High"
            reasoning = "Strong portfolio with excellent documentation and consistent activity"
        elif overall_score >= 60:
            decision = "MAYBE"
            confidence = "Medium"
            reasoning = "Decent portfolio but needs improvement in key areas"
        else:
            decision = "REJECT"
            confidence = "High" if overall_score < 40 else "Medium"
            reasoning = "Portfolio lacks critical elements expected from candidates"
        
        return {
            "decision": decision,
            "confidence": confidence,
            "reasoning": reasoning,
            "score": overall_score,
            "grade": grade
        }
    
    def _generate_interview_questions(self, repositories: List[Dict]) -> List[str]:
        """Generate potential interview questions based on repositories"""
        questions = []
        
        if not repositories:
            questions.append("Can you walk us through your development experience?")
            questions.append("What projects have you worked on that aren't on GitHub?")
            return questions
        
        # Pick top 2 repositories
        top_repos = sorted(repositories, 
                          key=lambda x: x.get("score", {}).get("overall", 0), 
                          reverse=True)[:2]
        
        for repo in top_repos:
            repo_name = repo.get("name")
            languages = repo.get("languages", {})
            primary_lang = list(languages.keys())[0] if languages else "Unknown"
            
            questions.append(f"Tell me about your role in developing {repo_name}.")
            questions.append(f"What challenges did you face while building {repo_name}?")
            questions.append(f"How do you handle {primary_lang} best practices in your projects?")
        
        # Add generic questions
        questions.append("How do you approach documentation in your projects?")
        questions.append("Describe your development workflow and commit practices.")
        
        return questions[:5]  # Return top 5 questions
    
    def _generate_summary(self, portfolio_score: Dict, repositories: List[Dict]) -> str:
        """Generate summary paragraph"""
        score = portfolio_score.get("overall", 0)
        grade = portfolio_score.get("grade", "F")
        repo_count = len(repositories)
        
        if score >= 80:
            return f"Strong candidate with an impressive portfolio (Grade {grade}). Shows consistency across {repo_count} projects with good documentation practices."
        elif score >= 60:
            return f"Promising candidate (Grade {grade}) with {repo_count} repositories. Shows potential but needs to improve documentation and project consistency."
        else:
            return f"Entry-level candidate (Grade {grade}) with basic GitHub presence. Needs significant improvement to be competitive in the job market."
    
    def _generate_recruiter_recommendations(self, repositories: List[Dict]) -> List[Dict]:
        """Generate recruiter-specific recommendations"""
        recommendations = []
        
        if not repositories:
            recommendations.append({
                "task": "Start building public repositories",
                "details": "Create repositories to showcase your coding skills and projects",
                "priority": "Critical",
                "estimated_time": "Ongoing"
            })
            recommendations.append({
                "task": "Contribute to open source projects",
                "details": "Find projects aligned with your interests and contribute code",
                "priority": "High",
                "estimated_time": "2-4 hours/week"
            })
            return recommendations
        
        # Check for documentation issues
        poor_docs = sum(1 for repo in repositories 
                       if repo.get("documentation_analysis", {}).get("quality_score", 0) < 50)
        if poor_docs > len(repositories) / 2:
            recommendations.append({
                "task": "Improve README documentation",
                "details": "Add clear descriptions, setup instructions, and usage examples to your projects",
                "priority": "High",
                "estimated_time": "1-2 hours per repo"
            })
        
        # Check for activity
        inactive = sum(1 for repo in repositories 
                      if not repo.get("activity_analysis", {}).get("is_active", False))
        if inactive > 0:
            recommendations.append({
                "task": "Show recent activity",
                "details": "Make regular commits to demonstrate active development",
                "priority": "Medium",
                "estimated_time": "30 minutes/week"
            })
        
        recommendations.append({
            "task": "Pin your best repositories",
            "details": "Select 3-6 repositories that best represent your skills and pin them to your profile",
            "priority": "Medium",
            "estimated_time": "15 minutes"
        })
        
        recommendations.append({
            "task": "Add a detailed bio",
            "details": "Update your GitHub profile with your current role, skills, and interests",
            "priority": "Low",
            "estimated_time": "10 minutes"
        })
        
        return recommendations[:4]