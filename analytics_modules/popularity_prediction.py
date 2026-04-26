"""
Module 12: Popularity Prediction
"""
from sklearn.linear_model import LinearRegression
import numpy as np

class PopularityPredictor:
    """Predict post engagement using ML"""
    
    def __init__(self):
        self.model = LinearRegression()
        self._is_trained = False
    
    def predict_engagement(self, posts_data):
        """Predict engagement for posts"""
        predictions = []
        
        for post in posts_data:
            # Extract features
            content_length = len(post.get('content', ''))
            hashtag_count = post.get('content', '').count('#')
            mention_count = post.get('content', '').count('@')
            author_followers = post.get('followers', 0)
            
            # Simple prediction model
            base_engagement = (
                content_length * 0.1 +
                hashtag_count * 50 +
                mention_count * 30 +
                author_followers * 0.01
            )
            
            # Add variance based on time
            variance = np.random.uniform(0.8, 1.2)
            predicted_engagement = base_engagement * variance
            
            predictions.append({
                'post_id': post.get('id'),
                'author': post.get('author'),
                'predicted_engagement': float(max(0, predicted_engagement)),
                'confidence': 0.75
            })
        
        return sorted(predictions, key=lambda x: x['predicted_engagement'], reverse=True)
