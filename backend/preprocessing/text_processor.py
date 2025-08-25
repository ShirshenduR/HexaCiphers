"""
Text Processing Module
Handles text cleaning, language detection, translation, and preprocessing
"""

import re
import logging
from typing import Dict, List, Optional
from langdetect import detect, LangDetectError
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

logger = logging.getLogger(__name__)

class TextProcessor:
    """Class for comprehensive text processing"""
    
    def __init__(self):
        self.stemmer = PorterStemmer()
        
        # Load stopwords for multiple languages
        try:
            self.stopwords = {
                'english': set(stopwords.words('english')),
                'hindi': set(['और', 'का', 'एक', 'में', 'के', 'है', 'को', 'से', 'पर', 'यह', 'वह']),
                'general': set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
            }
        except:
            self.stopwords = {'english': set(), 'hindi': set(), 'general': set()}
        
        # Common social media patterns
        self.url_pattern = re.compile(r'https?://[^\s]+')
        self.mention_pattern = re.compile(r'@[A-Za-z0-9_]+')
        self.hashtag_pattern = re.compile(r'#[A-Za-z0-9_]+')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # Anti-India keywords for classification assistance
        self.anti_india_keywords = [
            'boycott india', 'anti india', 'hate india', 'destroy india',
            'fake india', 'propaganda india', 'corrupt india', 'evil india',
            'boycottindia', 'antiindia', 'fakeindia'
        ]
        
        # Pro-India keywords
        self.pro_india_keywords = [
            'proud india', 'love india', 'support india', 'incredible india',
            'amazing india', 'beautiful india', 'great india', 'strong india',
            'digital india', 'make in india', 'proud indian', 'jai hind'
        ]
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing URLs, mentions, extra whitespace
        
        Args:
            text (str): Input text to clean
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = self.url_pattern.sub('', text)
        
        # Remove email addresses
        text = self.email_pattern.sub('', text)
        
        # Remove mentions (keep hashtags for analysis)
        text = self.mention_pattern.sub('', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s#@.,!?-]', '', text)
        
        return text.strip()
    
    def extract_hashtags(self, text: str) -> List[str]:
        """
        Extract hashtags from text
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of hashtags
        """
        hashtags = self.hashtag_pattern.findall(text)
        return [tag.lower() for tag in hashtags]
    
    def extract_mentions(self, text: str) -> List[str]:
        """
        Extract mentions from text
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of mentions
        """
        mentions = self.mention_pattern.findall(text)
        return [mention.lower() for mention in mentions]
    
    def detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text (str): Input text
            
        Returns:
            str: Detected language code
        """
        if not text or len(text.strip()) < 3:
            return 'unknown'
        
        try:
            return detect(text)
        except LangDetectError:
            return 'unknown'
    
    def remove_stopwords(self, text: str, language: str = 'english') -> str:
        """
        Remove stopwords from text
        
        Args:
            text (str): Input text
            language (str): Language for stopwords
            
        Returns:
            str: Text without stopwords
        """
        if not text:
            return ""
        
        words = word_tokenize(text)
        
        # Get appropriate stopwords
        if language in self.stopwords:
            stop_words = self.stopwords[language]
        else:
            stop_words = self.stopwords['general']
        
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered_words)
    
    def translate_text(self, text: str, target_language: str = 'en') -> str:
        """
        Translate text to target language (stub implementation)
        
        Args:
            text (str): Text to translate
            target_language (str): Target language code
            
        Returns:
            str: Translated text (currently returns original for stub)
        """
        # This is a stub implementation
        # In production, you would use Google Translate API or similar service
        logger.info(f"Translation requested: {target_language}")
        
        # Simple keyword translation for demonstration
        if target_language == 'en':
            # Basic Hindi to English translation for common words
            translations = {
                'भारत': 'India',
                'देश': 'country',
                'सरकार': 'government',
                'लोग': 'people',
                'समाज': 'society'
            }
            
            for hindi, english in translations.items():
                text = text.replace(hindi, english)
        
        return text
    
    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract important keywords from text
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of keywords
        """
        if not text:
            return []
        
        # Clean and tokenize
        cleaned_text = self.clean_text(text)
        words = word_tokenize(cleaned_text)
        
        # Filter meaningful words (length > 2)
        keywords = [word.lower() for word in words if len(word) > 2 and word.isalpha()]
        
        # Remove stopwords
        keywords = [word for word in keywords if word not in self.stopwords.get('english', set())]
        
        return list(set(keywords))  # Remove duplicates
    
    def get_sentiment_indicators(self, text: str) -> Dict[str, int]:
        """
        Get sentiment indicators from text
        
        Args:
            text (str): Input text
            
        Returns:
            Dict[str, int]: Dictionary with sentiment indicators
        """
        if not text:
            return {'positive': 0, 'negative': 0, 'neutral': 0}
        
        text_lower = text.lower()
        
        # Simple sentiment indicators
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'like', 'happy', 'proud']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'angry', 'sad', 'disappointed']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        return {
            'positive': positive_count,
            'negative': negative_count,
            'neutral': 1 if positive_count == negative_count == 0 else 0
        }
    
    def classify_india_relation(self, text: str) -> str:
        """
        Classify text relation to India
        
        Args:
            text (str): Input text
            
        Returns:
            str: Classification (Pro-India, Anti-India, Neutral)
        """
        if not text:
            return 'Neutral'
        
        text_lower = text.lower()
        
        # Check for anti-India indicators
        anti_score = sum(1 for keyword in self.anti_india_keywords if keyword in text_lower)
        
        # Check for pro-India indicators
        pro_score = sum(1 for keyword in self.pro_india_keywords if keyword in text_lower)
        
        if anti_score > pro_score and anti_score > 0:
            return 'Anti-India'
        elif pro_score > anti_score and pro_score > 0:
            return 'Pro-India'
        else:
            return 'Neutral'
    
    def process_text(self, text: str) -> Dict:
        """
        Complete text processing pipeline
        
        Args:
            text (str): Input text to process
            
        Returns:
            Dict: Comprehensive processing results
        """
        if not text:
            return {
                'original_text': '',
                'cleaned_text': '',
                'language': 'unknown',
                'hashtags': [],
                'mentions': [],
                'keywords': [],
                'sentiment_indicators': {'positive': 0, 'negative': 0, 'neutral': 0},
                'india_classification': 'Neutral',
                'translated_text': ''
            }
        
        # Basic processing
        cleaned_text = self.clean_text(text)
        language = self.detect_language(text)
        hashtags = self.extract_hashtags(text)
        mentions = self.extract_mentions(text)
        keywords = self.extract_keywords(text)
        sentiment_indicators = self.get_sentiment_indicators(text)
        india_classification = self.classify_india_relation(text)
        
        # Translation (if not English)
        translated_text = text
        if language != 'en' and language != 'unknown':
            translated_text = self.translate_text(text, 'en')
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'language': language,
            'hashtags': hashtags,
            'mentions': mentions,
            'keywords': keywords,
            'sentiment_indicators': sentiment_indicators,
            'india_classification': india_classification,
            'translated_text': translated_text
        }