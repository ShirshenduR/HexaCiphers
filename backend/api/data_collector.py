"""
Data Collection Module
Simulates data collection from various social media platforms
"""

import random
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class DataCollector:
    """Class for collecting data from social media platforms"""
    
    def __init__(self):
        # Sample data for simulation
        self.sample_tweets = [
            "India is making great progress in technology and innovation! #DigitalIndia #TechIndia",
            "Beautiful landscapes in Kashmir today #Kashmir #India #Nature",
            "Propaganda against India must be stopped #FakeNews #AntiIndia",
            "India's democracy is under threat from misinformation campaigns",
            "Boycott Indian products spreading fake news #BoycottIndia",
            "Indian culture and diversity should be celebrated worldwide",
            "Anti-India sentiment rising on social media platforms",
            "India's economic growth is impressive this quarter #IndianEconomy",
            "Coordinated attack on India's image using bots and fake accounts",
            "India's space program achievements are remarkable #ISRO #SpaceIndia"
        ]
        
        self.sample_reddit_posts = [
            "Discussion about India's foreign policy and international relations",
            "Indian startup ecosystem is booming with new innovations",
            "Misinformation campaigns targeting India on social media",
            "India's contribution to global peace and stability",
            "Analysis of anti-India propaganda on digital platforms",
            "India's cultural soft power and international influence",
            "Examining coordinated attacks on India's reputation online",
            "India's technological advancements in AI and machine learning",
            "Foreign interference in India's internal affairs through social media",
            "India's democratic values and their global significance"
        ]
        
        self.sample_users = [
            {"user_id": "user1", "username": "tech_enthusiast", "followers": 1500},
            {"user_id": "user2", "username": "india_defender", "followers": 2300},
            {"user_id": "user3", "username": "bot_account_123", "followers": 50},
            {"user_id": "user4", "username": "news_reporter", "followers": 5000},
            {"user_id": "user5", "username": "social_activist", "followers": 800},
        ]
    
    def collect_twitter_data(self, keywords, limit=10):
        """
        Simulate Twitter data collection
        
        Args:
            keywords (list): List of keywords to search for
            limit (int): Number of posts to collect
            
        Returns:
            list: List of simulated Twitter posts
        """
        logger.info(f"Simulating Twitter data collection for keywords: {keywords}")
        
        posts = []
        for i in range(min(limit, len(self.sample_tweets))):
            user = random.choice(self.sample_users)
            post = {
                "id": f"twitter_{i+1}",
                "platform": "Twitter",
                "user_id": user["user_id"],
                "username": user["username"],
                "content": self.sample_tweets[i],
                "followers": user["followers"],
                "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 24))).isoformat(),
                "likes": random.randint(0, 100),
                "retweets": random.randint(0, 50),
                "keywords": keywords
            }
            posts.append(post)
        
        return posts
    
    def collect_reddit_data(self, subreddit, limit=10):
        """
        Simulate Reddit data collection
        
        Args:
            subreddit (str): Subreddit to collect from
            limit (int): Number of posts to collect
            
        Returns:
            list: List of simulated Reddit posts
        """
        logger.info(f"Simulating Reddit data collection from r/{subreddit}")
        
        posts = []
        for i in range(min(limit, len(self.sample_reddit_posts))):
            user = random.choice(self.sample_users)
            post = {
                "id": f"reddit_{i+1}",
                "platform": "Reddit",
                "user_id": user["user_id"],
                "username": user["username"],
                "content": self.sample_reddit_posts[i],
                "subreddit": subreddit,
                "created_at": (datetime.utcnow() - timedelta(hours=random.randint(1, 48))).isoformat(),
                "upvotes": random.randint(0, 200),
                "comments": random.randint(0, 50)
            }
            posts.append(post)
        
        return posts
    
    def collect_youtube_data(self, query, limit=10):
        """
        Simulate YouTube data collection
        
        Args:
            query (str): Search query
            limit (int): Number of videos to collect
            
        Returns:
            list: List of simulated YouTube posts
        """
        logger.info(f"Simulating YouTube data collection for query: {query}")
        
        sample_titles = [
            "India's Amazing Cultural Heritage",
            "Technology Innovation in India",
            "Propaganda Analysis: Anti-India Campaigns",
            "Indian Democracy and Its Challenges",
            "Economic Growth in Modern India",
            "Social Media Manipulation Tactics",
            "India's Role in Global Politics",
            "Combating Misinformation Online",
            "Indian Values and Global Influence",
            "Digital India Success Stories"
        ]
        
        posts = []
        for i in range(min(limit, len(sample_titles))):
            user = random.choice(self.sample_users)
            post = {
                "id": f"youtube_{i+1}",
                "platform": "YouTube",
                "user_id": user["user_id"],
                "username": user["username"],
                "title": sample_titles[i],
                "content": f"Video content about: {sample_titles[i]}",
                "views": random.randint(1000, 100000),
                "likes": random.randint(10, 1000),
                "duration": f"{random.randint(2, 30)}:{random.randint(10, 59)}",
                "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat()
            }
            posts.append(post)
        
        return posts
    
    def simulate_real_time_feed(self, duration_minutes=5):
        """
        Simulate real-time data feed
        
        Args:
            duration_minutes (int): Duration to simulate in minutes
            
        Returns:
            list: List of posts with timestamps
        """
        logger.info(f"Simulating real-time feed for {duration_minutes} minutes")
        
        posts = []
        start_time = datetime.utcnow()
        
        for minute in range(duration_minutes):
            # Simulate 1-3 posts per minute
            posts_per_minute = random.randint(1, 3)
            
            for _ in range(posts_per_minute):
                platform = random.choice(["Twitter", "Reddit", "YouTube"])
                user = random.choice(self.sample_users)
                
                if platform == "Twitter":
                    content = random.choice(self.sample_tweets)
                else:
                    content = random.choice(self.sample_reddit_posts)
                
                post = {
                    "id": f"{platform.lower()}_{len(posts)+1}",
                    "platform": platform,
                    "user_id": user["user_id"],
                    "username": user["username"],
                    "content": content,
                    "created_at": (start_time + timedelta(minutes=minute)).isoformat(),
                    "engagement": random.randint(10, 500)
                }
                posts.append(post)
        
        return posts