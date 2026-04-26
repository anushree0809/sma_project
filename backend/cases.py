"""
Case Management Routes
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from database.models import User, Case, Post
from datetime import datetime

case_bp = Blueprint('cases', __name__, url_prefix='/api/cases')

@case_bp.route('', methods=['GET'])
@jwt_required()
def get_cases():
    """Get all cases for the current user"""
    try:
        user_id = get_jwt_identity()
        cases = Case.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'cases': [case.to_dict() for case in cases],
            'total': len(cases)
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@case_bp.route('/<int:case_id>', methods=['GET'])
@jwt_required()
def get_case(case_id):
    """Get a specific case"""
    try:
        user_id = get_jwt_identity()
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        case_dict = case.to_dict()
        case_dict['posts_count'] = len(case.posts)
        
        return jsonify({
            'case': case_dict
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@case_bp.route('', methods=['POST'])
@jwt_required()
def create_case():
    """Create a new case"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('platform'):
            return jsonify({'message': 'Missing required fields (name, platform)'}), 400
        
        case = Case(
            user_id=user_id,
            name=data['name'],
            description=data.get('description', ''),
            brand_name=data.get('brand_name', ''),
            platform=data['platform'],
            goal=data.get('goal', '')
        )
        
        db.session.add(case)
        db.session.commit()
        
        return jsonify({
            'message': 'Case created successfully',
            'case': case.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@case_bp.route('/<int:case_id>', methods=['PUT'])
@jwt_required()
def update_case(case_id):
    """Update a case"""
    try:
        user_id = get_jwt_identity()
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        data = request.get_json()
        
        if 'name' in data:
            case.name = data['name']
        if 'description' in data:
            case.description = data['description']
        if 'brand_name' in data:
            case.brand_name = data['brand_name']
        if 'platform' in data:
            case.platform = data['platform']
        if 'goal' in data:
            case.goal = data['goal']
        
        case.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Case updated successfully',
            'case': case.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@case_bp.route('/<int:case_id>', methods=['DELETE'])
@jwt_required()
def delete_case(case_id):
    """Delete a case"""
    try:
        user_id = get_jwt_identity()
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        db.session.delete(case)
        db.session.commit()
        
        return jsonify({'message': 'Case deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@case_bp.route('/<int:case_id>/posts', methods=['GET'])
@jwt_required()
def get_case_posts(case_id):
    """Get posts for a case"""
    try:
        user_id = get_jwt_identity()
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        return jsonify({
            'posts': [post.to_dict() for post in posts],
            'total': len(posts)
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@case_bp.route('/<int:case_id>/summary', methods=['GET'])
@jwt_required()
def get_case_summary(case_id):
    """Get case analytics summary"""
    try:
        user_id = get_jwt_identity()
        case = Case.query.filter_by(id=case_id, user_id=user_id).first()
        
        if not case:
            return jsonify({'message': 'Case not found'}), 404
        
        posts = Post.query.filter_by(case_id=case_id).all()
        
        # Calculate summary stats
        total_posts = len(posts)
        total_engagement = sum(p.likes + p.shares + p.comments for p in posts)
        avg_engagement = total_engagement / total_posts if total_posts > 0 else 0
        
        return jsonify({
            'case': case.to_dict(),
            'summary': {
                'total_posts': total_posts,
                'total_engagement': total_engagement,
                'avg_engagement': avg_engagement
            }
        }), 200
    
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
