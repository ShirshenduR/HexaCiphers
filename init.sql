-- HexaCiphers Database Initialization Script
-- PostgreSQL setup for the Anti-India Campaign Detection System

-- Create database (run as superuser)
-- CREATE DATABASE hexaciphers_db;
-- CREATE USER hexauser WITH PASSWORD 'hexapass123';
-- GRANT ALL PRIVILEGES ON DATABASE hexaciphers_db TO hexauser;

-- Connect to hexaciphers_db and run the following:

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Posts table
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    language VARCHAR(10),
    translated_text TEXT,
    sentiment VARCHAR(20),
    classification VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_record_id INTEGER
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(100) NOT NULL,
    followers INTEGER DEFAULT 0,
    is_bot BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campaigns table
CREATE TABLE IF NOT EXISTS campaigns (
    id SERIAL PRIMARY KEY,
    hashtag VARCHAR(100) NOT NULL,
    volume INTEGER DEFAULT 0,
    first_detected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_detected TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    risk_score REAL DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE
);

-- Add foreign key constraint
ALTER TABLE posts 
ADD CONSTRAINT fk_posts_users 
FOREIGN KEY (user_record_id) REFERENCES users(id) ON DELETE SET NULL;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_posts_platform ON posts(platform);
CREATE INDEX IF NOT EXISTS idx_posts_sentiment ON posts(sentiment);
CREATE INDEX IF NOT EXISTS idx_posts_classification ON posts(classification);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at);
CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_hashtag ON campaigns(hashtag);
CREATE INDEX IF NOT EXISTS idx_campaigns_risk_score ON campaigns(risk_score);

-- Insert sample data for demonstration
INSERT INTO users (user_id, username, followers, is_bot) VALUES
('user_1', 'tech_enthusiast', 1500, FALSE),
('user_2', 'india_defender', 2300, FALSE),
('user_3', 'bot_account_123', 50, TRUE),
('user_4', 'news_reporter', 5000, FALSE),
('user_5', 'social_activist', 800, FALSE)
ON CONFLICT (user_id) DO NOTHING;

INSERT INTO posts (platform, user_id, content, language, sentiment, classification) VALUES
('Twitter', 'user_1', 'India is making great progress in technology and innovation! #DigitalIndia #TechIndia', 'en', 'positive', 'Pro-India'),
('Reddit', 'user_2', 'Beautiful landscapes in Kashmir today #Kashmir #India #Nature', 'en', 'positive', 'Pro-India'),
('Twitter', 'user_3', 'Propaganda against India must be stopped #FakeNews #AntiIndia', 'en', 'negative', 'Anti-India'),
('YouTube', 'user_4', 'India''s democracy is under threat from misinformation campaigns', 'en', 'negative', 'Neutral'),
('Twitter', 'user_5', 'Indian culture and diversity should be celebrated worldwide', 'en', 'positive', 'Pro-India'),
('Reddit', 'user_3', 'Boycott Indian products spreading fake news #BoycottIndia', 'en', 'negative', 'Anti-India'),
('Twitter', 'user_1', 'India''s economic growth is impressive this quarter #IndianEconomy', 'en', 'positive', 'Pro-India'),
('YouTube', 'user_2', 'Coordinated attack on India''s image using bots and fake accounts', 'en', 'negative', 'Anti-India'),
('Twitter', 'user_4', 'India''s space program achievements are remarkable #ISRO #SpaceIndia', 'en', 'positive', 'Pro-India'),
('Reddit', 'user_5', 'Anti-India sentiment rising on social media platforms', 'en', 'negative', 'Neutral');

INSERT INTO campaigns (hashtag, volume, risk_score) VALUES
('#DigitalIndia', 15, 0.2),
('#BoycottIndia', 8, 0.85),
('#TechIndia', 12, 0.1),
('#AntiIndia', 6, 0.9),
('#IndianEconomy', 10, 0.15),
('#FakeNews', 20, 0.6)
ON CONFLICT DO NOTHING;