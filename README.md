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

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/ShirshenduR/HexaCiphers.git
cd HexaCiphers

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
# Database: localhost:5432
```

### Option 2: Manual Setup

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

## 🔧 Features

### 🔍 Data Collection
- **Social Media APIs:** Twitter, Reddit, YouTube integration (simulated)
- **Real-time Monitoring:** Continuous data ingestion
- **Multi-platform Support:** Cross-platform campaign tracking

### 🧠 AI & Machine Learning
- **Sentiment Analysis:** BERT-based multilingual classification
- **Content Classification:** Pro-India / Anti-India / Neutral detection
- **Language Support:** English, Hindi, Bengali, Tamil, Telugu
- **Bot Detection:** Network analysis and behavioral patterns

### 📊 Campaign Detection
- **Coordinated Activity:** Time-based clustering analysis
- **Hashtag Monitoring:** Trending and suspicious hashtag tracking
- **Network Analysis:** User interaction graphs and community detection
- **Risk Scoring:** Multi-factor risk assessment algorithms

### 🖥️ Dashboard
- **Real-time Monitoring:** Live updates and alerts
- **Interactive Visualizations:** Charts, graphs, heatmaps
- **Campaign Timeline:** Historical trend analysis
- **Export Capabilities:** Reports and data export

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

### Production Deployment

```bash
# Build and deploy with Docker
docker-compose -f docker-compose.prod.yml up -d

# Or deploy to cloud platforms
# Instructions for AWS, GCP, Azure available in docs/
```

### Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost/hexaciphers_db
POSTGRES_DB=hexaciphers_db
POSTGRES_USER=username
POSTGRES_PASSWORD=password

# API Keys (Optional)
TWITTER_BEARER_TOKEN=your-token
REDDIT_CLIENT_ID=your-id
GOOGLE_TRANSLATE_API_KEY=your-key

# ML Configuration
HUGGINGFACE_CACHE_DIR=./models/cache
MODEL_NAME=bert-base-multilingual-cased
```

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
