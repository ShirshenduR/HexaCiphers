import os
import tweepy
import logging
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DataCollector:
    """Class for collecting data from social media platforms"""
    
    def __init__(self):
        self.twitter_api = self._initialize_twitter_api()
    
    def _initialize_twitter_api(self):
        """Initialize Twitter API client"""
        try:
            # Twitter API v2 client
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_SECRET')
            
            if not bearer_token:
                logger.warning("Twitter Bearer Token not found. Twitter API will not work.")
                return None
            
            # Initialize Twitter API v2 client
            client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                wait_on_rate_limit=True
            )
            
            logger.info("Twitter API client initialized successfully")
            return client
            
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API: {str(e)}")
            return None
    
    def collect_twitter_data(self, keywords: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """Collect tweets based on keywords using Twitter API v2"""
        try:
            if not self.twitter_api:
                logger.warning("Twitter API not available, returning empty data")
                return self._get_fallback_twitter_data(keywords, limit)
            
            # Construct search query
            query = " OR ".join([f'"{keyword}"' for keyword in keywords])
            query += " -is:retweet lang:en"  # Exclude retweets, English only
            
            # Search tweets using API v2
            tweets = tweepy.Paginator(
                self.twitter_api.search_recent_tweets,
                query=query,
                tweet_fields=['created_at', 'author_id', 'public_metrics', 'lang'],
                user_fields=['username', 'public_metrics'],
                expansions=['author_id'],
                max_results=min(limit, 100)  # API limit
            ).flatten(limit=limit)
            
            # Process tweets
            collected_tweets = []
            users_data = {}
            
            # Get users data if available
            if hasattr(tweets, 'includes') and 'users' in tweets.includes:
                for user in tweets.includes['users']:
                    users_data[user.id] = user
            
            for tweet in tweets:
                # Get user info
                user = users_data.get(tweet.author_id, {})
                
                tweet_data = {
                    'id': str(tweet.id),
                    'platform': 'Twitter',
                    'content': tweet.text,
                    'user_id': str(tweet.author_id),
                    'username': getattr(user, 'username', f'user_{tweet.author_id}'),
                    'followers': getattr(user, 'public_metrics', {}).get('followers_count', 0),
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else datetime.utcnow().isoformat(),
                    'likes': tweet.public_metrics.get('like_count', 0) if tweet.public_metrics else 0,
                    'retweets': tweet.public_metrics.get('retweet_count', 0) if tweet.public_metrics else 0,
                    'replies': tweet.public_metrics.get('reply_count', 0) if tweet.public_metrics else 0,
                    'keywords': keywords,
                    'language': tweet.lang if hasattr(tweet, 'lang') else 'en'
                }
                collected_tweets.append(tweet_data)
            
            logger.info(f"Collected {len(collected_tweets)} tweets from Twitter API")
            return collected_tweets
            
        except Exception as e:
            logger.error(f"Error collecting Twitter data: {str(e)}")
            return self._get_fallback_twitter_data(keywords, limit)
    
    def _get_fallback_twitter_data(self, keywords: List[str], limit: int) -> List[Dict[str, Any]]:
        """Fallback data when Twitter API is not available - returns empty list for production"""
        logger.warning("Twitter API not available - no fallback data in production mode")
        return []

    def collect_reddit_data(self, subreddit: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Collect Reddit data - disabled in production (Twitter-only focus)"""
        logger.info("Reddit data collection disabled - Twitter-only monitoring in production")
        return []

    def collect_youtube_data(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Collect YouTube data - disabled in production (Twitter-only focus)"""
        logger.info("YouTube data collection disabled - Twitter-only monitoring in production")
        return []

    def collect_data_for_timeframe(self, platforms: List[str], keywords: List[str], 
                                 start_time: datetime, end_time: datetime) -> List[Dict[str, Any]]:
        """Collect data from specified platforms for a given timeframe"""
        all_posts = []
        
        for platform in platforms:
            if platform.lower() == 'twitter':
                posts = self.collect_twitter_data(keywords, limit=100)
                all_posts.extend(posts)
            elif platform.lower() == 'reddit':
                logger.info("Reddit collection disabled - Twitter-only monitoring")
            elif platform.lower() == 'youtube':
                logger.info("YouTube collection disabled - Twitter-only monitoring")
            else:
                logger.warning(f"Unknown platform: {platform}")
        
        return all_posts


# Initialize global data collector instance
data_collector = DataCollector()

# Export both class and instance for backward compatibility
__all__ = ['DataCollector', 'data_collector']