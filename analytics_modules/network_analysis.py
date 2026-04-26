"""
Module 3: Network Analysis
"""
import networkx as nx
from collections import defaultdict

class NetworkAnalyzer:
    """Social Network Analysis using NetworkX"""
    
    def build_network(self, posts_data):
        """Build network graph from posts"""
        G = nx.Graph()
        
        # Create nodes and edges from posts
        user_interactions = defaultdict(list)
        
        for post in posts_data:
            author = post.get('author', 'unknown')
            G.add_node(author)
            
            # Add engagement as weight
            engagement = post.get('likes', 0) + post.get('shares', 0) + post.get('comments', 0)
            G.nodes[author]['engagement'] = G.nodes[author].get('engagement', 0) + engagement
        
        # Add edges based on interactions
        nodes_list = list(G.nodes())
        for i in range(len(nodes_list)):
            for j in range(i + 1, len(nodes_list)):
                G.add_edge(nodes_list[i], nodes_list[j], weight=1)
        
        return self._serialize_network(G)
    
    def detect_communities(self, G):
        """Detect communities in network"""
        try:
            communities = list(nx.community.greedy_modularity_communities(G))
            return [list(c) for c in communities]
        except:
            return []
    
    def detect_influencers(self, G):
        """Detect influencers using centrality measures"""
        if len(G) == 0:
            return []
        
        # Eigenvector centrality
        try:
            eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
            sorted_influencers = sorted(eigenvector.items(), key=lambda x: x[1], reverse=True)
            return [{'node': node, 'centrality': score} for node, score in sorted_influencers[:10]]
        except:
            return []
    
    def detect_connectors(self, G):
        """Detect connector nodes (bridges)"""
        if len(G) == 0:
            return []
        
        # Betweenness centrality
        betweenness = nx.betweenness_centrality(G)
        sorted_connectors = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
        return [{'node': node, 'betweenness': score} for node, score in sorted_connectors[:10]]
    
    def _serialize_network(self, G):
        """Serialize network for JSON"""
        nodes = [
            {
                'id': node,
                'engagement': G.nodes[node].get('engagement', 0),
                'label': node
            }
            for node in G.nodes()
        ]
        
        edges = [
            {'source': u, 'target': v, 'weight': G[u][v].get('weight', 1)}
            for u, v in G.edges()
        ]
        
        return {
            'nodes': nodes,
            'edges': edges,
            'metrics': {
                'nodes_count': len(G),
                'edges_count': len(G.edges()),
                'density': nx.density(G)
            }
        }
