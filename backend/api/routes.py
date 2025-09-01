"""
API Routes for HexaCiphers Backend
RESTful endpoints for data collection, processing, and classification
"""

from flask import Blueprint, request, jsonify
from backend.app import db
from backend.db.models import Post, User, Campaign
from backend.preprocessing.text_processor import TextProcessor
from backend.models.classifier import SentimentClassifier
from backend.detection.campaign_detector import CampaignDetector
from backend.api.data_collector import data_collector
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Initialize processors
text_processor = TextProcessor()
classifier = SentimentClassifier()
campaign_detector = CampaignDetector()
# data_collector is imported from backend.api.data_collector

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'HexaCiphers API is running'})

@api_bp.route('/collect/twitter', methods=['POST'])
def collect_twitter_data():
    """Collect data from Twitter API"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', ['India', 'India government', 'Indian politics'])
        limit = data.get('limit', 10)
        
        # Collect data using Twitter API
        posts = data_collector.collect_twitter_data(keywords, limit)
        
        # Store posts in database if any were collected
        stored_posts = []
        for post_data in posts:
            try:
                # Classify the content
                classification_result = classifier.classify(post_data['content'])
                
                # Create post in database
                post = Post(
                    platform=post_data['platform'],
                    user_id=post_data.get('user_id'),
                    content=post_data['content'],
                    sentiment=classification_result.get('sentiment', {}).get('sentiment', 'neutral'),
                    classification=classification_result.get('india_classification', {}).get('classification', 'Neutral'),
                    url=f"https://twitter.com/{post_data.get('username', 'unknown')}/status/{post_data['id']}"
                )
                db.session.add(post)
                stored_posts.append(post_data)
            except Exception as store_error:
                logger.warning(f"Failed to store post {post_data.get('id')}: {str(store_error)}")
                continue
        
        if stored_posts:
            db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Collected {len(posts)} posts from Twitter, stored {len(stored_posts)} in database',
            'data': posts
        })
    except Exception as e:
        if 'db.session' in locals():
            db.session.rollback()
        logger.error(f"Error collecting Twitter data: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/collect/dashboard', methods=['POST'])
def collect_dashboard_data():
    """Collect 10 recent tweets for dashboard display"""
    try:
        # Default keywords for India monitoring
        keywords = ['India', 'Indian government', 'Modi', 'BJP', 'Congress', 'Delhi', 'Mumbai']
        limit = 10
        
        # Collect data using Twitter API
        posts = data_collector.collect_twitter_data(keywords, limit)
        
        # Process and store posts
        processed_posts = []
        for post_data in posts:
            try:
                # Classify the content
                classification_result = classifier.classify(post_data['content'])
                
                # Create post in database
                post = Post(
                    platform=post_data['platform'],
                    user_id=post_data.get('user_id'),
                    content=post_data['content'],
                    sentiment=classification_result.get('sentiment', {}).get('sentiment', 'neutral'),
                    classification=classification_result.get('india_classification', {}).get('classification', 'Neutral'),
                    url=f"https://twitter.com/{post_data.get('username', 'unknown')}/status/{post_data['id']}"
                )
                db.session.add(post)
                processed_posts.append({
                    'id': post_data['id'],
                    'content': post_data['content'],
                    'platform': post_data['platform'],
                    'sentiment': post.sentiment,
                    'classification': post.classification,
                    'created_at': post_data.get('created_at'),
                    'username': post_data.get('username'),
                    'engagement': {
                        'likes': post_data.get('likes', 0),
                        'retweets': post_data.get('retweets', 0),
                        'replies': post_data.get('replies', 0)
                    }
                })
            except Exception as process_error:
                logger.warning(f"Failed to process post {post_data.get('id')}: {str(process_error)}")
                continue
        
        if processed_posts:
            db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Collected and processed {len(processed_posts)} posts for dashboard',
            'data': processed_posts
        })
        
    except Exception as e:
        if 'db.session' in locals():
            db.session.rollback()
        logger.error(f"Error collecting dashboard data: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/collect/reddit', methods=['POST'])
def collect_reddit_data():
    """Collect data from Reddit API (simulated)"""
    try:
        data = request.get_json()
        subreddit = data.get('subreddit', 'india')
        limit = data.get('limit', 10)
        
        # Simulate data collection
        posts = data_collector.collect_reddit_data(subreddit, limit)
        
        return jsonify({
            'status': 'success',
            'message': f'Collected {len(posts)} posts from Reddit',
            'data': posts
        })
    except Exception as e:
        logger.error(f"Error collecting Reddit data: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/process/text', methods=['POST'])
def process_text():
    """Process and clean text content"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'status': 'error', 'message': 'Text is required'}), 400
        
        # Process text
        processed_data = text_processor.process_text(text)
        
        return jsonify({
            'status': 'success',
            'data': processed_data
        })
    except Exception as e:
        logger.error(f"Error processing text: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/classify', methods=['POST'])
def classify_content():
    """Classify content sentiment and India-relation"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'status': 'error', 'message': 'Text is required'}), 400
        
        # Classify content
        classification_result = classifier.classify(text)
        
        return jsonify({
            'status': 'success',
            'data': classification_result
        })
    except Exception as e:
        logger.error(f"Error classifying content: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/posts', methods=['GET', 'POST'])
def posts():
    """Handle posts CRUD operations"""
    if request.method == 'GET':
        try:
            # Get query parameters
            platform = request.args.get('platform')
            sentiment = request.args.get('sentiment')
            classification = request.args.get('classification')
            limit = int(request.args.get('limit', 50))
            
            # Build query
            query = Post.query
            if platform:
                query = query.filter(Post.platform == platform)
            if sentiment:
                query = query.filter(Post.sentiment == sentiment)
            if classification:
                query = query.filter(Post.classification == classification)
            
            posts = query.order_by(Post.created_at.desc()).limit(limit).all()
            
            return jsonify({
                'status': 'success',
                'data': [post.to_dict() for post in posts]
            })
        except Exception as e:
            logger.error(f"Error fetching posts: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Create new post
            post = Post(
                platform=data.get('platform'),
                user_id=data.get('user_id'),
                content=data.get('content'),
                language=data.get('language'),
                translated_text=data.get('translated_text'),
                sentiment=data.get('sentiment'),
                classification=data.get('classification')
            )
            
            db.session.add(post)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'Post created successfully',
                'data': post.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating post: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/campaigns', methods=['GET'])
def get_campaigns():
    """Get detected campaigns"""
    try:
        campaigns = Campaign.query.filter(Campaign.is_active == True).order_by(Campaign.risk_score.desc()).all()
        
        return jsonify({
            'status': 'success',
            'data': [campaign.to_dict() for campaign in campaigns]
        })
    except Exception as e:
        logger.error(f"Error fetching campaigns: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/campaigns/detect', methods=['POST'])
def detect_campaigns():
    """Detect coordinated campaigns"""
    try:
        # Get recent posts for analysis
        recent_posts = Post.query.order_by(Post.created_at.desc()).limit(1000).all()
        
        # Detect campaigns
        detected_campaigns = campaign_detector.detect_campaigns(recent_posts)
        
        # Save detected campaigns
        for campaign_data in detected_campaigns:
            campaign = Campaign(
                hashtag=campaign_data['hashtag'],
                volume=campaign_data['volume'],
                risk_score=campaign_data['risk_score']
            )
            db.session.add(campaign)
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Detected {len(detected_campaigns)} campaigns',
            'data': detected_campaigns
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error detecting campaigns: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/users', methods=['GET'])
def get_users():
    """Get users information"""
    try:
        users = User.query.all()
        
        return jsonify({
            'status': 'success',
            'data': [user.to_dict() for user in users]
        })
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/analyze-url', methods=['POST'])
def analyze_url():
    """Analyze a Twitter post by URL"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'status': 'error', 'message': 'URL is required'}), 400
        
        # Detect platform from URL
        platform = detect_platform_from_url(url)
        if not platform:
            return jsonify({'status': 'error', 'message': 'Only Twitter/X URLs are supported for analysis'}), 400
        
        # Extract content from URL (simulated)
        content_data = extract_content_from_url(url, platform)
        
        # Process and classify the content
        processed_data = text_processor.process_text(content_data['content'])
        classification_result = classifier.classify(content_data['content'])
        
        # Calculate risk score
        risk_score = calculate_risk_score(classification_result, content_data)
        
        # Simulate bot probability calculation
        bot_probability = calculate_bot_probability(content_data)
        
        analysis_result = {
            'platform': platform,
            'content': content_data['content'][:200] + '...' if len(content_data['content']) > 200 else content_data['content'],
            'sentiment': classification_result.get('sentiment', 'neutral'),
            'classification': classification_result.get('classification', 'Neutral'),
            'riskScore': risk_score,
            'botProbability': bot_probability,
            'hashtags': content_data.get('hashtags', []),
            'engagement': content_data.get('engagement', {}),
            'url': url
        }
        
        # Store the analysis result in database
        try:
            post = Post(
                platform=platform,
                content=content_data['content'],
                sentiment=classification_result.get('sentiment', {}).get('sentiment', 'neutral'),
                classification=classification_result.get('india_classification', {}).get('classification', 'Neutral'),
                url=url
            )
            db.session.add(post)
            db.session.commit()
            
            analysis_result['post_id'] = post.id
        except Exception as db_error:
            db.session.rollback()
            logger.warning(f"Failed to store post in database: {str(db_error)}")
            # Continue without storing if database operation fails
        
        return jsonify({
            'status': 'success',
            'message': 'URL analyzed successfully',
            'data': analysis_result
        })
        
    except Exception as e:
        if 'db.session' in locals():
            db.session.rollback()
        logger.error(f"Error analyzing URL: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def detect_platform_from_url(url):
    """Detect Twitter platform from URL - only Twitter/X URLs are supported"""
    url_lower = url.lower()
    
    if 'twitter.com' in url_lower or 'x.com' in url_lower:
        return 'Twitter'
    
    return None

def extract_content_from_url(url, platform):
    """Extract content from Twitter URL using Twitter API"""
    try:
        if platform != 'Twitter':
            return {
                'content': 'Only Twitter URLs are supported for analysis.',
                'hashtags': [],
                'engagement': {'likes': 0, 'shares': 0, 'comments': 0}
            }
        
        # Extract tweet ID from URL
        tweet_id = extract_tweet_id_from_url(url)
        if not tweet_id:
            return {
                'content': 'Could not extract tweet ID from URL.',
                'hashtags': [],
                'engagement': {'likes': 0, 'shares': 0, 'comments': 0}
            }
        
        # Use Twitter API to fetch tweet
        if hasattr(data_collector, 'twitter_api') and data_collector.twitter_api:
            try:
                # Fetch tweet using Twitter API v2
                tweet = data_collector.twitter_api.get_tweet(
                    tweet_id,
                    tweet_fields=['created_at', 'author_id', 'public_metrics', 'lang'],
                    user_fields=['username', 'public_metrics'],
                    expansions=['author_id']
                )
                
                if tweet.data:
                    # Extract hashtags from content
                    hashtags = []
                    content = tweet.data.text
                    import re
                    hashtag_pattern = r'#\w+'
                    hashtags = re.findall(hashtag_pattern, content)
                    
                    # Get engagement metrics
                    metrics = tweet.data.public_metrics if tweet.data.public_metrics else {}
                    engagement = {
                        'likes': metrics.get('like_count', 0),
                        'shares': metrics.get('retweet_count', 0),
                        'comments': metrics.get('reply_count', 0)
                    }
                    
                    return {
                        'content': content,
                        'hashtags': hashtags,
                        'engagement': engagement,
                        'created_at': tweet.data.created_at.isoformat() if tweet.data.created_at else None,
                        'author_id': str(tweet.data.author_id) if tweet.data.author_id else None
                    }
                else:
                    logger.warning(f"Tweet not found for ID: {tweet_id}")
                    return {
                        'content': 'Tweet not found or not accessible.',
                        'hashtags': [],
                        'engagement': {'likes': 0, 'shares': 0, 'comments': 0}
                    }
                    
            except Exception as api_error:
                logger.error(f"Twitter API error fetching tweet {tweet_id}: {str(api_error)}")
                return {
                    'content': f'Error fetching tweet from Twitter API: {str(api_error)}',
                    'hashtags': [],
                    'engagement': {'likes': 0, 'shares': 0, 'comments': 0}
                }
        else:
            logger.warning("Twitter API not available for URL analysis")
            return {
                'content': 'Twitter API not configured. Cannot fetch tweet content.',
                'hashtags': [],
                'engagement': {'likes': 0, 'shares': 0, 'comments': 0}
            }
            
    except Exception as e:
        logger.error(f"Error extracting content from URL: {str(e)}")
        return {
            'content': f'Error processing URL: {str(e)}',
            'hashtags': [],
            'engagement': {'likes': 0, 'shares': 0, 'comments': 0}
        }

def extract_tweet_id_from_url(url):
    """Extract tweet ID from Twitter/X URL"""
    import re
    
    # Patterns for Twitter URLs
    patterns = [
        r'twitter\.com/[^/]+/status/(\d+)',
        r'x\.com/[^/]+/status/(\d+)',
        r'mobile\.twitter\.com/[^/]+/status/(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def calculate_risk_score(classification_result, content_data):
    """Calculate risk score based on classification and engagement"""
    base_score = 0
    
    # Sentiment-based scoring
    sentiment = classification_result.get('sentiment', 'neutral')
    if sentiment == 'negative':
        base_score += 40
    elif sentiment == 'neutral':
        base_score += 10
    
    # Classification-based scoring
    classification = classification_result.get('classification', 'Neutral')
    if classification == 'Anti-India':
        base_score += 50
    elif classification == 'Neutral':
        base_score += 5
    
    # Engagement-based scoring (high engagement on negative content is riskier)
    engagement = content_data.get('engagement', {})
    total_engagement = engagement.get('likes', 0) + engagement.get('shares', 0) + engagement.get('comments', 0)
    
    if total_engagement > 500 and sentiment == 'negative':
        base_score += 20
    elif total_engagement > 100 and sentiment == 'negative':
        base_score += 10
    
    return min(100, base_score)

def calculate_bot_probability(content_data):
    """Calculate bot probability (simulated)"""
    import random
    # In real implementation, this would analyze user behavior patterns
    engagement = content_data.get('engagement', {})
    
    # Higher engagement might indicate bot activity
    total_engagement = engagement.get('likes', 0) + engagement.get('shares', 0) + engagement.get('comments', 0)
    
    if total_engagement > 1000:
        return random.randint(15, 35)
    elif total_engagement > 100:
        return random.randint(5, 25)
    else:
        return random.randint(0, 15)

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get comprehensive statistics"""
    try:
        # Get total counts
        total_posts = Post.query.count()
        total_users = User.query.count()
        total_campaigns = Campaign.query.count()
        
        # Get sentiment distribution
        sentiment_stats = db.session.query(
            Post.sentiment,
            db.func.count(Post.id)
        ).group_by(Post.sentiment).all()
        
        sentiment_distribution = {'positive': 0, 'negative': 0, 'neutral': 0}
        for sentiment, count in sentiment_stats:
            if sentiment:
                sentiment_distribution[sentiment] = count
        
        # Get classification distribution
        classification_stats = db.session.query(
            Post.classification,
            db.func.count(Post.id)
        ).group_by(Post.classification).all()
        
        classification_distribution = {'pro_india': 0, 'anti_india': 0, 'neutral': 0}
        for classification, count in classification_stats:
            if classification:
                if classification.lower() == 'pro-india':
                    classification_distribution['pro_india'] = count
                elif classification.lower() == 'anti-india':
                    classification_distribution['anti_india'] = count
                else:
                    classification_distribution['neutral'] = count
        
        # Get recent activity (last 24 hours)
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        posts_today = Post.query.filter(Post.created_at >= yesterday).count()
        users_today = User.query.filter(User.created_at >= yesterday).count()
        campaigns_today = Campaign.query.filter(Campaign.first_detected >= yesterday).count()
        
        # Calculate risk metrics
        high_risk_posts = Post.query.filter(Post.classification == 'Anti-India').count()
        flagged_users = User.query.filter(User.is_bot == True).count()
        
        # Simple risk score calculation
        total_analyzed = max(total_posts, 1)  # Avoid division by zero
        overall_risk_score = min(100, int((high_risk_posts / total_analyzed) * 100))
        
        stats_data = {
            'total_posts': total_posts,
            'total_users': total_users,
            'total_campaigns': total_campaigns,
            'sentiment_distribution': sentiment_distribution,
            'classification_distribution': classification_distribution,
            'recentActivity': {
                'posts_today': posts_today,
                'new_users_today': users_today,
                'campaigns_detected_today': campaigns_today
            },
            'riskMetrics': {
                'overall_risk_score': overall_risk_score,
                'high_risk_posts': high_risk_posts,
                'flagged_users': flagged_users
            }
        }
        
        return jsonify({
            'status': 'success',
            'data': stats_data
        })
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500