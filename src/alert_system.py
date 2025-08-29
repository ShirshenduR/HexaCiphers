import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.config import ALERT_THRESHOLD

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertSystem:
    def __init__(self, alert_threshold=ALERT_THRESHOLD, 
                 email_config=None, output_dir='./alerts'):
        """Initialize alert system"""
        self.alert_threshold = alert_threshold
        self.email_config = email_config
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"Initialized AlertSystem with threshold: {alert_threshold}")
    
    def generate_alerts(self, df, user_metrics=None, coord_df=None):
        """Generate alerts based on analysis results"""
        logger.info("Generating alerts")
        
        alerts = []
        
        # Filter for high anti-India scores
        if 'anti_india_score' in df.columns:
            high_score_tweets = df[df['anti_india_score'] > self.alert_threshold / 10].sort_values(
                by='anti_india_score', ascending=False)
            
            for _, tweet in high_score_tweets.head(10).iterrows():
                alerts.append({
                    'type': 'high_anti_india_score',
                    'severity': 'high' if tweet['anti_india_score'] > 0.8 else 'medium',
                    'tweet_id': tweet['id'],
                    'user_id': tweet['user_id'],
                    'username': tweet['username'],
                    'text': tweet['text'],
                    'score': float(tweet['anti_india_score']),
                    'engagement': int(tweet.get('total_engagement', 0)),
                    'timestamp': datetime.now().isoformat()
                })
        
        # Check for influential users
        if user_metrics is not None and not user_metrics.empty:
            influential_users = user_metrics[user_metrics['is_influential'] == True].sort_values(
                by='impact_score', ascending=False)
            
            for _, user in influential_users.head(5).iterrows():
                alerts.append({
                    'type': 'influential_user',
                    'severity': 'high',
                    'user_id': user['user_id'],
                    'username': user['username'],
                    'verified': bool(user['user_verified']),
                    'followers': int(user['user_followers']),
                    'tweet_count': int(user['tweet_count']),
                    'impact_score': float(user['impact_score']),
                    'timestamp': datetime.now().isoformat()
                })
        
        # Check for coordinated activity
        if coord_df is not None and not coord_df.empty:
            # Group by hashtag and time window
            coord_summary = coord_df.groupby(['time_window', 'common_hashtag']).agg({
                'tweet_id': 'count',
                'user_id': 'nunique'
            }).reset_index()
            
            for _, coord in coord_summary.sort_values(by='user_id', ascending=False).head(5).iterrows():
                alerts.append({
                    'type': 'coordinated_activity',
                    'severity': 'high' if coord['user_id'] > 5 else 'medium',
                    'hashtag': coord['common_hashtag'],
                    'time_window': coord['time_window'].isoformat(),
                    'tweet_count': int(coord['tweet_id']),
                    'user_count': int(coord['user_id']),
                    'timestamp': datetime.now().isoformat()
                })
        
        # Generate alert summary
        if alerts:
            alert_summary = {
                'alert_count': len(alerts),
                'generated_at': datetime.now().isoformat(),
                'alerts': alerts
            }
            
            # Save alerts to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"alerts_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(alert_summary, f, indent=2)
            
            logger.info(f"Generated {len(alerts)} alerts and saved to {filepath}")
            
            # Send email alerts if configured
            if self.email_config:
                self.send_email_alert(alert_summary)
            
            return alert_summary
        else:
            logger.info("No alerts generated")
            return None
    
    def send_email_alert(self, alert_summary):
        """Send email alerts"""
        try:
            # Create email
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from']
            msg['To'] = self.email_config['to']
            msg['Subject'] = f"ALERT: {alert_summary['alert_count']} Anti-India Content Alerts Detected"
            
            # Email body
            body = f"""
            <html>
            <body>
                <h2>Anti-India Content Alert Summary</h2>
                <p>Generated at: {alert_summary['generated_at']}</p>
                <p>Total alerts: {alert_summary['alert_count']}</p>
                
                <h3>High Priority Alerts:</h3>
                <ul>
            """
            
            # Add high priority alerts
            high_alerts = [a for a in alert_summary['alerts'] if a['severity'] == 'high']
            for alert in high_alerts:
                if alert['type'] == 'high_anti_india_score':
                    body += f"<li>High anti-India score ({alert['score']:.2f}) in tweet by @{alert['username']}: {alert['text'][:100]}...</li>"
                elif alert['type'] == 'influential_user':
                    body += f"<li>Influential user @{alert['username']} (followers: {alert['followers']}) with impact score {alert['impact_score']:.2f}</li>"
                elif alert['type'] == 'coordinated_activity':
                    body += f"<li>Coordinated activity using #{alert['hashtag']} by {alert['user_count']} users with {alert['tweet_count']} tweets</li>"
            
            body += """
                </ul>
                <p>Please check the alerts file for complete details.</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info("Email alert sent successfully")
        except Exception as e:
            logger.error(f"Error sending email alert: {e}")