"""
ESG Analyzer Configuration Module
Loads and provides configuration values from environment variables or .env file
"""
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Configuration for the ESG Analyzer application"""
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")
    
    # Database settings
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///esg_analyzer.db")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def setup_logging(cls):
        """Configure logging based on environment settings"""
        numeric_level = getattr(logging, cls.LOG_LEVEL.upper(), None)
        if not isinstance(numeric_level, int):
            numeric_level = logging.INFO
            
        logging.basicConfig(
            level=numeric_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
    @classmethod
    def validate(cls):
        """Validate that critical configuration is present"""
        if cls.SECRET_KEY == "supersecretkey" and cls.DEBUG is False:
            logging.warning("Using default SECRET_KEY in production is not recommended!")
            
        return True
