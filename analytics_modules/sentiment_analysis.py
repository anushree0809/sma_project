"""
Module 1: Sentiment Analysis
"""
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

class SentimentAnalyzer:
    """Sentiment Analysis using NLP"""
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
    
    def analyze(self, text):
        """Analyze sentiment of text"""
        try:
            # VADER analysis
            scores = self.sia.polarity_scores(text)
            compound = scores['compound']
            
            # Determine sentiment
            if compound >= 0.05:
                sentiment = 'positive'
            elif compound <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # TextBlob analysis for emotion detection
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            emotion = self._detect_emotion(text)
            
            return {
                'sentiment': sentiment,
                'confidence': abs(compound),
                'polarity': polarity,
                'emotion': emotion,
                'scores': scores
            }
        except Exception as e:
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'emotion': 'unknown',
                'error': str(e)
            }
    
    def _detect_emotion(self, text):
        """Detect emotion from text"""
        emotions = {
            'joy': ['happy', 'love', 'amazing', 'great', 'wonderful'],
            'anger': ['angry', 'hate', 'angry', 'furious', 'mad'],
            'sadness': ['sad', 'depressed', 'down', 'upset'],
            'surprise': ['wow', 'amazing', 'shocked'],
            'fear': ['afraid', 'scared', 'worried', 'anxious']
        }
        
        text_lower = text.lower()
        for emotion, keywords in emotions.items():
            if any(kw in text_lower for kw in keywords):
                return emotion
        
        return 'neutral'
