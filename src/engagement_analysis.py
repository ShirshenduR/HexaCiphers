import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EngagementAnalyzer:
    def __init__(self, engagement_threshold=100):
        """Initialize engagement analyzer"""
        self.engagement_threshold = engagement_threshold
        logger.info(f"Initialized EngagementAnalyzer with threshold: {engagement_threshold}")
    
    def calculate_engagement_metrics(self, df):
        """Calculate engagement metrics for tweets"""
        logger.info("Calculating engagement metrics")
        
        # Define possible engagement columns
        retweet_col = 'retweet_count' if 'retweet_count' in df.columns else None
        favorite_col = 'favorite_count' if 'favorite_count' in df.columns else 'like_count' if 'like_count' in df.columns else None
        reply_col = 'reply_count' if 'reply_count' in df.columns else None
        quote_col = 'quote_count' if 'quote_count' in df.columns else None
        
        # Calculate total engagement
        engagement_cols = [col for col in [retweet_col, favorite_col, reply_col, quote_col] if col is not None]
        
        if engagement_cols:
            df['total_engagement'] = df[engagement_cols].sum(axis=1)
            
            # Calculate engagement rate if follower count is available
            if 'user_followers' in df.columns:
                df['engagement_rate'] = df['total_engagement'] / df['user_followers'].apply(lambda x: max(x, 1))
            
            # Identify viral content
            df['is_viral'] = df['total_engagement'] > self.engagement_threshold
            
            # Calculate engagement velocity if creation time is available
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
                current_time = datetime.now()
                
                # Convert to hours since posting
                df['hours_since_posting'] = (current_time - df['created_at']).dt.total_seconds() / 3600
                
                # Calculate engagement per hour
                df['engagement_velocity'] = df['total_engagement'] / df['hours_since_posting'].apply(lambda x: max(x, 1))
        else:
            logger.warning("No engagement columns found in dataframe")
        
        return df
    
    def identify_influential_content(self, df):
        """Identify influential content based on engagement metrics"""
        logger.info("Identifying influential content")
        
        if 'total_engagement' not in df.columns:
            logger.warning("Total engagement not calculated, running calculate_engagement_metrics first")
            df = self.calculate_engagement_metrics(df)
        
        # Sort by engagement
        df_sorted = df.sort_values(by='total_engagement', ascending=False)
        
        # Top 10% of engaging content
        threshold = df['total_engagement'].quantile(0.9)
        df_influential = df_sorted[df_sorted['total_engagement'] >= threshold].copy()
        
        # Mark as influential
        df['is_influential'] = df['total_engagement'] >= threshold
        
        logger.info(f"Identified {len(df_influential)} influential tweets")
        return df, df_influential
    
    def analyze_user_engagement(self, df):
        """Analyze user engagement patterns"""
        logger.info("Analyzing user engagement patterns")
        
        if 'user_id' not in df.columns:
            logger.warning("User ID column not found in dataframe")
            return df, pd.DataFrame()
        
        # Group by user
        user_metrics = df.groupby('user_id').agg({
            'id': 'count',  # count of tweets
            'total_engagement': 'sum',
            'anti_india_score': 'mean',
            'user_followers': 'first',
            'user_following': 'first',
            'username': 'first',
            'user_verified': 'first'
        }).reset_index()
        
        # Rename columns
        user_metrics.rename(columns={'id': 'tweet_count'}, inplace=True)
        
        # Calculate impact score
        user_metrics['impact_score'] = (
            user_metrics['total_engagement'] * 
            user_metrics['anti_india_score'] * 
            np.log1p(user_metrics['user_followers']) / 
            np.log1p(user_metrics['tweet_count'])
        )
        
        # Sort by impact score
        user_metrics = user_metrics.sort_values(by='impact_score', ascending=False)
        
        # Flag influential users
        threshold = user_metrics['impact_score'].quantile(0.9)
        user_metrics['is_influential'] = user_metrics['impact_score'] >= threshold
        
        # Add influential user flag back to original dataframe
        influential_user_ids = user_metrics[user_metrics['is_influential']]['user_id'].tolist()
        df['user_is_influential'] = df['user_id'].isin(influential_user_ids)
        
        logger.info(f"Identified {len(influential_user_ids)} influential users")
        return df, user_metrics