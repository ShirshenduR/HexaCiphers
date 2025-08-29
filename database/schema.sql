-- Keywords and phrases database
CREATE TABLE keyword_database (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'anti_india', 'pro_india', 'neutral'
    weight FLOAT DEFAULT 1.0,
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Twitter content monitoring
CREATE TABLE twitter_content (
    id SERIAL PRIMARY KEY,
    tweet_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    retweet_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    reply_count INTEGER DEFAULT 0,
    quote_count INTEGER DEFAULT 0,
    hashtags TEXT[], -- Array of hashtags
    mentions TEXT[], -- Array of mentions
    urls TEXT[], -- Array of URLs
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sentiment analysis results
CREATE TABLE sentiment_analysis (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES twitter_content(id),
    sentiment_score FLOAT NOT NULL, -- -1 to 1 scale
    classification VARCHAR(50) NOT NULL, -- 'anti_india', 'pro_india', 'neutral'
    confidence FLOAT NOT NULL,
    keywords_matched TEXT[],
    analysis_model VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User influence tracking
CREATE TABLE user_influence (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) NOT NULL,
    follower_count INTEGER DEFAULT 0,
    following_count INTEGER DEFAULT 0,
    tweet_count INTEGER DEFAULT 0,
    influence_score FLOAT DEFAULT 0.0,
    risk_level VARCHAR(20) DEFAULT 'low', -- 'low', 'medium', 'high', 'critical'
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Campaign detection
CREATE TABLE detected_campaigns (
    id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(255),
    hashtags TEXT[],
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    participant_count INTEGER DEFAULT 0,
    total_engagement INTEGER DEFAULT 0,
    severity_level VARCHAR(20) DEFAULT 'low',
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'monitoring', 'resolved'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alerts system
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    alert_type VARCHAR(50) NOT NULL, -- 'trending_negative', 'coordinated_campaign', 'high_influence_user'
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'critical'
    related_content_ids INTEGER[],
    related_user_ids TEXT[],
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'acknowledged', 'resolved'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);