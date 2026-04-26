"""
Database Models for Social Media Analytics Application
"""
from datetime import datetime
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """User Model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cases = db.relationship('Case', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'created_at': self.created_at.isoformat()
        }

class Case(db.Model):
    """Case/Project Model"""
    __tablename__ = 'cases'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    brand_name = db.Column(db.String(120))
    platform = db.Column(db.String(50), nullable=False)  # X, Facebook, Instagram
    goal = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    posts = db.relationship('Post', backref='case', lazy=True, cascade='all, delete-orphan')
    analytics = db.relationship('Analytics', backref='case', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand_name': self.brand_name,
            'platform': self.platform,
            'description': self.description,
            'goal': self.goal,
            'created_at': self.created_at.isoformat()
        }

class Post(db.Model):
    """Social Media Post Model"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    post_id = db.Column(db.String(255), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(120))
    likes = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    followers = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posted_at = db.Column(db.DateTime)
    raw_data = db.Column(db.JSON)
    
    # Relationships
    sentiment_analysis = db.relationship('SentimentAnalysis', backref='post', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'platform': self.platform,
            'content': self.content,
            'author': self.author,
            'likes': self.likes,
            'shares': self.shares,
            'comments': self.comments,
            'created_at': self.created_at.isoformat()
        }

class SentimentAnalysis(db.Model):
    """Sentiment Analysis Results"""
    __tablename__ = 'sentiment_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)  # positive, negative, neutral
    confidence = db.Column(db.Float, default=0.0)
    emotion = db.Column(db.String(50))
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'sentiment': self.sentiment,
            'confidence': self.confidence,
            'emotion': self.emotion
        }

class TrendingTopic(db.Model):
    """Trending Topics"""
    __tablename__ = 'trending_topics'
    
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    hashtag = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.Integer, default=1)
    trend_score = db.Column(db.Float, default=0.0)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'hashtag': self.hashtag,
            'frequency': self.frequency,
            'trend_score': self.trend_score
        }

class UserSegment(db.Model):
    """User Segmentation Data"""
    __tablename__ = 'user_segments'
    
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    user_id_external = db.Column(db.String(255))
    segment = db.Column(db.String(100))  # segment cluster
    demographics = db.Column(db.JSON)
    behavior = db.Column(db.JSON)
    engagement_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id_external,
            'segment': self.segment,
            'engagement_score': self.engagement_score
        }

class Influencer(db.Model):
    """Influencer Detection"""
    __tablename__ = 'influencers'
    
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    user_id_external = db.Column(db.String(255))
    username = db.Column(db.String(255))
    followers = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0.0)
    centrality_score = db.Column(db.Float, default=0.0)  # Eigenvector centrality
    influence_tier = db.Column(db.String(50))  # Mega, Macro, Micro, Nano
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'followers': self.followers,
            'engagement_rate': self.engagement_rate,
            'influence_tier': self.influence_tier
        }

class Analytics(db.Model):
    """General Analytics Storage"""
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    module_name = db.Column(db.String(100), nullable=False)  # module 1-12
    metric_name = db.Column(db.String(255), nullable=False)
    metric_value = db.Column(db.Float)
    metric_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'module_name': self.module_name,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value
        }

class Report(db.Model):
    """Generated Reports"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    report_name = db.Column(db.String(255), nullable=False)
    report_type = db.Column(db.String(20))  # PDF, HTML
    file_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'report_name': self.report_name,
            'report_type': self.report_type,
            'created_at': self.created_at.isoformat()
        }
