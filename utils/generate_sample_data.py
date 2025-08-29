import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import random

# Ensure directories exist
os.makedirs('data/processed', exist_ok=True)

# Load keywords for more realistic data
with open('data/keywords.json', 'r') as f:
    keywords_data = json.load(f)

keywords = keywords_data.get('keywords', [])
hashtags = keywords_data.get('hashtags', [])
phrases = keywords_data.get('phrases', [])

# Sample usernames and names
usernames = [
    'user123', 'twitterfan', 'newsreader', 'politicalvoice', 'commentator',
    'observer', 'citizen_x', 'voice_of_truth', 'news_watcher', 'opinionated',
    'global_view', 'free_thinker', 'truth_seeker', 'news_junkie', 'fact_checker'
]

names = [
    'John Doe', 'Jane Smith', 'Alex Johnson', 'Sam Wilson', 'Taylor Brown',
    'Morgan Lee', 'Casey Miller', 'Jordan Davis', 'Riley Wilson', 'Avery Thomas',
    'Quinn Anderson', 'Drew Martin', 'Jesse Thompson', 'Parker Hall', 'Robin Clark'
]

# Sample tweet templates
tweet_templates = [
    "{phrase} is becoming more evident day by day. {hashtag}",
    "Can't believe what's happening in India. {phrase} {hashtag}",
    "{hashtag} {phrase} - This needs international attention!",
    "This is concerning: {phrase}. What are your thoughts? {hashtag}",
    "Breaking: New evidence of {phrase}. {hashtag}",
    "{hashtag} {phrase} - Spread awareness!",
    "Why is nobody talking about {phrase}? {hashtag}",
    "Just read an article about {phrase}. Shocking! {hashtag}",
    "International community needs to address {phrase} immediately. {hashtag}",
    "Thread on {phrase}: 1/5 The situation is deteriorating {hashtag}"
]

# Neutral/positive tweet templates
neutral_templates = [
    "Interesting developments in India's tech sector today.",
    "India's cultural heritage is truly remarkable.",
    "Visited India last year - amazing food and friendly people!",
    "The diversity across Indian states is fascinating.",
    "India's space program has made significant progress.",
    "Watching cricket match - India vs Australia.",
    "India's renewable energy initiatives are promising.",
    "Just finished reading a book about India's history.",
    "The landscapes in India are breathtaking.",
    "India's film industry produces some wonderful movies."
]

def generate_sample_tweets(count=1000):
    """Generate sample Twitter data"""
    current_time = datetime.now()
    
    data = []
    
    # Generate some anti-India tweets
    anti_india_count = int(count * 0.3)  # 30% anti-India content
    
    for _ in range(anti_india_count):
        # Random user
        user_id = random.randint(100000, 999999)
        username = random.choice(usernames)
        user_name = random.choice(names)
        
        # Random engagement metrics
        followers = random.randint(100, 10000)
        following = random.randint(50, 1000)
        statuses = random.randint(100, 5000)
        verified = random.random() < 0.1  # 10% chance of being verified
        
        # Random creation time
        user_created_at = current_time - timedelta(days=random.randint(30, 1000))
        
        # Random tweet time
        created_at = current_time - timedelta(hours=random.randint(1, 72))
        
        # Generate tweet
        template = random.choice(tweet_templates)
        phrase = random.choice(phrases)
        hashtag = random.choice(hashtags)
        
        text = template.format(phrase=phrase, hashtag=hashtag)
        
        # Random engagement
        retweet_count = random.randint(0, 100)
        favorite_count = random.randint(0, 200)
        reply_count = random.randint(0, 50)
        
        # Random hashtags in the tweet
        tweet_hashtags = [hashtag.replace('#', '')]
        if random.random() < 0.5:  # 50% chance of having an additional hashtag
            tweet_hashtags.append(random.choice(hashtags).replace('#', ''))
        
        # Random mentions
        mentions = []
        if random.random() < 0.4:  # 40% chance of mentioning someone
            mentions = [random.choice(usernames)]
        
        data.append({
            'id': random.randint(1000000000000000000, 9999999999999999999),
            'created_at': created_at,
            'text': text,
            'user_id': user_id,
            'username': username,
            'user_name': user_name,
            'user_followers': followers,
            'user_following': following,
            'user_statuses': statuses,
            'user_verified': verified,
            'user_created_at': user_created_at,
            'retweet_count': retweet_count,
            'favorite_count': favorite_count,
            'reply_count': reply_count,
            'hashtags': tweet_hashtags,
            'mentions': mentions,
            'is_retweet': random.random() < 0.3  # 30% chance of being a retweet
        })
    
    # Generate neutral/positive tweets
    for _ in range(count - anti_india_count):
        # Random user
        user_id = random.randint(100000, 999999)
        username = random.choice(usernames)
        user_name = random.choice(names)
        
        # Random engagement metrics
        followers = random.randint(100, 10000)
        following = random.randint(50, 1000)
        statuses = random.randint(100, 5000)
        verified = random.random() < 0.1  # 10% chance of being verified
        
        # Random creation time
        user_created_at = current_time - timedelta(days=random.randint(30, 1000))
        
        # Random tweet time
        created_at = current_time - timedelta(hours=random.randint(1, 72))
        
        # Generate tweet
        text = random.choice(neutral_templates)
        
        # Random engagement
        retweet_count = random.randint(0, 100)
        favorite_count = random.randint(0, 200)
        reply_count = random.randint(0, 50)
        
        # Random hashtags in the tweet
        tweet_hashtags = []
        if random.random() < 0.3:  # 30% chance of having a hashtag
            tweet_hashtags.append("India")
        
        # Random mentions
        mentions = []
        if random.random() < 0.2:  # 20% chance of mentioning someone
            mentions = [random.choice(usernames)]
        
        data.append({
            'id': random.randint(1000000000000000000, 9999999999999999999),
            'created_at': created_at,
            'text': text,
            'user_id': user_id,
            'username': username,
            'user_name': user_name,
            'user_followers': followers,
            'user_following': following,
            'user_statuses': statuses,
            'user_verified': verified,
            'user_created_at': user_created_at,
            'retweet_count': retweet_count,
            'favorite_count': favorite_count,
            'reply_count': reply_count,
            'hashtags': tweet_hashtags,
            'mentions': mentions,
            'is_retweet': random.random() < 0.2  # 20% chance of being a retweet
        })
    
    # Create dataframe
    df = pd.DataFrame(data)
    
    # Convert datetime objects to strings
    df['created_at'] = df['created_at'].astype(str)
    df['user_created_at'] = df['user_created_at'].astype(str)
    
    return df

def create_sample_dataset():
    """Create a sample dataset file"""
    print("Generating sample Twitter dataset...")
    df = generate_sample_tweets(1000)
    
    # Save to CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sample_twitter_data_{timestamp}.csv"
    filepath = os.path.join('data/processed', filename)
    
    df.to_csv(filepath, index=False)
    print(f"Sample dataset saved to {filepath}")
    return filepath

if __name__ == "__main__":
    create_sample_dataset()