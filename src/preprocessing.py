import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import logging

# Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextPreprocessor:
    def __init__(self, language='english'):
        """Initialize text preprocessor with specific language"""
        self.stop_words = set(stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()
        logger.info(f"TextPreprocessor initialized with language: {language}")
    
    def clean_text(self, text):
        """Basic text cleaning"""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove user mentions
        text = re.sub(r'@\w+', '', text)
        
        # Remove hashtag symbol but keep the text
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def remove_stopwords(self, text):
        """Remove stopwords from text"""
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        return ' '.join(filtered_tokens)
    
    def lemmatize_text(self, text):
        """Lemmatize text to root words"""
        tokens = word_tokenize(text)
        lemmatized_tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(lemmatized_tokens)
    
    def preprocess(self, text, remove_stops=True, lemmatize=True):
        """Full preprocessing pipeline"""
        text = self.clean_text(text)
        if remove_stops:
            text = self.remove_stopwords(text)
        if lemmatize:
            text = self.lemmatize_text(text)
        return text

def preprocess_dataset(df, text_column='text'):
    """Preprocess an entire dataframe of tweets"""
    logger.info(f"Preprocessing dataset with {len(df)} entries")
    
    if text_column not in df.columns:
        logger.error(f"Column '{text_column}' not found in dataframe")
        return df
    
    preprocessor = TextPreprocessor()
    
    # Create new columns for processed text
    df['cleaned_text'] = df[text_column].apply(preprocessor.clean_text)
    df['processed_text'] = df['cleaned_text'].apply(
        lambda x: preprocessor.preprocess(x, remove_stops=True, lemmatize=True)
    )
    
    logger.info("Dataset preprocessing completed")
    return df

def extract_features(df):
    """Extract additional features from tweets"""
    logger.info("Extracting features from tweets")
    
    # Text length features
    df['text_length'] = df['text'].apply(lambda x: len(str(x)))
    df['word_count'] = df['cleaned_text'].apply(lambda x: len(str(x).split()))
    
    # User features
    if 'user_followers' in df.columns and 'user_following' in df.columns:
        df['follower_following_ratio'] = df.apply(
            lambda row: row['user_followers'] / max(row['user_following'], 1), axis=1
        )
    
    # Time features
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['hour_of_day'] = df['created_at'].dt.hour
        df['day_of_week'] = df['created_at'].dt.dayofweek
    
    # Engagement features
    engagement_cols = ['retweet_count', 'favorite_count', 'like_count', 
                       'reply_count', 'quote_count']
    
    # Create total engagement column using available engagement metrics
    available_cols = [col for col in engagement_cols if col in df.columns]
    
    if available_cols:
        df['total_engagement'] = df[available_cols].sum(axis=1)
        
        # Calculate engagement rate if follower count is available
        if 'user_followers' in df.columns:
            df['engagement_rate'] = df['total_engagement'] / df['user_followers'].apply(lambda x: max(x, 1))
    
    logger.info("Feature extraction completed")
    return df