"""
Main Flask Application
"""
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config.config import config_by_name
from database import db
import os

def create_app(config_name='development'):
    """Application Factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    
    # Register blueprints
    from backend.auth import auth_bp
    from backend.cases import case_bp
    from backend.data_collection import data_bp
    from backend.analytics import analytics_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(case_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(analytics_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'message': 'Internal server error'}), 500
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'message': 'Unauthorized'}), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'message': 'Forbidden'}), 403
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'}), 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    app.run(debug=True, host='0.0.0.0', port=5000)
