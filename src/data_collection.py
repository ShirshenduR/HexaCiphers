import tweepy
import pandas as pd
import json
import os
import time
from datetime import datetime, timedelta
import logging
from config.config import (
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_SECRET,
    TWITTER_BEARER_TOKEN,
    KEYWORDS_PATH,
    SCAN_INTERVAL
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterClient:
    def __init__(self):
        """Initialize Twitter API client"""
        try:
            self.auth = tweepy.OAuth1UserHandler(
                TWITTER_API_KEY,
                TWITTER_API_SECRET,
                TWITTER_ACCESS_TOKEN,
                TWITTER_ACCESS_SECRET
            )
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
            
            # For v2 endpoints
            self.client = tweepy.Client(
                bearer_token=TWITTER_BEARER_TOKEN,
                consumer_key=TWITTER_API_KEY,
                consumer_secret=TWITTER_API_SECRET,
                access_token=TWITTER_ACCESS_TOKEN,
                access_token_secret=TWITTER_ACCESS_SECRET,
                wait_on_rate_limit=True
            )
            logger.info("Twitter API client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Twitter client: {e}")
            raise

    def load_keywords(self):
        """Load keywords from the JSON file"""
        try:
            with open(KEYWORDS_PATH, 'r') as f:
                data = json.load(f)
            
            all_terms = []
            all_terms.extend(data.get('keywords', []))
            all_terms.extend(data.get('hashtags', []))
            all_terms.extend(data.get('phrases', []))
            
            logger.info(f"Loaded {len(all_terms)} search terms")
            return all_terms
        except Exception as e:
            logger.error(f"Error loading keywords: {e}")
            return []

    def search_tweets(self, query, count=100, lang="en", result_type="recent"):
        """Search for tweets using v1.1 API (more detailed data)"""
        try:
            tweets = []
            for tweet in tweepy.Cursor(
                self.api.search_tweets,
                q=query,
                lang=lang,
                result_type=result_type,
                count=count,
                tweet_mode="extended"
            ).items(count):
                tweet_data = {
                    'id': tweet.id,
                    'created_at': tweet.created_at,
                    'text': tweet.full_text,
                    'user_id': tweet.user.id,
                    'username': tweet.user.screen_name,
                    'user_name': tweet.user.name,
                    'user_followers': tweet.user.followers_count,
                    'user_following': tweet.user.friends_count,
                    'user_statuses': tweet.user.statuses_count,
                    'user_verified': tweet.user.verified,
                    'user_created_at': tweet.user.created_at,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count,
                    'is_retweet': hasattr(tweet, 'retweeted_status'),
                    'hashtags': [h['text'] for h in tweet.entities.get('hashtags', [])],
                    'mentions': [m['screen_name'] for m in tweet.entities.get('user_mentions', [])]
                }
                tweets.append(tweet_data)
            
            logger.info(f"Retrieved {len(tweets)} tweets for query: {query}")
            return pd.DataFrame(tweets)
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return pd.DataFrame()

    def search_recent_tweets_v2(self, query, max_results=100):
        """Search for tweets using v2 API"""
        try:
            response = self.client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'author_id', 'entities'],
                user_fields=['name', 'username', 'public_metrics', 'verified', 'created_at'],
                expansions=['author_id']
            )
            
            if not response.data:
                logger.info(f"No tweets found for query: {query}")
                return pd.DataFrame()
                
            tweets = []
            users = {user.id: user for user in response.includes['users']} if 'users' in response.includes else {}
            
            for tweet in response.data:
                user = users.get(tweet.author_id, None)
                
                tweet_data = {
                    'id': tweet.id,
                    'created_at': tweet.created_at,
                    'text': tweet.text,
                    'user_id': tweet.author_id,
                    'retweet_count': tweet.public_metrics['retweet_count'],
                    'reply_count': tweet.public_metrics['reply_count'],
                    'like_count': tweet.public_metrics['like_count'],
                    'quote_count': tweet.public_metrics['quote_count'],
                }
                
                if user:
                    tweet_data.update({
                        'username': user.username,
                        'user_name': user.name,
                        'user_followers': user.public_metrics['followers_count'],
                        'user_following': user.public_metrics['following_count'],
                        'user_statuses': user.public_metrics['tweet_count'],
                        'user_verified': user.verified,
                        'user_created_at': user.created_at,
                    })
                    
                if hasattr(tweet, 'entities') and tweet.entities:
                    if 'hashtags' in tweet.entities:
                        tweet_data['hashtags'] = [h['tag'] for h in tweet.entities['hashtags']]
                    if 'mentions' in tweet.entities:
                        tweet_data['mentions'] = [m['username'] for m in tweet.entities['mentions']]
                
                tweets.append(tweet_data)
            
            logger.info(f"Retrieved {len(tweets)} tweets for query: {query}")
            return pd.DataFrame(tweets)
        except Exception as e:
            logger.error(f"Error searching tweets (v2): {e}")
            return pd.DataFrame()

    def collect_data(self, output_path):
        """Collect tweets based on keywords and save to CSV"""
        keywords = self.load_keywords()
        if not keywords:
            logger.error("No keywords available for search")
            return
        
        all_tweets = pd.DataFrame()
        
        for keyword in keywords:
            logger.info(f"Searching for tweets with keyword: {keyword}")
            try:
                # Try v2 API first
                tweets = self.search_recent_tweets_v2(keyword)
                
                # If v2 fails or returns empty, try v1.1
                if tweets.empty:
                    tweets = self.search_tweets(keyword)
                
                if not tweets.empty:
                    tweets['keyword'] = keyword
                    all_tweets = pd.concat([all_tweets, tweets], ignore_index=True)
            except Exception as e:
                logger.error(f"Error collecting data for keyword {keyword}: {e}")
                continue
        
        if not all_tweets.empty:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"twitter_data_{timestamp}.csv"
            filepath = os.path.join(output_path, filename)
            
            # Ensure output directory exists
            os.makedirs(output_path, exist_ok=True)
            
            all_tweets.to_csv(filepath, index=False)
            logger.info(f"Saved {len(all_tweets)} tweets to {filepath}")
            return filepath
        else:
            logger.warning("No tweets collected")
            return None

def continuous_collection(output_path, duration=None):
    """Run continuous collection for a specified duration or indefinitely"""
    client = TwitterClient()
    start_time = datetime.now()
    
    try:
        while True:
            logger.info(f"Starting data collection at {datetime.now()}")
            client.collect_data(output_path)
            
            if duration and (datetime.now() - start_time) > timedelta(minutes=duration):
                logger.info(f"Collection completed after {duration} minutes")
                break
                
            logger.info(f"Sleeping for {SCAN_INTERVAL} seconds...")
            time.sleep(SCAN_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Collection stopped by user")
    except Exception as e:
        logger.error(f"Error in continuous collection: {e}")