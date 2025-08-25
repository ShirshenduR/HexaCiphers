"""Database models for HexaCiphers application"""

from backend.app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

class Post(db.Model):
    """Model for storing social media posts"""
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    platform = Column(String(50), nullable=False)  # Twitter, Reddit, etc.
    user_id = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(10))
    translated_text = Column(Text)
    sentiment = Column(String(20))  # positive, neutral, negative
    classification = Column(String(20))  # Pro-India, Neutral, Anti-India
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Foreign key relationship
    user_record_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'platform': self.platform,
            'user_id': self.user_id,
            'content': self.content,
            'language': self.language,
            'translated_text': self.translated_text,
            'sentiment': self.sentiment,
            'classification': self.classification,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class User(db.Model):
    """Model for storing user information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), unique=True, nullable=False)
    username = Column(String(100), nullable=False)
    followers = Column(Integer, default=0)
    is_bot = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    posts = relationship("Post", back_populates="user")
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'followers': self.followers,
            'is_bot': self.is_bot,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Campaign(db.Model):
    """Model for storing detected campaigns"""
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True)
    hashtag = Column(String(100), nullable=False)
    volume = Column(Integer, default=0)
    first_detected = Column(DateTime, default=datetime.utcnow)
    last_detected = Column(DateTime, default=datetime.utcnow)
    risk_score = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'hashtag': self.hashtag,
            'volume': self.volume,
            'first_detected': self.first_detected.isoformat() if self.first_detected else None,
            'last_detected': self.last_detected.isoformat() if self.last_detected else None,
            'risk_score': self.risk_score,
            'is_active': self.is_active
        }