"""
Module 8: Ad Campaign Optimization & 11: Competitor Analysis
"""

class CompetitorAnalyzer:
    """Competitor Analysis"""
    
    def compare_cases(self, case_id, competitor_case_ids):
        """Compare case with competitors"""
        from database.models import Post, Case
        from database import db
        
        main_case = Case.query.get(case_id)
        if not main_case:
            return {}
        
        main_posts = Post.query.filter_by(case_id=case_id).all()
        
        comparison = {
            'case': main_case.to_dict(),
            'metrics': {}
        }
        
        # Calculate main case metrics
        main_engagement = sum(p.likes + p.shares + p.comments for p in main_posts)
        comparison['metrics']['engagement'] = main_engagement
        comparison['metrics']['posts'] = len(main_posts)
        comparison['metrics']['avg_engagement'] = main_engagement / len(main_posts) if main_posts else 0
        
        # Compare with competitors
        for comp_id in competitor_case_ids:
            comp_case = Case.query.get(comp_id)
            if comp_case:
                comp_posts = Post.query.filter_by(case_id=comp_id).all()
                comp_engagement = sum(p.likes + p.shares + p.comments for p in comp_posts)
                
                comparison[f'competitor_{comp_id}'] = {
                    'name': comp_case.name,
                    'engagement': comp_engagement,
                    'posts': len(comp_posts),
                    'avg_engagement': comp_engagement / len(comp_posts) if comp_posts else 0
                }
        
        return comparison
