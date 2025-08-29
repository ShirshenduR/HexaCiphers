import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# App settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALERT_THRESHOLD = int(os.getenv("ALERT_THRESHOLD", "10"))
ENGAGEMENT_THRESHOLD = int(os.getenv("ENGAGEMENT_THRESHOLD", "100"))
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "300"))  # in seconds

# Database settings
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
KEYWORDS_PATH = os.path.join(DB_PATH, "keywords.json")

# Model settings
MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"