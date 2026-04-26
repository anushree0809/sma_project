"""
Module 9: Influencer Detection
"""
import networkx as nx
import numpy as np

class InfluencerDetector:
    """Detect Influencers using Eigenvector Centrality"""
    
    def detect(self, posts_data):
        """Detect influencers from posts"""
        if not posts_data:
            return []
        
        # Build user graph
        G = nx.DiGraph()
        user_stats = {}
        
        for post in posts_data:
            author = post.get('author', 'unknown')
            
            if author not in G:
                G.add_node(author)
                user_stats[author] = {
                    'followers': post.get('followers', 0),
                    'engagement': 0,
                    'posts': 0
                }
            
            engagement = post.get('likes', 0) + post.get('shares', 0) + post.get('comments', 0)
            user_stats[author]['engagement'] += engagement
            user_stats[author]['posts'] += 1
        
        # Calculate centrality
        influencers = []
        try:
            centrality = nx.eigenvector_centrality(G, max_iter=1000) if len(G) > 0 else {}
        except:
            centrality = {node: 1.0 / len(G) for node in G.nodes()} if len(G) > 0 else {}
        
        for author, stats in user_stats.items():
            centrality_score = centrality.get(author, 0.0)
            engagement_rate = (
                stats['engagement'] / max(stats['posts'], 1)
                if stats['posts'] > 0 else 0
            )
            
            # Determine influence tier
            if stats['followers'] > 1000000:
                tier = 'Mega'
            elif stats['followers'] > 100000:
                tier = 'Macro'
            elif stats['followers'] > 10000:
                tier = 'Micro'
            else:
                tier = 'Nano'
            
            influencers.append({
                'id': author,
                'username': author,
                'followers': stats['followers'],
                'engagement_rate': float(engagement_rate),
                'centrality_score': float(centrality_score),
                'tier': tier,
                'posts': stats['posts']
            })
        
        # Sort by centrality score
        return sorted(influencers, key=lambda x: x['centrality_score'], reverse=True)
