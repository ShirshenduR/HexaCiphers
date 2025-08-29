"""
Sentiment and Content Classification Module
Uses HuggingFace transformers for text classification
"""

import logging
from typing import Dict, List, Optional
import os

try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logging.warning("Transformers not available. Using stub implementations.")

logger = logging.getLogger(__name__)

class SentimentClassifier:
    """Class for sentiment analysis and content classification"""
    
    def __init__(self):
        self.cache_dir = os.getenv('HUGGINGFACE_CACHE_DIR', './models/cache')
        self.model_name = os.getenv('MODEL_NAME', 'bert-base-multilingual-cased')
        self.indic_bert_model = os.getenv('INDIC_BERT_MODEL', 'ai4bharat/indic-bert')
        
        # Initialize models
        self.sentiment_pipeline = None
        self.classification_pipeline = None
        self.loaded = False
        
        # Fallback classifications for stub mode
        self.sentiment_keywords = {
            'positive': ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'happy', 'proud'],
            'negative': ['bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'sad', 'disappointed'],
        }
        
        self.india_keywords = {
            'pro_india': ['proud india', 'love india', 'support india', 'incredible india', 'digital india', 'make in india'],
            'anti_india': ['boycott india', 'anti india', 'hate india', 'destroy india', 'fake india']
        }
        
        # Try to load models
        self._load_models()
    
    def _load_models(self):
        """Load HuggingFace models"""
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers not available. Using stub implementations.")
            return
        
        try:
            # Load sentiment analysis pipeline
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                cache_dir=self.cache_dir
            )
            
            # Load multilingual BERT for custom classification
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir
            )
            
            logger.info("Models loaded successfully")
            self.loaded = True
            
        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            logger.info("Falling back to stub implementations")
            self.loaded = False
    
    def classify_sentiment(self, text: str) -> Dict[str, any]:
        """
        Classify sentiment of text
        
        Args:
            text (str): Input text
            
        Returns:
            Dict[str, any]: Sentiment classification results
        """
        if not text:
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'scores': {'positive': 0.0, 'negative': 0.0, 'neutral': 1.0}
            }
        
        if self.loaded and self.sentiment_pipeline:
            try:
                # Use HuggingFace model
                result = self.sentiment_pipeline(text[:512])  # Truncate for model limits
                
                # Convert to standard format
                label = result[0]['label'].lower()
                confidence = result[0]['score']
                
                # Map labels to standard format
                if label in ['positive', 'pos']:
                    sentiment = 'positive'
                elif label in ['negative', 'neg']:
                    sentiment = 'negative'
                else:
                    sentiment = 'neutral'
                
                return {
                    'sentiment': sentiment,
                    'confidence': confidence,
                    'scores': {sentiment: confidence, 'others': 1 - confidence},
                    'model_used': 'huggingface'
                }
                
            except Exception as e:
                logger.error(f"Error in sentiment classification: {str(e)}")
                # Fall back to keyword-based classification
                
        # Keyword-based fallback
        return self._keyword_based_sentiment(text)
    
    def _keyword_based_sentiment(self, text: str) -> Dict[str, any]:
        """
        Fallback keyword-based sentiment analysis
        
        Args:
            text (str): Input text
            
        Returns:
            Dict[str, any]: Sentiment classification results
        """
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.sentiment_keywords['positive'] if word in text_lower)
        negative_count = sum(1 for word in self.sentiment_keywords['negative'] if word in text_lower)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return {
                'sentiment': 'neutral',
                'confidence': 0.6,
                'scores': {'positive': 0.2, 'negative': 0.2, 'neutral': 0.6},
                'model_used': 'keyword_fallback'
            }
        
        if positive_count > negative_count:
            confidence = positive_count / total_sentiment_words
            return {
                'sentiment': 'positive',
                'confidence': confidence,
                'scores': {'positive': confidence, 'negative': 1-confidence, 'neutral': 0.0},
                'model_used': 'keyword_fallback'
            }
        elif negative_count > positive_count:
            confidence = negative_count / total_sentiment_words
            return {
                'sentiment': 'negative',
                'confidence': confidence,
                'scores': {'negative': confidence, 'positive': 1-confidence, 'neutral': 0.0},
                'model_used': 'keyword_fallback'
            }
        else:
            return {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'scores': {'positive': 0.25, 'negative': 0.25, 'neutral': 0.5},
                'model_used': 'keyword_fallback'
            }
    
    def classify_india_relation(self, text: str) -> Dict[str, any]:
        """
        Classify text relation to India
        
        Args:
            text (str): Input text
            
        Returns:
            Dict[str, any]: India relation classification
        """
        if not text:
            return {
                'classification': 'Neutral',
                'confidence': 0.0,
                'scores': {'Pro-India': 0.0, 'Anti-India': 0.0, 'Neutral': 1.0}
            }
        
        text_lower = text.lower()
        
        # Count keyword matches
        pro_count = sum(1 for phrase in self.india_keywords['pro_india'] if phrase in text_lower)
        anti_count = sum(1 for phrase in self.india_keywords['anti_india'] if phrase in text_lower)
        
        total_matches = pro_count + anti_count
        
        if total_matches == 0:
            # Check for India mentions without clear sentiment
            india_mentions = text_lower.count('india') + text_lower.count('भारत')
            if india_mentions > 0:
                confidence = min(0.7, india_mentions * 0.2)
                return {
                    'classification': 'Neutral',
                    'confidence': confidence,
                    'scores': {'Pro-India': 0.2, 'Anti-India': 0.2, 'Neutral': 0.6},
                    'model_used': 'keyword_analysis'
                }
            else:
                return {
                    'classification': 'Neutral',
                    'confidence': 0.9,
                    'scores': {'Pro-India': 0.05, 'Anti-India': 0.05, 'Neutral': 0.9},
                    'model_used': 'keyword_analysis'
                }
        
        if pro_count > anti_count:
            confidence = min(0.9, pro_count / max(total_matches, 1))
            return {
                'classification': 'Pro-India',
                'confidence': confidence,
                'scores': {'Pro-India': confidence, 'Anti-India': 1-confidence, 'Neutral': 0.0},
                'model_used': 'keyword_analysis'
            }
        elif anti_count > pro_count:
            confidence = min(0.9, anti_count / max(total_matches, 1))
            return {
                'classification': 'Anti-India',
                'confidence': confidence,
                'scores': {'Anti-India': confidence, 'Pro-India': 1-confidence, 'Neutral': 0.0},
                'model_used': 'keyword_analysis'
            }
        else:
            return {
                'classification': 'Neutral',
                'confidence': 0.6,
                'scores': {'Pro-India': 0.2, 'Anti-India': 0.2, 'Neutral': 0.6},
                'model_used': 'keyword_analysis'
            }
    
    def classify(self, text: str) -> Dict[str, any]:
        """
        Complete classification pipeline
        
        Args:
            text (str): Input text
            
        Returns:
            Dict[str, any]: Complete classification results
        """
        sentiment_result = self.classify_sentiment(text)
        india_result = self.classify_india_relation(text)
        
        return {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'sentiment': sentiment_result,
            'india_classification': india_result,
            'processing_status': 'success',
            'model_info': {
                'sentiment_model': sentiment_result.get('model_used', 'unknown'),
                'classification_model': india_result.get('model_used', 'unknown'),
                'transformers_available': TRANSFORMERS_AVAILABLE
            }
        }
    
    def batch_classify(self, texts: List[str]) -> List[Dict[str, any]]:
        """
        Classify multiple texts in batch
        
        Args:
            texts (List[str]): List of texts to classify
            
        Returns:
            List[Dict[str, any]]: List of classification results
        """
        results = []
        for text in texts:
            result = self.classify(text)
            results.append(result)
        
        return results
    
    def get_model_info(self) -> Dict[str, any]:
        """
        Get information about loaded models
        
        Returns:
            Dict[str, any]: Model information
        """
        return {
            'transformers_available': TRANSFORMERS_AVAILABLE,
            'models_loaded': self.loaded,
            'model_name': self.model_name,
            'indic_bert_model': self.indic_bert_model,
            'cache_dir': self.cache_dir,
            'sentiment_pipeline_loaded': self.sentiment_pipeline is not None,
            'fallback_mode': not self.loaded
        }