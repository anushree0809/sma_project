"""
Application Configuration
"""
import os
from datetime import timedelta

class Config:
    """Base Configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    
    # Apify Configuration
    APIFY_API_KEY = os.getenv('APIFY_API_KEY', 'your-apify-key')
    APIFY_BASE_URL = 'https://api.apify.com/v2'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///sma_app.db'
    )

class DevelopmentConfig(Config):
    """Development Configuration"""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing Configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production Configuration"""
    DEBUG = False
    TESTING = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
