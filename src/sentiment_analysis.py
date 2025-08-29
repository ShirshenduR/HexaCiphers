import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from torch.nn.functional import softmax
import logging
import json
import os
from config.config import MODEL_NAME, KEYWORDS_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self, model_name=MODEL_NAME):
        """Initialize sentiment analyzer with a pre-trained model"""
        logger.info(f"Initializing SentimentAnalyzer with model: {model_name}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Using device: {self.device}")
            self.model.to(self.device)
            self.load_keywords()
        except Exception as e:
            logger.error(f"Error initializing sentiment model: {e}")
            raise
    
    def load_keywords(self):
        """Load keywords from the JSON file"""
        try:
            with open(KEYWORDS_PATH, 'r') as f:
                data = json.load(f)
            
            self.keywords = data.get('keywords', [])
            self.hashtags = data.get('hashtags', [])
            self.phrases = data.get('phrases', [])
            self.contexts = data.get('contexts', [])
            
            logger.info(f"Loaded keywords: {len(self.keywords)} keywords, {len(self.hashtags)} hashtags, "
                        f"{len(self.phrases)} phrases, {len(self.contexts)} contexts")
        except Exception as e:
            logger.error(f"Error loading keywords: {e}")
            self.keywords = []
            self.hashtags = []
            self.phrases = []
            self.contexts = []
    
    def predict_sentiment(self, text):
        """Predict sentiment score for a single text"""
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get probabilities
            probs = softmax(outputs.logits, dim=1)
            
            # Return sentiment score (negative to positive, 0-1)
            return probs[0][1].item()
        except Exception as e:
            logger.error(f"Error predicting sentiment: {e}")
            return 0.5  # Neutral sentiment as fallback
    
    def analyze_batch(self, texts, batch_size=16):
        """Analyze sentiment for a batch of texts"""
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_results = [self.predict_sentiment(text) for text in batch]
            results.extend(batch_results)
        return results
    
    def keyword_match_score(self, text):
        """Calculate how many sensitive keywords match in the text"""
        text = text.lower()
        
        # Count exact keyword matches
        keyword_matches = sum(1 for keyword in self.keywords if keyword.lower() in text)
        
        # Count hashtag matches (both with and without # symbol)
        hashtag_matches = sum(1 for hashtag in self.hashtags if 
                             hashtag.lower() in text or 
                             hashtag.lower().replace('#', '') in text)
        
        # Count phrase matches
        phrase_matches = sum(1 for phrase in self.phrases if phrase.lower() in text)
        
        # Count context matches
        context_matches = sum(1 for context in self.contexts if context.lower() in text)
        
        # Calculate weighted score (phrases and contexts given higher weight)
        total_score = (keyword_matches + hashtag_matches + 
                      phrase_matches * 2 + context_matches * 1.5)
        
        # Normalize to 0-1 range
        max_possible = (len(self.keywords) + len(self.hashtags) + 
                        len(self.phrases) * 2 + len(self.contexts) * 1.5)
        
        return total_score / max(1, max_possible)
    
    def analyze_tweets(self, df, text_column='cleaned_text'):
        """Analyze tweets in a dataframe"""
        logger.info(f"Analyzing sentiment for {len(df)} tweets")
        
        if text_column not in df.columns:
            logger.error(f"Column '{text_column}' not found in dataframe")
            return df
        
        # Get list of texts
        texts = df[text_column].tolist()
        
        # Analyze sentiment
        sentiment_scores = self.analyze_batch(texts)
        df['sentiment_score'] = sentiment_scores
        
        # Convert to categorical
        df['sentiment'] = pd.cut(
            df['sentiment_score'],
            bins=[-0.01, 0.4, 0.6, 1.01],
            labels=['negative', 'neutral', 'positive']
        )
        
        # Calculate keyword match score
        df['keyword_match_score'] = df[text_column].apply(self.keyword_match_score)
        
        # Calculate anti-India score (combination of negative sentiment and keyword matches)
        df['anti_india_score'] = (1 - df['sentiment_score']) * 0.5 + df['keyword_match_score'] * 0.5
        
        # Flag potentially concerning tweets
        df['flagged'] = df['anti_india_score'] > 0.6
        
        logger.info(f"Sentiment analysis completed. Flagged {df['flagged'].sum()} tweets.")
        return df