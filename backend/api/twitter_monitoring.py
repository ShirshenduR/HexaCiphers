from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.twitter_monitor import TwitterMonitor
from backend.models.campaign_detector import CampaignDetector
from backend.models.alert_system import AlertSystem
from backend.models.keyword_manager import KeywordManager
from typing import List, Dict, Optional
import asyncio

router = APIRouter(prefix="/api/twitter", tags=["twitter-monitoring"])

@router.post("/start-monitoring")
async def start_monitoring(
    keywords: List[str],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start Twitter monitoring for specified keywords"""
    monitor = TwitterMonitor(
        api_key=os.getenv('TWITTER_API_KEY'),
        api_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )
    
    background_tasks.add_task(monitor.monitor_keywords, keywords, limit=1000)
    
    return {"message": "Twitter monitoring started", "keywords": keywords}

@router.get("/campaigns")
async def get_detected_campaigns(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get detected campaigns with optional filtering"""
    # Query campaigns from database
    campaigns = []  # Placeholder
    return {"campaigns": campaigns}

@router.get("/alerts")
async def get_alerts(
    status: Optional[str] = "active",
    severity: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get system alerts"""
    # Query alerts from database
    alerts = []  # Placeholder
    return {"alerts": alerts}

@router.post("/keywords")
async def add_keyword(
    keyword: str,
    category: str,
    weight: float = 1.0,
    language: str = "en",
    db: Session = Depends(get_db)
):
    """Add new keyword to monitoring database"""
    keyword_manager = KeywordManager()
    keyword_manager.add_keyword(keyword, category, weight, language, db)
    
    return {"message": "Keyword added successfully"}

@router.get("/influence-rankings")
async def get_influence_rankings(
    risk_level: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get user influence rankings"""
    # Query user influence data
    rankings = []  # Placeholder
    return {"rankings": rankings}

@router.post("/analyze-content")
async def analyze_content(
    content: str,
    db: Session = Depends(get_db)
):
    """Analyze specific content for anti-India sentiment"""
    from backend.models.classifier import SentimentClassifier
    
    classifier = SentimentClassifier()
    result = classifier.classify(content)
    
    return result