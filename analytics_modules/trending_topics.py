"""
Module 2: Trending Topics Detection
"""
import re
from collections import Counter

class TrendingTopicsDetector:
    """Detect trending topics and hashtags"""
    
    def extract_hashtags(self, texts):
        """Extract hashtags from texts"""
        hashtags = []
        for text in texts:
            found_hashtags = re.findall(r'#\w+', text)
            hashtags.extend(found_hashtags)
        return hashtags
    
    def extract_mentions(self, texts):
        """Extract mentions from texts"""
        mentions = []
        for text in texts:
            found_mentions = re.findall(r'@\w+', text)
            mentions.extend(found_mentions)
        return mentions
    
    def rank_trends(self, hashtags, top_n=50):
        """Rank hashtags by frequency"""
        if not hashtags:
            return []
        
        # Count frequency
        counter = Counter(hashtags)
        ranked = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        
        return ranked[:top_n]
    
    def get_trending_terms(self, texts, top_n=20):
        """Extract trending terms/keywords"""
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been'
        }
        
        terms = []
        for text in texts:
            words = re.findall(r'\b\w+\b', text.lower())
            terms.extend([w for w in words if w not in stop_words and len(w) > 3])
        
        counter = Counter(terms)
        return sorted(counter.items(), key=lambda x: x[1], reverse=True)[:top_n]
