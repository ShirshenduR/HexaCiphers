#!/bin/bash
# HexaCiphers Production Setup Script

set -e

echo "🚀 HexaCiphers Production Setup Starting..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found!"
    echo -e "${YELLOW}📝 Please create a .env file with your configuration."
    echo -e "${BLUE}💡 You can copy from .env.example or follow PRODUCTION_SETUP.md"
    exit 1
fi

# Function to check if a service is running
check_service() {
    if docker-compose ps | grep -q "$1.*Up"; then
        echo -e "${GREEN}✅ $1 is running"
        return 0
    else
        echo -e "${RED}❌ $1 is not running"
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    echo -e "${BLUE}⏳ Waiting for $1 to be ready..."
    local retries=30
    while [ $retries -gt 0 ]; do
        if [ "$1" = "postgres" ]; then
            if docker-compose exec postgres pg_isready -U hexaciphers_user >/dev/null 2>&1; then
                echo -e "${GREEN}✅ PostgreSQL is ready"
                return 0
            fi
        elif [ "$1" = "redis" ]; then
            if docker-compose exec redis redis-cli ping >/dev/null 2>&1; then
                echo -e "${GREEN}✅ Redis is ready"
                return 0
            fi
        elif [ "$1" = "backend" ]; then
            if curl -s http://localhost:5000/api/health >/dev/null 2>&1; then
                echo -e "${GREEN}✅ Backend API is ready"
                return 0
            fi
        fi
        
        retries=$((retries - 1))
        sleep 2
    done
    
    echo -e "${RED}❌ $1 failed to start within timeout"
    return 1
}

echo -e "${BLUE}🔧 Step 1: Building and starting services..."
docker-compose down -v 2>/dev/null || true
docker-compose up --build -d

echo -e "${BLUE}🔧 Step 2: Waiting for services to be ready..."
sleep 5

if ! wait_for_service "postgres"; then
    echo -e "${RED}❌ PostgreSQL failed to start. Check logs: docker-compose logs postgres"
    exit 1
fi

if ! wait_for_service "redis"; then
    echo -e "${RED}❌ Redis failed to start. Check logs: docker-compose logs redis"
    exit 1
fi

if ! wait_for_service "backend"; then
    echo -e "${RED}❌ Backend failed to start. Check logs: docker-compose logs backend"
    exit 1
fi

echo -e "${BLUE}🔧 Step 3: Initializing database..."
docker-compose exec backend python -c "
from backend.app import create_app
from backend.db.models import db, User
from datetime import datetime
import os

try:
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print('📊 Database tables created successfully')
        
        # Create a sample admin user if none exists
        if User.query.count() == 0:
            admin_user = User(
                user_id='admin_001',
                username='admin',
                followers=1000,
                is_bot=False
            )
            db.session.add(admin_user)
            db.session.commit()
            print('👤 Sample admin user created')
        
        print('✅ Database initialization completed')
except Exception as e:
    print(f'❌ Database initialization failed: {e}')
    exit(1)
"

echo -e "${BLUE}🔧 Step 4: Testing API endpoints..."

# Test health endpoint
if curl -s http://localhost:5000/api/health | grep -q "healthy"; then
    echo -e "${GREEN}✅ Health endpoint working"
else
    echo -e "${RED}❌ Health endpoint failed"
fi

# Test stats endpoint
if curl -s http://localhost:5000/api/stats | grep -q "success"; then
    echo -e "${GREEN}✅ Stats endpoint working"
else
    echo -e "${RED}❌ Stats endpoint failed"
fi

# Test Twitter API if keys are provided
TWITTER_KEY=$(grep TWITTER_API_KEY .env | cut -d'=' -f2)
if [ "$TWITTER_KEY" != "your-twitter-api-key" ] && [ "$TWITTER_KEY" != "your-twitter-api-key-here" ] && [ -n "$TWITTER_KEY" ]; then
    echo -e "${BLUE}🐦 Testing Twitter API integration..."
    if curl -s -X POST "http://localhost:5000/api/collect/twitter" \
        -H "Content-Type: application/json" \
        -d '{"keywords": ["test"], "limit": 1}' | grep -q "status"; then
        echo -e "${GREEN}✅ Twitter API integration working"
    else
        echo -e "${YELLOW}⚠️  Twitter API test inconclusive (check your API keys)"
    fi
else
    echo -e "${YELLOW}⚠️  Twitter API keys not configured - using fallback data"
fi

echo -e "${BLUE}🔧 Step 5: Starting frontend..."
if ! docker-compose ps | grep -q frontend; then
    # If frontend service doesn't exist in docker-compose, start it manually
    echo -e "${BLUE}📱 Starting frontend manually..."
    cd frontend && npm install >/dev/null 2>&1 && npm start >/dev/null 2>&1 &
    FRONTEND_PID=$!
    cd ..
    sleep 10
    
    if curl -s http://localhost:3001 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend is running on http://localhost:3001"
    else
        echo -e "${YELLOW}⚠️  Frontend may take a moment to start"
    fi
fi

echo -e "${BLUE}🔧 Step 6: Final system check..."

# Check all services
echo -e "${BLUE}📊 Service Status:"
check_service "postgres" && echo -e "${GREEN}  PostgreSQL: Running"
check_service "redis" && echo -e "${GREEN}  Redis: Running"  
check_service "backend" && echo -e "${GREEN}  Backend: Running"

if check_service "celery"; then
    echo -e "${GREEN}  Celery: Running"
else
    echo -e "${YELLOW}  Celery: Not configured (optional)"
fi

# Display access URLs
echo -e "\n${GREEN}🎉 HexaCiphers Production Setup Complete!"
echo -e "\n${BLUE}📱 Access URLs:"
echo -e "   Frontend Dashboard: ${GREEN}http://localhost:3001${NC}"
echo -e "   Backend API:        ${GREEN}http://localhost:5000/api${NC}"
echo -e "   API Health Check:   ${GREEN}http://localhost:5000/api/health${NC}"

echo -e "\n${BLUE}🔧 Quick API Tests:"
echo -e "   Health:   ${YELLOW}curl http://localhost:5000/api/health${NC}"
echo -e "   Stats:    ${YELLOW}curl http://localhost:5000/api/stats${NC}"
echo -e "   Twitter:  ${YELLOW}curl -X POST http://localhost:5000/api/collect/twitter -H 'Content-Type: application/json' -d '{\"keywords\":[\"india\"],\"limit\":5}'${NC}"

echo -e "\n${BLUE}📊 View Logs:"
echo -e "   All logs: ${YELLOW}docker-compose logs${NC}"
echo -e "   Backend:  ${YELLOW}docker-compose logs backend${NC}"
echo -e "   Database: ${YELLOW}docker-compose logs postgres${NC}"

echo -e "\n${BLUE}🛑 Stop Services:"
echo -e "   ${YELLOW}docker-compose down${NC}"

# Check for API keys warning
if grep -q "your-twitter-api-key" .env 2>/dev/null; then
    echo -e "\n${YELLOW}⚠️  WARNING: Please update your Twitter API keys in .env file for real data collection${NC}"
fi

echo -e "\n${GREEN}✨ Setup completed successfully! HexaCiphers is ready for production use.${NC}"
