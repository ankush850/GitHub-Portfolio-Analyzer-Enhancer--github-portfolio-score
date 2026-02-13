from typing import Dict, List, Any
from datetime import datetime, timedelta

class RoadmapGenerator:
    def __init__(self):
        pass
    
    def generate_roadmap(self, portfolio_score: Dict, repositories: List[Dict]) -> Dict[str, Any]:
        """Generate personalized improvement roadmap"""
        
        # Generate immediate actions (7 days)
        immediate_actions = self._generate_immediate_actions(portfolio_score, repositories)
        
        # Generate short-term goals (30 days)
        short_term_goals = self._generate_short_term_goals(portfolio_score, repositories)
        
        # Generate long-term goals (90 days)
        long_term_goals = self._generate_long_term_goals(portfolio_score, repositories)
        
        return {
            "generated_at": datetime.now().isoformat(),
            "timeline": {
                "immediate": {
                    "timeframe": "Next 7 Days",
                    "actions": immediate_actions
                },
                "short_term": {
                    "timeframe": "Next 30 Days",
                    "actions": short_term_goals
                },
                "long_term": {
                    "timeframe": "Next 90 Days",
                    "goals": long_term_goals
                }
            },
            "priority_focus": self._get_priority_focus(portfolio_score),
            "estimated_impact": self._estimate_impact(portfolio_score)
        }
    
    def _generate_immediate_actions(self, portfolio_score: Dict, repositories: List[Dict]) -> List[Dict]:
        """Generate actions for next 7 days"""
        actions = []
        
        # Get red flags and weaknesses
        red_flags = portfolio_score.get("red_flags", [])
        
        if "No public repositories" in red_flags:
            actions.append({
                "task": "Create your first public repository",
                "details": "Start with a simple project to showcase your skills",
                "priority": "Critical",
                "estimated_time": "2-3 hours"
            })
        
        # Check README issues
        repos_without_readme = [r for r in repositories 
                              if not r.get("documentation_analysis", {}).get("has_readme", False)]
        if repos_without_readme:
            actions.append({
                "task": f"Add README to {repos_without_readme[0]['name']}",
                "details": "Include project description, setup instructions, and usage examples",
                "priority": "High",
                "estimated_time": "1-2 hours"
            })
        
        # Check for pinned repos
        actions.append({
            "task": "Pin your best repositories",
            "details": "Select 3-6 repositories that best represent your skills",
            "priority": "Medium",
            "estimated_time": "15 minutes"
        })
        
        # Add bio improvement
        actions.append({
            "task": "Update your GitHub profile bio",
            "details": "Add your current role, skills, and what you're looking for",
            "priority": "Medium",
            "estimated_time": "30 minutes"
        })
        
        return actions[:4]  # Return top 4 actions
    
    def _generate_short_term_goals(self, portfolio_score: Dict, repositories: List[Dict]) -> List[Dict]:
        """Generate goals for next 30 days"""
        goals = []
        
        # Documentation improvement
        poor_docs = [r for r in repositories 
                    if r.get("documentation_analysis", {}).get("quality_score", 0) < 50]
        if poor_docs:
            goals.append({
                "goal": "Improve documentation for 3 repositories",
                "tasks": [
                    "Add setup instructions",
                    "Include usage examples",
                    "Add badges for build status, license"
                ],
                "target_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            })
        
        # Activity consistency
        goals.append({
            "goal": "Establish consistent commit pattern",
            "tasks": [
                "Commit at least 4 times per week",
                "Work on one project consistently",
                "Create a contribution schedule"
            ],
            "target_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        })
        
        # New project
        goals.append({
            "goal": "Start a new project in a different language",
            "tasks": [
                "Choose a language you want to learn",
                "Build a small utility or tool",
                "Document the learning process"
            ],
            "target_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        })
        
        return goals[:3]
    
    def _generate_long_term_goals(self, portfolio_score: Dict, repositories: List[Dict]) -> List[Dict]:
        """Generate goals for next 90 days"""
        goals = []
        
        # Major project
        goals.append({
            "goal": "Complete a portfolio-worthy project",
            "milestones": [
                "Week 1-2: Project planning and setup",
                "Week 3-6: Core feature development",
                "Week 7-8: Testing and documentation",
                "Week 9-10: Deployment and polish"
            ],
            "success_criteria": [
                "Comprehensive README",
                "Working demo",
                "Tests coverage > 70%",
                "Clear documentation"
            ]
        })
        
        # Open source contribution
        goals.append({
            "goal": "Contribute to an open source project",
            "steps": [
                "Find a project aligned with your skills",
                "Start with good first issues",
                "Submit 2-3 meaningful PRs",
                "Engage with the community"
            ]
        })
        
        # Technical depth
        goals.append({
            "goal": "Demonstrate technical depth",
            "actions": [
                "Add tests to existing projects",
                "Implement CI/CD pipeline",
                "Create project documentation site",
                "Add code comments and examples"
            ]
        })
        
        return goals
    
    def _get_priority_focus(self, portfolio_score: Dict) -> str:
        """Determine priority focus area"""
        components = portfolio_score.get("components", {})
        
        # Find lowest scoring component
        lowest_component = min(components.items(), key=lambda x: x[1])
        
        focus_areas = {
            "documentation": "Improving documentation quality",
            "code_quality": "Enhancing code structure and best practices",
            "consistency": "Establishing regular contribution patterns",
            "impact": "Building projects with real-world impact",
            "depth": "Expanding technical skill diversity"
        }
        
        return focus_areas.get(lowest_component[0], "Overall portfolio improvement")
    
    def _estimate_impact(self, portfolio_score: Dict) -> Dict[str, Any]:
        """Estimate potential score improvement"""
        current_score = portfolio_score.get("overall", 0)
        
        if current_score < 50:
            potential = min(current_score + 30, 100)
        elif current_score < 70:
            potential = min(current_score + 20, 100)
        else:
            potential = min(current_score + 10, 100)
        
        return {
            "current_score": current_score,
            "potential_score": potential,
            "improvement": round(potential - current_score, 2),
            "timeframe": "3 months with consistent effort"
        }