"""
Unit Tests for Social Media Analytics Application
"""
import unittest
from backend.app import create_app
from database import db
from database.models import User, Case
import json

class TestAuthentication(unittest.TestCase):
    """Test authentication endpoints"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_register_user(self):
        """Test user registration"""
        response = self.client.post('/api/auth/register',
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123',
                'full_name': 'Test User'
            }
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('access_token', data or {})
    
    def test_login_user(self):
        """Test user login"""
        # Register first
        self.client.post('/api/auth/register',
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123'
            }
        )
        
        # Try login
        response = self.client.post('/api/auth/login',
            json={
                'username': 'testuser',
                'password': 'password123'
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
    
    def test_invalid_login(self):
        """Test invalid login"""
        response = self.client.post('/api/auth/login',
            json={
                'username': 'nonexistent',
                'password': 'password'
            }
        )
        self.assertEqual(response.status_code, 401)

class TestCases(unittest.TestCase):
    """Test case management"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create test user
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            self.user_id = user.id
        
        # Login to get token
        response = self.client.post('/api/auth/login',
            json={'username': 'testuser', 'password': 'password123'}
        )
        self.token = json.loads(response.data)['access_token']
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_case(self):
        """Test case creation"""
        response = self.client.post('/api/cases',
            json={
                'name': 'Tesla Analysis',
                'brand_name': 'Tesla',
                'platform': 'x',
                'description': 'Brand sentiment'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('case', data)
    
    def test_get_cases(self):
        """Test getting cases"""
        # Create a case first
        self.client.post('/api/cases',
            json={
                'name': 'Test Case',
                'platform': 'x'
            },
            headers={'Authorization': f'Bearer {self.token}'}
        )
        
        response = self.client.get('/api/cases',
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('cases', data)
        self.assertEqual(len(data['cases']), 1)

class TestHealthCheck(unittest.TestCase):
    """Test health check endpoint"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()
