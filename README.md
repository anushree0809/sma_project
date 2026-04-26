# Social Media Analytics Application

## 📊 Overview
A comprehensive full-stack application for analyzing social media data from X (Twitter) and Facebook using AI/ML algorithms and advanced analytics.

## 🎯 Features

### Core Modules (12 Analytics Features)
1. **Sentiment Analysis** - Analyze positive/negative/neutral sentiment
2. **Trending Topics Detection** - Extract and rank trending hashtags
3. **Network Analysis** - Build and analyze social networks
4. **Recommendation System** - Suggest content using collaborative/content filtering
5. **Fake News Detection** - Classify posts as fake/real
6. **User Segmentation** - Cluster users by demographics and behavior
7. **Data Visualization** - Interactive charts and dashboards
8. **Ad Campaign Optimization** - Calculate CTR, conversion rate, ROI
9. **Influencer Detection** - Identify influencers using eigenvector centrality
10. **Real-Time Monitoring** - Track keywords in real-time
11. **Competitor Analysis** - Compare metrics across cases
12. **Popularity Prediction** - ML-based engagement prediction

### Key Features
✅ User Authentication (JWT)  
✅ Case Management  
✅ Multi-platform Support (X, Facebook)  
✅ Apify API Integration  
✅ Real-time Analytics Dashboard  
✅ PDF/HTML Report Generation  
✅ NLP & ML Models  
✅ Network Graphs  
✅ Data Export  

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask / FastAPI
- **Database**: SQLAlchemy + SQLite/MySQL
- **Authentication**: JWT
- **APIs**: Apify, Requests

### Frontend
- **Framework**: React 18
- **Styling**: CSS3 + Bootstrap
- **Charts**: Chart.js
- **State Management**: React Hooks

### ML/NLP Libraries
- **NLP**: NLTK, TextBlob
- **ML**: Scikit-learn
- **Network Analysis**: NetworkX
- **Data Processing**: Pandas, NumPy

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

### Backend Setup

```bash
# Clone repository
git clone <repo-url>
cd sma_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python run.py

# Run Flask server
python run.py
```

The backend will start at `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will start at `http://localhost:3000`

## 🚀 Quick Start

### 1. Start Backend
```bash
cd sma_project
python run.py
```

### 2. Start Frontend (in new terminal)
```bash
cd sma_project/frontend
npm start
```

### 3. Access Application
Open browser and go to `http://localhost:3000`

### 4. Create Account
- Register or Login
- Create a new Case
- Add sample data
- Run analytics modules

## 📝 API Documentation

### Authentication
```bash
# Register
POST /api/auth/register
{
  "username": "user",
  "email": "user@example.com",
  "password": "password",
  "full_name": "User Name"
}

# Login
POST /api/auth/login
{
  "username": "user",
  "password": "password"
}
```

### Cases
```bash
# Get all cases
GET /api/cases
Headers: Authorization: Bearer <token>

# Create case
POST /api/cases
{
  "name": "Tesla Analysis",
  "brand_name": "Tesla",
  "platform": "x",
  "description": "Brand sentiment analysis",
  "goal": "Sentiment + Trends"
}

# Get case details
GET /api/cases/<case_id>

# Delete case
DELETE /api/cases/<case_id>
```

### Analytics
```bash
# Run sentiment analysis
POST /api/analytics/sentiment/analyze
{ "case_id": 1 }

# Get trends
POST /api/analytics/trends/detect
{ "case_id": 1 }

# Analyze network
POST /api/analytics/network/analyze
{ "case_id": 1 }

# Detect influencers
POST /api/analytics/influencers/detect
{ "case_id": 1 }
```

## 📊 Dashboard Features

### Multi-Tab Interface
- **Dashboard**: Overview and KPIs
- **Sentiment**: Sentiment distribution
- **Trends**: Top hashtags and topics
- **Network**: User interaction graph
- **Influencers**: Top influencers list
- **Analytics**: Custom analysis views

### Data Visualization
- Bar charts
- Pie charts
- Line graphs
- Network graphs
- Heat maps

### Export Options
- PDF Reports
- HTML Reports
- CSV Data Export
- JSON Export

## 🔌 API Integration

### Apify Configuration
1. Get API key from [apify.com](https://apify.com)
2. Set environment variable:
   ```bash
   export APIFY_API_KEY="your-api-key"
   ```

### Sample Data
To test without API:
```bash
# Add 10 sample posts to a case
POST /api/data/sample-data
{ "case_id": 1 }
```

## 📁 Project Structure

```
sma_project/
├── backend/
│   ├── app.py              # Main Flask app
│   ├── auth.py             # Authentication routes
│   ├── cases.py            # Case management
│   ├── data_collection.py  # Data collection (Apify)
│   └── analytics.py        # Analytics endpoints
├── database/
│   ├── models.py           # Database models
│   └── __init__.py
├── analytics_modules/
│   ├── sentiment_analysis.py
│   ├── trending_topics.py
│   ├── network_analysis.py
│   ├── recommendation_system.py
│   ├── fake_news_detection.py
│   ├── user_segmentation.py
│   ├── influencer_detection.py
│   ├── competitor_analysis.py
│   └── popularity_prediction.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   └── Dashboard/
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   └── package.json
├── utils/
│   └── report_generator.py
├── reports/           # Generated reports
├── config/
│   └── config.py
├── requirements.txt
└── run.py
```

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Test authentication
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'

# Test health check
curl http://localhost:5000/api/health
```

## 📊 Database Models

### User
- id, username, email, password_hash, full_name, timestamps

### Case
- id, user_id, name, brand_name, platform, description, goal, timestamps

### Post
- id, case_id, post_id, platform, content, author, engagement metrics, timestamps

### SentimentAnalysis
- id, post_id, sentiment, confidence, emotion, timestamps

### TrendingTopic
- id, case_id, hashtag, frequency, trend_score

### Influencer
- id, case_id, username, followers, engagement_rate, centrality_score, influence_tier

### Analytics
- id, case_id, module_name, metric_name, metric_value, metric_data

## 🔐 Security

- JWT authentication for all protected endpoints
- Password hashing with werkzeug
- CORS enabled for cross-origin requests
- SQL injection prevention with SQLAlchemy ORM
- Input validation on all endpoints

## 📈 Deployment

### Heroku
```bash
heroku create sma-app
git push heroku main
```

### Docker
```bash
docker build -t sma-app .
docker run -p 5000:5000 sma-app
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 📞 Support

For support, email support@example.com or create an issue on GitHub.

## 🙏 Acknowledgments

- Apify for data collection API
- Flask, React, and open-source community
- All contributors and testers
