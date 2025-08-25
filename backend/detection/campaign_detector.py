"""
Campaign Detection Module
Detects coordinated campaigns, bot networks, and suspicious activities
"""

import logging
from typing import Dict, List, Set, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re

try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    logging.warning("NetworkX not available. Graph analysis will be limited.")

logger = logging.getLogger(__name__)

class CampaignDetector:
    """Class for detecting coordinated campaigns and bot activities"""
    
    def __init__(self):
        self.min_campaign_volume = 5  # Minimum posts to consider a campaign
        self.max_time_window = 24  # Hours to consider for campaign detection
        self.bot_indicators_threshold = 3  # Number of bot indicators to flag as bot
        
        # Bot detection patterns
        self.bot_username_patterns = [
            r'.*\d{8,}$',  # Usernames ending with 8+ digits
            r'^[a-zA-Z]+\d{4,}$',  # Letter followed by 4+ digits
            r'.*bot.*',  # Contains 'bot'
            r'.*fake.*',  # Contains 'fake'
        ]
        
        # Suspicious hashtag patterns
        self.suspicious_hashtag_patterns = [
            r'#boycott.*india',
            r'#anti.*india',
            r'#fake.*india',
            r'#destroy.*india',
            r'#hate.*india'
        ]
    
    def detect_campaigns(self, posts: List) -> List[Dict]:
        """
        Detect coordinated campaigns from posts
        
        Args:
            posts (List): List of post objects or dictionaries
            
        Returns:
            List[Dict]: List of detected campaigns
        """
        logger.info(f"Analyzing {len(posts)} posts for campaign detection")
        
        # Extract hashtags and their usage patterns
        hashtag_activity = self._analyze_hashtag_activity(posts)
        
        # Detect coordinated hashtag usage
        coordinated_hashtags = self._detect_coordinated_hashtags(hashtag_activity)
        
        # Analyze user behavior patterns
        user_patterns = self._analyze_user_patterns(posts)
        
        # Detect suspicious user networks
        suspicious_networks = self._detect_suspicious_networks(posts)
        
        campaigns = []
        
        # Create campaign objects from detected patterns
        for hashtag, activity in coordinated_hashtags.items():
            campaign = {
                'hashtag': hashtag,
                'volume': activity['total_posts'],
                'unique_users': len(activity['users']),
                'time_span': activity['time_span'],
                'risk_score': self._calculate_risk_score(activity, user_patterns),
                'first_detected': activity['first_post'],
                'last_detected': activity['last_post'],
                'suspicious_indicators': activity['indicators'],
                'user_network': activity['users'][:10]  # Top 10 users
            }
            campaigns.append(campaign)
        
        # Add network-based campaigns
        for network in suspicious_networks:
            if network['risk_score'] > 0.5:
                campaign = {
                    'hashtag': f"network_{network['id']}",
                    'volume': network['total_posts'],
                    'unique_users': len(network['users']),
                    'time_span': network['time_span'],
                    'risk_score': network['risk_score'],
                    'first_detected': network['first_activity'],
                    'last_detected': network['last_activity'],
                    'suspicious_indicators': network['indicators'],
                    'user_network': network['users']
                }
                campaigns.append(campaign)
        
        # Sort by risk score
        campaigns.sort(key=lambda x: x['risk_score'], reverse=True)
        
        logger.info(f"Detected {len(campaigns)} potential campaigns")
        return campaigns
    
    def _analyze_hashtag_activity(self, posts: List) -> Dict:
        """Analyze hashtag usage patterns"""
        hashtag_activity = defaultdict(lambda: {
            'posts': [],
            'users': set(),
            'timestamps': [],
            'total_posts': 0
        })
        
        for post in posts:
            # Extract hashtags from post content
            content = post.content if hasattr(post, 'content') else post.get('content', '')
            hashtags = re.findall(r'#\w+', content.lower())
            
            user_id = post.user_id if hasattr(post, 'user_id') else post.get('user_id', '')
            timestamp = post.created_at if hasattr(post, 'created_at') else post.get('created_at', datetime.utcnow())
            
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except:
                    timestamp = datetime.utcnow()
            
            for hashtag in hashtags:
                hashtag_activity[hashtag]['posts'].append(post)
                hashtag_activity[hashtag]['users'].add(user_id)
                hashtag_activity[hashtag]['timestamps'].append(timestamp)
                hashtag_activity[hashtag]['total_posts'] += 1
        
        return hashtag_activity
    
    def _detect_coordinated_hashtags(self, hashtag_activity: Dict) -> Dict:
        """Detect coordinated hashtag campaigns"""
        coordinated = {}
        
        for hashtag, activity in hashtag_activity.items():
            if activity['total_posts'] < self.min_campaign_volume:
                continue
            
            # Calculate time span
            timestamps = sorted(activity['timestamps'])
            if len(timestamps) < 2:
                continue
                
            time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 3600  # Hours
            
            # Check for coordination indicators
            indicators = []
            
            # Rapid posting in short time window
            if time_span < 2 and activity['total_posts'] > 10:
                indicators.append('rapid_posting')
            
            # High user-to-post ratio (each user posting multiple times)
            avg_posts_per_user = activity['total_posts'] / len(activity['users'])
            if avg_posts_per_user > 3:
                indicators.append('repeated_posting')
            
            # Check for suspicious hashtag patterns
            for pattern in self.suspicious_hashtag_patterns:
                if re.match(pattern, hashtag):
                    indicators.append('suspicious_hashtag')
                    break
            
            # Analyze posting time distribution
            hour_distribution = defaultdict(int)
            for ts in timestamps:
                hour_distribution[ts.hour] += 1
            
            # Check for unnatural time distribution
            max_hour_posts = max(hour_distribution.values()) if hour_distribution else 0
            if max_hour_posts > activity['total_posts'] * 0.5:
                indicators.append('concentrated_timing')
            
            coordinated[hashtag] = {
                'total_posts': activity['total_posts'],
                'users': list(activity['users']),
                'time_span': time_span,
                'first_post': timestamps[0],
                'last_post': timestamps[-1],
                'indicators': indicators,
                'avg_posts_per_user': avg_posts_per_user
            }
        
        return coordinated
    
    def _analyze_user_patterns(self, posts: List) -> Dict:
        """Analyze user behavior patterns"""
        user_patterns = defaultdict(lambda: {
            'posts': [],
            'hashtags': set(),
            'post_times': [],
            'content_similarity': 0,
            'bot_indicators': []
        })
        
        for post in posts:
            user_id = post.user_id if hasattr(post, 'user_id') else post.get('user_id', '')
            content = post.content if hasattr(post, 'content') else post.get('content', '')
            timestamp = post.created_at if hasattr(post, 'created_at') else post.get('created_at', datetime.utcnow())
            
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except:
                    timestamp = datetime.utcnow()
            
            hashtags = set(re.findall(r'#\w+', content.lower()))
            
            user_patterns[user_id]['posts'].append(post)
            user_patterns[user_id]['hashtags'].update(hashtags)
            user_patterns[user_id]['post_times'].append(timestamp)
            
            # Check for bot indicators
            username = post.username if hasattr(post, 'username') else post.get('username', user_id)
            self._check_bot_indicators(user_patterns[user_id], username, content)
        
        return user_patterns
    
    def _check_bot_indicators(self, user_pattern: Dict, username: str, content: str):
        """Check for bot indicators in user behavior"""
        indicators = user_pattern['bot_indicators']
        
        # Username pattern analysis
        for pattern in self.bot_username_patterns:
            if re.match(pattern, username.lower()):
                if 'suspicious_username' not in indicators:
                    indicators.append('suspicious_username')
                break
        
        # Repetitive content
        if len(user_pattern['posts']) > 1:
            recent_content = [p.content if hasattr(p, 'content') else p.get('content', '') 
                            for p in user_pattern['posts'][-5:]]  # Last 5 posts
            
            # Check for exact duplicates
            if len(set(recent_content)) < len(recent_content) * 0.8:
                if 'repetitive_content' not in indicators:
                    indicators.append('repetitive_content')
        
        # High posting frequency
        if len(user_pattern['post_times']) > 1:
            time_diffs = []
            for i in range(1, len(user_pattern['post_times'])):
                diff = (user_pattern['post_times'][i] - user_pattern['post_times'][i-1]).total_seconds()
                time_diffs.append(diff)
            
            avg_interval = sum(time_diffs) / len(time_diffs) if time_diffs else 0
            if avg_interval < 300:  # Less than 5 minutes between posts
                if 'high_frequency_posting' not in indicators:
                    indicators.append('high_frequency_posting')
    
    def _detect_suspicious_networks(self, posts: List) -> List[Dict]:
        """Detect suspicious user networks"""
        if not NETWORKX_AVAILABLE:
            logger.warning("NetworkX not available. Skipping network analysis.")
            return []
        
        # Build interaction graph
        G = nx.Graph()
        
        # Add nodes and edges based on shared hashtags and timing
        hashtag_users = defaultdict(set)
        
        for post in posts:
            user_id = post.user_id if hasattr(post, 'user_id') else post.get('user_id', '')
            content = post.content if hasattr(post, 'content') else post.get('content', '')
            hashtags = re.findall(r'#\w+', content.lower())
            
            G.add_node(user_id)
            
            for hashtag in hashtags:
                hashtag_users[hashtag].add(user_id)
        
        # Add edges between users who use similar hashtags
        for hashtag, users in hashtag_users.items():
            users_list = list(users)
            for i in range(len(users_list)):
                for j in range(i + 1, len(users_list)):
                    if G.has_edge(users_list[i], users_list[j]):
                        G[users_list[i]][users_list[j]]['weight'] += 1
                    else:
                        G.add_edge(users_list[i], users_list[j], weight=1)
        
        # Find connected components
        networks = []
        for component in nx.connected_components(G):
            if len(component) >= 3:  # At least 3 users in network
                subgraph = G.subgraph(component)
                
                # Calculate network metrics
                density = nx.density(subgraph)
                centrality = nx.degree_centrality(subgraph)
                
                # Calculate risk score based on network properties
                risk_score = min(1.0, density * len(component) / 10)
                
                # Get network activity details
                network_posts = [p for p in posts if 
                               (p.user_id if hasattr(p, 'user_id') else p.get('user_id', '')) in component]
                
                if network_posts:
                    timestamps = [p.created_at if hasattr(p, 'created_at') else p.get('created_at', datetime.utcnow()) 
                                for p in network_posts]
                    timestamps = [ts if isinstance(ts, datetime) else datetime.utcnow() for ts in timestamps]
                    
                    network = {
                        'id': f"net_{len(networks)}",
                        'users': list(component),
                        'size': len(component),
                        'density': density,
                        'total_posts': len(network_posts),
                        'risk_score': risk_score,
                        'first_activity': min(timestamps),
                        'last_activity': max(timestamps),
                        'time_span': (max(timestamps) - min(timestamps)).total_seconds() / 3600,
                        'indicators': self._get_network_indicators(subgraph, network_posts)
                    }
                    networks.append(network)
        
        return networks
    
    def _get_network_indicators(self, graph, posts: List) -> List[str]:
        """Get indicators of suspicious network behavior"""
        indicators = []
        
        # High density networks (users highly connected)
        if nx.density(graph) > 0.7:
            indicators.append('high_density_network')
        
        # Coordinated posting times
        timestamps = [p.created_at if hasattr(p, 'created_at') else p.get('created_at', datetime.utcnow()) 
                     for p in posts]
        timestamps = [ts if isinstance(ts, datetime) else datetime.utcnow() for ts in timestamps]
        
        if len(timestamps) > 1:
            time_diffs = []
            sorted_times = sorted(timestamps)
            for i in range(1, len(sorted_times)):
                diff = (sorted_times[i] - sorted_times[i-1]).total_seconds()
                time_diffs.append(diff)
            
            # Check for very similar posting times
            if len([d for d in time_diffs if d < 60]) > len(time_diffs) * 0.3:
                indicators.append('coordinated_timing')
        
        return indicators
    
    def _calculate_risk_score(self, activity: Dict, user_patterns: Dict) -> float:
        """Calculate risk score for a campaign"""
        score = 0.0
        
        # Volume factor
        volume_score = min(1.0, activity['total_posts'] / 100)
        score += volume_score * 0.3
        
        # Time concentration factor
        if activity['time_span'] < 1:  # Less than 1 hour
            score += 0.3
        elif activity['time_span'] < 6:  # Less than 6 hours
            score += 0.2
        
        # User behavior factor
        bot_users = 0
        for user in activity['users']:
            if user in user_patterns:
                bot_indicators = len(user_patterns[user]['bot_indicators'])
                if bot_indicators >= self.bot_indicators_threshold:
                    bot_users += 1
        
        if len(activity['users']) > 0:
            bot_ratio = bot_users / len(activity['users'])
            score += bot_ratio * 0.3
        
        # Indicators factor
        score += len(activity['indicators']) * 0.1
        
        return min(1.0, score)
    
    def detect_bot_users(self, posts: List) -> List[Dict]:
        """Detect potential bot users"""
        user_patterns = self._analyze_user_patterns(posts)
        
        bots = []
        for user_id, pattern in user_patterns.items():
            bot_score = len(pattern['bot_indicators']) / max(len(self.bot_username_patterns), 1)
            
            if len(pattern['bot_indicators']) >= self.bot_indicators_threshold:
                bot = {
                    'user_id': user_id,
                    'bot_score': min(1.0, bot_score),
                    'indicators': pattern['bot_indicators'],
                    'post_count': len(pattern['posts']),
                    'hashtag_count': len(pattern['hashtags']),
                    'risk_level': 'high' if bot_score > 0.7 else 'medium'
                }
                bots.append(bot)
        
        return sorted(bots, key=lambda x: x['bot_score'], reverse=True)