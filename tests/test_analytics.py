"""
Analytics Modules Unit Tests
"""
import unittest
from analytics_modules.sentiment_analysis import SentimentAnalyzer
from analytics_modules.trending_topics import TrendingTopicsDetector
from analytics_modules.influencer_detection import InfluencerDetector

class TestSentimentAnalysis(unittest.TestCase):
    """Test sentiment analysis module"""
    
    def setUp(self):
        self.analyzer = SentimentAnalyzer()
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection"""
        result = self.analyzer.analyze("I love this product! It's amazing!")
        self.assertEqual(result['sentiment'], 'positive')
        self.assertGreater(result['confidence'], 0)
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection"""
        result = self.analyzer.analyze("This is terrible and I hate it!")
        self.assertEqual(result['sentiment'], 'negative')
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment detection"""
        result = self.analyzer.analyze("The weather is cloudy today")
        self.assertEqual(result['sentiment'], 'neutral')

class TestTrendingTopics(unittest.TestCase):
    """Test trending topics detection"""
    
    def setUp(self):
        self.detector = TrendingTopicsDetector()
    
    def test_extract_hashtags(self):
        """Test hashtag extraction"""
        texts = [
            "Check out #Tesla #Electric vehicles",
            "I love #Tesla products",
            "#Tesla is amazing"
        ]
        hashtags = self.detector.extract_hashtags(texts)
        self.assertIn('#Tesla', hashtags)
        self.assertEqual(hashtags.count('#Tesla'), 3)
    
    def test_rank_trends(self):
        """Test trend ranking"""
        hashtags = ['#tesla', '#tesla', '#electric', '#ev', '#ev', '#ev']
        ranked = self.detector.rank_trends(hashtags)
        self.assertEqual(ranked[0][0], '#ev')
        self.assertEqual(ranked[0][1], 3)

class TestInfluencerDetection(unittest.TestCase):
    """Test influencer detection"""
    
    def setUp(self):
        self.detector = InfluencerDetector()
    
    def test_detect_influencers(self):
        """Test influencer detection"""
        posts = [
            {
                'id': '1',
                'author': 'user1',
                'followers': 100000,
                'likes': 1000,
                'shares': 500,
                'comments': 200
            },
            {
                'id': '2',
                'author': 'user2',
                'followers': 5000,
                'likes': 10,
                'shares': 5,
                'comments': 2
            }
        ]
        
        influencers = self.detector.detect(posts)
        self.assertGreater(len(influencers), 0)
        self.assertEqual(influencers[0]['username'], 'user1')

if __name__ == '__main__':
    unittest.main()
