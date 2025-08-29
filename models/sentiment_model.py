import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentModel:
    def __init__(self, model_name="distilbert-base-uncased-finetuned-sst-2-english"):
        """Initialize a pre-trained sentiment analysis model"""
        logger.info(f"Loading sentiment model: {model_name}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            logger.info(f"Model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def predict(self, text):
        """Predict sentiment for a single text"""
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Get probabilities using softmax
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            
            # Return positive sentiment probability (score between 0-1)
            return probs[0][1].item()
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return 0.5  # Neutral sentiment as fallback
    
    def predict_batch(self, texts, batch_size=16):
        """Predict sentiment for a batch of texts"""
        results = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            
            try:
                # Tokenize batch
                inputs = self.tokenizer(batch, padding=True, truncation=True, 
                                       max_length=512, return_tensors="pt")
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                # Get predictions
                with torch.no_grad():
                    outputs = self.model(**inputs)
                
                # Get probabilities using softmax
                probs = torch.nn.functional.softmax(outputs.logits, dim=1)
                
                # Get positive sentiment scores
                batch_results = [prob[1].item() for prob in probs]
                results.extend(batch_results)
            except Exception as e:
                logger.error(f"Error in batch prediction: {e}")
                # Return neutral sentiment for the whole batch on error
                results.extend([0.5] * len(batch))
        
        return results