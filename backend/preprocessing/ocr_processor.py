"""
OCR Module for extracting text from images
Uses Tesseract OCR engine for text extraction from memes and images
"""

import logging
from typing import Optional, Dict
from PIL import Image
import io
import base64

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logging.warning("Tesseract not available. OCR functionality will be limited.")

logger = logging.getLogger(__name__)

class OCRProcessor:
    """Class for processing images and extracting text using OCR"""
    
    def __init__(self):
        self.supported_formats = ['PNG', 'JPEG', 'JPG', 'BMP', 'TIFF']
        
        # Configure Tesseract for multiple languages
        self.languages = 'eng+hin+ben+tam+tel'  # English, Hindi, Bengali, Tamil, Telugu
        
    def extract_text_from_image(self, image_path: str) -> Dict[str, str]:
        """
        Extract text from image file
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            Dict[str, str]: Extracted text and metadata
        """
        if not TESSERACT_AVAILABLE:
            return {
                'text': '',
                'confidence': 0,
                'status': 'error',
                'message': 'Tesseract OCR not available'
            }
        
        try:
            # Open and process image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(
                image, 
                lang=self.languages,
                config='--psm 6'  # Assume a single uniform block of text
            )
            
            # Get confidence score
            try:
                data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
                confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            except:
                avg_confidence = 0
            
            return {
                'text': extracted_text.strip(),
                'confidence': avg_confidence,
                'status': 'success',
                'message': 'Text extracted successfully',
                'language_detected': self._detect_script(extracted_text)
            }
            
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            return {
                'text': '',
                'confidence': 0,
                'status': 'error',
                'message': f'OCR processing failed: {str(e)}'
            }
    
    def extract_text_from_base64(self, base64_image: str) -> Dict[str, str]:
        """
        Extract text from base64 encoded image
        
        Args:
            base64_image (str): Base64 encoded image data
            
        Returns:
            Dict[str, str]: Extracted text and metadata
        """
        if not TESSERACT_AVAILABLE:
            return {
                'text': '',
                'confidence': 0,
                'status': 'error',
                'message': 'Tesseract OCR not available'
            }
        
        try:
            # Decode base64 image
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text
            extracted_text = pytesseract.image_to_string(
                image,
                lang=self.languages,
                config='--psm 6'
            )
            
            return {
                'text': extracted_text.strip(),
                'confidence': 80,  # Default confidence for base64 processing
                'status': 'success',
                'message': 'Text extracted from base64 image',
                'language_detected': self._detect_script(extracted_text)
            }
            
        except Exception as e:
            logger.error(f"Error extracting text from base64 image: {str(e)}")
            return {
                'text': '',
                'confidence': 0,
                'status': 'error',
                'message': f'Base64 OCR processing failed: {str(e)}'
            }
    
    def _detect_script(self, text: str) -> str:
        """
        Detect script/language of extracted text
        
        Args:
            text (str): Extracted text
            
        Returns:
            str: Detected script
        """
        if not text:
            return 'unknown'
        
        # Simple script detection based on character ranges
        char_counts = {
            'latin': 0,
            'devanagari': 0,
            'bengali': 0,
            'tamil': 0,
            'telugu': 0
        }
        
        for char in text:
            code_point = ord(char)
            
            if 0x0020 <= code_point <= 0x007F:  # Basic Latin
                char_counts['latin'] += 1
            elif 0x0900 <= code_point <= 0x097F:  # Devanagari (Hindi)
                char_counts['devanagari'] += 1
            elif 0x0980 <= code_point <= 0x09FF:  # Bengali
                char_counts['bengali'] += 1
            elif 0x0B80 <= code_point <= 0x0BFF:  # Tamil
                char_counts['tamil'] += 1
            elif 0x0C00 <= code_point <= 0x0C7F:  # Telugu
                char_counts['telugu'] += 1
        
        # Return script with highest count
        if max(char_counts.values()) == 0:
            return 'unknown'
        
        return max(char_counts, key=char_counts.get)
    
    def preprocess_image(self, image_path: str) -> str:
        """
        Preprocess image for better OCR results
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            str: Path to preprocessed image
        """
        try:
            image = Image.open(image_path)
            
            # Convert to grayscale for better OCR
            if image.mode != 'L':
                image = image.convert('L')
            
            # Enhance contrast
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Save preprocessed image
            preprocessed_path = image_path.replace('.', '_preprocessed.')
            image.save(preprocessed_path)
            
            return preprocessed_path
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            return image_path  # Return original path if preprocessing fails
    
    def extract_text_from_meme(self, image_path: str) -> Dict[str, str]:
        """
        Specialized text extraction for memes
        
        Args:
            image_path (str): Path to meme image
            
        Returns:
            Dict[str, str]: Extracted text and analysis
        """
        # Preprocess image for better meme text extraction
        preprocessed_path = self.preprocess_image(image_path)
        
        # Extract text
        result = self.extract_text_from_image(preprocessed_path)
        
        if result['status'] == 'success' and result['text']:
            # Additional meme-specific processing
            text = result['text']
            
            # Check for meme indicators
            meme_indicators = ['top text', 'bottom text', 'impact font', 'meme']
            has_meme_indicators = any(indicator in text.lower() for indicator in meme_indicators)
            
            result['is_meme'] = has_meme_indicators
            result['text_length'] = len(text)
            result['word_count'] = len(text.split())
        
        return result