import tweepy
import asyncio
import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.classifier import SentimentClassifier
import logging

logger = logging.getLogger(__name__)

class TwitterMonitor:
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        self.classifier = SentimentClassifier()
        
    def extract_hashtags(self, text: str) -> List[str]:
        return re.findall(r'#\w+', text.lower())
    
    def extract_mentions(self, text: str) -> List[str]:
        return re.findall(r'@\w+', text.lower())
    
    def extract_urls(self, text: str) -> List[str]:
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return url_pattern.findall(text)
    
    async def monitor_keywords(self, keywords: List[str], limit: int = 100):
        db = next(get_db())
        
        for keyword in keywords:
            try:
                tweets = tweepy.Cursor(
                    self.api.search_tweets,
                    q=keyword,
                    lang='en',
                    result_type='recent',
                    tweet_mode='extended'
                ).items(limit)
                
                for tweet in tweets:
                    await self.process_tweet(tweet, db)
                    
            except Exception as e:
                logger.error(f"Error monitoring keyword {keyword}: {str(e)}")
        
        db.close()
    
    async def process_tweet(self, tweet, db: Session):
        # Extract tweet data
        tweet_data = {
            'tweet_id': str(tweet.id),
            'user_id': str(tweet.user.id),
            'username': tweet.user.screen_name,
            'content': tweet.full_text,
            'created_at': tweet.created_at,
            'retweet_count': tweet.retweet_count,
            'like_count': tweet.favorite_count,
            'reply_count': tweet.reply_count if hasattr(tweet, 'reply_count') else 0,
            'hashtags': self.extract_hashtags(tweet.full_text),
            'mentions': self.extract_mentions(tweet.full_text),
            'urls': self.extract_urls(tweet.full_text)
        }
        
        # Store in database
        content_id = self.store_tweet(tweet_data, db)
        
        # Analyze sentiment
        analysis_result = self.classifier.classify(tweet.full_text)
        self.store_sentiment_analysis(content_id, analysis_result, db)
        
        # Update user influence
        await self.update_user_influence(tweet.user, db)
        
        return content_id
    
    def store_tweet(self, tweet_data: Dict, db: Session) -> int:
        # Implementation to store tweet in database
        # Return content_id
        pass
    
    def store_sentiment_analysis(self, content_id: int, analysis: Dict, db: Session):
        # Store sentiment analysis results
        pass
    
    async def update_user_influence(self, user, db: Session):
        # Calculate and update user influence score
        influence_score = self.calculate_influence_score(user)
        # Store in user_influence table
        pass
    
    def calculate_influence_score(self, user) -> float:
        # Weight factors for influence calculation
        follower_weight = 0.4
        engagement_weight = 0.3
        activity_weight = 0.2
        account_age_weight = 0.1
        
        # Normalize follower count (log scale)
        follower_score = min(1.0, user.followers_count / 1000000)
        
        # Calculate engagement rate
        total_tweets = max(1, user.statuses_count)
        avg_engagement = (user.favourites_count / total_tweets) * 0.1
        engagement_score = min(1.0, avg_engagement)
        
        # Activity score based on tweet frequency
        account_age_days = (datetime.now() - user.created_at).days
        activity_score = min(1.0, total_tweets / max(1, account_age_days) * 365)
        
        # Account age score
        age_score = min(1.0, account_age_days / (365 * 5))  # 5 years max
        
        influence_score = (
            follower_score * follower_weight +
            engagement_score * engagement_weight +
            activity_score * activity_weight +
            age_score * account_age_weight
        )
        
        return influence_score