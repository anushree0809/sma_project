#!/bin/bash
# Social Media Analytics Application - Setup Script

echo "=================================="
echo "Social Media Analytics Setup"
echo "=================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check Node.js
if ! command -v npm &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 14+"
    exit 1
fi

echo "✅ Python and Node.js found"
echo ""

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Setup frontend
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create .env file
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "⚠️ Update .env with your Apify API key"
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start backend (Terminal 1):"
echo "   source venv/bin/activate"
echo "   python run.py"
echo ""
echo "2. Start frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "Then open http://localhost:3000"
echo ""
