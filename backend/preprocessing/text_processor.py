"""
Text Processing Module
Handles text cleaning, language detection, translation, and preprocessing
"""

import re
import logging
from typing import Dict, List
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
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
        if not text:
            return ""
        text = text.lower()
        text = self.url_pattern.sub('', text)
        text = self.email_pattern.sub('', text)
        text = self.mention_pattern.sub('', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s#@.,!?-]', '', text)
        return text.strip()
    
    def extract_hashtags(self, text: str) -> List[str]:
        return [tag.lower() for tag in self.hashtag_pattern.findall(text)]
    
    def extract_mentions(self, text: str) -> List[str]:
        return [mention.lower() for mention in self.mention_pattern.findall(text)]
    
    def detect_language(self, text: str) -> str:
        if not text or len(text.strip()) < 3:
            return 'unknown'
        try:
            return detect(text)
        except LangDetectException:
            return 'unknown'
    
    def remove_stopwords(self, text: str, language: str = 'english') -> str:
        if not text:
            return ""
        words = word_tokenize(text)
        stop_words = self.stopwords.get(language, self.stopwords['general'])
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered_words)
    
    def translate_text(self, text: str, target_language: str = 'en') -> str:
        logger.info(f"Translation requested: {target_language}")
        if target_language == 'en':
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
        if not text:
            return []
        cleaned_text = self.clean_text(text)
        words = word_tokenize(cleaned_text)
        keywords = [word.lower() for word in words if len(word) > 2 and word.isalpha()]
        keywords = [word for word in keywords if word not in self.stopwords.get('english', set())]
        return list(set(keywords))
    
    def get_sentiment_indicators(self, text: str) -> Dict[str, int]:
        if not text:
            return {'positive': 0, 'negative': 0, 'neutral': 0}
        text_lower = text.lower()
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
        if not text:
            return 'Neutral'
        text_lower = text.lower()
        anti_score = sum(1 for keyword in self.anti_india_keywords if keyword in text_lower)
        pro_score = sum(1 for keyword in self.pro_india_keywords if keyword in text_lower)
        if anti_score > pro_score and anti_score > 0:
            return 'Anti-India'
        elif pro_score > anti_score and pro_score > 0:
            return 'Pro-India'
        else:
            return 'Neutral'
    
    def process_text(self, text: str) -> Dict:
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
        cleaned_text = self.clean_text(text)
        language = self.detect_language(text)
        hashtags = self.extract_hashtags(text)
        mentions = self.extract_mentions(text)
        keywords = self.extract_keywords(text)
        sentiment_indicators = self.get_sentiment_indicators(text)
        india_classification = self.classify_india_relation(text)
        translated_text = text if language == 'en' or language == 'unknown' else self.translate_text(text, 'en')
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
