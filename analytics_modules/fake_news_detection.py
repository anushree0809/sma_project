"""
Module 5: Fake News Detection
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class FakeNewsDetector:
    """Fake News Detection using ML"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self._is_trained = False
    
    def _train_model(self):
        """Train model with sample data"""
        if self._is_trained:
            return
        
        # Sample training data (would be replaced with real data)
        sample_texts = [
            "Breaking news: President announces new policy",
            "SHOCKING: Celebrity revealed as alien!",
            "Study shows climate change impact",
            "FAKE: Man jumps to moon with springs",
            "Government report on economy",
            "HOAX: Water turns people invisible",
        ]
        
        # 0 = real, 1 = fake
        labels = np.array([0, 1, 0, 1, 0, 1])
        
        X = self.vectorizer.fit_transform(sample_texts)
        self.model.fit(X, labels)
        self._is_trained = True
    
    def predict(self, texts):
        """Predict if posts are fake news"""
        self._train_model()
        
        try:
            # Check for fake news indicators
            fake_indicators = [
                'fake', 'hoax', 'breaking', 'shocking', 'revealed',
                'unbelievable', 'fake news', 'conspiracy'
            ]
            
            predictions = []
            for text in texts:
                # Rule-based detection
                text_lower = text.lower()
                fake_score = sum(1 for indicator in fake_indicators if indicator in text_lower) / len(fake_indicators)
                
                # ML-based detection
                try:
                    X = self.vectorizer.transform([text])
                    ml_pred = self.model.predict(X)[0]
                    ml_proba = self.model.predict_proba(X)[0][1]
                    fake_score = max(fake_score, ml_proba)
                except:
                    pass
                
                is_fake = fake_score > 0.5
                
                predictions.append({
                    'text': text[:100],
                    'is_fake': bool(is_fake),
                    'confidence': float(fake_score)
                })
            
            return predictions[0] if predictions else {'is_fake': False, 'confidence': 0.0}
        except:
            return {'is_fake': False, 'confidence': 0.0}
