"""
Pytest configuration file
"""
import pytest
from backend.app import create_app
from database import db

@pytest.fixture
def app():
    """Create and configure test app"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client fixture"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI runner fixture"""
    return app.test_cli_runner()
