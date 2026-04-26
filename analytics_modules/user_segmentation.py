"""
Module 6: User Segmentation
"""
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

class UserSegmenter:
    """User Segmentation using K-Means"""
    
    def __init__(self, n_clusters=3):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    
    def segment_users(self, posts_data):
        """Segment users based on behavior and demographics"""
        if not posts_data:
            return {}
        
        # Extract features
        users = {}
        for post in posts_data:
            author = post.get('author', 'unknown')
            if author not in users:
                users[author] = {
                    'posts': 0,
                    'total_engagement': 0,
                    'avg_likes': 0,
                    'followers': post.get('followers', 0)
                }
            
            users[author]['posts'] += 1
            engagement = post.get('likes', 0) + post.get('shares', 0) + post.get('comments', 0)
            users[author]['total_engagement'] += engagement
            users[author]['avg_likes'] = users[author]['total_engagement'] / users[author]['posts']
        
        if len(users) < self.n_clusters:
            self.kmeans = KMeans(n_clusters=len(users), random_state=42)
        
        # Create feature matrix
        user_list = list(users.items())
        X = np.array([
            [
                user_data['posts'],
                user_data['total_engagement'],
                user_data['followers']
            ]
            for _, user_data in user_list
        ])
        
        # Normalize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Cluster
        clusters_pred = self.kmeans.fit_predict(X_scaled)
        
        # Group users by cluster
        clusters = {}
        for idx, (username, user_data) in enumerate(user_list):
            cluster_id = int(clusters_pred[idx])
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            
            clusters[cluster_id].append({
                'id': username,
                'username': username,
                'demographics': {'followers': user_data['followers']},
                'behavior': {
                    'posts': user_data['posts'],
                    'engagement': user_data['total_engagement']
                }
            })
        
        return clusters
