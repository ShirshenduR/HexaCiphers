# 🚀 HexaCiphers Production Deployment Guide

## 📋 Overview

HexaCiphers is a production-ready Twitter monitoring system for detecting anti-India sentiment campaigns. This guide will help you deploy the complete system using Docker.

## 🏗️ Architecture

- **Backend**: Flask API with PostgreSQL database
- **Frontend**: React.js dashboard  
- **Background Tasks**: Celery with Redis
- **Data Source**: Twitter API v2 (Real-time)
- **Deployment**: Docker Compose

## 📋 Prerequisites

- Docker & Docker Compose
- Twitter Developer Account with API keys
- 4GB+ RAM for optimal performance
- Port 3000 (frontend) and 5000 (backend) available

## 🔑 Required API Keys

### Twitter API Setup
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Create a new App with "Essential" access minimum
3. Generate the following credentials:
   - API Key
   - API Secret  
   - Access Token
   - Access Token Secret
   - Bearer Token

## ⚙️ Environment Configuration

Update your `.env` file with production values:

```env
# Database Configuration - Production
DATABASE_URL=postgresql://hexaciphers_user:secure_password_123@postgres:5432/hexaciphers_db
POSTGRES_DB=hexaciphers_db
POSTGRES_USER=hexaciphers_user
POSTGRES_PASSWORD=secure_password_123

# Flask Configuration - Production
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=CHANGE-THIS-TO-A-SECURE-RANDOM-STRING

# Twitter API Keys - Add your real keys here
TWITTER_API_KEY=your-real-twitter-api-key
TWITTER_API_SECRET=your-real-twitter-api-secret
TWITTER_ACCESS_TOKEN=your-real-access-token
TWITTER_ACCESS_SECRET=your-real-access-token-secret
TWITTER_BEARER_TOKEN=your-real-bearer-token

# Redis Configuration
REDIS_URL=redis://redis:6379/0
```

## 🚀 Deployment Steps

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd HexaCiphers
```

### 2. Configure Environment

```bash
# Edit the .env file with your real API keys
nano .env
```

**Important**: Replace ALL placeholder values with your real credentials!

### 3. Deploy with Docker

```bash
# Build and start all services  
docker-compose up --build -d

# Check all services are running
docker-compose ps

# View logs (optional)
docker-compose logs -f backend
```

### 4. Verify Deployment

```bash
# Test backend health
curl http://localhost:5000/api/health

# Test database connection  
curl http://localhost:5000/api/stats

# Access frontend
open http://localhost:3000
```

```bash
# Test API health
curl http://localhost:5000/api/health

# Test Twitter integration
curl -X POST "http://localhost:5000/api/collect/twitter" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["india"], "limit": 5}'

# Test dashboard
curl http://localhost:3001
```

## 🔍 Service URLs

- **Frontend Dashboard**: http://localhost:3001
- **Backend API**: http://localhost:5000/api
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## 📊 Production Features

### ✅ Enabled Features
- Real Twitter API v2 integration
- PostgreSQL database with proper schema
- Redis caching for performance
- Celery background task processing
- Production-grade Gunicorn WSGI server
- Comprehensive error handling
- Database migrations support
- Health check endpoints

### 🔧 API Endpoints

#### Core APIs
```bash
# Health check
GET /api/health

# Real-time stats from database
GET /api/stats

# Collect real Twitter data
POST /api/collect/twitter
{
  "keywords": ["india", "campaign"],
  "limit": 100
}

# AI-powered content classification
POST /api/classify
{
  "text": "Content to analyze for sentiment and India-relation"
}

# Analyze Twitter URLs
POST /api/analyze-url
{
  "url": "https://twitter.com/user/status/123456789"
}
```

## 🛡️ Security Considerations

### Production Security Checklist
- [ ] Change default passwords in `.env`
- [ ] Use HTTPS in production (add SSL certificates)
- [ ] Configure firewall rules
- [ ] Restrict database access
- [ ] Use strong SECRET_KEY
- [ ] Enable API rate limiting
- [ ] Regular security updates

### Recommended Security Settings

```env
# Use strong passwords
POSTGRES_PASSWORD=ComplexPassword123!@#
SECRET_KEY=very-long-random-string-at-least-32-characters

