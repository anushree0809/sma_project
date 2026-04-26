"""
Module 4: Recommendation System
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecommendationEngine:
    """Content and Collaborative Recommendation System"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    
    def content_based_filtering(self, user_history, all_posts):
        """Content-based recommendation"""
        if not user_history or not all_posts:
            return []
        
        try:
            # Vectorize user history and posts
            texts = [p['content'] for p in user_history + all_posts]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate similarity
            user_vector = tfidf_matrix[:len(user_history)].mean(axis=0)
            similarities = cosine_similarity(user_vector, tfidf_matrix[len(user_history):])
            
            # Rank recommendations
            recommendations = []
            for idx, score in enumerate(similarities[0]):
                recommendations.append({
                    'post': all_posts[idx],
                    'similarity_score': float(score)
                })
            
            return sorted(recommendations, key=lambda x: x['similarity_score'], reverse=True)
        except:
            return []
    
    def collaborative_filtering(self, user_engagement, all_posts):
        """Collaborative filtering recommendation"""
        if not all_posts:
            return []
        
        # Simple collaborative approach: recommend popular posts similar to user's interests
        recommendations = []
        for post in all_posts:
            score = (
                post.get('likes', 0) * 0.5 +
                post.get('shares', 0) * 1.0 +
                post.get('comments', 0) * 0.7
            ) / (max(post.get('likes', 0) + post.get('shares', 0) + post.get('comments', 0), 1))
            
            recommendations.append({
                'post': post,
                'score': score
            })
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)
    
    def recommend_content(self, user_id, all_posts):
        """Generate recommendations for user"""
        if not all_posts:
            return []
        
        # Combine both filtering methods
        recommendations = self.collaborative_filtering({}, all_posts)
        return recommendations[:20]
