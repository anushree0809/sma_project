# API Endpoints Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication Endpoints

### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string",
  "full_name": "string (optional)"
}

Response: 201
{
  "message": "User registered successfully",
  "user": {
    "id": number,
    "username": "string",
    "email": "string",
    "full_name": "string",
    "created_at": "ISO 8601 datetime"
  }
}
```

### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}

Response: 200
{
  "message": "Login successful",
  "access_token": "JWT_TOKEN",
  "user": {
    "id": number,
    "username": "string",
    "email": "string"
  }
}
```

### Get User Profile
```http
GET /auth/profile
Authorization: Bearer <access_token>

Response: 200
{
  "user": {
    "id": number,
    "username": "string",
    "email": "string",
    "full_name": "string",
    "created_at": "ISO 8601 datetime"
  }
}
```

## Case Management Endpoints

### Get All Cases
```http
GET /cases
Authorization: Bearer <access_token>

Response: 200
{
  "cases": [
    {
      "id": number,
      "name": "string",
      "brand_name": "string",
      "platform": "string",
      "description": "string",
      "goal": "string",
      "created_at": "ISO 8601 datetime"
    }
  ],
  "total": number
}
```

### Create Case
```http
POST /cases
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "string (required)",
  "brand_name": "string",
  "platform": "x | facebook",
  "description": "string",
  "goal": "string"
}

Response: 201
{
  "message": "Case created successfully",
  "case": {
    "id": number,
    "name": "string",
    ...
  }
}
```

### Get Case Details
```http
GET /cases/<case_id>
Authorization: Bearer <access_token>

Response: 200
{
  "case": {
    "id": number,
    "name": "string",
    "brand_name": "string",
    "platform": "string",
    "posts_count": number
  }
}
```

### Update Case
```http
PUT /cases/<case_id>
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "string",
  "description": "string",
  "brand_name": "string",
  "platform": "string",
  "goal": "string"
}

Response: 200
{
  "message": "Case updated successfully",
  "case": {...}
}
```

### Delete Case
```http
DELETE /cases/<case_id>
Authorization: Bearer <access_token>

Response: 200
{
  "message": "Case deleted successfully"
}
```

## Analytics Endpoints

### Module 1: Sentiment Analysis
```http
POST /analytics/sentiment/analyze
{
  "case_id": number
}

Response:
{
  "message": "Sentiment analysis completed",
  "statistics": {
    "total_analyzed": number,
    "positive": number,
    "negative": number,
    "neutral": number
  },
  "results_count": number
}
```

### Module 2: Trending Topics
```http
POST /analytics/trends/detect
{
  "case_id": number
}

Response:
{
  "message": "Trending topics detected",
  "top_trends": [[hashtag, frequency], ...],
  "total_trends": number
}
```

### Module 3: Network Analysis
```http
POST /analytics/network/analyze
{
  "case_id": number
}

Response:
{
  "message": "Network analysis completed",
  "nodes": number,
  "edges": number
}
```

### Module 9: Influencer Detection
```http
POST /analytics/influencers/detect
{
  "case_id": number
}

Response:
{
  "message": "Influencer detection completed",
  "influencers_found": number,
  "influencers": [
    {
      "id": "string",
      "username": "string",
      "followers": number,
      "engagement_rate": number,
      "centrality_score": number,
      "tier": "Mega|Macro|Micro|Nano"
    }
  ]
}
```

## Data Collection Endpoints

### Add Sample Data
```http
POST /data/sample-data
{
  "case_id": number
}

Response: 201
{
  "message": "Sample data added successfully",
  "posts_count": number
}
```

## Health Check

```http
GET /health

Response: 200
{
  "status": "healthy"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "message": "Invalid request"
}
```

### 401 Unauthorized
```json
{
  "message": "Unauthorized"
}
```

### 404 Not Found
```json
{
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "message": "Internal server error"
}
```

## Authentication

All protected endpoints require:
```
Authorization: Bearer <JWT_TOKEN>
```

The JWT token is obtained from the login endpoint and should be stored in the client.
