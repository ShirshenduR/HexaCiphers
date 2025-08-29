import os
import json
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ensure_dir(directory):
    """Ensure directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")

def save_to_json(data, filepath):
    """Save data to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Data saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error saving data to {filepath}: {e}")
        return False

def load_from_json(filepath):
    