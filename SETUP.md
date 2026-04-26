# Social Media Analytics Application - Setup Guide

## 📋 Installation Steps

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd sma_project
```

### Step 2: Backend Setup

#### Create Virtual Environment
```bash
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Setup Environment Variables
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
# APIFY_API_KEY=your-key-here
```

#### Initialize Database
```bash
python run.py
```

#### Start Backend Server
```bash
python run.py
```
Backend runs on: http://localhost:5000

### Step 3: Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Start Frontend Server
```bash
npm start
```
Frontend runs on: http://localhost:3000

## 🔑 Getting API Keys

### Apify API Key
1. Go to https://apify.com
2. Sign up for free account
3. Navigate to Account Settings → API tokens
4. Copy your API key
5. Add to `.env` file

## 🧪 Testing

### Test Backend
```bash
# Check health
curl http://localhost:5000/api/health

# Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### Test Frontend
1. Open http://localhost:3000
2. Register/Login with test account
3. Create a case
4. Add sample data
5. Run analytics

## 📊 Using the Application

### Create a Case
1. Login to dashboard
2. Click "New Case"
3. Fill in case details:
   - Case Name: "Tesla Analysis"
   - Brand Name: "Tesla"
   - Platform: X (Twitter)
   - Description: Your analysis description
   - Goal: "Sentiment + Trends"
4. Click Create

### Add Data
1. Select case from list
2. Click "Add Sample Data" button
3. System adds 10 sample posts

### Run Analytics
1. Click on analytics module buttons
2. Click "Analyze" button
3. View results and metrics

### Export Reports
1. Generate analytics first
2. Click "Export" button
3. Choose PDF or HTML format

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -i :5000
kill -9 <PID>
```

### Database Errors
```bash
# Reset database
rm sma_app.db
python run.py
```

### CORS Errors
Check frontend URL in CORS_ORIGINS in config/config.py

### Module Not Found Errors
```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

## 📚 Documentation

- API Docs: See README.md
- Database Schema: database/models.py
- Module Details: analytics_modules/

## 🚀 Deployment

### Heroku
```bash
heroku create app-name
git push heroku main
```

### AWS
```bash
# Use EC2 instance with RDS database
# Deploy using Elastic Beanstalk
```

### Docker
```bash
docker build -t sma-app .
docker run -p 5000:5000 sma-app
```

## 📞 Support

For issues and questions:
- Check README.md
- Review error logs
- Check GitHub issues
