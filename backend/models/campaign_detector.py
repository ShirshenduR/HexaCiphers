from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import numpy as np
from sqlalchemy.orm import Session
from backend.database import get_db
import logging

logger = logging.getLogger(__name__)

class CampaignDetector:
    def __init__(self):
        self.min_participants = 10
        self.time_window_hours = 24
        self.hashtag_threshold = 0.7  # Similarity threshold for hashtag clustering
        
    async def detect_coordinated_campaigns(self, db: Session) -> List[Dict]:
        campaigns = []
        
        # Get recent content within time window
        since_time = datetime.now() - timedelta(hours=self.time_window_hours)
        
        # Detect hashtag-based campaigns
        hashtag_campaigns = await self.detect_hashtag_campaigns(db, since_time)
        campaigns.extend(hashtag_campaigns)
        
        # Detect timing-based coordination
        timing_campaigns = await self.detect_timing_coordination(db, since_time)
        campaigns.extend(timing_campaigns)
        
        # Detect similar content campaigns
        content_campaigns = await self.detect_similar_content_campaigns(db, since_time)
        campaigns.extend(content_campaigns)
        
        return campaigns
    
    async def detect_hashtag_campaigns(self, db: Session, since_time: datetime) -> List[Dict]:
        # Query for hashtag usage patterns
        # Group by hashtags and count unique users
        hashtag_usage = defaultdict(set)
        
        # Mock query - replace with actual database query
        recent_posts = []  # Query recent posts from database
        
        for post in recent_posts:
            for hashtag in post.hashtags:
                hashtag_usage[hashtag].add(post.user_id)
        
        campaigns = []
        for hashtag, users in hashtag_usage.items():
            if len(users) >= self.min_participants:
                # Calculate campaign metrics
                total_engagement = 0  # Sum engagement for all posts with this hashtag
                severity = self.calculate_campaign_severity(len(users), total_engagement)
                
                campaigns.append({
                    'type': 'hashtag_campaign',
                    'hashtag': hashtag,
                    'participants': list(users),
                    'participant_count': len(users),
                    'total_engagement': total_engagement,
                    'severity': severity,
                    'detected_at': datetime.now()
                })
        
        return campaigns
    
    async def detect_timing_coordination(self, db: Session, since_time: datetime) -> List[Dict]:
        # Detect posts published in suspicious time patterns
        campaigns = []
        
        # Group posts by 15-minute time slots
        time_slots = defaultdict(list)
        
        # Mock query - replace with actual database query
        recent_posts = []  # Query recent posts
        
        for post in recent_posts:
            time_slot = post.created_at.replace(minute=(post.created_at.minute // 15) * 15, second=0, microsecond=0)
            time_slots[time_slot].append(post)
        
        for time_slot, posts in time_slots.items():
            unique_users = set(post.user_id for post in posts)
            if len(unique_users) >= self.min_participants:
                # Check if posts have similar anti-India sentiment
                anti_india_posts = [p for p in posts if self.is_anti_india_content(p)]
                
                if len(anti_india_posts) >= self.min_participants * 0.7:
                    campaigns.append({
                        'type': 'timing_coordination',
                        'time_slot': time_slot,
                        'participants': list(unique_users),
                        'participant_count': len(unique_users),
                        'posts': len(posts),
                        'anti_india_posts': len(anti_india_posts),
                        'severity': self.calculate_campaign_severity(len(unique_users), sum(p.total_engagement for p in posts)),
                        'detected_at': datetime.now()
                    })
        
        return campaigns
    
    async def detect_similar_content_campaigns(self, db: Session, since_time: datetime) -> List[Dict]:
        # Detect campaigns based on similar content patterns
        campaigns = []
        
        # Implementation for content similarity detection
        # This would involve NLP techniques to find similar posts
        
        return campaigns
    
    def is_anti_india_content(self, post) -> bool:
        # Check if content is classified as anti-India
        # This would query the sentiment_analysis table
        return False  # Placeholder
    
    def calculate_campaign_severity(self, participant_count: int, total_engagement: int) -> str:
        # Calculate severity based on reach and engagement
        base_score = participant_count * 0.1 + total_engagement * 0.001
        
        if base_score > 100:
            return 'critical'
        elif base_score > 50:
            return 'high'
        elif base_score > 20:
            return 'medium'
        else:
            return 'low'
    
    async def store_detected_campaign(self, campaign: Dict, db: Session):
        # Store detected campaign in database
        pass