"""
Analytics Modules (Modules 1-12)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from database.models import (
    Case, Post, SentimentAnalysis, TrendingTopic, 
    UserSegment, Influencer, Analytics
)
from analytics_modules.sentiment_analysis import SentimentAnalyzer
from analytics_modules.trending_topics import TrendingTopicsDetector
from analytics_modules.network_analysis import NetworkAnalyzer
from analytics_modules.recommendation_system import RecommendationEngine
from analytics_modules.fake_news_detection import FakeNewsDetector
from analytics_modules.user_segmentation import UserSegmenter
from analytics_modules.influencer_detection import InfluencerDetector
from analytics_modules.competitor_analysis import CompetitorAnalyzer
from analytics_modules.popularity_prediction import PopularityPredictor
from datetime import datetime
import json

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

# ============ MODULE 1: SENTIMENT ANALYSIS ============
@analytics_bp.route('/sentiment/analyze', methods=['POST'])
@jwt_required()
def analyze_sentiment():
    """Module 1: Sentiment Analysis"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        analyzer = SentimentAnalyzer()
        results = []
        
        for post in posts:
            if not SentimentAnalysis.query.filter_by(post_id=post.id).first():
                sentiment_result = analyzer.analyze(post.content)
                
                sentiment_record = SentimentAnalysis(
                    post_id=post.id,
                    sentiment=sentiment_result['sentiment'],
                    confidence=sentiment_result['confidence'],
                    emotion=sentiment_result.get('emotion', '')
                )
                db.session.add(sentiment_record)
                results.append(sentiment_result)
        
        db.session.commit()
        
        # Calculate statistics
        sentiments = [r['sentiment'] for r in results]
        stats = {
            'total_analyzed': len(results),
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral')
        }
        
        return jsonify({
            'message': 'Sentiment analysis completed',
            'statistics': stats,
            'results_count': len(results)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@analytics_bp.route('/sentiment/summary/<int:case_id>', methods=['GET'])
@jwt_required()
def get_sentiment_summary(case_id):
    """Get sentiment summary for a case"""
    try:
        user_id = get_jwt_identity()
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        sentiments = db.session.query(
            SentimentAnalysis.sentiment,
            db.func.count(SentimentAnalysis.id).label('count')
        ).join(Post).filter(Post.case_id == case_id).group_by(SentimentAnalysis.sentiment).all()
        
        summary = {sentiment: count for sentiment, count in sentiments}
        
        return jsonify({'summary': summary}), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 2: TRENDING TOPICS ============
@analytics_bp.route('/trends/detect', methods=['POST'])
@jwt_required()
def detect_trends():
    """Module 2: Trending Topics Detection"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        detector = TrendingTopicsDetector()
        topics = detector.extract_hashtags([post.content for post in posts])
        topics_ranked = detector.rank_trends(topics)
        
        # Save trending topics
        for topic, frequency in topics_ranked[:20]:  # Top 20 trends
            trend = TrendingTopic(
                case_id=case_id,
                hashtag=topic,
                frequency=frequency,
                trend_score=frequency / len(posts) if posts else 0
            )
            db.session.add(trend)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Trending topics detected',
            'top_trends': topics_ranked[:10],
            'total_trends': len(topics_ranked)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@analytics_bp.route('/trends/list/<int:case_id>', methods=['GET'])
@jwt_required()
def get_trends(case_id):
    """Get trending topics for a case"""
    try:
        user_id = get_jwt_identity()
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        trends = TrendingTopic.query.filter_by(case_id=case_id).order_by(
            TrendingTopic.frequency.desc()
        ).limit(20).all()
        
        return jsonify({
            'trends': [t.to_dict() for t in trends],
            'total': len(trends)
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 3: NETWORK ANALYSIS ============
@analytics_bp.route('/network/analyze', methods=['POST'])
@jwt_required()
def analyze_network():
    """Module 3: Network Analysis"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        analyzer = NetworkAnalyzer()
        network_data = analyzer.build_network([p.to_dict() for p in posts])
        
        analytics_record = Analytics(
            case_id=case_id,
            module_name='Module 3: Network Analysis',
            metric_name='network_graph',
            metric_data=network_data
        )
        db.session.add(analytics_record)
        db.session.commit()
        
        return jsonify({
            'message': 'Network analysis completed',
            'nodes': len(network_data.get('nodes', [])),
            'edges': len(network_data.get('edges', []))
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 4: RECOMMENDATION SYSTEM ============
@analytics_bp.route('/recommendations/generate', methods=['POST'])
@jwt_required()
def generate_recommendations():
    """Module 4: Recommendation System"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        user_id_external = data.get('user_id')
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        recommender = RecommendationEngine()
        recommendations = recommender.recommend_content(
            user_id_external,
            [p.to_dict() for p in posts]
        )
        
        return jsonify({
            'message': 'Recommendations generated',
            'recommendations': recommendations[:10]
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 5: FAKE NEWS DETECTION ============
@analytics_bp.route('/fake-news/detect', methods=['POST'])
@jwt_required()
def detect_fake_news():
    """Module 5: Fake News Detection"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        detector = FakeNewsDetector()
        results = []
        
        for post in posts:
            prediction = detector.predict([post.content])
            results.append({
                'post_id': post.id,
                'is_fake': prediction['is_fake'],
                'confidence': prediction['confidence']
            })
        
        return jsonify({
            'message': 'Fake news detection completed',
            'results': results,
            'fake_count': sum(1 for r in results if r['is_fake'])
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 6: USER SEGMENTATION ============
@analytics_bp.route('/segmentation/cluster', methods=['POST'])
@jwt_required()
def cluster_users():
    """Module 6: User Segmentation"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        segmenter = UserSegmenter()
        clusters = segmenter.segment_users([p.to_dict() for p in posts])
        
        # Save segments
        for cluster_id, users in clusters.items():
            for user_data in users:
                segment = UserSegment(
                    case_id=case_id,
                    user_id_external=user_data.get('id'),
                    segment=f'cluster_{cluster_id}',
                    demographics=user_data.get('demographics', {}),
                    behavior=user_data.get('behavior', {})
                )
                db.session.add(segment)
        
        db.session.commit()
        
        return jsonify({
            'message': 'User segmentation completed',
            'clusters': len(clusters),
            'users_segmented': sum(len(u) for u in clusters.values())
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 7: DATA VISUALIZATION ============
@analytics_bp.route('/visualization/<int:case_id>', methods=['GET'])
@jwt_required()
def get_visualizations(case_id):
    """Module 7: Data Visualization"""
    try:
        user_id = get_jwt_identity()
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        # Engagement data
        engagement_data = {
            'labels': [f'post_{i}' for i in range(len(posts))],
            'likes': [p.likes for p in posts],
            'shares': [p.shares for p in posts],
            'comments': [p.comments for p in posts]
        }
        
        # Sentiment distribution
        sentiments = db.session.query(
            SentimentAnalysis.sentiment,
            db.func.count(SentimentAnalysis.id)
        ).join(Post).filter(Post.case_id == case_id).group_by(
            SentimentAnalysis.sentiment
        ).all()
        
        sentiment_data = {sentiment: count for sentiment, count in sentiments}
        
        return jsonify({
            'engagement': engagement_data,
            'sentiment': sentiment_data,
            'posts_count': len(posts)
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 8: AD CAMPAIGN OPTIMIZATION ============
@analytics_bp.route('/ads/optimize', methods=['POST'])
@jwt_required()
def optimize_ads():
    """Module 8: Ad Campaign Optimization"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        ad_spend = data.get('ad_spend', 1000)
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        total_engagement = sum(p.likes + p.shares + p.comments for p in posts)
        
        # Calculate metrics
        ctr = (total_engagement / len(posts)) if posts else 0
        conversion_rate = (ctr * 0.05) if ctr > 0 else 0
        roi = ((conversion_rate * ad_spend) / ad_spend) if ad_spend > 0 else 0
        
        return jsonify({
            'message': 'Ad optimization analysis completed',
            'metrics': {
                'ctr': ctr,
                'conversion_rate': conversion_rate,
                'roi': roi,
                'ad_spend': ad_spend,
                'estimated_conversions': conversion_rate * ad_spend
            }
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 9: INFLUENCER DETECTION ============
@analytics_bp.route('/influencers/detect', methods=['POST'])
@jwt_required()
def detect_influencers():
    """Module 9: Influencer Detection"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        detector = InfluencerDetector()
        influencers = detector.detect([p.to_dict() for p in posts])
        
        # Save influencers
        for inf in influencers:
            influencer = Influencer(
                case_id=case_id,
                user_id_external=inf.get('id'),
                username=inf.get('username'),
                followers=inf.get('followers', 0),
                engagement_rate=inf.get('engagement_rate', 0),
                centrality_score=inf.get('centrality_score', 0),
                influence_tier=inf.get('tier')
            )
            db.session.add(influencer)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Influencer detection completed',
            'influencers_found': len(influencers),
            'influencers': influencers[:10]
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@analytics_bp.route('/influencers/list/<int:case_id>', methods=['GET'])
@jwt_required()
def get_influencers(case_id):
    """Get detected influencers for a case"""
    try:
        user_id = get_jwt_identity()
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        influencers = Influencer.query.filter_by(case_id=case_id).order_by(
            Influencer.centrality_score.desc()
        ).limit(20).all()
        
        return jsonify({
            'influencers': [i.to_dict() for i in influencers],
            'total': len(influencers)
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 10: REAL-TIME MONITORING ============
@analytics_bp.route('/monitoring/keywords', methods=['POST'])
@jwt_required()
def monitor_keywords():
    """Module 10: Real-Time Monitoring"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        keywords = data.get('keywords', [])
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        # Filter posts by keywords
        matching_posts = []
        for post in posts:
            if any(kw.lower() in post.content.lower() for kw in keywords):
                matching_posts.append(post.to_dict())
        
        return jsonify({
            'message': 'Keyword monitoring completed',
            'keywords': keywords,
            'matching_posts': len(matching_posts),
            'posts': matching_posts[:20]
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 11: COMPETITOR ANALYSIS ============
@analytics_bp.route('/competitors/analyze', methods=['POST'])
@jwt_required()
def analyze_competitors():
    """Module 11: Competitor Analysis"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        competitor_cases = data.get('competitor_case_ids', [])
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        analyzer = CompetitorAnalyzer()
        comparison = analyzer.compare_cases(case_id, competitor_cases)
        
        return jsonify({
            'message': 'Competitor analysis completed',
            'comparison': comparison
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# ============ MODULE 12: POPULARITY PREDICTION ============
@analytics_bp.route('/prediction/engagement', methods=['POST'])
@jwt_required()
def predict_engagement():
    """Module 12: Popularity Prediction"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        case_id = data.get('case_id')
        
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        predictor = PopularityPredictor()
        predictions = predictor.predict_engagement([p.to_dict() for p in posts])
        
        return jsonify({
            'message': 'Popularity prediction completed',
            'predictions': predictions[:10],
            'avg_predicted_engagement': sum(p['predicted_engagement'] for p in predictions) / len(predictions) if predictions else 0
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
