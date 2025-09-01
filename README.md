# 🚩 HexaCiphers - Detecting Anti-India Campaign on Digital Platforms

A comprehensive AI-driven system for detecting and analyzing anti-India campaigns on digital platforms through real-time monitoring of text, images, videos, and network behavior.

## 📌 Problem Statement

With the rapid growth of social media and digital platforms, malicious actors are leveraging these spaces to spread misinformation, propaganda, and anti-national sentiments. The challenge is to **build an AI-driven system that can detect and analyze Anti-India campaigns on digital platforms** by monitoring text, images, videos, and network behavior in real-time.

## 🎯 Objectives

* Detect and classify **anti-India content** from social media (Twitter, YouTube, Reddit, etc.)
* Identify **coordinated campaigns** (bots, fake accounts, foreign influence)
* Track **sentiment trends, hashtags, and misinformation networks**
* Generate **real-time alerts** with supporting evidence

## 🏗️ Project Structure

```
├── backend/
│   ├── api/              # Flask REST API routes
│   ├── models/           # HuggingFace ML models
│   ├── preprocessing/    # Text, OCR, audio processing
│   ├── detection/        # Campaign & bot detection
│   └── db/              # Database models & schema
├── frontend/            # React + Tailwind dashboard
├── notebooks/           # Jupyter notebooks for ML experiments
├── docker-compose.yml   # Container orchestration
├── requirements.txt     # Python dependencies
└── README.md
```

## 🚀 Quick Start (Docker - Easy Setup)

### Prerequisites
- Docker and Docker Compose installed on your system
- 4GB+ RAM available for containers

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/ShirshenduR/HexaCiphers.git
cd HexaCiphers

# 2. Set up environment variables (optional - has defaults)
cp .env.example .env
# Edit .env if you want to add Twitter API keys for real data

# 3. Build and start all services (this may take 5-10 minutes first time)
docker-compose up -d

# 4. Wait for all services to be ready (check with)
docker-compose ps

# 5. Access the application
# 🌐 Frontend Dashboard: http://localhost:3000
# 🔧 Backend API: http://localhost:5000
# 📊 Database: localhost:5432 (postgres/password)
```

### Quick Commands

```bash
# Stop all services
docker-compose down

# View logs (useful for debugging)
docker-compose logs -f

# Restart specific service
docker-compose restart [backend|frontend|postgres|nginx]

# Clean rebuild (if you face issues)
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Manual Setup (Advanced Users)

#### Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and API keys

# Run the backend
python backend/app.py
```

#### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

#### Database Setup

```bash
# Install PostgreSQL
# Create database: hexaciphers_db
# Update DATABASE_URL in .env file

# Initialize database (optional - auto-created)
python -c "from backend.app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask with SQLAlchemy ORM
- **Database:** PostgreSQL + Redis for caching
- **ML/NLP:** HuggingFace Transformers, BERT, IndicBERT
- **Graph Analysis:** NetworkX for bot detection
- **Image Processing:** Tesseract OCR, PIL
- **Audio Processing:** Whisper API (stub implementation)

### Frontend
- **Framework:** React 18 with functional components
- **Styling:** Tailwind CSS
- **Charts:** Recharts, D3.js
- **Icons:** Lucide React
- **Routing:** React Router

### Infrastructure
- **Containerization:** Docker, Docker Compose
- **Task Queue:** Celery with Redis
- **Reverse Proxy:** Nginx
- **Environment:** Development, Production configs

## 🔧 Current Features (Working Now)

### ✅ **Dashboard & UI**
- **React Dashboard:** Modern, responsive interface with dark/light themes
- **Real-time Stats:** System statistics and metrics display
- **Navigation:** Multi-page application with routing
- **Error Handling:** Comprehensive error boundaries and user feedback

### ✅ **Backend API**
- **Flask REST API:** Complete backend with database integration
- **URL Analysis:** Extract and analyze content from web URLs
- **Twitter Integration:** Fetch and analyze real Twitter posts (requires API key)
- **Database Operations:** PostgreSQL with proper schema and relationships
- **CORS Support:** Frontend-backend communication enabled

### ✅ **Text Processing**
- **Sentiment Analysis:** BERT-based multilingual sentiment classification
- **Language Detection:** Automatic language identification
- **Text Cleaning:** Preprocessing and normalization
- **Translation Ready:** Framework for multi-language support

### ✅ **Infrastructure**
- **Docker Setup:** Complete containerized deployment
- **Database:** PostgreSQL with automated schema creation
- **Nginx Proxy:** Production-ready reverse proxy configuration
- **Environment Config:** Flexible configuration management

### ✅ **Monitoring & Analytics**
- **Recent Alerts:** Display system alerts and notifications
- **Campaign Detection:** Basic framework for identifying coordinated activities
- **Data Visualization:** Charts and graphs for sentiment trends

---

## 🚧 Features To Be Implemented

### 🔄 **Enhanced AI & ML**
- **Advanced Bot Detection:** Network analysis and behavioral pattern recognition
- **Coordinated Campaign Detection:** Time-based clustering and network analysis
- **Multi-platform Integration:** Reddit, YouTube, Telegram APIs
- **Image/Video Analysis:** OCR and multimedia content processing
- **Audio Processing:** Speech-to-text and audio sentiment analysis

### 🔄 **Advanced Analytics**
- **Network Graph Visualization:** Interactive network maps of user connections
- **Hashtag Trend Analysis:** Real-time hashtag monitoring and clustering
- **Geographic Analysis:** Location-based campaign tracking
- **Influencer Detection:** Key account identification and analysis
- **Misinformation Tracking:** Fact-checking and source verification

