#!/usr/bin/env python
"""
Social Media Analytics Application - Main Entry Point
"""
import os
import sys
from backend.app import create_app
from database import db
from config.config import config_by_name

# Get configuration
config_name = os.getenv('FLASK_ENV', 'development')
print(f"\n{'='*60}")
print(f"Starting Social Media Analytics Application")
print(f"Environment: {config_name}")
print(f"{'='*60}\n")

# Create app
app = create_app(config_name)

# CLI Commands
@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database initialized!")

@app.cli.command()
def create_admin():
    """Create an admin user."""
    from database.models import User
    
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    
    if User.query.filter_by(username=username).first():
        print("Username already exists!")
        return
    
    user = User(username=username, email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    print(f"Admin user '{username}' created successfully!")

if __name__ == '__main__':
    print("API Documentation:")
    print(f"  Base URL: http://localhost:5000")
    print(f"  Health Check: GET /api/health")
    print(f"  Authentication: POST /api/auth/login")
    print(f"  Cases: GET/POST /api/cases")
    print(f"  Analytics: POST /api/analytics/[module]")
    print()
    app.run(debug=True, host='0.0.0.0', port=5000)
