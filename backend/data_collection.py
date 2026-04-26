"""
Apify API Data Collection Module
"""
import requests
import json
from config.config import Config
from database import db
from database.models import Post
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

data_bp = Blueprint('data', __name__, url_prefix='/api/data')

class ApifyClient:
    """Apify API Client"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or Config.APIFY_API_KEY
        self.base_url = Config.APIFY_BASE_URL
        self.headers = {'Content-Type': 'application/json'}
    
    def run_actor(self, actor_id, input_data):
        """Run an Apify actor"""
        try:
            url = f"{self.base_url}/acts/{actor_id}/runs"
            params = {'token': self.api_key}
            
            response = requests.post(
                url,
                json=input_data,
                params=params,
                headers=self.headers
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                return {'error': response.text}
        except Exception as e:
            return {'error': str(e)}
    
    def get_dataset(self, dataset_id):
        """Get dataset from Apify"""
        try:
            url = f"{self.base_url}/datasets/{dataset_id}/items"
            params = {'token': self.api_key}
            
            response = requests.get(url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': response.text}
        except Exception as e:
            return {'error': str(e)}
    
    def collect_twitter_data(self, keywords, max_items=100):
        """Collect Twitter/X data"""
        actor_input = {
            "searches": keywords,
            "maxItems": max_items,
            "maxRequestRetries": 3,
            "startUrls": []
        }
        return self.run_actor('heLL_oSkq47sYasVP', actor_input)
    
    def collect_facebook_data(self, page_urls, max_items=100):
        """Collect Facebook data"""
        actor_input = {
            "startUrls": [{"url": url} for url in page_urls],
            "maxItems": max_items,
            "maxRequestRetries": 3
        }
        return self.run_actor('17LB3f0rXdCzD3c3p', actor_input)

@data_bp.route('/collect', methods=['POST'])
@jwt_required()
def collect_data():
    """Collect data from social media"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        case_id = data.get('case_id')
        platform = data.get('platform')
        keywords = data.get('keywords', [])
        urls = data.get('urls', [])
        
        if not case_id or not platform:
            return jsonify({'message': 'Missing case_id or platform'}), 400
        
        # Verify case ownership
        from database.models import Case
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        # Initialize Apify client
        client = ApifyClient()
        result = None
        
        if platform.lower() == 'x':
            result = client.collect_twitter_data(keywords, data.get('max_items', 100))
        elif platform.lower() == 'facebook':
            result = client.collect_facebook_data(urls, data.get('max_items', 100))
        
        if 'error' in result:
            return jsonify({'message': f'Collection error: {result["error"]}'}), 500
        
        return jsonify({
            'message': 'Data collection started',
            'result': result
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@data_bp.route('/posts', methods=['POST'])
@jwt_required()
def add_posts():
    """Add collected posts to case"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        case_id = data.get('case_id')
        posts_data = data.get('posts', [])
        
        if not case_id or not posts_data:
            return jsonify({'message': 'Missing case_id or posts'}), 400
        
        # Verify case ownership
        from database.models import Case
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        # Add posts to database
        added_posts = []
        for post_data in posts_data:
            post = Post(
                case_id=case_id,
                post_id=post_data.get('id', ''),
                platform=case.platform,
                content=post_data.get('content', post_data.get('text', '')),
                author=post_data.get('author', post_data.get('username', '')),
                likes=post_data.get('likes', 0),
                shares=post_data.get('shares', post_data.get('retweets', 0)),
                comments=post_data.get('comments', 0),
                followers=post_data.get('followers', 0),
                posted_at=datetime.utcnow(),
                raw_data=post_data
            )
            db.session.add(post)
            added_posts.append(post)
        
        db.session.commit()
        
        return jsonify({
            'message': f'{len(added_posts)} posts added successfully',
            'posts_count': len(added_posts)
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@data_bp.route('/sample-data', methods=['POST'])
@jwt_required()
def add_sample_data():
    """Add sample data for testing"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        case_id = data.get('case_id')
        
        if not case_id:
            return jsonify({'message': 'Missing case_id'}), 400
        
        # Verify case ownership
        from database.models import Case
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        # Sample posts for demo
        sample_posts = [
            {
                'id': f'post_{i}',
                'content': f'Amazing product! Love using Tesla Model S. #Tesla #Electric',
                'author': f'user_{i}',
                'likes': 100 + i * 10,
                'shares': 20 + i,
                'comments': 30 + i * 2,
                'followers': 1000 + i * 100
            } for i in range(10)
        ]
        
        added_posts = []
        for post_data in sample_posts:
            post = Post(
                case_id=case_id,
                post_id=post_data['id'],
                platform=case.platform,
                content=post_data['content'],
                author=post_data['author'],
                likes=post_data['likes'],
                shares=post_data['shares'],
                comments=post_data['comments'],
                followers=post_data['followers'],
                posted_at=datetime.utcnow(),
                raw_data=post_data
            )
            db.session.add(post)
            added_posts.append(post)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Sample data added successfully',
            'posts_count': len(added_posts)
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500