### � **Real-time Features**
- **Live Data Streaming:** WebSocket-based real-time updates
- **Automated Alerts:** Email/SMS notifications for critical campaigns
- **API Rate Limiting:** Advanced rate limiting and quota management
- **Caching Layer:** Redis-based caching for improved performance

### 🔄 **Security & Compliance**
- **User Authentication:** Role-based access control
- **Data Privacy:** GDPR compliance and data anonymization
- **API Security:** JWT tokens and API key management
- **Audit Logging:** Complete activity tracking and logging

### 🔄 **Deployment & Scaling**
- **Cloud Deployment:** AWS/GCP/Azure deployment scripts
- **Kubernetes Support:** Container orchestration for scaling
- **Load Balancing:** Multi-instance deployment
- **Monitoring:** Prometheus/Grafana integration

## 🔬 Machine Learning Notebooks

Explore the ML experiments and training processes:

1. **Sentiment Analysis Training** (`notebooks/sentiment_analysis_training.ipynb`)
   - BERT fine-tuning for Indian context
   - Multilingual classification
   - Model evaluation and metrics

2. **Campaign Detection Analysis** (`notebooks/campaign_detection_analysis.ipynb`)
   - Network graph analysis
   - Bot detection algorithms
   - Coordinated behavior patterns

## 🗃️ Database Schema

### Posts Table
```sql
- id (Primary Key)
- platform (Twitter/Reddit/etc.)
- user_id (Foreign Key)
- content (Text)
- language (Language code)
- translated_text (Translated content)
- sentiment (positive/neutral/negative)
- classification (Pro-India/Neutral/Anti-India)
- created_at (Timestamp)
```

### Users Table
```sql
- id (Primary Key)
- user_id (Unique identifier)
- username (Display name)
- followers (Follower count)
- is_bot (Boolean flag)
- created_at (Timestamp)
```

### Campaigns Table
```sql
- id (Primary Key)
- hashtag (Campaign hashtag)
- volume (Post count)
- first_detected (Start timestamp)
- last_detected (End timestamp)
- risk_score (0.0 - 1.0)
```

## 🔑 API Endpoints

### Data Collection
- `POST /api/collect/twitter` - Collect Twitter data
- `POST /api/collect/reddit` - Collect Reddit data

### Text Processing
- `POST /api/process/text` - Process and clean text
- `POST /api/classify` - Classify content sentiment

### Campaign Management
- `GET /api/campaigns` - Get detected campaigns
- `POST /api/campaigns/detect` - Run campaign detection

### Analytics
- `GET /api/stats` - Get system statistics
- `GET /api/posts` - Get posts with filters
- `GET /api/users` - Get user information

## 📋 Testing the Application

### Quick Test Steps

1. **Access Dashboard:** Open http://localhost:3000
2. **Test URL Analysis:** 
   - Navigate to "URL Analysis" page
   - Enter any news article URL
   - Click "Analyze" to see sentiment analysis
3. **View Dashboard:** Check the main dashboard for system stats
4. **API Testing:** Visit http://localhost:5000/api/stats for backend health

### API Endpoints (Currently Working)

```bash
# System Statistics
GET http://localhost:5000/api/stats

# URL Analysis
POST http://localhost:5000/api/analyze-url
Body: {"url": "https://example.com/article"}

# Dashboard Data
GET http://localhost:5000/api/dashboard

# Text Classification
POST http://localhost:5000/api/classify
Body: {"text": "Sample text to analyze"}
```

## 🧪 Testing

```bash
# Test basic setup
python test_setup.py

# Run backend tests (when available)
python -m pytest backend/tests/

# Run frontend tests
cd frontend && npm test
```

## 🚀 Deployment

### Production Deployment with Docker

```bash
# Clone and setup
git clone https://github.com/ShirshenduR/HexaCiphers.git
cd HexaCiphers

# Production deployment
docker-compose up -d

# Monitor deployment
docker-compose logs -f

# Scale services (if needed)
docker-compose up -d --scale backend=2
```

### Troubleshooting

```bash
# If containers fail to start
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d

# Check service health
docker-compose ps
docker-compose logs [service-name]

# Database issues
docker-compose exec postgres psql -U postgres -d hexaciphers_db

# Frontend build issues
docker-compose exec frontend npm install
docker-compose restart frontend
```

### Cloud Deployment (Future)

- **AWS ECS/Fargate:** Container deployment
- **Google Cloud Run:** Serverless containers  
- **Azure Container Instances:** Managed containers
- **DigitalOcean App Platform:** Simple deployment

### Environment Variables

```bash
# Required for Twitter Integration (Optional)
TWITTER_BEARER_TOKEN=your-twitter-api-bearer-token

# Database Configuration (Has defaults)
DATABASE_URL=postgresql://postgres:password@postgres:5432/hexaciphers_db
POSTGRES_DB=hexaciphers_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# Application Settings
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Optional API Keys
REDDIT_CLIENT_ID=your-reddit-client-id
GOOGLE_TRANSLATE_API_KEY=your-google-translate-key
```

### Docker Services Overview

The application runs 4 main services:

1. **Frontend (React)** - Port 3000
   - User interface and dashboard
   - Built with React and Tailwind CSS

2. **Backend (Flask)** - Port 5000
   - REST API and data processing
   - ML models and sentiment analysis

3. **Database (PostgreSQL)** - Port 5432
   - Data storage and persistence
   - Automated schema creation

4. **Nginx (Reverse Proxy)** - Port 80
   - Production-ready web server
   - Static file serving and routing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- HuggingFace for pre-trained models
- React and Tailwind CSS communities
- NetworkX for graph analysis capabilities
- All contributors and supporters of this project

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation in `/docs`

---

**⚠️ Disclaimer:** This project is for research and educational purposes. Use responsibly and in accordance with platform terms of service and applicable laws.
