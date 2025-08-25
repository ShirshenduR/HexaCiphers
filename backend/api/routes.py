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