# Production settings
FLASK_ENV=production
FLASK_DEBUG=False
```

## 📈 Monitoring & Maintenance

### Health Monitoring

```bash
# Check all services
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs postgres
docker-compose logs redis

# Resource usage
docker stats
```

### Database Operations

```bash
# Create backup
docker-compose exec postgres pg_dump -U hexaciphers_user hexaciphers_db > backup_$(date +%Y%m%d).sql

# Restore backup
docker-compose exec -T postgres psql -U hexaciphers_user hexaciphers_db < backup.sql

# Database migration
docker-compose exec backend flask db migrate -m "Migration description"
docker-compose exec backend flask db upgrade
```

### Performance Tuning

```bash
# Scale Celery workers
docker-compose up --scale celery=3 -d

# Monitor Redis memory usage
docker-compose exec redis redis-cli info memory

# Check PostgreSQL connections
docker-compose exec postgres psql -U hexaciphers_user -c "SELECT count(*) FROM pg_stat_activity;"
```

## 🚨 Troubleshooting

### Common Issues

#### Twitter API Not Working
```bash
# Check API keys
docker-compose exec backend python -c "
import os
print('Twitter API Key:', os.getenv('TWITTER_API_KEY', 'NOT SET'))
print('Bearer Token:', os.getenv('TWITTER_BEARER_TOKEN', 'NOT SET'))
"

# Test API connection
docker-compose exec backend python -c "
import tweepy
import os
client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))
print('Twitter API connection:', 'OK' if client else 'FAILED')
"
```

#### Database Connection Issues
```bash
# Check database
docker-compose exec postgres psql -U hexaciphers_user -d hexaciphers_db -c "SELECT version();"

# Reset database
docker-compose down -v
docker-compose up postgres -d
# Wait for postgres to start, then:
docker-compose up backend -d
```

#### Frontend Not Loading
```bash
# Check backend connectivity
curl http://localhost:5000/api/health

# Check frontend proxy
cd frontend && cat package.json | grep proxy

# Restart frontend
docker-compose restart frontend
```

## 🔄 Updates & Maintenance

### Update Process
```bash
# Pull latest changes
git pull origin main

# Rebuild containers
docker-compose down
docker-compose up --build -d

# Apply database migrations if any
docker-compose exec backend flask db upgrade
```

### Backup Strategy
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U hexaciphers_user hexaciphers_db > "backups/hexaciphers_$DATE.sql"
find backups/ -name "*.sql" -mtime +7 -delete  # Keep 7 days
```

## 🎯 Production Checklist

Before going live:

- [ ] All API keys configured correctly
- [ ] Database credentials changed from defaults
- [ ] Strong SECRET_KEY set
- [ ] Twitter API working with real data
- [ ] All services healthy (docker-compose ps)
- [ ] Frontend accessible and functional
- [ ] Backend API responding correctly
- [ ] Database storing data properly
- [ ] SSL certificates configured (if using HTTPS)
- [ ] Firewall rules configured
- [ ] Backup strategy implemented
- [ ] Monitoring set up

## 📞 Support

If you encounter issues:

1. Check the logs: `docker-compose logs [service-name]`
2. Verify environment variables: `docker-compose config`
3. Test individual components using the troubleshooting commands above
4. Create an issue with error details and logs

## 🎉 Success!

Once deployed successfully, you'll have:
- Real-time Twitter monitoring with your API keys
- Production PostgreSQL database storing all data
- Interactive React dashboard showing live statistics
- ML-powered content classification and sentiment analysis
- Campaign detection algorithms identifying coordinated attacks
- Scalable architecture ready for high-volume data processing
