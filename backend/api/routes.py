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
from backend.api.data_collector import DataCollector
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Initialize processors
text_processor = TextProcessor()
classifier = SentimentClassifier()
campaign_detector = CampaignDetector()
data_collector = DataCollector()

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'HexaCiphers API is running'})

@api_bp.route('/collect/twitter', methods=['POST'])
def collect_twitter_data():
    """Collect data from Twitter API (simulated)"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', ['#India'])
        limit = data.get('limit', 10)
        
        # Simulate data collection
        posts = data_collector.collect_twitter_data(keywords, limit)
        
        return jsonify({
            'status': 'success',
            'message': f'Collected {len(posts)} posts from Twitter',
            'data': posts
        })
    except Exception as e:
        logger.error(f"Error collecting Twitter data: {str(e)}")
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
        
        # Store the analysis result
        post = Post(
            platform=platform,
            content=content_data['content'],
            sentiment=classification_result.get('sentiment', 'neutral'),
            classification=classification_result.get('classification', 'Neutral'),
            url=url
        )
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'URL analyzed successfully',
            'data': analysis_result
        })
        
    except Exception as e:
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
    """Extract content from Twitter URL (simulated)"""
    # In a real implementation, this would use Twitter APIs or web scraping
    # For now, we'll simulate the content extraction for Twitter only
    
    twitter_sample_contents = [
        {
            'content': 'India is becoming a global superpower! Amazing progress in technology and space exploration. #ProudIndian #Technology #ISRO',
            'hashtags': ['#ProudIndian', '#Technology', '#ISRO'],
            'engagement': {'likes': 245, 'shares': 12, 'comments': 8}
        },
        {
            'content': 'Another propaganda piece about India. The reality is very different from what they show. Wake up people! #Truth #Reality',
            'hashtags': ['#Truth', '#Reality'],
            'engagement': {'likes': 89, 'shares': 23, 'comments': 45}
        },
        {
            'content': 'Today I visited the beautiful Red Fort in Delhi. The architecture is absolutely stunning! #Travel #India #Heritage',
            'hashtags': ['#Travel', '#India', '#Heritage'],
            'engagement': {'likes': 156, 'shares': 7, 'comments': 12}
        }
    ]
    
    # Return a random sample content for Twitter
    import random
    return random.choice(twitter_sample_contents)

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
    """Get system statistics"""
    try:
        total_posts = Post.query.count()
        total_users = User.query.count()
        total_campaigns = Campaign.query.filter(Campaign.is_active == True).count()
        
        # Sentiment distribution
        positive_posts = Post.query.filter(Post.sentiment == 'positive').count()
        negative_posts = Post.query.filter(Post.sentiment == 'negative').count()
        neutral_posts = Post.query.filter(Post.sentiment == 'neutral').count()
        
        # Classification distribution
        pro_india = Post.query.filter(Post.classification == 'Pro-India').count()
        anti_india = Post.query.filter(Post.classification == 'Anti-India').count()
        neutral_india = Post.query.filter(Post.classification == 'Neutral').count()
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_posts': total_posts,
                'total_users': total_users,
                'total_campaigns': total_campaigns,
                'sentiment_distribution': {
                    'positive': positive_posts,
                    'negative': negative_posts,
                    'neutral': neutral_posts
                },
                'classification_distribution': {
                    'pro_india': pro_india,
                    'anti_india': anti_india,
                    'neutral': neutral_india
                }
            }
        })
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500