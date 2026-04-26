#!/usr/bin/env python3
"""
Test Apify API Key Connection
"""
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_apify_connection():
    """Test Apify API connection"""
    api_key = os.getenv('APIFY_API_KEY')

    if not api_key:
        print("❌ No APIFY_API_KEY found in .env file")
        return False

    print(f"🔑 Testing API key: {api_key[:10]}...")

    # Test basic API access
    url = "https://api.apify.com/v2/users/me"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            user_data = response.json()
            print("✅ API key is valid!")
            print(f"👤 User: {user_data.get('data', {}).get('username', 'Unknown')}")
            return True
        else:
            print(f"❌ API key invalid. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Apify API Key Connection...")
    test_apify_connection()